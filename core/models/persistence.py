import json
from functools import wraps

from core.models.mysql import get_mysql
from core.models.exceptions import AlreadyExists

class RemoteEntity():
    metadata = {}
    """A simple unit for persisting state remotely"""

    async def _init(self, **kwargs):
        assert isinstance(kwargs['name'], str)
        self.pm = await get_mysql()
        self.name = kwargs['name']
        self.metadata.update(kwargs)
        await self.recall()

    def class_name(self):
        return self.__class__.__name__

    async def recall(self):
        """Retrieve this entity's metadata"""
        await self.pm.recall(self)

    async def save(self, **kwargs):
        """Persist this entity's name and metadata"""
        # Get overwrite argument, default to False
        overwrite = kwargs.get('overwrite', False)
        # Save the change to the persistence module
        await self.pm.save(self, overwrite=overwrite)

    async def link(self, target_object):
        """Links a target object to this entity"""
        # Check compatibility with target object
        self._compatible_with(target_object)
        target_object._compatible_with(self)
        # Link the target object to this namespace
        await self.pm.link(self, target_object)

    async def unlink(self, target_object):
        """Unlinks a target object from this entity"""
        await self.pm.unlink(self, target_object)
