import tkinter as tk
from tkinter import ttk, messagebox

class AirdropManager:
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.airdrops = []
        self.setup_ui()
        self.load_airdrops()

    def setup_ui(self):
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(toolbar, text="Add Airdrop", command=self.add_airdrop).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Edit Airdrop", command=self.edit_airdrop).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Delete Airdrop", command=self.delete_airdrop).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.load_airdrops).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Project', 'Network', 'Type', 'Status', 'Wallet')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', selectmode='browse')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=115 if col != 'ID' else 50)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', lambda e: self.edit_airdrop())

    def load_airdrops(self):
        self.tree.delete(*self.tree.get_children())
        self.airdrops = self.db_manager.get_all_airdrops() or []
        for a in self.airdrops:
            self.tree.insert('', 'end', values=(
                a.get('id'), a.get('project_name'), a.get('network'), a.get('airdrop_type'),
                a.get('status'), a.get('wallet_address')))

    def add_airdrop(self):
        AirdropDialog(self.parent, self.db_manager, callback=self.load_airdrops)

    def edit_airdrop(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        AirdropDialog(self.parent, self.db_manager, airdrop_id=item['values'][0], callback=self.load_airdrops)

    def delete_airdrop(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        aid = item['values'][0]
        if messagebox.askyesno("Confirm", "Delete this airdrop?"):
            self.db_manager.delete_airdrop(aid)
            self.load_airdrops()

class AirdropDialog:
    def __init__(self, parent, db_manager, airdrop_id=None, callback=None):
        self.db_manager = db_manager
        self.airdrop_id = airdrop_id
        self.callback = callback
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Airdrop" if airdrop_id else "Add Airdrop")
        self.dialog.geometry("400x500")
        self.setup_ui()
        if airdrop_id:
            self.load_data()
    def setup_ui(self):
        f = ttk.Frame(self.dialog, padding=20)
        f.pack(fill=tk.BOTH, expand=True)
        self.project = tk.StringVar()
        self.network = tk.StringVar()
        self.type = tk.StringVar(value="Retroactive")
        self.status = tk.StringVar(value="Active")
        self.wallet = tk.StringVar()

        ttk.Label(f, text="Project").grid(row=0, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.project).grid(row=0, column=1)
        ttk.Label(f, text="Network").grid(row=1, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.network).grid(row=1, column=1)
        ttk.Label(f, text="Type").grid(row=2, column=0, sticky='w')
        ttk.Combobox(f, textvariable=self.type, values=["Retroactive", "Task-based", "Holder"]).grid(row=2, column=1)
        ttk.Label(f, text="Status").grid(row=3, column=0, sticky='w')
        ttk.Combobox(f, textvariable=self.status, values=["Active", "Pending", "Claimed", "Missed"]).grid(row=3, column=1)
        ttk.Label(f, text="Wallet").grid(row=4, column=0, sticky='w')
        ttk.Entry(f, textvariable=self.wallet).grid(row=4, column=1)

        ttk.Button(f, text="Save", command=self.save).grid(row=10, column=0, pady=16)
        ttk.Button(f, text="Cancel", command=self.dialog.destroy).grid(row=10, column=1)
    def load_data(self):
        ads = self.db_manager.execute("SELECT * FROM airdrops WHERE id=?", (self.airdrop_id,), fetch=True)
        if not ads: return
        a = ads[0]
        self.project.set(a['project_name'])
        self.network.set(a['network'])
        self.type.set(a['airdrop_type'])
        self.status.set(a['status'])
        self.wallet.set(a.get('wallet_address',''))
    def save(self):
        data = {
            'project_name': self.project.get(),
            'network': self.network.get(),
            'airdrop_type': self.type.get(),
            'status': self.status.get(),
            'wallet_address': self.wallet.get(),
        }
        if self.airdrop_id:
            self.db_manager.execute(
                "UPDATE airdrops SET project_name=?, network=?, airdrop_type=?, status=?, wallet_address=? WHERE id=?",
                (data['project_name'], data['network'], data['airdrop_type'], data['status'], data['wallet_address'], self.airdrop_id))
        else:
            self.db_manager.add_airdrop(data)
        if self.callback: self.callback()
        self.dialog.destroy()
