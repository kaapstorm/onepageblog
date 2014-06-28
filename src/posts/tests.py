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

from django.test import TestCase


class TestPostModel(TestCase):
    def test_save_creates_markdown(self):
        # TODO: ...
        pass

    def test_save_creates_unique_slug(self):
        # TODO: ...
        pass

    def test_save_sets_published_at(self):
        # TODO: ...
        pass


class TestViews(TestCase):
    def test_post_list_view(self):
        # TODO: ...
        pass

    def test_post_detail_view(self):
        # TODO: ...
        pass

    def test_feed(self):
        # TODO: ...
        pass

# TODO: Test user views

# TODO: Test feed

# TODO: Test only members of  Moderators group can preview unpublished posts

# TODO: Comments notification e-mails

# TODO: Test comment feeds & add comments feeds
