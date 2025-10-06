# Authentification sécurisée — Node-Vault-Py

Ce module ajoute une protection par mot de passe maître local côté client.

Points clés:
- Mot de passe maître non stocké en clair ni réversible
- Hachage PBKDF2-HMAC-SHA256 avec ~310k itérations, sel aléatoire 16 octets
- Empreinte stockée dans %USERPROFILE%\.node_vault_py\auth.json (Windows) ou ~/.node_vault_py/auth.json
- Dialogue premium: création (double saisie), connexion, messages d’erreur clairs
- Intégration: l’app se lance uniquement après authentification réussie

Utilisation:
1) Premier lancement: définir le mot de passe (double saisie)
2) Lancements suivants: saisir le mot de passe pour déverrouiller
3) En cas d’oubli, il n’y a pas de récupération intégrée; supprimer le fichier auth.json réinitialise l’enrôlement (vous perdrez l’accès aux données chiffrées si ajouté ultérieurement)

Bonnes pratiques:
- Choisir une phrase secrète longue (12+ caractères)
- Sauvegarder régulièrement la base locale (dossier data/)
- Ne jamais partager auth.json ni vos mots de passe

Technique:
- Fichier: src/gui/authentication.py
- API: require_auth(parent) -> bool
- Intégré dans main.py avant l’initialisation de l’UI (withdraw/deiconify)

Dépendances:
- cryptography (déjà dans requirements.txt)
