# This file is part of onepageblog.
#
# onepageblog is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# onepageblog is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with onepageblog.  If not, see <http://www.gnu.org/licenses/>.
from contextlib import contextmanager

from posts.models import Post


@contextmanager
def get_post():
    post = Post(title='My Post')
    post.save()
    yield post
    post.delete()


def test_post_list_view_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_new_post_view_200(client):
    response = client.get('/new/')
    assert response.status_code == 200


def test_post_detail_view_200(client):
    with get_post():
        response = client.get('/post/my-post/')
        assert response.status_code == 200


def test_feed_200(client):
    with get_post():
        response = client.get('/feed/rss20.xml')
        assert response.status_code == 200


# TODO: Test user views

# TODO: Test only members of Moderators group can preview unpublished posts

# TODO: Comments notification e-mails

# TODO: Test comment feeds & add comments feeds
