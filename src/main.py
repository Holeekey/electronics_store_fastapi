from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from common.infrastructure.id_generator.uuid.uuid_generator import UUIDGenerator
import config
from common.infrastructure.database.database import SessionLocal
from routes import router
from user.infrastructure.models.postgres.sqlalchemy.user_model import UserModel, UserRole, UserStatus

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    user_count = db.query(UserModel).count()
    if(user_count == 0):
        user = UserModel(
            id=UUIDGenerator().generate(),
            username="admin",
            email="admin@gmail.com",
            password="admin",
            role=UserRole.ADMIN.name,
            status=UserStatus.ACTIVE.name,
            first_name="admin",
            last_name="admin"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=router, prefix=config.API_PREFIX)

if __name__ == "__main__":

    reload = config.STAGE == "dev"

    uvicorn.run("main:app", host="0.0.0.0", port=config.APP_PORT, reload=reload)
