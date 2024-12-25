import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from common.infrastructure.bus.bus import setup_bindings, command_bus
from command_bindings import command_bus_bindings
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
from common.infrastructure.rabbitmq.rabbitmq_event_handler import rabbit_event_listener
from common.infrastructure.cryptography.fernet_cryptography_provider import get_fernet_provider
import config
from common.infrastructure.database.database import SessionLocal
from event_bindings import event_bindings
from routes import router
from user.infrastructure.models.postgres.sqlalchemy.user_model import (
    UserModel,
    UserRole,
    UserStatus,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_bindings(command_bus, command_bus_bindings)
    rabbit_event_listener.setup_bindings(event_bindings)
    rabbit_event_listener.start_consuming_in_thread()
    db = SessionLocal()
    admin_count = db.query(UserModel).filter(UserModel.role == UserRole.ADMIN).count()
    if admin_count == 0:
        user = UserModel(
            id=UUIDGenerator().generate(),
            username=config.ADMIN_USERNAME,
            email=config.ADMIN_PASSWORD,
            password= get_fernet_provider().encrypt(config.ADMIN_PASSWORD),
            role=UserRole.ADMIN.name,
            status=UserStatus.ACTIVE.name,
            first_name="admin",
            last_name="admin",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    try:
        yield
    finally:
        rabbit_event_listener.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router=router, prefix=config.API_PREFIX)

if __name__ == "__main__":

    reload = config.STAGE == "dev"

    uvicorn.run("main:app", host="0.0.0.0", port=config.APP_PORT, reload=reload)
