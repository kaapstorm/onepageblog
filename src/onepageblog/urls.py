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
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, password_change

from onepageblog.tips.feeds import PostsFeed
from onepageblog.tips.views import (PostListView, PostDetailView, add_tip, 
    profile, edit_profile, register, logout)


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), 
        name='tip_list_view'),
    url(r'^tip/(?P<slug>[\w\-_]+)/$', PostDetailView.as_view(), 
        name='tip_detail_view'),
    url(r'^tip/(?P<slug>[\w\-_]+)/ajax/$', 
        PostDetailView.as_view(template_name='tips/tip_detail_ajax.html'), 
        name='tip_detail_ajax_view'),
    url(r'^new/$', add_tip,
        name='add_tip_view'),
    
    url(r'^feed/atom.xml$', PostsFeed(), 
        name='feed'),
                       
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/register/$', register),
    (r'^accounts/profile/$', profile),
    url(r'^accounts/edit/$', edit_profile,
        name='edit_profile_view'),
    url(r'^accounts/passwd/$', password_change,
        name='password_change_view',
        kwargs={'post_change_redirect': '../../'}),
    
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
