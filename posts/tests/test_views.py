from unmagic import use

from posts.tests.fixtures import client, moderator_client, post, unpublished_post


@use("db")
@use(client)
def test_post_list_view_200():
    response = client().get('/')
    assert response.status_code == 200


@use("db")
@use(client)
def test_new_post_view_redirects_anonymous():
    response = client().get('/new/')
    assert response.status_code == 302


@use("db")
@use(client, post)
def test_post_detail_view_200():
    response = client().get('/post/my-post/')
    assert response.status_code == 200


@use("db")
@use(client, post)
def test_feed_200():
    response = client().get('/feed/rss20.xml')
    assert response.status_code == 200


@use("db")
@use(client, unpublished_post)
def test_unpublished_post_not_visible_to_anonymous():
    response = client().get('/post/draft-post/')
    assert response.status_code == 404


@use("db")
@use(moderator_client, unpublished_post)
def test_unpublished_post_visible_to_moderator():
    response = moderator_client().get('/post/draft-post/')
    assert response.status_code == 200


@use("db")
@use(moderator_client, unpublished_post)
def test_post_list_shows_unpublished_to_moderator():
    response = moderator_client().get('/')
    assert b'Draft Post' in response.content


@use("db")
@use(client, unpublished_post)
def test_post_list_hides_unpublished_from_anonymous():
    response = client().get('/')
    assert b'Draft Post' not in response.content
