# Refresh roadmap

This document plans the modernization of onepageblog. The work is
ordered so that each phase produces a working codebase — no phase
depends on a later one.


## Phase 1: Project tooling

Switch from `standalone/requirements.txt` + manual venv to **uv** with
a `pyproject.toml` at the repo root.

- [ ] Create `pyproject.toml` with project metadata (name, version,
      license, Python version, etc.) and dependencies.
- [ ] Pin Django 5.2 and current versions of Markdown, pytest,
      pytest-django, pytest-unmagic, dj-database-url.
- [ ] Remove `standalone/requirements.txt`.
- [ ] Replace `manage-dev` shell script with a simpler wrapper that
      works with `uv run`, or document `uv run manage.py` directly.
- [ ] Add `uv.lock` to version control.
- [ ] Update `CLAUDE.md` and `CONTRIBUTING.md` with the new commands.
- [ ] Update `.gitignore`: drop old `src/` paths, add `venv/`,
      `__pycache__/`, `*.pyc`, `.python-version`.


## Phase 2: Django 5.2 upgrade

Upgrade from Django 2.2 to 5.2. The main breaking changes are:

### URL configuration

- `django.conf.urls.include` was removed in Django 4.0. Change
  `posts/urls.py` to import `include` from `django.urls`.

### Settings

- `TEMPLATE_DEBUG` was removed in Django 1.10 — delete it.
- `TEMPLATE_DIRS` was removed in Django 1.10 — delete it (already
  covered by `TEMPLATES[0]['APP_DIRS']`).
- Add `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'` to
  suppress the Django 3.2+ warning.

### Markdown `safe_mode`

The `safe_mode` parameter was removed from the `markdown` library in
version 3.0. In `Post.save()`, replace:

```python
markdown.markdown(
    self.content_markdown,
    extensions=['extra'],
    safe_mode=settings.MARKDOWN_SAFE_MODE
)
```

with the `bleach` library or `nh3` for HTML sanitization after
rendering, or simply drop sanitization if all authors are trusted
(admin-only publishing). Remove the `MARKDOWN_SAFE_MODE` setting.

### Model / ORM

- `super(Post, self).save(...)` → `super().save(...)` (Python 3 style).

### Auth views

- `django.contrib.auth.views.LoginView` / `PasswordChangeView` are
  already class-based — these are fine.
- Verify the custom `logout` view still works (Django 5.0 changed
  `LogoutView` to reject GET requests, but we use a custom function
  view so this is not affected).

### Other

- Run `python manage.py check --deploy` and fix any warnings.
- Regenerate migrations if needed (`makemigrations`).
- Run the full test suite.


## Phase 3: Frontend — drop jQuery, add HTMX + Alpine.js

The frontend currently uses jQuery for two things:

1. **AJAX post loading** (`onepageblog.js` → `load_post`): clicking a
   post title on the list page fetches `/post/<slug>/ajax/` and injects
   the HTML.
2. **Toggle**: clicking the title again hides/shows the loaded content.

### Replace with HTMX

HTMX handles the AJAX load natively:

```html
<div class="list_item"
     x-data="{ open: false }">
  <h2>
    <a href="{{ post.get_absolute_url }}"
       hx-get="/post/{{ post.slug }}/ajax/"
       hx-target="next .list_item_outer"
       hx-swap="innerHTML"
       @click.prevent="open = !open"
       hx-trigger="click once">
      {{ post.title }}
    </a>
  </h2>
  <h3>...</h3>
  <div class="list_item_outer" x-show="open"></div>
</div>
```

### Replace with Alpine.js

Alpine handles the toggle state (`x-data`, `x-show`, `@click`). No
build step needed — just a `<script>` tag.

### Steps

- [ ] Remove `posts/static/onepageblog/js/jquery-3.5.1.min.js`.
- [ ] Remove `posts/static/onepageblog/js/onepageblog.js`.
- [ ] Add HTMX and Alpine.js via CDN `<script>` tags in `base.html`
      (no bundling — keep it simple).
- [ ] Rewrite `post_list.html` to use `hx-get` + `x-show` for the
      AJAX-load-and-toggle behavior.
- [ ] Remove the `to_button` jQuery function (unused in templates).
- [ ] Remove the inline `<script>` block from `post_list.html`.


## Phase 4: Remove Disqus and social links

Drop the Disqus comment integration and the social sharing links. Both
pull in third-party scripts/services that add complexity without much
value.

### Disqus

- [ ] Delete Disqus `<script>` blocks from `base.html` and
      `post_detail.html`.
- [ ] Remove `DISQUS_SHORTNAME` from settings and
      `context_processors.py`.
- [ ] Remove the Disqus comment link from `post_detail_ajax.html`.

### Social links

- [ ] Delete `posts/templates/posts/social_links.html`.
- [ ] Remove the `{% include "posts/social_links.html" %}` from
      `post_detail.html` and `post_detail_ajax.html`.


## Phase 5: Test improvements

Existing tests use standard pytest fixtures and the `client` magic
fixture. Migrate to pytest-unmagic per `CONTRIBUTING.md`.

- [ ] Add `pytest-unmagic` to `pyproject.toml` dependencies.
- [ ] Rewrite `test_models.py` fixtures from `@pytest.fixture` to
      `@fixture` / `@use` from `unmagic`.
- [ ] Rewrite `test_views.py` to use explicit fixtures instead of the
      magic `client` parameter.
- [ ] Remove `tox.ini` (run pytest via `uv run pytest` instead).
- [ ] Add tests for moderator-only views (noted as TODO in
      `test_views.py`).


## Phase 6: Housekeeping

Small items that don't need their own phase.

- [ ] Delete `.pyc` files from the repo and ensure `.gitignore` covers
      `__pycache__/` and `*.pyc`.
- [ ] Update license headers: source files say "GNU General Public
      License" but `COPYING` is AGPL-3.0. Make them consistent.
- [ ] Remove `absurl` templatetag (`posts/templatetags/absurl.py`).
      With social links gone, it's only used for the feed link in
      `base.html` — replace with `request.build_absolute_uri` or a
      plain `{% url 'feed' %}`.
- [ ] Remove `posts.templatetags` from `INSTALLED_APPS` if no other
      templatetags remain.
