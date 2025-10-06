"""Node Manager Module - GUI component for managing blockchain nodes"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime


class NodeManager:
    """Manager for blockchain nodes"""
    
    def __init__(self, parent, db_manager):
        self.parent = parent
        self.db_manager = db_manager
        self.nodes = []
        
        self.setup_ui()
        self.load_nodes()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Add Node", command=self.add_node).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Edit Node", command=self.edit_node).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Delete Node", command=self.delete_node).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.load_nodes).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Export", command=self.export_nodes).pack(side=tk.LEFT, padx=5)
        
        # Search bar
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_nodes)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('ID', 'Name', 'Address', 'Network', 'Port', 'Status', 'Last Sync')
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
        self.tree.bind('<Double-1>', lambda e: self.edit_node())
        
    def load_nodes(self):
        """Load nodes from database"""
        self.tree.delete(*self.tree.get_children())
        self.nodes = self.db_manager.get_all_nodes()
        
        for node in self.nodes:
            self.tree.insert('', 'end', values=(
                node['id'],
                node['name'],
                node['address'],
                node['network'],
                node['port'],
                node['status'],
                node.get('last_sync', 'N/A')
            ))
            
    def filter_nodes(self, *args):
        """Filter nodes based on search query"""
        query = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        
        for node in self.nodes:
            if (query in str(node['name']).lower() or 
                query in str(node['address']).lower() or
                query in str(node['network']).lower()):
                self.tree.insert('', 'end', values=(
                    node['id'],
                    node['name'],
                    node['address'],
                    node['network'],
                    node['port'],
                    node['status'],
                    node.get('last_sync', 'N/A')
                ))
                
    def add_node(self):
        """Add new node"""
        NodeDialog(self.parent, self.db_manager, callback=self.load_nodes)
        
    def edit_node(self):
        """Edit selected node"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a node to edit")
            return
            
        item = self.tree.item(selection[0])
        node_id = item['values'][0]
        NodeDialog(self.parent, self.db_manager, node_id=node_id, callback=self.load_nodes)
        
    def delete_node(self):
        """Delete selected node"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a node to delete")
            return
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this node?"):
            item = self.tree.item(selection[0])
            node_id = item['values'][0]
            self.db_manager.delete_node(node_id)
            self.load_nodes()
            messagebox.showinfo("Success", "Node deleted successfully")
            
    def export_nodes(self):
        """Export nodes to CSV"""
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
                    writer.writerow(['ID', 'Name', 'Address', 'Network', 'Port', 'Status', 'Last Sync', 'Notes'])
                    for node in self.nodes:
                        writer.writerow([
                            node['id'],
                            node['name'],
                            node['address'],
                            node['network'],
                            node['port'],
                            node['status'],
                            node.get('last_sync', ''),
                            node.get('notes', '')
                        ])
                messagebox.showinfo("Success", f"Exported {len(self.nodes)} nodes to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")


class NodeDialog:
    """Dialog for adding/editing nodes"""
    
    def __init__(self, parent, db_manager, node_id=None, callback=None):
        self.db_manager = db_manager
        self.node_id = node_id
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Node" if node_id else "Add Node")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
        if node_id:
            self.load_node_data()
            
    def setup_ui(self):
        """Setup dialog UI"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Fields
        ttk.Label(main_frame, text="Node Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, pady=5)
        
        ttk.Label(main_frame, text="Node Address:").grid(row=1, column=0, sticky='w', pady=5)
        self.address_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.address_var, width=40).grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Network Type:").grid(row=2, column=0, sticky='w', pady=5)
        self.network_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.network_var, width=40).grid(row=2, column=1, pady=5)
        
        ttk.Label(main_frame, text="Port:").grid(row=3, column=0, sticky='w', pady=5)
        self.port_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.port_var, width=40).grid(row=3, column=1, pady=5)
        
        ttk.Label(main_frame, text="Status:").grid(row=4, column=0, sticky='w', pady=5)
        self.status_var = tk.StringVar(value="Active")
        ttk.Combobox(main_frame, textvariable=self.status_var, 
                     values=['Active', 'Inactive'], width=37).grid(row=4, column=1, pady=5)
        
        ttk.Label(main_frame, text="Notes:").grid(row=5, column=0, sticky='nw', pady=5)
        self.notes_text = scrolledtext.ScrolledText(main_frame, width=40, height=10)
        self.notes_text.grid(row=5, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def load_node_data(self):
        """Load existing node data"""
        node = self.db_manager.get_node(self.node_id)
        if node:
            self.name_var.set(node['name'])
            self.address_var.set(node['address'])
            self.network_var.set(node['network'])
            self.port_var.set(node['port'])
            self.status_var.set(node['status'])
            self.notes_text.insert('1.0', node.get('notes', ''))
            
    def save(self):
        """Save node"""
        # Validate
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Node name is required")
            return
            
        if not self.address_var.get().strip():
            messagebox.showerror("Error", "Node address is required")
            return
        
        # Prepare data
        node_data = {
            'name': self.name_var.get().strip(),
            'address': self.address_var.get().strip(),
            'network': self.network_var.get().strip(),
            'port': self.port_var.get().strip(),
            'status': self.status_var.get(),
            'notes': self.notes_text.get('1.0', 'end-1c'),
            'last_sync': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            if self.node_id:
                self.db_manager.update_node(self.node_id, node_data)
                messagebox.showinfo("Success", "Node updated successfully")
            else:
                self.db_manager.add_node(node_data)
                messagebox.showinfo("Success", "Node added successfully")
                
            if self.callback:
                self.callback()
                
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save node: {str(e)}")
