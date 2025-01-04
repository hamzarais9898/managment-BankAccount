from models import *
from datetime import datetime
import dal
from User_module import User

class Bank:
    def __init__(self):
        self.accounts = []
        self.users = []
    
    def load(self):
        if not self.accounts:
            print("Aucun compte à charger.")
            return
        print(dal.insert_accounts(self.accounts))
        dal.insert_user(self.users)
    
    def search(self,numaccount:int)->BankAccount: # type: ignore
        for account in self.accounts:
            if account.id == numaccount:
                return account
        print(f'Account  numéro {numaccount} est introuvable')
        
    def list(self):
        if not self.accounts:
            print("Aucun compte disponible.")
            return
        
        # Trier les comptes par solde (balance)
        sorted_accounts = sorted(self.accounts, key=lambda account: account.balance)
        
        print("\nListe des comptes (triés par solde) :")
        print(f"{'ID':<5}{'Type':<15}{'Balance':<10}")
        print("-" * 35)
        for account in sorted_accounts:
            account_type = type(account).__name__
            print(f"{account.id:<5}{account_type:<15}{account.balance:<10.2f}")
            
    def create(self,account:BankAccount):
        for existing_accounts in self.accounts:
            if account.id == existing_accounts.id:
                print(f"Compte numéro {account.id} existe déjà")
                return
        
        self.accounts.append(account)
        print(f'Account N° {account.id} créé avec succès')
    
    def createuser(self,user:User):
        for existing_user in self.users:
            if user.id == existing_user.id:
                print(f'Utilisateur N° {user.id} existe déjà')
                return
        
        self.users.append(user)
        print(f'Utilisateur N° {user.id} créé avec succès')
     
    def deposite(self,account_id:int,amount:float):
        
        account = next((acc for acc in self.accounts if acc.id == account_id), None)
        if account is None:
            print(f"Compte numéro {account_id} n'est pas trouvé.")
            return
        
        account.deposit(amount,False)
        
    def withdrow(self,account_id:int,amount:float):
        
        account = next((acc for acc in self.accounts if acc.id == account_id), None)
        if account is None:
            print(f"Compte numéro {account_id} n'est pas trouvé.")
            return
        
        
        account.withdrow(amount,False)
        
    def transfert(self,accountfrom_id:int,accountto_id:int,amount:float):
        accountfrom:BankAccount =  next((acc for acc in self.accounts if acc.id == accountfrom_id), None) # type: ignore
        accountto:BankAccount =  next((acc for acc in self.accounts if acc.id == accountto_id), None) # type: ignore
        
        if(accountfrom is None or accountto is None):
            print(f"Compte numéro {accountfrom_id} ou {accountto_id} est introuvable")
        
        accountfrom.transfer(accountto,amount)
        
        
        
    def delete(self,account:BankAccount):
        self.accounts.remove(account)
        
    def receipt(self,account_id: int):
        
        account = next((acc for acc in self.accounts if acc.id == account_id), None)
        
        if account is None:
            print(f"Compte numéro {account_id} n'est pas trouvé.")
            return
        
        print(f"\nRelevé du compte : {account.id}")
        print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'Date/Heure':<20}{'Type d\'opération':<20}{'Montant':<10}")
        print("-" * 50)
        
        for op in account.operation:
            date = op["date"].strftime('%Y-%m-%d %H:%M:%S')
            operation_type = op["type"]
            amount = op["amount"]
            print(f"{date:<20}{operation_type:<20}{amount:<10.2f}")

        print(f"\nSolde final : {account.balance:.2f} DH")
        
    
    def load_from_database(self):
        
        # Charger les comptes depuis la base de données
        accounts_data = dal.fetch_accounts()
        for account_data in accounts_data:
            # Identifier le type de compte et créer une instance
            account_type = account_data['BankAccountType'] # type: ignore
            balance:int = account_data['Balance'] # type: ignore
            account_id = account_data['id'] # type: ignore
            
            if account_type == "SavingAccount":
                account = SavingAccount(0.03, balance)  # Exemple : taux d'intérêt par défaut
            elif account_type == "ChekingAccount":
                account = ChekingAccount(balance)
            else:
                print(f"Type de compte inconnu : {account_type}")
                continue 
            account.id = account_id # type: ignore
            BankAccount.id = max(BankAccount.id, account_id + 1)  # type: ignore # Ajuster l'auto-incrément
            
            # Charger les opérations pour ce compte
            operations_data = dal.fetch_operations(account_id)
            for operation in operations_data:
                account.operation.append({
                    "date": operation["TransferDate"], # type: ignore
                    "type": operation["Type"],# type: ignore
                    "amount": operation["Amount"],# type: ignore
                    "account_id": operation["SourceAccountID"]# type: ignore
                })
            self.accounts.append(account)