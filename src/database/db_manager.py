import sqlite3, os, base64
from datetime import datetime
from .models import NodeModel, WalletModel, AirdropModel
from src.utils.encryption import CryptoManager

class DatabaseManager:
    def __init__(self, db_path='data/node_vault.db', encryption_key=None):
        self.db_path = db_path
        self.crypto = CryptoManager(encryption_key)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, 
            address TEXT NOT NULL, network TEXT, port TEXT, status TEXT, 
            last_sync TEXT, notes TEXT, created_date TEXT, updated_date TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, 
            address TEXT NOT NULL, network TEXT, type TEXT, balance TEXT, 
            private_key TEXT, notes TEXT, created_date TEXT, updated_date TEXT)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS airdrops (
            id INTEGER PRIMARY KEY AUTOINCREMENT, project_name TEXT NOT NULL, 
            network TEXT NOT NULL, airdrop_type TEXT, eligibility_requirements TEXT, 
            start_date TEXT, end_date TEXT, claim_date TEXT, status TEXT, 
            estimated_value TEXT, wallet_address TEXT, tasks_completed TEXT, 
            notes TEXT, created_date TEXT, updated_date TEXT)""")
        conn.commit()
        conn.close()

    def execute(self, query, params=None, fetch=False):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query, params or [])
        conn.commit()
        rows = cur.fetchall() if fetch else None
        conn.close()
        return [dict(row) for row in rows] if rows else None

    # Node CRUD
    def add_node(self, node: dict):
        node = NodeModel(**node)
        return self.execute("""INSERT INTO nodes (name,address,network,port,status,last_sync,notes,created_date,updated_date) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (node.name, node.address, node.network, node.port, node.status, 
             datetime.now(), node.notes, datetime.now(), datetime.now()))
    def delete_node(self, node_id): self.execute("DELETE FROM nodes WHERE id=?", (node_id,))
    def get_all_nodes(self): return self.execute("SELECT * FROM nodes", fetch=True)

    # Wallet CRUD
    def add_wallet(self, wallet: dict):
        wallet = WalletModel(**wallet)
        priv = self.crypto.encrypt(wallet.private_key) if wallet.private_key else ''
        return self.execute("""INSERT INTO wallets (name,address,network,type,balance,private_key,notes,created_date,updated_date) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (wallet.name, wallet.address, wallet.network, wallet.type, wallet.balance, 
             priv, wallet.notes, datetime.now(), datetime.now()))
    def delete_wallet(self, wallet_id): self.execute("DELETE FROM wallets WHERE id=?", (wallet_id,))
    def get_all_wallets(self):
        wallets = self.execute("SELECT * FROM wallets", fetch=True) or []
        for w in wallets:
            if w.get('private_key'):
                w['private_key'] = self.crypto.decrypt(w['private_key'])
        return wallets

    # Airdrop CRUD
    def add_airdrop(self, airdrop: dict):
        airdrop = AirdropModel(**airdrop)
        return self.execute("""INSERT INTO airdrops (project_name,network,airdrop_type,eligibility_requirements,start_date,end_date,
                           claim_date,status,estimated_value,wallet_address,tasks_completed,notes,created_date,updated_date)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
           (airdrop.project_name, airdrop.network, airdrop.airdrop_type, airdrop.eligibility_requirements,
            airdrop.start_date, airdrop.end_date, airdrop.claim_date, airdrop.status,
            airdrop.estimated_value, airdrop.wallet_address, airdrop.tasks_completed, airdrop.notes, datetime.now(), datetime.now()))
    def delete_airdrop(self, airdrop_id): self.execute("DELETE FROM airdrops WHERE id=?", (airdrop_id,))
    def get_all_airdrops(self): return self.execute("SELECT * FROM airdrops", fetch=True)
