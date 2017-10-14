from functools import wraps

from core.models.mysql import MySQL
from core.models.exceptions import AlreadyExists

class Inventory():
    pass

def _container_pair(container, item, reverse=False):
    """Creates a tuple of container and item types and names"""
    container_type = container.__class__.__name__
    container_name = container.name
    item_type = item.__class__.__name__
    item_name = item.name
    if reverse:
        return (item_type, item_name, container_type, container_name)
    return (container_type, container_name, item_type, item_name)

def _item_triplet(item):
    """Creates a tuple of item type, name and metadata"""
    item_type = item.__class__.__name__
    item_name = item.name
    item_metadata = item.metadata
    return (item_type, item_name, item_metadata)

def persistence(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        kwargs['pm'] = await MySQL()
        try:
            return await func(*args, **kwargs)
        finally:
            kwargs['pm'].destroy()
    return wrapper

@persistence
async def recall(item):
    """Recall item metadata using persistence module"""
    assert hasattr(item, 'name')
    assert hasattr(item, 'metadata')
    # Get persistence module
    pm = kwargs['pm']

@persistence
async def save(item, **kwargs):
    """Save item metadata using persistence module"""
    assert hasattr(item, 'name')
    assert hasattr(item, 'metadata')
    # Get persistence module
    pm = kwargs['pm']
    # Get overwrite argument, default to False
    overwrite = kwargs.get('overwrite', False)
    # Ask the persistence module to save
    await pm.save(_item_triplet(item))

@persistence
async def unlink(container, item):
    """Unlink container and item using persistence module"""
    assert hasattr(container, 'name')
    assert hasattr(item, 'name')
    # Get persistence module
    pm = kwargs['pm']
    # Check compatibility
    container._compatible_with(item)
    item._compatible_with(container)
    # Ask the persistence module to unlink the container from the item
    await pm.unlink(*_container_pair(container, item))

@persistence
async def link(container, item, **kwargs):
    """Link container and item using persistence module"""
    assert hasattr(container, 'name')
    assert hasattr(item, 'name')
    # Get persistence module
    pm = kwargs['pm']
    # Check compatibility
    container._compatible_with(item)
    item._compatible_with(container)
    # Ask the persistence module to link the container with the item
    await pm.link(*_container_pair(container, item))
