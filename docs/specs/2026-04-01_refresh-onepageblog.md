# onepageblog Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modernize onepageblog from Django 2.2 + jQuery to Django 5.2 + HTMX/Alpine.js, with uv for project management, pytest-unmagic for tests, and removal of Disqus/social links/absurl.

**Architecture:** The app structure stays the same — `posts/` is the reusable Django app, `standalone/` is the dev harness. We replace the build tooling (uv + pyproject.toml), upgrade Django, swap the frontend JS layer, strip dead features, and modernize the tests.

**Tech Stack:** Django 5.2, HTMX 2.x, Alpine.js 3.x, Markdown, uv, pytest + pytest-django + pytest-unmagic

---

## File map

### Files to create

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata, dependencies, pytest config |
| `posts/tests/fixtures.py` | Shared pytest-unmagic fixtures |

### Files to modify

| File | Changes |
|------|---------|
| `standalone/settings.py` | Remove deprecated settings, add `DEFAULT_AUTO_FIELD`, drop Disqus/Markdown safe_mode |
| `posts/urls.py` | Fix `include` import |
| `posts/models.py` | Drop `safe_mode`, modernize `super()` call |
| `posts/context_processors.py` | Remove `disqus_shortname` |
| `posts/templates/base.html` | Replace jQuery/Disqus scripts with HTMX + Alpine CDN tags, remove `{% load absurl %}` |
| `posts/templates/posts/post_list.html` | Replace jQuery AJAX with HTMX + Alpine |
| `posts/templates/posts/post_detail.html` | Remove Disqus block and social links include |
| `posts/templates/posts/post_detail_ajax.html` | Remove Disqus comment link, social links include, `{% load absurl %}` |
| `posts/templates/posts/post_add.html` | Remove jQuery `to_button` script block |
| `posts/templates/registration/login.html` | Remove jQuery `to_button` script block |
| `posts/templates/registration/register.html` | Remove jQuery `to_button` script block |
| `posts/templates/registration/edit_profile.html` | Remove jQuery `to_button` script block |
| `posts/templates/registration/password_change_form.html` | Remove jQuery `to_button` script block |
| `posts/templates/registration/profile.html` | Remove jQuery `to_button` script block |
| `posts/tests/test_models.py` | Migrate to pytest-unmagic |
| `posts/tests/test_views.py` | Migrate to pytest-unmagic |
| `.gitignore` | Modernize ignore patterns |
| `manage-dev` | Update for uv |
| `CLAUDE.md` | Update commands, structure, remove stale tech debt |
| `CONTRIBUTING.md` | Update setup instructions for uv |

### Files to delete

| File | Reason |
|------|--------|
| `standalone/requirements.txt` | Replaced by `pyproject.toml` |
| `standalone/tox.ini` | Replaced by `uv run pytest` |
| `posts/static/onepageblog/js/jquery-3.5.1.min.js` | jQuery removed |
| `posts/static/onepageblog/js/onepageblog.js` | jQuery removed |
| `posts/templates/posts/social_links.html` | Feature removed |
| `posts/templatetags/absurl.py` | Feature removed |
| All `*.pyc` files and `__pycache__/` dirs | Should never be in git |

---

## Task 1: Housekeeping — clean .pyc files and .gitignore

Get the repo into a clean state before making functional changes.

**Files:**
- Modify: `.gitignore`
- Delete: all `*.pyc` files and `__pycache__/` directories (outside `venv/`)

- [ ] **Step 1: Remove .pyc files and __pycache__ directories from git tracking**

```bash
find . -path ./venv -prune -o -name '*.pyc' -print -exec git rm --cached {} +
find . -path ./venv -prune -o -name '__pycache__' -type d -print -exec git rm -r --cached {} +
```

- [ ] **Step 2: Update .gitignore**

Replace the contents of `.gitignore` with:

```
*.pyc
__pycache__/
*.egg-info/
venv/
.venv/
.python-version
standalone/settings_local.py
standalone/sqlite3.db
standalone/fixtures.json
standalone/utcfixtures.json
.idea/
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: clean .pyc files from repo and update .gitignore"
```

