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
from datetime import datetime
import re
import markdown
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


class Post(models.Model):
    """
    A blog post

    `content_markdown` stores the content as entered by the blogger. `content`
    stores safe HTML, which is generated from `content_markdown` by the `save`
    method.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.CharField(max_length=255, blank=True)
    content_markdown = models.TextField(
        verbose_name='Content (Markdown-formatted)',
        help_text='Use <a href="http://daringfireball.net/projects/markdown/">Markdown</a> syntax')
    content = models.TextField()
    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Converts markdown to safe HTML, creates unique slug, and sets the
        published_at timestamp.
        """
        # Convert Markdown to safe HTML
        # Useful: https://code.djangoproject.com/wiki/UsingMarkup
        # See also:
        # http://pypi.python.org/pypi/django-markupfield/
        # http://www.freewisdom.org/projects/python-markdown/CodeHilite
        # Enable extra features. Escape tags.
        self.content = markdown.markdown(self.content_markdown, ['extra'],
                                         safe_mode=settings.MARKDOWN_SAFE_MODE)

        # Create unique slug
        # Check slug is unique
        if self.slug is None or len(self.slug) == 0:
            # self.slug will be None if the post was created using PostForm
            self.slug = slugify(self.title)
        if len(self.slug) == 0:
            # If the title has no alphanumeric characters, slug will be empty
            self.slug = 'x'
        # Strip off any final digits
        match = re.match('(.+?)(?:-\d+)?$', self.slug)
        initial_slug = match.group(1)
        serial = 1
        while Post.objects.exclude(id=self.id).filter(slug=self.slug).count() > 0:
            serial += 1
            self.slug = '%s-%s' % (initial_slug, serial)

        # Set published_at timestamp
        if self.is_published and not self.published_at:
            self.published_at = datetime.now()

        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
