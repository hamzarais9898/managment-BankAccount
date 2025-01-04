from abc import ABC,abstractmethod
from typing import Final
from datetime import datetime
import dal

class BankAccount(ABC):
    #id:int=1#une proprièter hors du constructeur donc c'est une méthode de la class et non pas d'object
    
    def __init__(self,balance:float=0) -> None:
        self.balance=balance
        self.id = None
        self.operation=[]
    
    def deposit(self,amount:float,istransfère:bool)->float:
        self.balance += amount
        if not istransfère:
            self.operation.append({"date": datetime.now(),"type":"Depot","amount":amount})
            dal.insert_operations(datetime.now(),"Depot",amount,self.id)
        return amount
    
    @abstractmethod
    def withdrow(self,amount:float,istransfère:bool)->float:#cette méthode dépend du type de compte car il y a une contraint sur la balance à ne pas franchir la marge elle doit être abstraite et plus le savingaccount on ne peut pas tirer de ce type de compte
       pass
   
    
    def transfer(self,other:'BankAccount',amount:float)->float:
        withdraw_amount:float = self.withdrow(amount,True)
        other.deposit(withdraw_amount,True)
        self.operation.append({"date": datetime.now(),"type":"transfere sortant","amount":-amount})
        dest_account:str=f'transfere sortant to {other.id}'
        print(dest_account)
        dal.insert_operations(datetime.now(),dest_account,-amount,self.id)
        other.operation.append({"date": datetime.now(),"type":f"transfere entrant from {self.id}","amount":amount})
        source_account:str=f'transfere entrant from {self.id}'
        print(source_account)
        dal.insert_operations(datetime.now(),source_account,amount,other.id)
        return amount

        

class SavingAccount(BankAccount):
    SAVING_AMOUNT:Final[float]=100#constante
    def __init__(self,interestRate:float,balance:float) -> None:
        if balance > SavingAccount.SAVING_AMOUNT:
            super().__init__(balance)
            self.interestRate = interestRate
        else :
            print("montant insuffisant")
            return None
    
    def withdrow(self, amount: float,istransfère:bool)->float:
        if self.balance - amount >= SavingAccount.SAVING_AMOUNT:
            self.balance -= amount
            if not istransfère: 
                self.operation.append({"date": datetime.now(),"type":"Retrait","amount":-amount})
                dal.insert_operations(datetime.now(),"Retrait",-amount,self.id)
            return amount
        available_amount:float = self.balance - SavingAccount.SAVING_AMOUNT
        self.balance = SavingAccount.SAVING_AMOUNT
        if not istransfère:
            self.operation.append({"date": datetime.now(),"type":"Retrait","amount":-available_amount})
            dal.insert_operations(datetime.now(),"Retrait",-available_amount,self.id)
        return available_amount
    
    def addperiodiqueinterest(self)->float:
        interest:float=self.balance * self.interestRate
        self.balance += interest
        return interest
    
class ChekingAccount(BankAccount):
    FREE_TRANSACTIONS:Final[int]=3
    TRANSACTION_FEE:Final[float]=0.2
    DRAFT_OVER:Final[float]=500
    
    def __init__(self,balance: float = 0) -> None:
        super().__init__(balance)
        self.trasaction_count = 0
    
    def deposit(self, amount: float,istransfère:bool)->float:
        self.trasaction_count += 1
        super().deposit(amount,istransfère)
        return amount
    
    def transfer(self, other: BankAccount, amount: float)->float:
        self.trasaction_count += 1
        super().transfer(other, amount)
        return amount
    
    def withdrow(self, amount: float,istransfère:bool)->float:
        self.trasaction_count += 1
        if self.balance + ChekingAccount.DRAFT_OVER - amount >= 0:
            self.balance -= amount
            if not istransfère:
                self.operation.append({"date": datetime.now(),"type":"Retrait","amount":-amount})
                dal.insert_operations(datetime.now(),"Retrait",-amount,self.id)
            return amount
        available_amount= self.balance+ChekingAccount.DRAFT_OVER 
        self.balance = -ChekingAccount.DRAFT_OVER
        if not istransfère:
            self.operation.append({"date": datetime.now(),"type":"Retrait","amount":-available_amount})
            dal.insert_operations(datetime.now(),"Retrait",-available_amount,self.id)
        return available_amount

    
    def deductFees(self):
        fees:float=0
        if self.trasaction_count - ChekingAccount.FREE_TRANSACTIONS >= 0:
            fees += (self.trasaction_count - ChekingAccount.FREE_TRANSACTIONS) * ChekingAccount.TRANSACTION_FEE
            self.balance -= fees
        self.trasaction_count=0
        self.operation.append({"date": datetime.now(),"type":"frais de transaction","amount":-fees})
        dal.insert_operations(datetime.now(),"frais de transaction",-fees,self.id)

    
if __name__=="__main__":
    pass