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

from django.contrib import admin
from onepageblog.posts.models import Post


class PostAdmin(admin.ModelAdmin):
    # List parameters
    list_display = ('title', 'created_by', 'is_published', 'published_at')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'created_by')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'content_markdown')

    # Detail parameters
    fields = ('title', 'slug', 'content_markdown', 'created_by', 'created_at', 'is_published', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'created_by', 'published_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()


admin.site.register(Post, PostAdmin)
