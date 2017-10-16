import pytest

import core.models.alert
import core.models.monitor
import core.models.notify
from core.models.exceptions import AlreadyExists
from core.models.persistence import RemoteEntity

class Check(RemoteEntity):
    """A status check that can utilize Checks and Metrics to make
    alerting decisions. 
    
    Args:
        name (str): short name to identify the check
        description (str): a short description of what the check indicates
    """
    def _compatible_with(self, target):
        # Make sure we are only linking one of the following types
        assert isinstance(target, core.models.alert.Alert) or \
               isinstance(target, core.models.monitor.Monitor) or \
               isinstance(target, core.models.notify.Notification)

async def get_check(name):
    ns = Namespace()
    await ns._init(name, )
    return ns

def get_checks():
    pass

# Tests
import asyncio
@pytest.yield_fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop()
    yield loop
    loop.close

@pytest.mark.asyncio
async def test_that_check_returns_its_name():
    check = await get_check('abcdefg')
    assert check.name == 'abcdefg'

@pytest.mark.asyncio
async def test_that_check_rejects_incompatible_types():
    class IncompatibleType():
        pass
    with pytest.raises(AssertionError):
        check = await get_check('test')
        await check._compatible_with(IncompatibleType())

@pytest.mark.asyncio
async def test_that_check_returcheck_id():
    check = await get_check('test')
    print(await check.pm.recall(check))
    assert isichecktance(check.id, int)

@pytest.mark.asyncio
async def test_that_check_metadata_can_be_saved():
    check = await get_check('test')
    test_metadata = {'test': 'metadata'}
    check.metadata = test_metadata
    await check.save()
    await check.recall()
    assert check.metadata == test_metadata

@pytest.mark.asyncio
async def test_that_check_can_be_linked_to_namespace():
    from core.models.namespace import get_namespace
    check = await get_check('test_check')
    ns = await get_namespace('test_namespace')
    await check.link(ns)
    assert ns.id in check.links['Namespace']
