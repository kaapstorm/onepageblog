from django.contrib.auth.models import Group, User
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


@fixture
def moderator_client():
    mod_user = User.objects.create_user(username='mod', password='pass')
    group, _ = Group.objects.get_or_create(name='Moderators')
    mod_user.groups.add(group)
    c = Client()
    c.login(username='mod', password='pass')
    yield c
    mod_user.delete()


@fixture
def unpublished_post():
    u = User.objects.create_user(username='draftauthor', password='pass')
    p = Post(title='Draft Post', is_published=False, created_by=u)
    p.save()
    yield p
    p.delete()
    u.delete()
