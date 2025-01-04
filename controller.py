from flask import (Flask,
                   request,
                   jsonify,
                   render_template,
                   abort,
                   session,
                   redirect,
                   url_for
                   )
import secrets
from dal import *
from models import *
from User_module import User
app = Flask(__name__)
app.secret_key=secrets.token_hex(32)

@app.route('/')
def inscription():
    return render_template('loging.html')

@app.route('/login', methods=['POST'])
def authen():
    login = request.form.get('login')
    password = request.form.get('password')
    
    user_profile = fetch_user_profile(login, password)
    if user_profile:
        # Stocke les informations utilisateur dans la session
        session['user'] = user_profile
        if user_profile.get('accountID'): # type: ignore
            return redirect(url_for('home'))
        else:
            return render_template('create_account.html')
    else:
        return render_template('loging.html', error='Login or password incorrect')

@app.route('/create_account', methods=['POST'])
def create_Bankaccount():
    account_type = request.form.get('account_type')
    balance = float(request.form.get('initial_balance'))# type: ignore
    user_profile = session.get('user')
    
    bankaccount:BankAccount = None # type: ignore
    
    if account_type == "SavingAccount":
        bankaccount:BankAccount = SavingAccount(0.02,balance)
    elif account_type == "ChekingAccount":
        bankaccount:BankAccount = ChekingAccount(balance)
    
    if bankaccount is None:
        # Gérer le cas où account_type n'est pas valide
        return "Type de compte invalide", 400
    
    insert_accounts([bankaccount])
    
    account_id = bankaccount.id
    
    
    user_id = user_profile['id']# type: ignore
    
    
    
    cnx = getconnection()
    db = cnx.cursor()
    update_query = '''
        UPDATE T_USER
        SET accountID = %s
        WHERE id = %s
    '''
    db.execute(update_query, (account_id, user_id))
    cnx.commit()
    db.close()
    cnx.close()
    user_profile['accountID'] = account_id# type: ignore
    user_profile['id_BA'] = account_id# type: ignore
    user_profile['Balance']= balance# type: ignore
    user_profile['BankAccountType']=account_type # type: ignore
    session['user'] = user_profile

    return redirect(url_for('home'))


@app.route('/register', methods=['POST'])
def register1():
    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')

    # Vérifier si un utilisateur avec cet email existe déjà
    existing_user = fetch_user_profile(email, password=None)  # Utiliser `auth` pour chercher par email uniquement
    if existing_user:
        return render_template('register.html', error="Email already in use.")

    # Créer le nouvel utilisateur
    user = User(email=email, password=password, nom=username)
    insert_user1(user)  # Insérer dans la base de données

    return redirect(url_for('inscription'))

    

@app.route('/profile')
def profile():
    user = session.get('user')  # Récupère les informations utilisateur depuis la session
    if not user:
        return redirect(url_for('authen'))  # Redirige vers la page de login si non connecté
    
    return render_template('profile.html', user=user)
#return jsonify(user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inscription'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/deposit')
def deposit():
    return render_template('deposit.html')

@app.route('/deposit',methods = ['POST'])
def deposit1():
    account_ID = request.form.get('account_id')
    amount = float(request.form.get('amount'))# type: ignore
    user_profile = session.get('user')
    
    BA:BankAccount = None # type: ignore
    if user_profile['BankAccountType'] == 'ChekingAccount':# type: ignore
        BA:BankAccount = ChekingAccount(user_profile['Balance'])# type: ignore
    elif user_profile['BankAccountType'] == 'SavingAccount':# type: ignore
        BA:BankAccount = SavingAccount(0.05,user_profile['Balance'])# type: ignore
    
    BA.id = user_profile['id_BA']# type: ignore
    BA.deposit(amount,False)
    user_profile['Balance']=BA.balance # type: ignore
    update_balance( BA.balance,account_ID)# type: ignore
    
    session['user']=user_profile
    return redirect(url_for('home'))

@app.route('/withdrow')
def withdrow():
    return render_template('withdrow.html')

@app.route('/withdrow',methods = ['POST'])
def withdrow1():
    account_ID = request.form.get('account_id')
    amount = float(request.form.get('amount'))# type: ignore
    user_profile = session.get('user')
    
    
    BA:BankAccount = None # type: ignore
    if user_profile['BankAccountType'] == 'ChekingAccount':# type: ignore
        BA:BankAccount = ChekingAccount(user_profile['Balance'])# type: ignore
    elif user_profile['BankAccountType'] == 'SavingAccount':# type: ignore
        BA:BankAccount = SavingAccount(0.05,user_profile['Balance'])# type: ignore
    
    BA.id = user_profile['id_BA']# type: ignore
    BA.withdrow(amount,False)
    user_profile['Balance']=BA.balance # type: ignore
    update_balance( BA.balance,account_ID)# type: ignore
    
    session['user']=user_profile
    return redirect(url_for('home'))


@app.route('/transfer')
def transfere():
    return render_template('transfere.html')

@app.route('/transfer',methods = ['POST'])
def transfere1():
    sourceID = request.form.get('from_account_id') 
    destID = request.form.get('to_account_id')
    amount = float(request.form.get('amount'))#type: ignore
    user_profile = session.get('user')
    
    BA:BankAccount = None # type: ignore
    if user_profile['BankAccountType'] == 'ChekingAccount':# type: ignore
        BA:BankAccount = ChekingAccount(user_profile['Balance'])# type: ignore
    elif user_profile['BankAccountType'] == 'SavingAccount':# type: ignore
        BA:BankAccount = SavingAccount(0.05,user_profile['Balance'])# type: ignore
    
    BA.id = user_profile['id_BA']# type: ignore
    
    other_BA = fetch_other_bankaccount(destID)#type: ignore
    OBA:BankAccount = None # type: ignore
    if other_BA['BankAccountType'] == 'ChekingAccount':# type: ignore
        OBA = ChekingAccount(other_BA['Balance'])# type: ignore
    elif other_BA['BankAccountType'] == 'SavingAccount':# type: ignore
        OBA = SavingAccount(0.05,other_BA['Balance'])# type: ignore
    
    OBA.id = other_BA['id_BA']# type: ignore
    BA.transfer(OBA,amount)# type: ignore
    user_profile['Balance']=BA.balance# type: ignore
    update_balance( BA.balance,sourceID )# type: ignore
    update_balance( OBA.balance,OBA.id )# type: ignore
    
    session['user']=user_profile
    return redirect(url_for('home'))
    
@app.route('/home')
def home():
    user = session.get('user')  # Ensure session contains user data
    if not user:
        return redirect(url_for('authen'))  # Redirect to login if user not in session
    
    # Fetch transactions for the logged-in user
    transactions = fetch_operations(user['accountID']) if user.get('accountID') else []
    return render_template('home.html', transactions=transactions)

from flask import session, redirect, url_for

@app.route('/supprimer')
def supprimer():
    user_profile = session.get('user') 
    delete_account(user_profile['accountID'])  #type: ignore
    return redirect(url_for('inscription'))  # Redirection vers la page d'inscription ou une autre page appropriée


    
if __name__=="__main__":
    app.run(debug=True)