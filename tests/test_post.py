


import pytest
from app import schemas


def test_get_all_post(authorized_client,test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate,response.json())    
    posts_list = list(post_map)

    assert len(posts_list) == 4
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client,test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401
                      

def test_get_one_post(authorized_client,test_posts):
    post = test_posts[0]
    response = authorized_client.get(f"/posts/{post.id}")
    returned_post = schemas.PostOut(**response.json())
    assert returned_post.Post.id == post.id
    assert returned_post.Post.title == post.title
    assert returned_post.Post.content == post.content
    assert returned_post.Post.owner_id == post.owner_id
    assert response.status_code == 200

def test_unauthorized_user_get_one_post(client,test_posts):
    post = test_posts[0]
    response = client.get(f"/posts/{post.id}")
    assert response.status_code == 401


def test_get_non_exist_post(authorized_client,test_posts):
    response = authorized_client.get(f"/posts/9999")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "title,content,published",
    [
        ("new title 1", "new content 1", True),
        ("new title 2", "new content 2", False),
        ("new title 3", "new content 3", True),
    ]
)
def test_create_post(authorized_client,test_user,title,content,published):
    response = authorized_client.post(
        '/posts/',json={"title":title,"content":content,"published":published}
    )
    created_post = schemas.Post(**response.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_default_published_true(authorized_client,test_user):
    response = authorized_client.post(
        '/posts/',json={"title":"title published default","content":"content published default"}
    )
    created_post = schemas.Post(**response.json())

    assert created_post.title == "title published default"
    assert created_post.content == "content published default"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client):
    response = client.post(
        '/posts/',json={"title":"title","content":"content"}
    )
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client,test_posts):
    post = test_posts[0]
    response = client.delete(f"/posts/{post.id}")
    assert response.status_code == 401

def test_delete_post_success(authorized_client,test_posts):
    post = test_posts[0]
    response = authorized_client.delete(f"/posts/{post.id}")
    assert response.status_code == 204

def test_delete_post_not_exist(authorized_client,test_posts):
    response = authorized_client.delete("/posts/9999")
    assert response.status_code == 404

def test_delete_post_no_permission(authorized_client,test_posts):
    post = test_posts[3] # post owned by another user
    response = authorized_client.delete(f"/posts/{post.id}")
    assert response.status_code == 403


def test_update_post_success(authorized_client,test_posts):
    post = test_posts[0]
    response = authorized_client.put(
        f"/posts/{post.id}",
        json={"title":"updated title","content":"updated content","published":False}
    )
    updated_post = schemas.Post(**response.json())
    assert updated_post.title == "updated title"
    assert updated_post.content == "updated content"
    assert updated_post.published == False
    assert response.status_code == 200

def test_update_post_not_exist(authorized_client,test_posts):
    response = authorized_client.put(
        "/posts/9999",
        json={"title":"updated title","content":"updated content","published":False}
    )
    assert response.status_code == 404

def test_update_post_no_permission(authorized_client,test_posts):
    post = test_posts[3] # post owned by another user
    response = authorized_client.put(
        f"/posts/{post.id}",
        json={"title":"updated title","content":"updated content","published":False}
    )
    assert response.status_code == 403

def test_unauthorized_user_update_post(client,test_posts):
    post = test_posts[0]
    response = client.put(
        f"/posts/{post.id}",
        json={"title":"updated title","content":"updated content","published":False}
    )
    assert response.status_code == 401