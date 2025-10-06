class NodeModel:
    def __init__(self, name, address, network="", port="", status="Active", notes=""):
        self.name = str(name)
        self.address = str(address)
        self.network = str(network)
        self.port = str(port)
        self.status = str(status)
        self.notes = notes

class WalletModel:
    def __init__(self, name, address, network="", type="Hot", balance="0", private_key="", notes=""):
        self.name = str(name)
        self.address = str(address)
        self.network = str(network)
        self.type = str(type)
        self.balance = str(balance)
        self.private_key = private_key
        self.notes = notes

class AirdropModel:
    def __init__(self, project_name, network, airdrop_type="Retroactive", eligibility_requirements="",
                 start_date="", end_date="", claim_date="", status="Active", estimated_value="0",
                 wallet_address="", tasks_completed="", notes=""):
        self.project_name = str(project_name)
        self.network = str(network)
        self.airdrop_type = str(airdrop_type)
        self.eligibility_requirements = eligibility_requirements
        self.start_date = start_date
        self.end_date = end_date
        self.claim_date = claim_date
        self.status = str(status)
        self.estimated_value = str(estimated_value)
        self.wallet_address = str(wallet_address)
        self.tasks_completed = tasks_completed
        self.notes = notes
