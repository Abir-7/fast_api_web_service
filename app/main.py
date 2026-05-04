from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import auth
from app.routers import user
from app.utils.admin_seeder import create_initial_admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await create_initial_admin()
    yield
    # Shutdown logic (if any)

app = FastAPI(lifespan=lifespan)


app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")


app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


