
from src.user.application.commands.create.types.dto import CreateUserDto
from src.user.application.models.user import UserRole


user_data: list[CreateUserDto] = [
    CreateUserDto(
        username='juanperez',
        email='juanperez@elecstore.com',
        first_name='Juan',
        last_name='Pérez',
        password='abcd1234*',
        user_role=UserRole.CLIENT,
    ),
    CreateUserDto(
        username='manuelgonzalez',
        email='manuelgonzalez@elecstore.com',
        first_name='Manuel',
        last_name='González',
        password='abcd1234*',
        user_role=UserRole.CLIENT,
    ),
    CreateUserDto(
        username='nicolasnunes',
        email='nicolasnunes@elecstore.com',
        first_name='Nicolás',
        last_name='Nunes',
        password='abcd1234*',
        user_role=UserRole.CLIENT,
    ),
    CreateUserDto(
        username='mariagomez',
        email='mariagomez@elecstore.com',
        first_name='María',
        last_name='Goméz',
        password='abcd1234*',
        user_role=UserRole.MANAGER,
    ),
]