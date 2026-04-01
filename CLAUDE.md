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
| `posts/`      | The reusable Django app (models, views, urls, feeds, forms, tests)               |
| `standalone/` | Standalone harness: settings.py, wsgi.py, fixtures                               |
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
DEPLOY_ENV=dev SECRET_KEY=x ALLOWED_HOSTS=localhost DATABASE_URL='sqlite:///standalone/sqlite3.db' uv run pytest posts/tests/
```

## Environment variables (required for dev)

Set automatically by `manage-dev`, or set manually:

| Variable           | Dev value                              |
|--------------------|----------------------------------------|
| `DEPLOY_ENV`       | `dev`                                  |
| `SECRET_KEY`       | any string                             |
| `ALLOWED_HOSTS`    | space-separated hostnames              |
| `DATABASE_URL`     | e.g. `sqlite:///standalone/sqlite3.db` |

## Key patterns

- **Post content:** Stored as Markdown in `content_markdown`, saved as
  HTML in `content`. Conversion happens in `Post.save()`.
- **Slug generation:** Auto-generated from title on first save; appends
  `-2`, `-3` etc. for duplicates.
- **Authorization:** Moderators (users in the `Moderators` group) can
  see unpublished posts.
- **AJAX loading:** HTMX fetches `/post/<slug>/ajax/` when the title
  is clicked; Alpine.js handles the toggle state.

## Documentation

- Design specs: `docs/specs/YYYY-MM-DD_<design_spec_title>.md`
- Roadmap: `docs/roadmap.md`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing
conventions (pytest + pytest-unmagic), and code style.
