# Generated by Django 2.1.5 on 2019-02-17 00:35

from django.conf import settings
from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('summary', models.CharField(blank=True, max_length=255)),
                ('content_markdown', models.TextField(help_text='Use <a href="http://daringfireball.net/projects/markdown/">Markdown</a> syntax', verbose_name='Content (Markdown-formatted)')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=False)),
                ('published_at', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=models.SET(posts.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
