from __future__ import annotations

from datetime import datetime
from ._base import PlankaModel
from ._helpers import dtfromiso
from ..api import schemas

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Generator, Iterator
    from models import *

class BackgroundImage(PlankaModel[schemas.BackgroundImage]):
    """Python interface for Planka Background Images"""

    # BackgroundImage Properties
    @property
    def created_at(self) -> datetime:
        """When the BackgroundImage was created"""
        return dtfromiso(self.schema['createdAt'], self.session.timezone)
    
    @property
    def updated_at(self) -> datetime:
        """When the BackgroundImage was last updated"""
        return dtfromiso(self.schema['updatedAt'], self.session.timezone)
    
    @property
    def project(self) -> Project:
        """The Project the BackgroundImage belongs to"""
        return Project(self.endpoints.getProject(self.schema['projectId'])['item'], self.session)
    
    @property
    def size_in_bytes(self) -> int:
        """The size of the BackgroundImage in bytes"""
        # The Swagger schema says this is a string, but it's should be an int
        return int(self.schema['sizeInBytes'])
    
    @property
    def url(self) -> str:
        """The URL to access the BackgroundImage"""
        return self.schema['url']
    
    @property
    def thumbnails(self) -> dict[str, str]:
        """URLs for different thumbnail sizes of the background image"""
        return self.schema['thumbnailUrls']
    
    # Special Methods
    def download(self) -> Iterator[bytes]:
        """Get bytes for the full image
        
        Returns:
            (Iterator[bytes]): A byte iterator for the full image
        """
        return self.client.get(self.url).iter_bytes()
    
    def download_thumbnails(self) -> Generator[tuple[str, Iterator[bytes]]]:
        """Get byte iterators for all thumbnails
        
        Yields:
            (tuple[str, Iterator[bytes]]): A tuple containing the size key and the thumbnail byte iterator
        """
        for size, url in self.thumbnails.items():
            yield size, self.client.get(url).iter_bytes()
        
    def delete(self):
        """Delete the BackgroundImage"""
        return self.endpoints.deleteBackgroundImage(self.id)
