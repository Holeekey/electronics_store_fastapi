import uuid
from common.application.id_generator.id_generator import IDGenerator


class UUIDGenerator(IDGenerator):
    def generate(self) -> str:
        return str(uuid.uuid4())


uuid_generator = UUIDGenerator()


def get_uuid_generator() -> UUIDGenerator:
    return uuid_generator
