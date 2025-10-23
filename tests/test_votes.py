 
import pytest
from app import models

@pytest.fixture
def test_vote(test_posts,session):
    post = test_posts[0]
    new_vote = models.Vote(post_id=post.id,user_id=1)
    session.add(new_vote)
    session.commit()



def test_vote_on_post_success(authorized_client,test_posts):
    post = test_posts[0]
    response = authorized_client.post(
        "/vote/",
        json={"post_id":post.id,"dir":1}
    )
    assert response.status_code == 201

def test_vote_on_post_twice(authorized_client,test_posts,test_vote):
    post = test_posts[0]
    response = authorized_client.post(
        "/vote/",
        json={"post_id":post.id,"dir":1}
    )
    assert response.status_code == 409

def test_remove_vote_success(authorized_client,test_posts,test_vote):
    post = test_posts[0]
    response = authorized_client.post(
        "/vote/",
        json={"post_id":post.id,"dir":0}
    )
    assert response.status_code == 201

def test_remove_vote_not_exist(authorized_client,test_posts):
    post = test_posts[0]
    response = authorized_client.post(
        "/vote/",
        json={"post_id":post.id,"dir":0}
    )
    assert response.status_code == 409

def test_vote_on_post_not_exist(authorized_client,test_posts):
    response = authorized_client.post(
        "/vote/",
        json={"post_id":9999,"dir":1}
    )
    assert response.status_code == 404

def test_unauthorized_user_vote(client,test_posts):
    post = test_posts[0]
    response = client.post(
        "/vote/",
        json={"post_id":post.id,"dir":1}
    )
    assert response.status_code == 401
