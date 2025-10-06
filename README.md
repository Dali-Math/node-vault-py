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

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## CRUD Execution Proof

The application has been tested with real database operations. Below is the console output demonstrating full CRUD functionality:

```
=== Node-Vault-Py CRUD Operations Test ===

Wallet ajouté avec succès. ID: 42
Wallet récupéré: Mon Wallet Ethereum - 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
Balance mis à jour: 1.5 ETH
Wallet ID 42 supprimé avec succès

=== Test completed successfully ===
```

### Visual Proof

![CRUD Operations](screenshots/crud-operations.png)

*Screenshot showing the application interface after CRUD operations*

## Build Windows

### Creating the Windows Executable

To build the Windows executable (NodeVaultPy.exe), use PyInstaller:

```bash
pip install pyinstaller
pyinstaller --name=NodeVaultPy --onefile --windowed --icon=icon.ico main.py
```

### Build Options

- `--onefile`: Creates a single executable file
- `--windowed`: Runs without console window (GUI mode)
- `--icon=icon.ico`: Sets the application icon (optional)

### Execution

After building, the executable will be located in:
```
dist/NodeVaultPy.exe
```

**To run the application:**
1. Navigate to the `dist` folder
2. Double-click `NodeVaultPy.exe`
3. No Python installation required on the target machine

### Distribution Note

Due to GitHub file size limitations, the compiled executable is not included in the repository. Users should build it locally using the PyInstaller command above.

**Alternative**: Pre-built releases may be available on the [Releases](https://github.com/Dali-Math/node-vault-py/releases) page.

## Usage

### Adding a Node
1. Click "Add Node" button
2. Fill in node details (name, address, network type)
3. Click "Save"

### Managing Wallets
1. Navigate to "Wallets" tab
2. Click "Add Wallet" to create a new wallet entry
3. Enter wallet details and save
4. Use "Edit" or "Delete" buttons to manage existing wallets

### Tracking Airdrops
1. Go to "Airdrops" tab
2. Click "Add Airdrop"
3. Enter project details, dates, and eligibility requirements
4. Track status and update as needed

## Security Notes

⚠️ **Important Security Considerations:**

- Private keys are encrypted using industry-standard encryption
- Database file (`node_vault.db`) should be backed up securely
- Never share your private keys or database file
- Use strong encryption passwords
- Regular backups recommended

## Database Structure

The application uses SQLite database with three main tables:
- `nodes`: Stores blockchain node information
- `wallets`: Stores wallet addresses and encrypted keys
- `airdrops`: Stores airdrop campaign tracking data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

- [ ] API integration for real-time balance updates
- [ ] Multi-language support
- [ ] Advanced reporting and analytics
- [ ] Mobile companion app
- [ ] Cloud backup integration

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Acknowledgments

- Built with Python and tkinter/PyQt
- Encryption powered by cryptography library
- Database management with SQLite3

---

**Made with ❤️ by Dali-Math**
