from models import *
from Bankaccount import *
from User_module import *
import dal

class Menu():
    def __init__(self,Title:str,Option:list[str]) -> None:
        self.Title = Title
        self.Option = Option
    
    def DisplayMenu(self):
        cp:int=1
        print(f'{'-' * 20} {self.Title} {'-' * 20}')
        for elem in self.Option:
            print(f'{cp}- {elem}')
            cp+=1
        print(f'{len(self.Option) + 1}- Exit')
    def choice(self)->int:
        while True:
            try:
                choice = int(input(f"Choisissez une option [1-{len(self.Option) + 1}]: "))
                if 1 <= choice <= len(self.Option) + 1:
                    return choice
                print("Veuillez choisir une option valide.")
            except ValueError:
                print("Entrée invalide, veuillez entrer un nombre.")
    

if __name__=="__main__":
    menu = Menu("Account Management", [
    "List All Accounts",
    "Search for Account",
    "Create Account",
    "Delete Account",
    "Deposit Amount",
    "Withdraw Amount",
    "Transfer",
    "Generate Receipt"
])     
bank = Bank()
#tawfir1:BankAccount = SavingAccount(0.01,200)    
#hisab1:BankAccount = ChekingAccount(500)

menu.DisplayMenu()
choix:int=0
#bank.load_from_database()
while(choix!=9):
    choix:int=menu.choice()
    if choix==1:
        bank.list()
    elif choix==2:
        account=bank.search(2)
        
        print(f'id : {account.id} ; type : {type(account).__name__} ; balance : {account.balance}')
    elif choix==3:
        #tawfir1:BankAccount = SavingAccount(0.01,200)    
        hisab1:BankAccount = ChekingAccount(500)
        #user:User = User("chainegaming2004@gmail.com","hamzay989","hamza rais",tawfir1.id)
        #user2:User = User("alizaime2003@gmial.com","iftahyasimsim","Zaime ali",hisab1.id)
        #bank.create(tawfir1)
        #bank.create(hisab1)
        #bank.createuser(user)
        #bank.createuser(user2)
        print(hisab1.id)
        dal.insert_accounts([hisab1])
        print(hisab1.id)
    elif choix==4:
        bank.delete(hisab1)
    elif choix==5:
        bank.deposite(1,1200)
        bank.deposite(1,500)
        bank.load()
    elif choix==6:
        bank.withdrow(1,750)
        bank.withdrow(1,200)
        bank.withdrow(1,2000)
        bank.load()
    elif choix==7:
        bank.transfert(1,2,150)
        bank.transfert(2,1,78)
        bank.transfert(2,1,300)
        bank.load()
    elif choix==8:
        bank.receipt(1)
    elif choix==9:
        exit()




#bank.create(tawfir1)
#bank.create(hisab1)
#bank.create(tawfir1)

#bank.deposite(tawfir1,1200)
#bank.deposite(tawfir1,500)
#bank.withdrow(tawfir1,750)
#bank.withdrow(tawfir1,200)
#bank.transfert(tawfir1,hisab1,150)
#bank.transfert(hisab1,tawfir1,78)

#bank.withdrow(hisab1,2000)

#bank.transfert(hisab1,tawfir1,300)

#bank.delete(hisab1)


""" found_account = bank.search(10)
if(found_account):
    print(f"Compte trouvé : ID={found_account.id}, Solde={found_account.balance}") """
    
#bank.list()

#bank.receipt(tawfir1)

