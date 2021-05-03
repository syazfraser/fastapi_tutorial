from fastapi import FastAPI
from typing import Optional

from pydantic import BaseModel

app = FastAPI()


@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[bool] = None):
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} unpublished blogs from the db'}


@app.get('/blog/{id}')
def show(id: int):
    # Fetch blog with id = id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int, limit=10):
    # Fetch comments of blog with id = id
    return {'data': {id: {'comments': {'1', '2'}}}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
    return {
        'data': {
            'title': blog.title,
            'body': blog.body,
            'published': blog.published
        }
    }
