from __future__ import annotations

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas, paths

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Unpack
    from models import *
    from ._literals import WebhookEvent

__all__ = ('Webhook', )

class Webhook(PlankaModel[schemas.Webhook]):
    """Python interface for Planka Webhooks"""
    
    @property
    def name(self) -> str:
        """Name/title of the Webhook"""
        return self.schema['name']
    
    @property
    def url(self) -> str:
        """URL endpoint for the Webhook"""
        return self.schema['url']
    
    @property
    def access_token(self) -> str:
        """Access token for webhook authentication"""
        return self.schema['accessToken']
    
    @property
    def events(self) -> list[WebhookEvent]:
        """List of events that trigger the Webhook"""
        return self.schema['events']
    
    @property
    def excluded_events(self) -> list[WebhookEvent]:
        """List of events excluded from the Webhook"""
        return self.schema['excludedEvents']
    
    @property
    def created_at(self) -> datetime:
        """When the Webhook was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
        
    @property
    def updated_at(self) -> datetime:
        """When the Webhook was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
    # Special Methods
    def sync(self):
        """Sync the Webhook with the Planka server (admin only)"""
        if self.current_role == 'admin':
            self.schema = [
                Webhook(w, self.session) 
                for w in self.endpoints.getWebhooks()['items'] 
                if w['id'] == self.id
            ].pop().schema
        
    def update(self, **kwargs: Unpack[paths.Request_updateWebhook]):
        """Update the Webhook (admin only)"""
        if self.current_role == 'admin':
            self.schema = self.endpoints.updateWebhook(self.id, **kwargs)['item']
    
    def delete(self):
        """Delete the Webhook (admin only)"""
        if self.current_role == 'admin':
            self.endpoints.deleteWebhook(self.id)
  