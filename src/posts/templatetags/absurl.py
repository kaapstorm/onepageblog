# Snippet 1518
# by johnboxall
# http://djangosnippets.org/snippets/1518/

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

try:
    # Python 2
    import urlparse
except ImportError:
    # Python 3
    from urllib import parse as urlparse
from django.template import Library
from django.template.defaulttags import URLNode, url
from django.contrib.sites.models import Site

register = Library()


class AbsoluteURLNode(URLNode):
    def render(self, context):
        path = super(AbsoluteURLNode, self).render(context)
        domain = "http://%s" % Site.objects.get_current().domain
        return urlparse.urljoin(domain, path)


@register.tag
def absurl(parser, token, node_cls=AbsoluteURLNode):
    """Just like {% url %} but prepends the domain of the current site."""
    node_instance = url(parser, token)
    return node_cls(view_name=node_instance.view_name,
                    args=node_instance.args,
                    kwargs=node_instance.kwargs,
                    asvar=node_instance.asvar)
