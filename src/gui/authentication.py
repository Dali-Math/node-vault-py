import os
import json
import base64
import secrets
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Local storage path for auth metadata
APP_DIR = os.path.join(os.path.expanduser("~"), ".node_vault_py")
AUTH_FILE = os.path.join(APP_DIR, "auth.json")

PBKDF2_ITERATIONS = 310000  # OWASP recommendation range
SALT_BYTES = 16
KEY_BYTES = 32


def _ensure_app_dir():
    os.makedirs(APP_DIR, exist_ok=True)


def _derive_key(password: str, salt: bytes, iterations: int = PBKDF2_ITERATIONS) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_BYTES,
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return kdf.derive(password.encode("utf-8"))


def _save_auth(salt: bytes, key_hash: bytes, iterations: int = PBKDF2_ITERATIONS):
    _ensure_app_dir()
    payload = {
        "salt": base64.b64encode(salt).decode("utf-8"),
        "key_hash": base64.b64encode(key_hash).decode("utf-8"),
        "iterations": iterations,
        "version": 1,
    }
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f)


def _load_auth() -> Optional[Tuple[bytes, bytes, int]]:
    if not os.path.exists(AUTH_FILE):
        return None
    try:
        with open(AUTH_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        salt = base64.b64decode(data["salt"])  # type: ignore
        key_hash = base64.b64decode(data["key_hash"])  # type: ignore
        iterations = int(data.get("iterations", PBKDF2_ITERATIONS))
        return salt, key_hash, iterations
    except Exception:
        return None


def is_enrolled() -> bool:
    return _load_auth() is not None


def enroll_master_password(password: str) -> None:
    salt = secrets.token_bytes(SALT_BYTES)
    key = _derive_key(password, salt)
    _save_auth(salt, key)


def verify_master_password(password: str) -> bool:
    record = _load_auth()
    if not record:
        return False
    salt, key_hash, iterations = record
    try:
        derived = _derive_key(password, salt, iterations)
        return secrets.compare_digest(derived, key_hash)
    except Exception:
        return False


class AuthDialog(tk.Toplevel):
    """
    A premium-feel authentication dialog that supports first-time enrollment
    and subsequent sign-in using a master password (not stored, only PBKDF2 hash).
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.title("Node-Vault-Py — Sécurité")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.var_pwd1 = tk.StringVar()
        self.var_pwd2 = tk.StringVar()
        self.var_pwd_login = tk.StringVar()

        if not is_enrolled():
            self._build_enroll_ui(container)
        else:
            self._build_login_ui(container)

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.result_ok = False

    def _build_enroll_ui(self, parent):
        title = ttk.Label(parent, text="Créer votre mot de passe maître", font=("Segoe UI", 12, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        subtitle = ttk.Label(parent, text="Conseil: utilisez une phrase longue et unique.")
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(parent, text="Mot de passe").grid(row=2, column=0, sticky="w")
        pwd1 = ttk.Entry(parent, textvariable=self.var_pwd1, show="•", width=32)
        pwd1.grid(row=2, column=1, pady=5)

        ttk.Label(parent, text="Confirmer").grid(row=3, column=0, sticky="w")
        pwd2 = ttk.Entry(parent, textvariable=self.var_pwd2, show="•", width=32)
        pwd2.grid(row=3, column=1, pady=5)

        self.lbl_msg = ttk.Label(parent, foreground="#cc0000")
        self.lbl_msg.grid(row=4, column=0, columnspan=2, pady=(4, 10))

        btn_row = ttk.Frame(parent)
        btn_row.grid(row=5, column=0, columnspan=2, sticky="e")
        ttk.Button(btn_row, text="Annuler", command=self._on_cancel).pack(side=tk.RIGHT, padx=(0, 6))
        ttk.Button(btn_row, text="Enregistrer", command=self._on_enroll).pack(side=tk.RIGHT)

    def _build_login_ui(self, parent):
        title = ttk.Label(parent, text="Connexion sécurisée", font=("Segoe UI", 12, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        subtitle = ttk.Label(parent, text="Entrez votre mot de passe maître pour déverrouiller l'application.")
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(parent, text="Mot de passe").grid(row=2, column=0, sticky="w")
        pwd = ttk.Entry(parent, textvariable=self.var_pwd_login, show="•", width=32)
        pwd.grid(row=2, column=1, pady=5)
        pwd.bind("<Return>", lambda e: self._on_login())

        self.lbl_msg = ttk.Label(parent, foreground="#cc0000")
        self.lbl_msg.grid(row=3, column=0, columnspan=2, pady=(4, 10))

        btn_row = ttk.Frame(parent)
        btn_row.grid(row=4, column=0, columnspan=2, sticky="e")
        ttk.Button(btn_row, text="Quitter", command=self._on_cancel).pack(side=tk.RIGHT, padx=(0, 6))
        ttk.Button(btn_row, text="Se connecter", command=self._on_login).pack(side=tk.RIGHT)

    # Event handlers
    def _on_cancel(self):
        self.result_ok = False
        self.destroy()

    def _on_enroll(self):
        p1 = self.var_pwd1.get()
        p2 = self.var_pwd2.get()

        # Validation and premium-style feedback
        if len(p1) < 10:
            self._set_msg("Mot de passe trop court (min 10 caractères)")
            return
        if p1 != p2:
            self._set_msg("Les mots de passe ne correspondent pas")
            return
        try:
            enroll_master_password(p1)
            messagebox.showinfo(
                "Configuration réussie",
                "Votre mot de passe maître a été enregistré de façon sécurisée.",
                parent=self,
            )
            self.result_ok = True
            self.destroy()
        except Exception as e:
            self._set_msg("Erreur lors de l'enregistrement. Veuillez réessayer.")

    def _on_login(self):
        p = self.var_pwd_login.get()
        try:
            if verify_master_password(p):
                self.result_ok = True
                self.destroy()
            else:
                self._set_msg("Mot de passe incorrect. Réessayez.")
        except Exception:
            self._set_msg("Erreur de vérification. Réessayez.")

    def _on_close(self):
        # force explicit choice; default to cancel
        self._on_cancel()

    def _set_msg(self, text: str):
        # Premium UI microcopy for trust and clarity
        self.lbl_msg.configure(text=text)


def require_auth(parent: tk.Tk) -> bool:
    """Shows the auth dialog and returns True if authentication passes."""
    dlg = AuthDialog(parent)
    parent.wait_window(dlg)
    return dlg.result_ok
