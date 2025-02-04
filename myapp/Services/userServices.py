from myapp.Dal.userDal import UserDao
from myapp.Models.userModel import User


class UserManage:
    def __init__(self)->None:
        self.userDao=UserDao()
        
    def listUsers(self)->list[User]:
        return self.userDao.getUsers()
    
    def auth(self,login:str,password:str)->User|None:
        return self.userDao.auth(login,password)    

