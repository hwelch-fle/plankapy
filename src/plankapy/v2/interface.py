from .api import PlankaEndpoints
from httpx import Client

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
        