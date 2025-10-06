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

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Dali-Math/node-vault-py.git
   cd node-vault-py
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

### Building Standalone Executable

To create a standalone Windows executable (.exe):

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build the Executable**
   ```bash
   pyinstaller --onefile --windowed --name NodeVaultPy main.py
   ```

3. **Locate the Executable**
   - The .exe file will be in the `dist` folder
   - You can distribute this file without requiring Python installation

### Alternative: Using Auto-py-to-exe

For a GUI-based approach to creating executables:

1. **Install auto-py-to-exe**
   ```bash
   pip install auto-py-to-exe
   ```

2. **Launch the Tool**
   ```bash
   auto-py-to-exe
   ```

3. **Configure Settings**
   - Select `main.py` as the script
   - Choose "One File" option
   - Choose "Window Based" (no console)
   - Add application icon if desired
   - Click "Convert .py to .exe"

## Configuration

The application uses a local SQLite database to store all data securely. On first run, the database will be created automatically.

### Security Recommendations
- Always encrypt sensitive data (private keys)
- Keep regular backups of your database file
- Use strong passwords for encrypted fields
- Store the application in a secure location

## Usage

1. **Launch the application**
2. **Add Nodes**: Navigate to Node Management tab and add your blockchain nodes
3. **Add Wallets**: Use Wallet Management to add and organize your wallet addresses
4. **Track Airdrops**: Add airdrop campaigns in the Airdrop Management section
5. **Update Status**: Regularly update the status of your nodes, wallets, and airdrops
6. **Export Data**: Use the export function to backup your data

## Project Structure

```
node-vault-py/
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
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
