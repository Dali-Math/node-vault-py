        if not address:
            messagebox.showerror('Error', 'Wallet address is required')
            return

        network = self.network_var.get().strip()
        wtype = self.type_var.get().strip() or 'Hot'
        balance = self.balance_var.get().strip() or '0'
        notes = self.notes_text.get('1.0', 'end-1c')
        priv = self.private_key_var.get().strip()

        data = {
            'name': name,
            'address': address,
            'network': network,
            'type': wtype,
            'balance': balance,
            # Private key encryption is handled by db_manager using the master key
            'private_key': priv,
            'notes': notes,
        }

        try:
            if self.wallet_id:
                self.db_manager.update_wallet(self.wallet_id, data)
                messagebox.showinfo('Success', 'Wallet updated successfully')
            else:
                # When creating, set created_date on insertion time
                data['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.db_manager.add_wallet(data)
                messagebox.showinfo('Success', 'Wallet added successfully')
            if self.callback:
                self.callback()
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to save wallet: {e}')
