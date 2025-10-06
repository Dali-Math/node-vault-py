"""Main Window Module

This module contains the main application window with tabbed interface
for managing nodes, wallets, and airdrops.
"""

import tkinter as tk
from tkinter import ttk, messagebox, Menu
import sys
import os

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.gui.node_manager import NodeManager
from src.gui.wallet_manager import WalletManager
from src.gui.airdrop_manager import AirdropManager
from src.database.db_manager import DatabaseManager


class MainWindow:
    """Main application window with tabbed interface"""
    
    def __init__(self, root, master_key):
        """Initialize the main window
        
        Args:
            root: The Tk root window
            master_key: The master key for encryption
        """
        self.root = root
        self.master_key = master_key
        self.root.title("Node-Vault-Py - Crypto Management")
        self.root.geometry("1200x700")
        
        # Initialize database manager
        self.db_manager = DatabaseManager(master_key=self.master_key)
        
        # Set window icon (if available)
        try:
            # You can add an icon file later
            pass
        except:
            pass
        
        # Configure style
        self.configure_style()
        
        # Create menu bar
        self.create_menu()
        
        # Create main container
        self.create_widgets()
        
        # Configure window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def configure_style(self):
        """Configure the application theme and styles"""
        style = ttk.Style()
        style.theme_use('clam')  # Modern look
        
        # Configure colors
        bg_color = '#2C3E50'
        fg_color = '#ECF0F1'
        accent_color = '#3498DB'
        
        style.configure('TNotebook', background=bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background='#34495E', foreground=fg_color,
                       padding=[20, 10], font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', accent_color)],
                 foreground=[('selected', fg_color)])
        
        # Configure frame style
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color,
                       font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 9))
        
    def create_menu(self):
        """Create application menu bar"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Backup Database", command=self.backup_database)
        file_menu.add_command(label="Restore Database", command=self.restore_database)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        
    def create_widgets(self):
        """Create the main widgets and layout"""
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_tabs()
        
        # Create status bar
        self.create_status_bar()
        
    def create_tabs(self):
        """Create and populate tabs"""
        # Node Manager Tab
        node_frame = ttk.Frame(self.notebook)
        self.notebook.add(node_frame, text="  Nodes  ")
        self.node_manager = NodeManager(node_frame, self.db_manager)
        
        # Wallet Manager Tab
        wallet_frame = ttk.Frame(self.notebook)
        self.notebook.add(wallet_frame, text="  Wallets  ")
        self.wallet_manager = WalletManager(wallet_frame, self.db_manager)
        
        # Airdrop Manager Tab
        airdrop_frame = ttk.Frame(self.notebook)
        self.notebook.add(airdrop_frame, text="  Airdrops  ")
        self.airdrop_manager = AirdropManager(airdrop_frame, self.db_manager)
        
    def create_status_bar(self):
        """Create status bar at bottom of window"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN,
                                   anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_status(self, message):
        """Update status bar message
        
        Args:
            message: Status message to display
        """
        self.status_bar.config(text=message)
        self.root.update_idletasks()
        
    def backup_database(self):
        """Backup the database"""
        try:
            from tkinter import filedialog
            from datetime import datetime
            import shutil
            
            # Get backup location
            default_name = f"node_vault_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")],
                initialfile=default_name
            )
            
            if file_path:
                # Copy database file
                db_path = os.path.join('data', 'node_vault.db')
                if os.path.exists(db_path):
                    shutil.copy2(db_path, file_path)
                    messagebox.showinfo("Success", "Database backed up successfully!")
                    self.update_status("Database backed up")
                else:
                    messagebox.showerror("Error", "Database file not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup database: {str(e)}")
            
    def restore_database(self):
        """Restore database from backup"""
        try:
            from tkinter import filedialog
            import shutil
            
            # Confirm action
            if not messagebox.askyesno("Confirm Restore",
                                       "This will replace your current database. Continue?"):
                return
            
            # Get backup file
            file_path = filedialog.askopenfilename(
                title="Select backup file",
                filetypes=[("Database files", "*.db"), ("All files", "*.*")]
            )
            
            if file_path:
                # Close current database connection
                self.db_manager.close()
                
                # Restore database file
                db_path = os.path.join('data', 'node_vault.db')
                shutil.copy2(file_path, db_path)
                
                # Reinitialize database manager
                self.db_manager = DatabaseManager(master_key=self.master_key)
                
                # Refresh all managers
                self.node_manager.db_manager = self.db_manager
                self.wallet_manager.db_manager = self.db_manager
                self.airdrop_manager.db_manager = self.db_manager
                
                # Reload data
                self.node_manager.load_nodes()
                self.wallet_manager.load_wallets()
                self.airdrop_manager.load_airdrops()
                
                messagebox.showinfo("Success", "Database restored successfully!")
                self.update_status("Database restored")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restore database: {str(e)}")
            
    def show_about(self):
        """Show about dialog"""
        about_text = (
            "Node-Vault-Py\n"
            "Version 1.0.0\n\n"
            "A comprehensive Python Windows application\n"
            "for managing cryptocurrency nodes, wallets,\n"
            "and airdrop campaigns.\n\n"
            "Author: Dali-Math\n"
            "License: MIT\n"
            "© 2025"
        )
        messagebox.showinfo("About Node-Vault-Py", about_text)
        
    def show_documentation(self):
        """Open documentation"""
        import webbrowser
        webbrowser.open('https://github.com/Dali-Math/node-vault-py')
        
    def on_closing(self):
        """Handle window closing event"""
        if messagebox.askokcancel("Quit", "Do you want to quit Node-Vault-Py?"):
            # Close database connection
            self.db_manager.close()
            self.root.destroy()
            sys.exit(0)


if __name__ == "__main__":
    # For testing purposes
    root = tk.Tk()
    app = MainWindow(root, "test_master_key")
    root.mainloop()
