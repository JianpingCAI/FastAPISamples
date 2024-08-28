from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.api import (
    user_api,
    blog_api,
    post_api,
    comment_api,
    category_api,
    tag_api,
    auth_api,
)

# Initialize FastAPI app
app = FastAPI(
    title="Online Blog Platform API",
    description="This is the API backend for the online blog platform.",
    version="1.0.0",
)

# Set up CORS
origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(user_api.router, prefix="/users", tags=["Users"])
app.include_router(blog_api.router, prefix="/blogs", tags=["Blogs"])
app.include_router(post_api.router, prefix="/posts", tags=["Posts"])
app.include_router(comment_api.router, prefix="/comments", tags=["Comments"])
app.include_router(category_api.router, prefix="/categories", tags=["Categories"])
app.include_router(tag_api.router, prefix="/tags", tags=["Tags"])
app.include_router(auth_api.router, tags=["Authentication"])


# Root path
@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Blog Platform API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
