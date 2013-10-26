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
        'user': 'extrange',
        'passwd': 'secret',
        'db': 'extrange_db1'
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
    created_at = tz.localize(record[ttotd['fields'].index('created_at')])
    post = Post(
        title=record[ttotd['fields'].index('title')],
        slug=record[ttotd['fields'].index('slug')],
        content_markdown=record[ttotd['fields'].index('content_markdown')],
        content=record[ttotd['fields'].index('content')],
        created_by=user,
        is_published=record[ttotd['fields'].index('is_published')],
        published_at=created_at
    )
    post.save()
    post.created_at = created_at  # Reset it from now() to original
    post.save()
    print('Saved {}'.format(post.slug))


def import_extrange(record, user):
    created_at = tz.localize(record[extrange['fields'].index('created')])
    post = Post(
        title=record[extrange['fields'].index('title')],
        slug=record[extrange['fields'].index('slug')],
        content_markdown=record[extrange['fields'].index('body')],
        content=record[extrange['fields'].index('body')],
        created_by=user,
        is_published=record[extrange['fields'].index('enabled')],
        published_at=created_at
        # summary is dropped
        # body_type is ignored
    )
    post.save()
    post.created_at = created_at
    post.save()
    print('Saved {}'.format(post.slug))


def import_norman(record, user):
    created_at = tz.localize(record[norman['fields'].index('created')])
    post = Post(
        title=record[norman['fields'].index('title')],
        slug=record[norman['fields'].index('slug')],
        content_markdown=record[norman['fields'].index('body')],
        content=record[norman['fields'].index('body')],
        created_by=user,
        is_published=record[norman['fields'].index('enabled')],
        published_at=created_at
        # summary is dropped
        # image_tags is dropped
    )
    post.save()
    post.created_at = created_at
    post.save()
    print('Saved {}'.format(post.slug))


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
    main(
        settings=ttotd,
        import_post=import_ttotd,
        i_uid=ttotd['fields'].index('created_by_id')
    )
    main(
        settings=extrange,
        import_post=import_extrange,
        i_uid=extrange['fields'].index('author_id')
    )
    main(
        settings=norman,
        import_post=import_norman
    )
