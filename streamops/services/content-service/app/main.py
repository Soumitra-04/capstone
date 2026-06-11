from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Content Catalog Service", version="1.0.0", description="StreamOps Content Catalog Service")
app.include_router(router)
