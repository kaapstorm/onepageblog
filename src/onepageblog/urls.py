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
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import (
    urls as auth_urls,
    views as auth_views,
)
from django.urls import path, re_path, reverse_lazy
from django.views.generic import RedirectView
from django.views.static import serve

from posts.feeds import PostsFeed
from posts.views import (
    PostListView,
    PostDetailView,
    add_post,
    profile,
    edit_profile,
    register,
    logout
)


admin.autodiscover()


urlpatterns = [
    # Post URLs
    path('',
         PostListView.as_view(),
         name='post_list_view'),
    path('post/<slug:slug>/',
         PostDetailView.as_view(),
         name='post_detail_view'),
    path('post/<slug:slug>/ajax/',
         PostDetailView.as_view(template_name='posts/post_detail_ajax.html'),
         name='post_detail_ajax_view'),
    path('new/',
         add_post,
         name='add_post_view'),

    # Feed URL
    path('feed/rss20.xml', PostsFeed(), name='feed'),

    # Redirect "/blog/" to "/"
    path('blog/', RedirectView.as_view(url='/')),
    # Redirect old-style "/blog/post/n/<slug>/" to "/post/<slug>/"
    re_path(r'^blog/post/\d+/(?P<slug>[\w\-_]+)/$',
            RedirectView.as_view(url='/post/%(slug)s/')),

    # Account URLs
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', logout, name='logout'),
    path('accounts/register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/edit/', edit_profile, name='edit_profile_view'),
    path('accounts/passwd/',
         auth_views.PasswordChangeView.as_view(
             success_url=reverse_lazy('post_list_view')
         ),
         name='password_change_view'),
    path('accounts/', include(auth_urls)),

    # Non-standard admin URL
    path('django-admin/', admin.site.urls),
]

if settings.DEBUG :
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
