from fastapi import FastAPI

from users.router import router as router_users
from posts.router import router as posts_users

app = FastAPI(
    debug=True,
    title='Webtronics v.1'
)

app.include_router(
    router_users
)

app.include_router(
    posts_users
)
