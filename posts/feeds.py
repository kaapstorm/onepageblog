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

from django.contrib.syndication.views import Feed
from posts.models import Post


class PostsFeed(Feed):
    title = "Posts"
    link = "/"

    @staticmethod
    def items():
        return Post.objects.filter(is_published=True).order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        if item.summary:
            # Should we return only the summary? For now, return everything.
            return '<blockquote>' + item.summary + '</blockquote>' + item.content
        return item.content

    def item_link(self, item):
        return item.get_absolute_url()