---

## Task 2: Project tooling — uv + pyproject.toml

Replace `standalone/requirements.txt` with `pyproject.toml` and uv.

**Files:**
- Create: `pyproject.toml`
- Modify: `manage-dev`
- Delete: `standalone/requirements.txt`, `standalone/tox.ini`

- [ ] **Step 1: Create pyproject.toml**

```toml
[project]
name = "onepageblog"
version = "2.0.0"
description = "A small Django blogging application"
license = "AGPL-3.0-or-later"
requires-python = ">=3.10"
dependencies = [
    "django~=5.2",
    "dj-database-url",
    "markdown",
]

[dependency-groups]
dev = [
    "pytest",
    "pytest-django",
    "pytest-unmagic",
]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "standalone.settings"
python_files = "tests.py test_*.py"
```

- [ ] **Step 2: Update manage-dev**

Replace `manage-dev` contents with:

```sh
#!/bin/sh

export DEPLOY_ENV=dev
export SECRET_KEY=this-key-is-not-secret
export ALLOWED_HOSTS='127.0.0.1 localhost'
export DATABASE_URL='sqlite:///standalone/sqlite3.db'

uv run python manage.py "$@"
```

Note: `$*` → `"$@"` to correctly handle arguments with spaces.

- [ ] **Step 3: Delete old files**

```bash
git rm standalone/requirements.txt standalone/tox.ini
```

- [ ] **Step 4: Lock dependencies**

```bash
uv lock
```

- [ ] **Step 5: Verify the dev server starts**

```bash
./manage-dev check
```

