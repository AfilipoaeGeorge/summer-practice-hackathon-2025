from fastapi import FastAPI
from auth import router as auth_router
from projects_update import router as projects_update_router
from routers.users import router as users_router
from routers.projects import router as projects_router
from routers.comments import router as comments_router
from routers.tasks import router as tasks_router
from routers.suggestions import router as suggestions_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(projects_router, prefix="/projects", tags=["projects"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(suggestions_router, prefix="/suggestions", tags=["suggestions"])
app.include_router(projects_update_router)


@app.get("/")
async def root():
    return {"message": "API is running"}
