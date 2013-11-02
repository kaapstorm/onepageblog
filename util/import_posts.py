#!/usr/bin/env python
import sys
from django.contrib.auth.models import User
import pymysql
import pytz
from onepageblog.posts.models import Post


tz = pytz.timezone('Africa/Johannesburg')
ttotd = {
    'database': {
        'user': 'ttotd',
        'passwd': 'secret',
        'db': 'ttotd_db1',
    },
    'table': 'tips_tip',
    'fields': ['id', 'title', 'slug', 'content_markdown', 'content', 'created_by_id', 'created_at', 'is_published']
}
extrange = {
    'database': {
        'user': 'extran',
        'passwd': 'secret',
        'db': 'extran_db1'
    },
    'table': 'blog_post',
    'fields': ['id', 'author_id', 'title', 'slug', 'summary', 'body', 'body_type', 'created', 'modified', 'enabled']
}
norman = {
    'database': {
        'user': 'norman',
        'passwd': 'secret',
        'db': 'norman_db1'
    },
    'table': 'blog_post',
    'fields': ['id', 'title', 'slug', 'summary', 'body', 'image_tags', 'created', 'modified', 'enabled']
}


def import_ttotd(record, user):
    fields = ttotd['fields']
    print('Saving {}'.format(record[fields.index('slug')]))
    created_at = tz.localize(record[fields.index('created_at')])
    post = Post(
	title=unicode(record[fields.index('title')], 'windows-1252'),
	slug=unicode(record[fields.index('slug')], 'windows-1252'),
	content_markdown=unicode(record[fields.index('content_markdown')], 'windows-1252'),
	content=unicode(record[fields.index('content')], 'windows-1252'),
	created_by=user,
	is_published=record[fields.index('is_published')],
	published_at=created_at
    )
    post.save()
    post.created_at = created_at  # Reset it from now() to original
    post.save()


def import_extrange(record, user):
    fields = extrange['fields']
    print('Saving {}'.format(record[fields.index('slug')]))
    created_at = tz.localize(record[fields.index('created')])
    post = Post(
	title=unicode(record[fields.index('title')], 'windows-1252'),
	slug=unicode(record[fields.index('slug')], 'windows-1252'),
	summary=unicode(record[fields.index('summary')], 'windows-1252'),
	content_markdown=unicode(record[fields.index('body')], 'windows-1252'),
	content=unicode(record[fields.index('body')], 'windows-1252'),
	created_by=user,
	is_published=record[fields.index('enabled')],
	published_at=created_at
	# body_type is ignored
    )
    post.save()
    post.created_at = created_at
    post.save()


def import_norman(record, user):
    fields = norman['fields']
    print('Saving {}'.format(record[fields.index('slug')]))
    created_at = tz.localize(record[fields.index('created')])
    post = Post(
	title=unicode(record[fields.index('title')], 'windows-1252'),
	slug=unicode(record[fields.index('slug')], 'windows-1252'),
	summary=unicode(record[fields.index('summary')], 'windows-1252'),
	content_markdown=unicode(record[fields.index('body')], 'windows-1252'),
	content=unicode(record[fields.index('body')], 'windows-1252'),
	created_by=user,
	is_published=record[fields.index('enabled')],
	published_at=created_at
	# image_tags is dropped
    )
    post.save()
    post.created_at = created_at
    post.save()


def get_username(conn, uid):
    cur = conn.cursor()
    cur.execute('SELECT username FROM auth_user WHERE id = {}'.format(uid))
    for r in cur:
        record = r
        break
    else:
        record = [None]
    cur.close()
    return record[0]


def get_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print('User "{}" not found'.format(username))
        sys.exit(1)
    return user


def main(settings, import_post, i_uid=None):
    conn = pymysql.connect(**settings['database'])
    cur = conn.cursor()
    cur.execute('SELECT * FROM {}'.format(settings['table']))
    for record in cur:
        username = get_username(conn, record[i_uid]) if i_uid else 'norman'
        user = get_user(username)
        import_post(record, user)
    cur.close()
    conn.close()


if __name__ == '__main__':
#    main(
#        settings=ttotd,
#        import_post=import_ttotd,
#        i_uid=ttotd['fields'].index('created_by_id')
#    )
    main(
        settings=extrange,
        import_post=import_extrange,
        i_uid=extrange['fields'].index('author_id')
    )
    main(
        settings=norman,
        import_post=import_norman
    )

