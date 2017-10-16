import pytest

import core.models.alert
import core.models.check
import core.models.contact
import core.models.namespace
import core.models.escalation
from core.models.exceptions import AlreadyExists
from core.models.persistence import RemoteEntity

class Monitor(RemoteEntity):
    """A status monitor that can utilize Checks and Metrics to make
    alerting decisions. 
    
    Args:
        name (str): short name to identify the monitor
        description (str): a short description of what the monitor indicates
    """
    def _compatible_with(self, target):
        # Make sure we are only linking one of the following types
        assert isinstance(target, core.models.alert.Alert) or \
               isinstance(target, core.models.check.Check) or \
               isinstance(target, core.models.contact.ContactGroup) or \
               isinstance(target, core.models.namespace.Namespace) or \
               isinstance(target, core.models.escalation.EscalationPolicy)

async def get_monitor(name):
    monitor = Monitor()
    await monitor._init(name=name)
    return monitor

def get_monitors():
    pass

# Tests
import asyncio
@pytest.yield_fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_that_monitor_returns_its_name():
    monitor = await get_monitor('abcdefg')
    assert monitor.name == 'abcdefg'

@pytest.mark.asyncio
async def test_that_monitor_rejects_incompatible_types():
    class IncompatibleType():
        pass
    with pytest.raises(AssertionError):
        monitor = await get_monitor('test')
        await monitor._compatible_with(IncompatibleType())

@pytest.mark.asyncio
async def test_that_monitor_metadata_can_be_saved():
    monitor = await get_monitor('test')
    test_metadata = {'test': 'metadata'}
    monitor.metadata = test_metadata
    await monitor.save()

@pytest.mark.asyncio
async def test_that_monitor_returns_metadata():
    monitor = await get_monitor('test')
    assert monitor.metadata == {'name': 'test',
                                'test': 'metadata'}

@pytest.mark.asyncio
async def test_that_monitor_returns_id():
    monitor = await get_monitor('test')
    assert isinstance(monitor.id, int)

@pytest.mark.asyncio
async def test_that_monitor_can_be_linked_to_namespace():
    from core.models.namespace import get_namespace
    monitor = await get_monitor('test_monitor')
    ns = await get_namespace('test_namespace')
    await monitor.link(ns)
    assert ns.id in monitor.links['Namespace']
