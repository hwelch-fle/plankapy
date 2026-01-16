from .api import PlankaEndpoints
from httpx import Client
from .models import *

class Planka:
    def __init__(self, client: Client, lang: str='en_US') -> None:
        self.client = client
        self.endpoints = PlankaEndpoints(client)
        self.lang = lang
        
    def logon(self, username: str, password: str, 
              *, token: str='', 
              accept_terms: bool=False
        ):
        """Authenticate with the planka instance"""
        if not token:
            token = self.endpoints.createAccessToken(
                emailOrUsername=username, 
                password=password,
                withHttpOnlyToken=True,
            )['item']
        if accept_terms:
            raise NotImplementedError('Term accepting workflow is not implemented yet')
            self.endpoints.getTerms(type='general', language=self.lang)
            self.endpoints.acceptTerms(pendingToken=token, signature=None)
        self.client.headers['Authorization'] = f'Bearer {token}'
    
    def logout(self) -> None:
        self.endpoints.deleteAccessToken()
    
    @property
    def projects(self) -> list[Project]:
        """Get all Projects available to the current user"""
        return [Project(p, self.endpoints) for p in self.endpoints.getProjects()['items']]

    @property
    def users(self) -> list[User]:
        """Get all Users on the current instance"""
        return [User(u, self.endpoints) for u in self.endpoints.getUsers()['items']]
    
    @property
    def me(self) -> User:
        """The current logged on user"""
        return User(self.client.get('/api/me').json()['item'], self.endpoints)