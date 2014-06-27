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

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, password_change

from posts.feeds import PostsFeed
from posts.views import PostListView, PostDetailView, add_post, profile, edit_profile, register, logout
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = patterns(
    '',
    # Post URLs
    url(r'^$', PostListView.as_view(),
        name='post_list_view'),
    url(r'^post/(?P<slug>[\w\-_]+)/$', PostDetailView.as_view(),
        name='post_detail_view'),
    url(r'^post/(?P<slug>[\w\-_]+)/ajax/$',
        PostDetailView.as_view(template_name='posts/post_detail_ajax.html'),
        name='post_detail_ajax_view'),
    url(r'^new/$', add_post,
        name='add_post_view'),

    # Feed URL
    url(r'^feed/rss20.xml$', PostsFeed(),
        name='feed'),

    # Redirect "/blog/" to "/"
    url(r'^blog/$', RedirectView.as_view(url='/')),
    # Redirect old-style "/blog/post/n/<slug>/" to "/post/<slug>/"
    url(r'^blog/post/\d+/(?P<slug>[\w\-_]+)/$', RedirectView.as_view(url='/post/%(slug)s/')),

    # Account URLs
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/register/$', register),
    (r'^accounts/profile/$', profile),
    url(r'^accounts/edit/$', edit_profile,
        name='edit_profile_view'),
    url(r'^accounts/passwd/$', password_change,
        name='password_change_view',
        kwargs={'post_change_redirect': '../../'}),

    # Admin URL
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    # Serve media when developing
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
