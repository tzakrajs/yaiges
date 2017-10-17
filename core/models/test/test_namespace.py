import asyncio
import pytest

from core.models.namespace import get_namespace

# Tests
@pytest.yield_fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

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
    #await ns.link(monitor)
    #assert monitor.id in ns.links['Monitor']
