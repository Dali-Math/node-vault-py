"""Wallet Manager Module - GUI component for managing cryptocurrency wallets"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

class WalletManager:
    """Manager for cryptocurrency wallets"""
    
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.wallets = []
        
        self.setup_ui()
        self.load_wallets()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Add Wallet", command=self.add_wallet).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Edit Wallet", command=self.edit_wallet).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Delete Wallet", command=self.delete_wallet).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.load_wallets).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Export", command=self.export_wallets).pack(side=tk.LEFT, padx=5)
        
        # Search bar
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_wallets)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Address', 'Network', 'Type', 'Balance', 'Created')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings', selectmode='browse')
        
        # Column headers
        self.tree.heading('#0', text='', anchor='w')
        self.tree.column('#0', width=0, stretch=False)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == 'ID':
                self.tree.column(col, width=50)
            elif col == 'Address':
                self.tree.column(col, width=200)
            else:
                self.tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_wallet())
        
    def load_wallets(self):
        """Load wallets from database"""
        self.tree.delete(*self.tree.get_children())
        self.wallets = self.db_manager.get_all_wallets()
        
        for wallet in self.wallets:
            self.tree.insert('', 'end', values=(
                wallet['id'],
                wallet['name'],
                wallet['address'][:20] + '...' if len(wallet['address']) > 20 else wallet['address'],
                wallet['network'],
                wallet['type'],
                wallet.get('balance', '0'),
                wallet.get('created_date', 'N/A')
            ))
            
    def filter_wallets(self, *args):
        """Filter wallets based on search query"""
        query = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        
        for wallet in self.wallets:
            if (query in str(wallet['name']).lower() or 
                query in str(wallet['address']).lower() or
                query in str(wallet['network']).lower()):
                self.tree.insert('', 'end', values=(
                    wallet['id'],
                    wallet['name'],
                    wallet['address'][:20] + '...' if len(wallet['address']) > 20 else wallet['address'],
                    wallet['network'],
                    wallet['type'],
                    wallet.get('balance', '0'),
                    wallet.get('created_date', 'N/A')
                ))
                
    def add_wallet(self):
        """Add new wallet"""
        WalletDialog(self.parent, self.db_manager, callback=self.load_wallets)
        
    def edit_wallet(self):
        """Edit selected wallet"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a wallet to edit")
            return
            
        item = self.tree.item(selection[0])
        wallet_id = item['values'][0]
        WalletDialog(self.parent, self.db_manager, wallet_id=wallet_id, callback=self.load_wallets)
        
    def delete_wallet(self):
        """Delete selected wallet"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a wallet to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this wallet?"):
            item = self.tree.item(selection[0])
            wallet_id = item['values'][0]
            self.db_manager.delete_wallet(wallet_id)
            self.load_wallets()
            messagebox.showinfo("Success", "Wallet deleted successfully")
            
    def export_wallets(self):
        """Export wallets to CSV"""
        try:
            from tkinter import filedialog
            import csv
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['ID', 'Name', 'Address', 'Network', 'Type', 'Balance', 'Created', 'Notes'])
                    for wallet in self.wallets:
                        writer.writerow([
                            wallet['id'],
                            wallet['name'],
                            wallet['address'],
                            wallet['network'],
                            wallet['type'],
                            wallet.get('balance', ''),
                            wallet.get('created_date', ''),
                            wallet.get('notes', '')
                        ])
                messagebox.showinfo("Success", f"Exported {len(self.wallets)} wallets to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

class WalletDialog:
    """Dialog for adding/editing wallets"""
    
    def __init__(self, parent, db_manager, wallet_id=None, callback=None):
        self.db_manager = db_manager
        self.wallet_id = wallet_id
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Wallet" if wallet_id else "Add Wallet")
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
        if wallet_id:
            self.load_wallet_data()
            
    def setup_ui(self):
        """Setup dialog UI"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fields
        ttk.Label(main_frame, text="Wallet Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=50).grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="Public Address:").grid(row=1, column=0, sticky='w', pady=5)
        self.address_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.address_var, width=50).grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Blockchain/Network:").grid(row=2, column=0, sticky='w', pady=5)
        self.network_var = tk.StringVar()
        ttk.Combobox(main_frame, textvariable=self.network_var, 
                     values=['Ethereum', 'Bitcoin', 'BSC', 'Polygon', 'Avalanche', 'Solana', 'Other'],
                     width=47).grid(row=2, column=1, pady=5)
        
        ttk.Label(main_frame, text="Wallet Type:").grid(row=3, column=0, sticky='w', pady=5)
        self.type_var = tk.StringVar(value="Hot")
        ttk.Combobox(main_frame, textvariable=self.type_var, 
                     values=['Hot', 'Cold', 'Hardware'], width=47).grid(row=3, column=1, pady=5)
        
        ttk.Label(main_frame, text="Balance:").grid(row=4, column=0, sticky='w', pady=5)
        self.balance_var = tk.StringVar(value="0")
        ttk.Entry(main_frame, textvariable=self.balance_var, width=50).grid(row=4, column=1, pady=5)
        
        ttk.Label(main_frame, text="Private Key (Encrypted):").grid(row=5, column=0, sticky='w', pady=5)
        self.private_key_var = tk.StringVar()
        private_key_entry = ttk.Entry(main_frame, textvariable=self.private_key_var, width=50, show="*")
        private_key_entry.grid(row=5, column=1, pady=5)
        
        ttk.Label(main_frame, text="Notes:").grid(row=6, column=0, sticky='nw', pady=5)
        self.notes_text = scrolledtext.ScrolledText(main_frame, width=50, height=12)
        self.notes_text.grid(row=6, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def load_wallet_data(self):
        """Load existing wallet data"""
        wallet = self.db_manager.get_wallet(self.wallet_id)
        if wallet:
            self.name_var.set(wallet['name'])
            self.address_var.set(wallet['address'])
            self.network_var.set(wallet['network'])
            self.type_var.set(wallet['type'])
            self.balance_var.set(wallet.get('balance', '0'))
            self.private_key_var.set(wallet.get('private_key', ''))
            self.notes_text.insert('1.0', wallet.get('notes', ''))
            
    def save(self):
        """Save wallet"""
        # Validate
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Wallet name is required")
            return
            
        if not self.address_var.get().strip():
            messagebox.showerror("Error", "Wallet address is required")
            return
        
        # Prepare data
        wallet_data = {
            'name': self.name_var.get().strip(),
            'address': self.address_var.get().strip(),
            'network': self.network_var.get().strip(),
            'type': self.type_var.get(),
            'balance': self.balance_var.get().strip(),
            'private_key': self.private_key_var.get().strip(),  # Should be encrypted by db_manager
            'notes': self.notes_text.get('1.0', 'end-1c'),
            'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            if self.wallet_id:
                self.db_manager.update_wallet(self.wallet_id, wallet_data)
                messagebox.showinfo("Success", "Wallet updated successfully")
            else:
                self.db_manager.add_wallet(wallet_data)
                messagebox.showinfo("Success", "Wallet added successfully")
                
            if self.callback:
                self.callback()
                
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save wallet: {str(e)}")
