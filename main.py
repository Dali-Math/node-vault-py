#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Node-Vault-Py - Main Application Entry Point
Cryptocurrency Node, Wallet, and Airdrop Management System

Author: Dali-Math
Version: 1.0.0
License: MIT
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Color scheme: Dark background with gold accents
COLORS = {
    'bg_dark': '#1a1a1a',
    'bg_medium': '#2d2d2d',
    'bg_light': '#3d3d3d',
    'gold': '#FFD700',
    'gold_dark': '#B8860B',
    'text_white': '#FFFFFF',
    'text_gray': '#CCCCCC',
    'accent_green': '#00FF00',
    'accent_red': '#FF4444'
}


class NodeVaultPyApp:
    """
    Main application class for Node-Vault-Py
    Manages the main window and coordinates all application modules
    """
    
    def __init__(self):
        """Initialize the main application window"""
        self.root = tk.Tk()
        self.root.title("Node-Vault-Py v1.0.0 - Crypto Management System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Configure the main window background
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Set up the UI
        self._setup_styles()
        self._create_header()
        self._create_main_content()
        self._create_footer()
        
    def _setup_styles(self):
        """Configure custom styles for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Notebook (tabs) style
        style.configure('Custom.TNotebook', 
                       background=COLORS['bg_dark'],
                       borderwidth=0)
        style.configure('Custom.TNotebook.Tab',
                       background=COLORS['bg_medium'],
                       foreground=COLORS['text_gray'],
                       padding=[20, 10],
                       font=('Arial', 10, 'bold'))
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', COLORS['bg_light'])],
                 foreground=[('selected', COLORS['gold'])])
        
        # Configure Frame style
        style.configure('Custom.TFrame',
                       background=COLORS['bg_dark'])
        
    def _create_header(self):
        """Create the application header with title and branding"""
        header_frame = tk.Frame(self.root, bg=COLORS['bg_medium'], height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)
        
        # Application title
        title_label = tk.Label(
            header_frame,
            text="🔐 NODE-VAULT-PY",
            font=('Arial', 24, 'bold'),
            bg=COLORS['bg_medium'],
            fg=COLORS['gold']
        )
        title_label.pack(side='left', padx=30, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Cryptocurrency Management System",
            font=('Arial', 12),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_gray']
        )
        subtitle_label.pack(side='left', padx=10, pady=20)
        
        # Status indicator
        status_frame = tk.Frame(header_frame, bg=COLORS['bg_medium'])
        status_frame.pack(side='right', padx=30, pady=20)
        
        status_indicator = tk.Label(
            status_frame,
            text="●",
            font=('Arial', 20),
            bg=COLORS['bg_medium'],
            fg=COLORS['accent_green']
        )
        status_indicator.pack(side='left')
        
        status_text = tk.Label(
            status_frame,
            text="System Ready",
            font=('Arial', 10),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_gray']
        )
        status_text.pack(side='left', padx=5)
        
    def _create_main_content(self):
        """Create the main content area with navigation tabs"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self._create_dashboard_tab()
        self._create_nodes_tab()
        self._create_wallets_tab()
        self._create_airdrops_tab()
        self._create_settings_tab()
        
    def _create_dashboard_tab(self):
        """Create the dashboard overview tab"""
        dashboard_frame = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Welcome message
        welcome_label = tk.Label(
            dashboard_frame,
            text="Welcome to Node-Vault-Py!",
            font=('Arial', 18, 'bold'),
            bg=COLORS['bg_dark'],
            fg=COLORS['gold']
        )
        welcome_label.pack(pady=30)
        
        # Info cards container
        cards_frame = tk.Frame(dashboard_frame, bg=COLORS['bg_dark'])
        cards_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Create info cards
        self._create_info_card(cards_frame, "Nodes", "0", "Active nodes tracked")
        self._create_info_card(cards_frame, "Wallets", "0", "Wallets managed")
        self._create_info_card(cards_frame, "Airdrops", "0", "Active campaigns")
        
    def _create_info_card(self, parent, title, value, subtitle):
        """Create an info card widget"""
        card = tk.Frame(parent, bg=COLORS['bg_medium'], relief='raised', bd=2)
        card.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            card,
            text=title,
            font=('Arial', 14, 'bold'),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_gray']
        )
        title_label.pack(pady=(20, 10))
        
        value_label = tk.Label(
            card,
            text=value,
            font=('Arial', 36, 'bold'),
            bg=COLORS['bg_medium'],
            fg=COLORS['gold']
        )
        value_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            card,
            text=subtitle,
            font=('Arial', 10),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_gray']
        )
        subtitle_label.pack(pady=(10, 20))
        
    def _create_nodes_tab(self):
        """Create the node management tab"""
        nodes_frame = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(nodes_frame, text="🖥️ Nodes")
        
        label = tk.Label(
            nodes_frame,
            text="Node Management (Coming Soon)",
            font=('Arial', 16),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_gray']
        )
        label.pack(expand=True)
        
    def _create_wallets_tab(self):
        """Create the wallet management tab"""
        wallets_frame = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(wallets_frame, text="💰 Wallets")
        
        label = tk.Label(
            wallets_frame,
            text="Wallet Management (Coming Soon)",
            font=('Arial', 16),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_gray']
        )
        label.pack(expand=True)
        
    def _create_airdrops_tab(self):
        """Create the airdrop management tab"""
        airdrops_frame = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(airdrops_frame, text="🎁 Airdrops")
        
        label = tk.Label(
            airdrops_frame,
            text="Airdrop Management (Coming Soon)",
            font=('Arial', 16),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_gray']
        )
        label.pack(expand=True)
        
    def _create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = tk.Frame(self.notebook, bg=COLORS['bg_dark'])
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        label = tk.Label(
            settings_frame,
            text="Settings (Coming Soon)",
            font=('Arial', 16),
            bg=COLORS['bg_dark'],
            fg=COLORS['text_gray']
        )
        label.pack(expand=True)
        
    def _create_footer(self):
        """Create the application footer"""
        footer_frame = tk.Frame(self.root, bg=COLORS['bg_medium'], height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Footer text
        footer_label = tk.Label(
            footer_frame,
            text="Node-Vault-Py v1.0.0 | © 2025 Dali-Math | MIT License",
            font=('Arial', 9),
            bg=COLORS['bg_medium'],
            fg=COLORS['text_gray']
        )
        footer_label.pack(pady=10)
        
    def run(self):
        """Start the application main loop"""
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start the main loop
        self.root.mainloop()


def main():
    """
    Application entry point
    """
    print("Starting Node-Vault-Py...")
    print("Initializing cryptocurrency management system...")
    
    try:
        app = NodeVaultPyApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
