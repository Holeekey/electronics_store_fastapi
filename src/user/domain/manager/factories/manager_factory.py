from uuid import UUID
from src.user.domain.manager.manager import Manager
from src.user.domain.manager.value_objects.manager_id import ManagerId
from src.user.domain.manager.value_objects.manager_name import ManagerName
from src.user.domain.manager.value_objects.manager_email import ManagerEmail


def manager_factory(id: str, first_name: str, last_name: str, email: str):

    manager_id = ManagerId(UUID(id))
    manager_name = ManagerName(first_name, last_name)
    manager_email = ManagerEmail(email)

    return Manager(manager_id, manager_name, manager_email)
