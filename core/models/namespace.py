import pytest

from core.models.alert import Alert
from core.models.contact import ContactGroup
from core.models.escalation import EscalationPolicy
from core.models.exceptions import AlreadyExists
from core.models.history import NotificationHistory
from core.models.monitor import Monitor
from core.models.persistence import recall, save, link, unlink, RemoteEntity

class Inventory(RemoteEntity):
    """Container of containers"""
    
    def _compatible_with(self, target_object):
        # Make sure we are only linking one of the following types
        assert isinstance(target_object, Namespace)

class Namespace(RemoteEntity):
    """An isolated collection of monitors, policies, contact groups
    and history.
    
    Args:
        name (str): short name to identify the namespace
    """
    async def _init(self, name):
        assert isinstance(name, str)
        self.name = name

    def _compatible_with(self, target_object):
        # Make sure we are only linking one of the following types
        assert isinstance(target_object, Monitor) or \
               isinstance(target_object, EscalationPolicy) or \
               isinstance(target_object, ContactGroup) or \
               isinstance(target_object, NotificationHistory)

async def get_namespace(name):
    ns = Namespace()
    await ns._init(name)
    return ns

def get_namespaces():
    
    pass

# Tests
@pytest.mark.asyncio
async def test_that_namespace_returns_its_name():
    ns = await get_namespace('abcdefg')
    assert ns.name == 'abcdefg'

@pytest.mark.asyncio
async def test_that_namespace_rejects_incompatible_types():
    with pytest.raises(AssertionError):
        ns = await get_namespace('test')
        await ns._compatible_with(Alert())
