import pytest

from core.models.monitor import get_monitor
from core.models.namespace import get_namespace

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
    assert monitor.metadata == {'test': 'metadata'}

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
