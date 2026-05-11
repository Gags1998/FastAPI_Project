from fastapi import FastAPI, Request, HTTPException, status
# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from schema import BaseModel, PostBase, PostCreate, PostResponse


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "deepak",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "mahanth",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2026",
    },
    {
        "id": 3,
        "author": "venky",
        "title": "FastAPI is Amazing",
        "content": "This framework is really easy, fast and furious 1-10.",
        "date_posted": "April 20, 2026",
    },
]

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html",{"posts": posts})


@app.get("/posts/{post_id}",include_in_schema=False)
def post_page(request: Request, post_id: int):
    post = next((post for post in posts if post["id"] == post_id), None)
    title = post["title"][:50]
    if post:
        return templates.TemplateResponse(request, "post.html", {"post": post})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



@app.get("/posts",response_model=list[PostResponse])
def get_posts():    
    return {"data": posts}


@app.post("/posts",response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate):
    new_post = {
        "id": len(posts) + 1,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "date_posted": "April 22, 2026",
    }
    posts.append(new_post)
    return {"data": new_post}




@app.get("/posts/{post_id}",response_model=PostResponse)
def get_post(post_id: int):
    post = next((post for post in posts if post["id"] == post_id), None)
    if post:
        return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/static") or request.url.path.startswith("/static/posts"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/static") or request.url.path.startswith("/static/posts"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )