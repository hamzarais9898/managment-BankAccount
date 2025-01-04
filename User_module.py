from typing import Optional
class User():
    
    def __init__(self, email: str|None, password: str|None, nom: str|None, accountID: Optional[int] = None) -> None:
        self.id = None
        self.nom = nom
        self.email = email
        self.password = password
        self.accountID = accountID  # Peut être None si aucun compte n'est associé
        