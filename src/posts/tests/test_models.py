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
import inspect
from datetime import datetime

import pytest

from posts.models import Post


pytestmark = pytest.mark.django_db


@pytest.fixture
def posts():
    post0 = Post(title='My Post')
    post0.save()
    post1 = Post(title='My Post')
    post1.save()
    post2 = Post(title='My Post')
    post2.save()
    yield post0, post1, post2
    post2.delete()
    post1.delete()
    post0.delete()

@pytest.fixture
def markdown_post():
    post = Post(
        title='My Post',
        content_markdown=inspect.cleandoc("""
        Heading
        =======

        Body text
        """)
    )
    post.save()
    yield post
    post.delete()


def test_save_creates_markdown(markdown_post):
    assert markdown_post.content == """<h1>Heading</h1><p>Body text</p>"""


def test_save_creates_unique_slug(posts):
    assert posts[0].slug == 'my-post'
    assert posts[1].slug == 'my-post-1'
    assert posts[2].slug == 'my-post-2'


def test_published_at(markdown_post):
    ts1 = datetime.now()
    markdown_post.is_published = True
    markdown_post.save()
    ts2 = markdown_post.published_at
    assert (ts1.day, ts1.hour, ts1.minute) == (ts2.day, ts2.hour, ts2.minute)