Expected: `System check identified no issues` (or Django-version
warnings we'll fix in the next task).

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml uv.lock manage-dev
git commit -m "chore: switch to uv + pyproject.toml for dependency management"
```

---

## Task 3: Django 5.2 upgrade — settings

Fix `standalone/settings.py` for Django 5.2 compatibility.

**Files:**
- Modify: `standalone/settings.py`

- [ ] **Step 1: Fix the include import in posts/urls.py**

In `posts/urls.py`, change line 2:

```python
# Before
from django.conf.urls import include

# After
from django.urls import include
```

- [ ] **Step 2: Remove deprecated settings**

In `standalone/settings.py`:

Delete line 25 (`TEMPLATE_DEBUG = False`).

Delete lines 68-71 (the `TEMPLATE_DIRS` tuple):
```python
TEMPLATE_DIRS = (
    BASE_DIR + '/posts/templates/',
    BASE_DIR + '/standalone/templates/',
)
```

- [ ] **Step 3: Add DEFAULT_AUTO_FIELD**

Add after the `SITE_ID = 1` line in `standalone/settings.py`:

```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

- [ ] **Step 4: Remove MARKDOWN_SAFE_MODE setting**

Delete these lines from `standalone/settings.py`:

```python
# Disallow raw HTML in posts. Valid values are of "remove", "replace" or
# "escape". Set to False to support markup not supported by Markdown, but risk
# cross-site scripting.
MARKDOWN_SAFE_MODE = 'escape'
```

- [ ] **Step 5: Remove DISQUS_SHORTNAME setting**

Delete these lines from `standalone/settings.py`:

```python
# Disqus website shortname for Disqus comments.
# Set "DISQUS_SHORTNAME = None" to disable Disqus comments.
DISQUS_SHORTNAME = os.environ.get('DISQUS_SHORTNAME')
```

- [ ] **Step 6: Run Django system check**

```bash
./manage-dev check
```

Expected: `System check identified no issues.`

- [ ] **Step 7: Commit**

```bash
git add standalone/settings.py posts/urls.py
git commit -m "fix: update settings and urls for Django 5.2 compatibility"
```

---

## Task 4: Django 5.2 upgrade — model

Fix `Post.save()` for modern Markdown and Python 3 style.

**Files:**
- Modify: `posts/models.py`
- Test: `posts/tests/test_models.py`

- [ ] **Step 1: Run existing tests to establish baseline**

```bash
./manage-dev test posts.tests 2>&1 || uv run pytest posts/tests/ -v
```

Note: The tests may fail because `safe_mode` kwarg is rejected by
newer Markdown. That's expected — we're about to fix it.

- [ ] **Step 2: Update the markdown call in Post.save()**

In `posts/models.py`, replace lines 70-74:

```python
# Before
self.content = markdown.markdown(
    self.content_markdown,
    extensions=['extra'],
    safe_mode=settings.MARKDOWN_SAFE_MODE
)

# After
self.content = markdown.markdown(
    self.content_markdown,
    extensions=['extra'],
)
```

- [ ] **Step 3: Modernize the super() call**

In `posts/models.py`, replace line 94:

```python
# Before
super(Post, self).save(*args, **kwargs)

# After
super().save(*args, **kwargs)
```

- [ ] **Step 4: Remove the unused settings import**

In `posts/models.py`, line 20, remove:

```python
from django.conf import settings
```

(It was only used for `settings.MARKDOWN_SAFE_MODE`.)

- [ ] **Step 5: Run tests**

```bash
uv run pytest posts/tests/ -v
```

Expected: All tests pass.

- [ ] **Step 6: Run migrations check**

```bash
./manage-dev makemigrations --check
```

Expected: `No changes detected` (the model fields haven't changed).

- [ ] **Step 7: Commit**

```bash
git add posts/models.py
git commit -m "fix: remove deprecated markdown safe_mode, modernize super() call"
```

---

## Task 5: Remove Disqus and social links

Strip the Disqus integration, social sharing links, and absurl
templatetag.

**Files:**
- Modify: `posts/context_processors.py`
- Modify: `posts/templates/base.html`
- Modify: `posts/templates/posts/post_detail.html`
- Modify: `posts/templates/posts/post_detail_ajax.html`
- Delete: `posts/templates/posts/social_links.html`
- Delete: `posts/templatetags/absurl.py`
- Delete: `posts/templatetags/__init__.py`
- Modify: `standalone/settings.py` (remove `posts.templatetags` from INSTALLED_APPS)

- [ ] **Step 1: Simplify context_processors.py**

Remove `disqus_shortname` from the context processor. Replace the
entire `blog_settings` function body:

```python
from django.conf import settings


def blog_settings(request):
    return {
        'blog_title': settings.BLOG_TITLE,
    }
```

- [ ] **Step 2: Remove Disqus scripts from base.html**

Delete the entire Disqus `{% if disqus_shortname %}` block (lines
46-57 of `base.html`), which loads the Disqus count script.

Also remove `{% load absurl %}` (line 19).

Change the feed link (line 41) from:

```html
<link rel="alternate" type="application/rss+xml; version=2.0"
      title="{{ blog_title }} RSS 2.0 Feed" href="{% absurl 'feed' %}" />
```

to:

```html
<link rel="alternate" type="application/rss+xml; version=2.0"
      title="{{ blog_title }} RSS 2.0 Feed" href="{% url 'feed' %}" />
```

Change the feed nav link (line 75) from:

```html
[<a href="{% absurl 'feed' %}">Feed</a>]
```

to:

```html
[<a href="{% url 'feed' %}">Feed</a>]
```

- [ ] **Step 3: Strip post_detail.html**

Remove the entire `{% if disqus_shortname %}` block (lines 41-62),
which includes the Disqus embed script and the second "Back To List"
link.

Remove the social links include. Change lines 36-39 from:

```html
<p class="post_link">
  [<a href="{% url 'post_list_view' %}">Back To List</a>] |
  {% include "posts/social_links.html" %}
</p>
```

to:

```html
<p class="post_link">
  [<a href="{% url 'post_list_view' %}">Back To List</a>]
</p>
```

- [ ] **Step 4: Strip post_detail_ajax.html**

Remove `{% load absurl %}` (line 18).

Replace the `<p class="post_link">` block (lines 27-33) with:

```html
<p class="post_link">
  [<a href="{% url 'post_detail_view' slug=post.slug %}">Permalink</a>]
</p>
```

This removes the Disqus comment link, the social links include, and
switches from `{% absurl %}` to `{% url %}`.

- [ ] **Step 5: Delete social_links.html**

```bash
git rm posts/templates/posts/social_links.html
```

- [ ] **Step 6: Delete absurl templatetag**

```bash
git rm posts/templatetags/absurl.py posts/templatetags/__init__.py
git rm posts/templatetags/absurl.pyc posts/templatetags/__init__.pyc 2>/dev/null || true
```

- [ ] **Step 7: Remove posts.templatetags from INSTALLED_APPS**

In `standalone/settings.py`, delete the `'posts.templatetags',` line
from `INSTALLED_APPS`.

- [ ] **Step 8: Run tests**

```bash
uv run pytest posts/tests/ -v
```

Expected: All tests pass.

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "feat: remove Disqus, social links, and absurl templatetag"
```

---

## Task 6: Frontend — drop jQuery, add HTMX + Alpine.js

Replace jQuery with HTMX for AJAX loading and Alpine.js for toggle
state.

**Files:**
- Modify: `posts/templates/base.html`
- Modify: `posts/templates/posts/post_list.html`
- Modify: `posts/templates/posts/post_add.html`
- Modify: `posts/templates/registration/login.html`
- Modify: `posts/templates/registration/register.html`
- Modify: `posts/templates/registration/edit_profile.html`
- Modify: `posts/templates/registration/password_change_form.html`
- Modify: `posts/templates/registration/profile.html`
- Delete: `posts/static/onepageblog/js/jquery-3.5.1.min.js`
- Delete: `posts/static/onepageblog/js/onepageblog.js`

- [ ] **Step 1: Replace jQuery scripts with HTMX + Alpine in base.html**

In `base.html`, replace the two jQuery `<script>` tags (lines 43-44):

```html
<script type="text/javascript" src="{% static 'onepageblog/js/jquery-3.5.1.min.js' %}"></script>
<script type="text/javascript" src="{% static 'onepageblog/js/onepageblog.js' %}"></script>
```

with:

```html
<script src="https://unpkg.com/htmx.org@2.0.4"></script>
<script defer src="https://unpkg.com/alpinejs@3.14.9/dist/cdn.min.js"></script>
```

- [ ] **Step 2: Rewrite post_list.html**

Replace the entire content of `post_list.html` with:

```html
{% extends "base.html" %}

{% block content %}

<nav id="actions_nav">
  [<a href="{% url 'add_post_view' %}">Send Us A Post</a>]
</nav>

<div id="list_items">
    {% for post in post_list %}
    <div class="list_item" x-data="{ open: false, loaded: false }">

        <h2>
            <a href="{{ post.get_absolute_url }}"
               hx-get="{{ post.get_absolute_url }}ajax/"
               hx-target="next .list_item_outer"
               hx-swap="innerHTML"
               hx-trigger="click once"
               @click.prevent="open = !open; loaded = true"
               >{{ post.title }}</a>
        </h2>
        <h3>{{ post.published_at|date:"D, j M Y" }} | {{ post.created_by }}</h3>

        <div class="list_item_outer" x-show="open" x-cloak></div>
    </div>

    {% endfor %}

</div>

{% endblock %}
```

- [ ] **Step 3: Remove jQuery script blocks from form templates**

Each of these six templates has an identical `{% block script %}` block
(lines 20-29) that calls `onepageblog.to_button`. Delete that entire
block from each file:

- `posts/templates/posts/post_add.html`
- `posts/templates/registration/login.html`
- `posts/templates/registration/register.html`
- `posts/templates/registration/edit_profile.html`
- `posts/templates/registration/password_change_form.html`
- `posts/templates/registration/profile.html`

The `{% block script %}...{% endblock %}` block to delete in each is:

```html
{% block script %}
<script type="text/javascript"><!--

$(document).ready(function () {
    // Change ".to_button" links to buttons
    $('.to_button').each(onepageblog.to_button);
});

// -->
</script>
{% endblock %}
```

The `.to_button` spans in these templates can stay as-is — they're
just styled links and work fine without JavaScript.

- [ ] **Step 4: Add x-cloak CSS**

Add to `posts/static/onepageblog/css/default.css`:

```css
[x-cloak] {
    display: none !important;
}
```

This prevents HTMX-loaded content from flashing before Alpine
initializes.

- [ ] **Step 5: Delete jQuery files**

```bash
git rm posts/static/onepageblog/js/jquery-3.5.1.min.js
git rm posts/static/onepageblog/js/onepageblog.js
```

- [ ] **Step 6: Start dev server and manually verify**

```bash
./manage-dev runserver
```

Test in browser:
1. Post list page loads without JS errors.
2. Clicking a post title loads content via HTMX.
3. Clicking again toggles the content hidden/visible.
4. The post detail page (`/post/<slug>/`) still renders correctly.
5. Form pages (login, register, add post) load without JS errors.

- [ ] **Step 7: Run tests**

```bash
uv run pytest posts/tests/ -v
```

Expected: All tests pass.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "feat: replace jQuery with HTMX + Alpine.js"
```

---

## Task 7: Migrate tests to pytest-unmagic

Rewrite existing tests to use explicit fixtures per `CONTRIBUTING.md`.

**Files:**
- Create: `posts/tests/fixtures.py`
- Modify: `posts/tests/test_models.py`
- Modify: `posts/tests/test_views.py`

- [ ] **Step 1: Create shared fixtures module**

Create `posts/tests/fixtures.py`:

```python
from django.test import Client
from unmagic import fixture

from posts.models import Post


@fixture
def client():
    yield Client()


@fixture
def post():
    p = Post(title='My Post')
    p.save()
    yield p
    p.delete()
```

- [ ] **Step 2: Rewrite test_models.py**

Replace the entire contents of `posts/tests/test_models.py` with:

```python
import inspect
from datetime import datetime

from unmagic import fixture, use

from posts.models import Post


@fixture
def posts():
    post0 = Post(title='My Post')
    post0.save()
    post1 = Post(title='My Post')
    post1.save()
    post2 = Post(title='My Post')
    post2.save()
    yield post0, post1, post2
    post2.delete()
    post1.delete()
    post0.delete()


@fixture
def markdown_post():
    post = Post(
        title='My Post',
        content_markdown=inspect.cleandoc("""
        Heading
        =======

        Body text
        """)
    )
    post.save()
    yield post
    post.delete()


@use("db")
@use(markdown_post)
def test_save_creates_markdown():
    assert markdown_post().content == """<h1>Heading</h1><p>Body text</p>"""


@use("db")
@use(posts)
def test_save_creates_unique_slug():
    p = posts()
    assert p[0].slug == 'my-post'
    assert p[1].slug == 'my-post-1'
    assert p[2].slug == 'my-post-2'


@use("db")
@use(markdown_post)
def test_published_at():
    ts1 = datetime.now()
    post = markdown_post()
    post.is_published = True
    post.save()
    ts2 = post.published_at
    assert (ts1.day, ts1.hour, ts1.minute) == (ts2.day, ts2.hour, ts2.minute)
```

- [ ] **Step 3: Run model tests**

```bash
uv run pytest posts/tests/test_models.py -v
```

Expected: All 3 tests pass.

- [ ] **Step 4: Rewrite test_views.py**

Replace the entire contents of `posts/tests/test_views.py` with:

```python
from unmagic import use

from posts.tests.fixtures import client, post


@use("db")
@use(client)
def test_post_list_view_200():
    response = client().get('/')
    assert response.status_code == 200


@use("db")
@use(client)
def test_new_post_view_200():
    response = client().get('/new/')
    assert response.status_code == 200


@use("db")
@use(client, post)
def test_post_detail_view_200():
    response = client().get('/post/my-post/')
    assert response.status_code == 200


@use("db")
@use(client, post)
def test_feed_200():
    response = client().get('/feed/rss20.xml')
    assert response.status_code == 200
```

- [ ] **Step 5: Run all tests**

```bash
uv run pytest posts/tests/ -v
```

Expected: All 7 tests pass.

- [ ] **Step 6: Add moderator view tests**

Add the following fixtures and tests to `posts/tests/test_views.py`
(the file already imports `Client` via the `client` fixture, and the
additional imports needed are shown):

```python
from django.contrib.auth.models import Group, User
from django.test import Client as DjangoClient

from posts.models import Post


@fixture
def moderator_client():
    user = User.objects.create_user(username='mod', password='pass')
    group, _ = Group.objects.get_or_create(name='Moderators')
    user.groups.add(group)
    c = DjangoClient()
    c.login(username='mod', password='pass')
    yield c
    user.delete()


@fixture
def unpublished_post():
    p = Post(title='Draft Post', is_published=False)
    p.save()
    yield p
    p.delete()
```

And add the test functions:

```python
@use("db")
@use(client, unpublished_post)
def test_unpublished_post_not_visible_to_anonymous():
    response = client().get('/post/draft-post/')
    assert response.status_code == 404


@use("db")
@use(moderator_client, unpublished_post)
def test_unpublished_post_visible_to_moderator():
    response = moderator_client().get('/post/draft-post/')
    assert response.status_code == 200


@use("db")
@use(moderator_client, unpublished_post)
def test_post_list_shows_unpublished_to_moderator():
    response = moderator_client().get('/')
    assert b'Draft Post' in response.content


@use("db")
@use(client, unpublished_post)
def test_post_list_hides_unpublished_from_anonymous():
    response = client().get('/')
    assert b'Draft Post' not in response.content
```

- [ ] **Step 7: Run full test suite**

```bash
uv run pytest posts/tests/ -v
```

Expected: All 11 tests pass.

- [ ] **Step 8: Commit**

```bash
git add posts/tests/
git commit -m "refactor: migrate tests to pytest-unmagic, add moderator view tests"
```

---

## Task 8: Update license headers

Source files reference "GNU General Public License" but `COPYING` is
AGPL-3.0. Make consistent.

**Files:**
- Modify: all `.py` files and `.js`/`.html` files with license headers

- [ ] **Step 1: Update Python file headers**

In every `.py` file under `posts/` and `standalone/` that contains
the text `GNU General Public License`, replace:

```
# onepageblog is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
```

with:

```
# onepageblog is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
```

And replace `GNU General Public License` with
`GNU Affero General Public License` in the "see" URL lines as well.

- [ ] **Step 2: Update HTML template headers**

Same replacement in every `.html` template file under
`posts/templates/`, inside `{% comment %}` blocks.

- [ ] **Step 3: Verify no remaining references to non-AGPL**

```bash
grep -r "GNU General Public License" posts/ standalone/ --include='*.py' --include='*.html'
```

Expected: No output (all replaced with "GNU Affero General Public
License").

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "chore: fix license headers to reference AGPL-3.0 per COPYING"
```

---

## Task 9: Update documentation

Update `CLAUDE.md` and `CONTRIBUTING.md` to reflect the refreshed
state.

**Files:**
- Modify: `CLAUDE.md`
- Modify: `CONTRIBUTING.md`

- [ ] **Step 1: Update CLAUDE.md**

Rewrite `CLAUDE.md` to reflect the post-refresh state:

- Structure table: remove mention of `requirements.txt` from
  `standalone/` description.
- Commands: use `uv run` for pytest, keep `./manage-dev` for Django
  commands.
- Environment variables: remove `DISQUS_SHORTNAME` row.
- Key patterns: update AJAX loading to mention HTMX + Alpine.js
  instead of jQuery/`onepageblog.js`.
- Remove the "Known tech debt (pre-refresh)" section entirely.

- [ ] **Step 2: Update CONTRIBUTING.md**

- Development setup: replace `pip install -r standalone/requirements.txt`
  with `uv sync`.
- Running tests: simplify to `uv run pytest posts/tests/`.
- Add note that HTMX and Alpine.js are loaded via CDN in `base.html`
  (no npm/node needed).

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md CONTRIBUTING.md
git commit -m "docs: update CLAUDE.md and CONTRIBUTING.md for post-refresh state"
```
