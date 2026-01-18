from __future__ import annotations
from typing import Unpack

from httpx import Client
from .api import (
    PlankaEndpoints, 
    typ, # Response / Request typing
)
from . import models

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
class Action(models.Action): ...


class Attachment(models.Attachment): ...


class BackgroundImage(models.BackgroundImage): ...


class BaseCustomFieldGroup(models.BaseCustomFieldGroup): ...


class Board(models.Board): ...


class BoardMembership(models.BoardMembership): ...


class Card(models.Card): ...


class CardLabel(models.CardLabel): ...


class CardMembership(models.CardMembership): ...


class Comment(models.Comment): ...


class Config(models.Config): ...


class CustomField(models.CustomField): ...


class CustomFieldGroup(models.CustomFieldGroup): ... 


class CustomFieldValue(models.CustomFieldValue): ... 


class Label(models.Label): ... 


class List(models.List): ... 


class Notification(models.Notification): ... 


class NotificationService(models.NotificationService): ... 


class Project(models.Project): ...


class ProjectManager(models.ProjectManager): ...


class Task(models.Task): ... 


class TaskList(models.TaskList): ... 


class User(models.User): ...


class Webhook(models.Webhook): ...

