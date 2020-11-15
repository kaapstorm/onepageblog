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

# From: https://gist.github.com/laxxxguy/69aec1259131b5619fb7

from django.template import Library
from django.template.defaulttags import URLNode, url

register = Library()


class AbsoluteURL(str):
    pass


class AbsoluteURLNode(URLNode):
    def render(self, context):
        asvar, self.asvar = self.asvar, None
        path = super(AbsoluteURLNode, self).render(context)
        request_obj = context['request']
        abs_url = AbsoluteURL(request_obj.build_absolute_uri(path))

        if not asvar:
            return str(abs_url)
        else:
            if path == request_obj.path:
                abs_url.active = 'active'
            else:
                abs_url.active = ''
            context[asvar] = abs_url
            return ''


@register.tag
def absurl(parser, token):
    node = url(parser, token)
    return AbsoluteURLNode(
        view_name=node.view_name,
        args=node.args,
        kwargs=node.kwargs,
        asvar=node.asvar
    )
