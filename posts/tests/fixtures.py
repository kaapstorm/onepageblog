from django.contrib.auth.models import User
from django.test import Client
from unmagic import fixture, use

from posts.models import Post


@fixture
def user():
    u = User.objects.create_user(username='testuser', password='pass')
    yield u
    u.delete()


@fixture
def client():
    yield Client()


@use(user)
@fixture
def post():
    p = Post(title='My Post', created_by=user(), is_published=True)
    p.save()
    yield p
    p.delete()
