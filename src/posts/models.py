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
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def get_sentinel_user():
    # https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.SET
    return User.objects.get_or_create(username='deleted')[0]


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
        verbose_name=_('Content (Markdown-formatted)'),
        help_text=_(
            'Use <a href="http://daringfireball.net/projects/markdown/">'
            'Markdown</a> syntax'
        )
    )
    content = models.TextField()
    created_by = models.ForeignKey(User, models.SET(get_sentinel_user))
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True)
    # TODO: Allow comments to be enabled and disabled
    # comments_enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('post_detail_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Converts markdown to safe HTML, creates unique slug, and sets the
        published_at timestamp.
        """
        # Convert Markdown to safe HTML. Enable extra features. Escape tags.
        self.content = markdown.markdown(
            self.content_markdown,
            extensions=['extra'],
            safe_mode=settings.MARKDOWN_SAFE_MODE
        )

        # Create unique slug
        # Check slug is unique
        if not self.slug:
            # self.slug will be None if the post was created using PostForm
            # If the title has no alphanumeric characters, slugify will be empty
            self.slug = slugify(self.title) or 'x'
        # Strip off any final digits
        match = re.match('(.+?)(?:-\d+)?$', self.slug)
        initial_slug = match.group(1)
        serial = 1
        while Post.objects.exclude(pk=self.pk).filter(slug=self.slug).count() > 0:
            serial += 1
            self.slug = '%s-%s' % (initial_slug, serial)

        # Set published_at timestamp
        if self.is_published and not self.published_at:
            self.published_at = datetime.now()

        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
