# onepageblog

A small Django blog app. Posts are listed on a single page; body content
loads asynchronously via AJAX when clicked. Each post also has its own
URL.

Intended to be used as a submodule in a larger Django project. The
`standalone/` directory is a thin harness for running it independently
(dev server, tests).

## Structure

| Name          | Description                                                                      |
|---------------|----------------------------------------------------------------------------------|
| `posts/`      | The reusable Django app (models, views, urls, feeds, forms, templatetags, tests) |
| `standalone/` | Standalone harness: settings.py, wsgi.py, requirements.txt, fixtures             |
| `manage.py`   | Standard Django manage.py                                                        |
| `manage-dev`  | Shell script: sets dev env vars, then delegates to manage.py                     |

## Commands

```bash
# Run dev server
./manage-dev runserver

# Run migrations
./manage-dev migrate

# Load fixtures
./manage-dev loaddata standalone/fixtures.json

# Run tests (from repo root)
DJANGO_SETTINGS_MODULE=standalone.settings DEPLOY_ENV=dev SECRET_KEY=x ALLOWED_HOSTS=localhost DATABASE_URL='sqlite:///standalone/sqlite3.db' pytest posts/tests/
```

## Environment variables (required for dev)

Set automatically by `manage-dev`, or set manually:

| Variable           | Dev value                              |
|--------------------|----------------------------------------|
| `DEPLOY_ENV`       | `dev`                                  |
| `SECRET_KEY`       | any string                             |
| `ALLOWED_HOSTS`    | space-separated hostnames              |
| `DATABASE_URL`     | e.g. `sqlite:///standalone/sqlite3.db` |
| `DISQUS_SHORTNAME` | optional; omit to disable Disqus       |

## Key patterns

- **Post content:** Stored as Markdown in `content_markdown`, saved as
  HTML in `content`. Conversion happens in `Post.save()`.
- **Slug generation:** Auto-generated from title on first save; appends
  `-2`, `-3` etc. for duplicates.
- **Authorization:** Moderators (users in the `Moderators` group) can
  see unpublished posts.
- **AJAX loading:** `posts/static/onepageblog/js/onepageblog.js` fetches
  `/post/<slug>/ajax/` and injects into the page.

## Known tech debt (pre-refresh)

- Django 2.2 (EOL). Target: Django 4.2+ or 5.x.
- `from django.conf.urls import include` removed in Django 4.0 — needs 
  updating.
- `markdown.markdown(..., safe_mode=...)` — `safe_mode` was removed in
  Markdown 3.0.
- `tox.ini` references stale `DJANGO_SETTINGS_MODULE=onepageblog.settings`.
- jQuery 3.5.1 bundled locally — consider removing jQuery or updating.
- `.pyc` files checked into git (should be gitignored).
