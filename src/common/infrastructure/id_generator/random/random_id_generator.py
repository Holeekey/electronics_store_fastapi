import random
import string
from src.common.application.id_generator.id_generator import IDGenerator


class RandomIdGenerator(IDGenerator):
    def generate(self) -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
