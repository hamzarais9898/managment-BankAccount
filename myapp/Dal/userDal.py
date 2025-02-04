
import mysql.connector as my
from myapp.Models.userModel import User 
from decimal import Decimal
from myapp.Dal.cnxDal import Database 

class UserDao:
    def __init__(self)->None:
        self.cnx = Database.get_connection()
        
    def getUsers(self)->list[User]:
        users:list[User]=[]
        query = "SELECT * FROM users;"
        if self.cnx != None :
            cursor=self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query)
            rows=cursor.fetchall()
            for row in rows : # type: ignore
                users.append(User(username=row['username'],email=row['email'],password=row['password'],isadmin=row['isadmin'])) # type: ignore
        return users
    
    def auth(self,login:str,password:str)->User|None:
        query = "SELECT * FROM users WHERE email = %s AND password = %s;"
        if self.cnx != None :
            cursor=self.cnx.cursor(dictionary=True) # type: ignore
            cursor.execute(query,(login,password))
            row=cursor.fetchone()
            if row != None:
                return User(username=row['username'],email=row['email'],password=row['password'],isadmin=row['isadmin']) # type: ignore
            return None

