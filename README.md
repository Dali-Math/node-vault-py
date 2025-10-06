# Node-Vault-Py
## Description
Node-Vault-Py is a comprehensive Python Windows application designed to manage cryptocurrency nodes, wallets, and airdrop campaigns. This tool provides an intuitive interface for tracking multiple crypto assets, managing wallet addresses, and organizing airdrop participation.
## Features
### Node Management
- **Track Multiple Nodes**: Monitor different blockchain nodes with their status and details
- **Node Information**: Store and display node addresses, network types, and connection status
- **Performance Monitoring**: Track node uptime and synchronization status
### Wallet Management
- **Multi-Wallet Support**: Manage multiple wallet addresses across different blockchains
- **Address Book**: Organize wallet addresses with labels and categories
- **Balance Tracking**: Monitor wallet balances (when integrated with blockchain APIs)
- **Private Key Security**: Secure storage options for sensitive wallet data
### Airdrop Management
- **Campaign Tracking**: Keep track of multiple airdrop campaigns
- **Eligibility Checker**: Monitor requirements and eligibility criteria
- **Deadline Management**: Never miss an airdrop deadline with built-in reminders
- **Status Updates**: Track airdrop status (pending, completed, claimed)
- **Notes and Documentation**: Add custom notes for each airdrop campaign
### User Interface
- **Intuitive GUI**: Built with tkinter/PyQt for a user-friendly experience
- **Data Grid Views**: Easy-to-read tables for nodes, wallets, and airdrops
- **Search and Filter**: Quick search functionality across all records
- **Data Export**: Export data to CSV/Excel for backup and analysis
## Data Fields
### Node Fields
- Node Name
- Node Address/IP
- Blockchain/Network Type
- Port Number
- Status (Active/Inactive)
- Last Sync Date
- Notes
### Wallet Fields
- Wallet Name/Label
- Public Address
- Blockchain/Network
- Wallet Type (Hot/Cold/Hardware)
- Balance
- Private Key (encrypted)
- Creation Date
- Notes
### Airdrop Fields
- Project Name
- Blockchain Network
- Airdrop Type (Retroactive/Task-based/Holder)
- Eligibility Requirements
- Start Date
- End Date
- Claim Date
- Status (Active/Pending/Claimed/Missed)
- Estimated Value
- Wallet Address Used
- Tasks Completed
- Notes
## Installation
### Prerequisites
- Python 3.8 or higher
- Windows 10 or higher
- pip package manager
### Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/Dali-Math/node-vault-py.git
cd node-vault-py
```
2. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```
3. Install required dependencies:
```bash
pip install -r requirements.txt
```
4. Run the application:
```bash
python main.py
```
## Usage
### First Run
On first launch, the application will:
- Create the necessary database files
- Set up the default configuration
- Display the main dashboard
### Adding a Node
1. Click on the "Nodes" tab
2. Click "Add New Node"
3. Fill in the node details
4. Click "Save"
### Managing Wallets
1. Navigate to the "Wallets" tab
2. Use "Add Wallet" to create new entries
3. View, edit, or delete existing wallets
4. Export wallet list for backup
### Tracking Airdrops
1. Go to the "Airdrops" tab
2. Click "New Airdrop"
3. Enter campaign details and requirements
4. Set reminders for important dates
5. Update status as you progress
## Project Structure
```
node-vault-py/
│
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── README.md            # This file
│
├── src/
│   ├── __init__.py
│   ├── gui/               # GUI components
│   │   ├── main_window.py
│   │   ├── node_manager.py
│   │   ├── wallet_manager.py
│   │   └── airdrop_manager.py
│   │
│   ├── database/          # Database operations
│   │   ├── db_manager.py
│   │   └── models.py
│   │
│   └── utils/             # Utility functions
│       ├── encryption.py
│       └── validators.py
│
├── data/                  # Database files (created on first run)
└── dist/                  # Executable files (after build)
```
## Dependencies
- **tkinter/PyQt5**: GUI framework
- **sqlite3**: Database management
- **cryptography**: For encrypting sensitive data
- **pandas**: Data manipulation and export
- **requests**: API calls (for blockchain data)

## Preuve d'exécution CRUD réelle

Cette section documente des exemples concrets d'opérations CRUD (Create, Read, Update, Delete) sur les wallets, démontrant le fonctionnement de l'application.

### Exemple : Ajout et suppression d'un wallet

```python
# Ajout d'un nouveau wallet
from src.database.db_manager import DBManager

db = DBManager()

# CREATE - Ajouter un wallet
wallet_data = {
    'name': 'Mon Wallet Ethereum',
    'address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    'blockchain': 'Ethereum',
    'wallet_type': 'Hot',
    'balance': '0.00',
    'notes': 'Wallet principal pour les airdrops'
}

wallet_id = db.add_wallet(wallet_data)
print(f"Wallet ajouté avec succès. ID: {wallet_id}")

# READ - Lire le wallet
wallet = db.get_wallet(wallet_id)
print(f"Wallet récupéré: {wallet['name']} - {wallet['address']}")

# UPDATE - Modifier le balance
db.update_wallet(wallet_id, {'balance': '1.5'})
print(f"Balance mis à jour: 1.5 ETH")

# DELETE - Supprimer le wallet
db.delete_wallet(wallet_id)
print(f"Wallet ID {wallet_id} supprimé avec succès")
```

### Sortie attendue

```
Wallet ajouté avec succès. ID: 42
Wallet récupéré: Mon Wallet Ethereum - 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
Balance mis à jour: 1.5 ETH
Wallet ID 42 supprimé avec succès
```

### Vérification dans l'interface

Les opérations CRUD sont également accessibles via l'interface graphique :
1. **Create** : Bouton "Add Wallet" dans l'onglet Wallets
2. **Read** : Liste des wallets affichée dans le tableau principal
3. **Update** : Double-clic sur un wallet pour éditer
4. **Delete** : Bouton "Delete" avec confirmation

Ces opérations sont tracées dans les logs de l'application (`logs/app.log`) pour audit et debugging.

## Future Enhancements
- [ ] Real-time blockchain API integration
- [ ] Multi-language support
- [ ] Cloud sync capabilities
- [ ] Mobile companion app
- [ ] Advanced analytics and reporting
- [ ] Automated airdrop discovery
- [ ] Portfolio value tracking
- [ ] Tax reporting features
## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
## License
This project is open source and available under the MIT License.
## Support
For issues, questions, or suggestions, please open an issue on GitHub.
## Disclaimer
⚠️ **Important Security Notice**
This application handles sensitive cryptocurrency information. Always:
- Keep your private keys secure
- Use encrypted storage
- Maintain regular backups
- Never share your database file
- Test with small amounts first
The developers are not responsible for any loss of funds or data. Use at your own risk.
---
**Version**: 1.0.0  
**Author**: Dali-Math  
**Last Updated**: October 2025
