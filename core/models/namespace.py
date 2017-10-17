import core.models.contact
import core.models.escalation
import core.models.history
import core.models.monitor
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
