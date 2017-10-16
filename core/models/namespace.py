import pytest

import core.models.contact
import core.models.escalation
import core.models.history
import core.models.monitor
from core.models.exceptions import AlreadyExists
from core.models.persistence import RemoteEntity

class Namespace(RemoteEntity):
    """An isolated collection of monitors, policies, contact groups
    and history.
    
    Args:
        name (str): short name to identify the namespace
    """
    def _compatible_with(self, target):
        # Make sure we are only linking one of the following types
        assert isinstance(target, core.models.monitor.Monitor) or \
               isinstance(target, core.models.escalation.EscalationPolicy) or \
               isinstance(target, core.models.contact.ContactGroup) or \
               isinstance(target, core.models.history.NotificationHistory)

async def get_namespace(name):
    ns = Namespace()
    await ns._init(name=name)
    return ns

def get_namespaces():
    pass

# Tests
import asyncio
@pytest.yield_fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop()
    yield loop
    loop.close

@pytest.mark.asyncio
async def test_that_namespace_returns_its_name():
    ns = await get_namespace('abcdefg')
    assert ns.name == 'abcdefg'

@pytest.mark.asyncio
async def test_that_namespace_rejects_incompatible_types():
    class IncompatibleType():
        pass
    with pytest.raises(AssertionError):
        ns = await get_namespace('test')
        await ns._compatible_with(IncompatibleType())

@pytest.mark.asyncio
async def test_that_namespace_metadata_can_be_saved_and_retrieved():
    ns = await get_namespace('test')
    test_metadata = {'test': 'metadata'}
    ns.metadata = test_metadata
    await ns.save()
    ns = await get_namespace('test')
    assert ns.metadata == test_metadata

@pytest.mark.asyncio
async def test_that_namespace_returns_id():
    ns = await get_namespace('test')
    assert isinstance(ns.id, int)

@pytest.mark.asyncio
async def test_that_namespace_can_be_linked_to_monitor():
    from core.models.monitor import get_monitor
    ns = await get_namespace('test_namespace')
    await ns.save()
    monitor = await get_monitor('test_monitor')
    await monitor.save()
    await ns.link(monitor)
    assert monitor.id in ns.links['Monitor']
