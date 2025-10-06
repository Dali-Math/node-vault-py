  import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class WalletManager:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.wallets = []
        self.setup_ui()
        self.load_wallets()

    def setup_ui(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(toolbar, text="Add Wallet", command=self.add_wallet).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Edit Wallet", command=self.edit_wallet).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Delete Wallet", command=self.delete_wallet).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.load_wallets).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Name', 'Address', 'Network', 'Type', 'Balance')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=115 if col != 'ID' else 50)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', lambda e: self.edit_wallet())

    def load_wallets(self):
        self.tree.delete(*self.tree.get_children())
        self.wallets = self.db_manager.get_all_wallets() or []
        for w in self.wallets:
            self.tree.insert('', 'end', values=(
                w.get('id'), w.get('name'), w.get('address'), w.get('network'), w.get('type'), w.get('balance')))

    def add_wallet(self):
        WalletDialog(self.parent, self.db_manager, callback=self.load_wallets)

    def edit_wallet(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        WalletDialog(self.parent, self.db_manager, wallet_id=item['values'][0], callback=self.load_wallets)

    def delete_wallet(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        wid = item['values'][0]
        if messagebox.askyesno("Confirm", "Delete this wallet?"):
            self.db_manager.delete_wallet(wid)
            self.load_wallets()

class WalletDialog:
    def __init__(self, parent, db_manager, wallet_id=None, callback=None):
        self.db_manager = db_manager
        self.wallet_id = wallet_id
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Wallet" if wallet_id else "Add Wallet")
        self.dialog.geometry("400x400")
        self.setup_ui()
        if wallet_id:
            self.load_data()
    def setup_ui(self):
        f = ttk.Frame(self.dialog, padding=20)
        f.pack(fill=tk.BOTH, expand=True)
        self.name = tk.StringVar()
        self.address = tk.StringVar()
        self.network = tk.StringVar()
        self.type = tk.StringVar(value="Hot")
        self.balance = tk.StringVar()
        self.private_key = tk.StringVar()
        self.notes = tk.StringVar()

        ttk.Label(f, text="Name").grid(row=0, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.name).grid(row=0, column=1)
        ttk.Label(f, text="Address").grid(row=1, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.address).grid(row=1, column=1)
        ttk.Label(f, text="Network").grid(row=2, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.network).grid(row=2, column=1)
        ttk.Label(f, text="Type").grid(row=3, column=0, sticky='w')
        ttk.Combobox(f, textvariable=self.type, values=['Hot','Cold','Hardware']).grid(row=3, column=1)
        ttk.Label(f, text="Balance").grid(row=4, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.balance).grid(row=4, column=1)
        ttk.Label(f, text="Private Key").grid(row=5, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.private_key, show="•").grid(row=5, column=1)
        ttk.Label(f, text="Notes").grid(row=6, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.notes).grid(row=6, column=1)
        ttk.Button(f, text="Save", command=self.save).grid(row=10, column=0, pady=16)
        ttk.Button(f, text="Cancel", command=self.dialog.destroy).grid(row=10, column=1)
    def load_data(self):
        wallets = self.db_manager.execute("SELECT * FROM wallets WHERE id=?", (self.wallet_id,), fetch=True)
        if not wallets: return
        w = wallets[0]
        self.name.set(w['name'])
        self.address.set(w['address'])
        self.network.set(w['network'])
        self.type.set(w['type'])
        self.balance.set(w['balance'])
        self.private_key.set(w.get('private_key',''))
        self.notes.set(w.get('notes',''))
    def save(self):
        data = {
            'name': self.name.get(),
            'address': self.address.get(),
            'network': self.network.get(),
            'type': self.type.get(),
            'balance': self.balance.get(),
            'private_key': self.private_key.get(),
            'notes': self.notes.get(),
        }
        if self.wallet_id:
            self.db_manager.execute(
                "UPDATE wallets SET name=?, address=?, network=?, type=?, balance=?, private_key=?, notes=? WHERE id=?",
                (data['name'], data['address'], data['network'], data['type'], data['balance'], data['private_key'], data['notes'], self.wallet_id))
        else:
            self.db_manager.add_wallet(data)
        if self.callback: self.callback()
        self.dialog.destroy()
