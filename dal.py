import mysql.connector as my
def getconnection():
    cnx=None
    cnx=my.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port='3306',
        database='db_bankaccounts'
    )
    return cnx

def createtable():
    cnx=getconnection()
    db=cnx.cursor()
    db.execute('create table if not exists  BankAccount(id_BA int AUTO_INCREMENT primary key ,BankAccountType varchar(20),Balance float)')
    db.execute('CREATE TABLE IF NOT EXISTS TransfereTraking (id INT AUTO_INCREMENT PRIMARY KEY,TransferDate DATETIME,Type VARCHAR(50),Amount FLOAT,SourceAccountID INT,FOREIGN KEY (SourceAccountID) REFERENCES BankAccount(id_BA))')
    db.execute('CREATE TABLE IF NOT EXISTS T_USER(id int AUTO_INCREMENT primary key,nom varchar(50),email varchar(50) NOT NULL UNIQUE,password varchar(20),accountID int, FOREIGN KEY (accountID) REFERENCES BankAccount(id_BA))')
    cnx.commit()
    
def insert_accounts(accounts):
    cnx = getconnection()
    db = cnx.cursor()
    
    for account in accounts:
        account_type = type(account).__name__
        db.execute('''
            INSERT INTO BankAccount (BankAccountType, Balance)
            VALUES (%s, %s)
        ''', (account_type, account.balance))
        account.id=db.lastrowid
    
    cnx.commit()
    db.close()
    cnx.close()
    print(f"{len(accounts)} comptes ont été chargés dans la base de données.")
   
def insert_account(account):
    cnx = getconnection()
    db = cnx.cursor()
    
    account_type = type(account).__name__
    db.execute('''
            INSERT INTO BankAccount (BankAccountType, Balance)
            VALUES (%s, %s)
        ''', (account_type, account.balance))
    account.id=db.lastrowid
    
    cnx.commit()
    db.close()
    cnx.close()
    return account.id
      
def insert_user(users):
    cnx = getconnection()
    db = cnx.cursor()
    for user in users:
        db.execute('''INSERT INTO T_USER (id,nom,email,password,accountID) VALUES (%s,%s,%s,%s,%s)''',(user.id,user.nom,user.email,user.password,user.accountID))
    
    cnx.commit()
    db.close()
    print("user ajouter avec succes")  
  
def insert_user1(user):
    cnx = getconnection()
    db = cnx.cursor()
    db.execute('''INSERT INTO T_USER (id,nom,email,password,accountID) VALUES (%s,%s,%s,%s,%s)''',(user.id,user.nom,user.email,user.password,user.accountID))
    
    cnx.commit()
    db.close()
    print("user ajouter avec succes") 
    
def insert_operations(date,type:str,amount,accountID):
    """
    Insère une liste d'opérations dans la table TransfèreTraking.
    :param operations: Liste de dictionnaires représentant les opérations
    """
    cnx = getconnection()
    db = cnx.cursor()
    db.execute('''
        INSERT INTO TransfereTraking (TransferDate, Type, Amount, SourceAccountID)
        VALUES (%s, %s, %s, %s)
    ''', (date, type, amount, accountID))
    
    cnx.commit()
    db.close()
    cnx.close()
    print(" opérations ont été chargées dans la base de données.")
    
def fetch_accounts():
    """
    Récupère tous les comptes de la table BankAccount.
    :return: Une liste de dictionnaires représentant les comptes.
    """
    cnx = getconnection()
    db = cnx.cursor(dictionary=True)  # Utiliser dictionary=True pour un résultat en format dict
    db.execute('SELECT * FROM BankAccount')
    accounts = db.fetchall()  # Récupérer tous les comptes
    db.close()
    cnx.close()
    return accounts

def fetch_operations(account_id):
    """
    Récupère toutes les opérations d'un compte donné.
    :param account_id: L'ID du compte.
    :return: Une liste de dictionnaires représentant les opérations.
    """
    cnx = getconnection()
    db = cnx.cursor(dictionary=True)
    db.execute('SELECT * FROM TransfereTraking WHERE SourceAccountID = %s ORDER BY TransferDate DESC', (account_id,))
    operations = db.fetchall()
    db.close()
    cnx.close()
    return operations

def fetch_user_profile(login: str|None, password: str|None):
    cnx = getconnection()
    db = cnx.cursor(dictionary=True)
    query = '''
        select * from t_user 
        left join bankaccount 
        on bankaccount.id_BA = t_user.accountID 
        where email = %s and password = %s;
    '''
    db.execute(query, (login, password))
    user_profile = db.fetchone()  # Récupère une seule ligne
    db.close()
    cnx.close()
    return user_profile

def update_balance(amount:float|None,BA_id:int|None):
    cnx = getconnection()
    db = cnx.cursor(dictionary=True)
    query = ''' update bankaccount set Balance = %s where id_BA = %s '''
    db.execute(query, (amount, BA_id))
    cnx.commit()
    db.close()
    cnx.close()

def fetch_other_bankaccount(BA_id:int|None):
    cnx = getconnection()
    db = cnx.cursor(dictionary=True)
    query = ''' select * from bankaccount where id_BA = %s '''
    db.execute(query,(BA_id,))
    other_bankaccount = db.fetchone()
    db.close()
    cnx.close()
    return other_bankaccount
    
def delete_account(accountID:int):
    cnx = getconnection()
    db=cnx.cursor(dictionary=True)
    try:
        # 1. Supprimer les transactions liées à cet account_id
        delete_operations_query = '''
            DELETE FROM transferetraking
            WHERE SourceAccountID = %s
        '''
        db.execute(delete_operations_query, (accountID,))
        
        # 2. Mettre à NULL l'accountID dans la table T_USER pour les utilisateurs qui avaient ce compte
        update_user_query = '''
            UPDATE t_user
            SET accountID = NULL
            WHERE accountID = %s
        '''
        db.execute(update_user_query, (accountID,))
        
        # 3. Supprimer le compte de la table BankAccount
        delete_account_query = '''
            DELETE FROM bankaccount
            WHERE id_BA = %s
        '''
        db.execute(delete_account_query, (accountID,))
        
        ajuster_auto_increment_query = '''
            ALTER TABLE bankaccount AUTO_INCREMENT = %s;
        '''
        
        db.execute(ajuster_auto_increment_query, (accountID,))
        
        cnx.commit()
        return "Compte supprimé avec succès."
        
        
        
    except Exception as e:
        cnx.rollback()
        return f"Erreur lors de la suppression du compte : {str(e)}"
    
    finally:
        db.close()
        cnx.close()

if __name__=='__main__':
    #getconnection()
    #createtable()
    #print(fetch_user_profile("hmizourais557@gmail.com","hamzay989"))
    #print(fetch_other_bankaccount(2))
    #print(fetch_operations(1))
    delete_account(5)
#select * from bankaccount inner join t_user on t_user.accountID = bankaccount.id where email like "hizourais557@gmial.com" and password like "hamzay989"; 
    