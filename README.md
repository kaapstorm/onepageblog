onepageblog
===========

onepageblog is a small blogging application. It shows all post titles on
a single page, and loads the body asynchronously when the user clicks on
the title. Each post also has a unique URL and can be rendered on its
own page.

It is intended to be used as a submodule in a Django project. A
standalone harness is included for running it independently.


Quick start
-----------

```bash
uv sync
./manage-dev migrate
./manage-dev createsuperuser
./manage-dev runserver
```

Then open http://127.0.0.1:8000/.


Creating posts
--------------

### Via the admin

1. Go to http://127.0.0.1:8000/django-admin/ and log in with your
   superuser account.
2. Under **Posts**, click **Add**.
3. Enter a title and body. The body uses
   [Markdown](https://daringfireball.net/projects/markdown/) syntax.
4. Tick **Is published** to make the post visible on the public site.
   The **Published at** timestamp is set automatically when a post is
   first published.
5. Click **Save**.

The slug is auto-generated from the title. Duplicate titles get a
numeric suffix (`-2`, `-3`, etc.).

### Via the public form

Registered users can submit posts at http://127.0.0.1:8000/new/. These
posts are created unpublished and must be published by a staff member in
the admin.

### Moderation

Users in the **Moderators** group can see unpublished posts on the
public site, which is useful for reviewing submissions before
publishing.


License
-------

GNU Affero General Public License v3 — see [COPYING](COPYING).
