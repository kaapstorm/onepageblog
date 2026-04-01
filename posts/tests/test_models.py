import inspect
from datetime import datetime

from django.contrib.auth.models import User
from unmagic import fixture, use

from posts.models import Post


@fixture
def user():
    u = User.objects.create_user(username='testuser', password='pass')
    yield u
    u.delete()


@fixture
def posts_triple():
    u = User.objects.create_user(username='sluguser', password='pass')
    post0 = Post(title='My Post', created_by=u)
    post0.save()
    post1 = Post(title='My Post', created_by=u)
    post1.save()
    post2 = Post(title='My Post', created_by=u)
    post2.save()
    yield post0, post1, post2
    post2.delete()
    post1.delete()
    post0.delete()
    u.delete()


@use(user)
@fixture
def markdown_post():
    post = Post(
        title='My Post',
        created_by=user(),
        content_markdown=inspect.cleandoc("""
        Heading
        =======

        Body text
        """)
    )
    post.save()
    yield post
    post.delete()


@use("db")
@use(markdown_post)
def test_save_creates_markdown():
    assert markdown_post().content == '<h1>Heading</h1>\n<p>Body text</p>'


@use("db")
@use(posts_triple)
def test_save_creates_unique_slug():
    p = posts_triple()
    assert p[0].slug == 'my-post'
    assert p[1].slug == 'my-post-2'
    assert p[2].slug == 'my-post-3'


@use("db")
@use(markdown_post)
def test_published_at():
    ts1 = datetime.now()
    post = markdown_post()
    post.is_published = True
    post.save()
    ts2 = post.published_at
    assert (ts1.day, ts1.hour, ts1.minute) == (ts2.day, ts2.hour, ts2.minute)
