# Roadmap

The Django 2.2 → 5.2 refresh is complete. This document records what
comes next.


## Tests: reduce duplication

The `user` fixture is defined twice — once in `posts/tests/fixtures.py`
and again identically in `posts/tests/test_models.py`. The model tests
should import it from `fixtures.py` rather than redefining it.

Similarly, `posts_triple` creates its own user inline rather than
composing the shared `user` fixture, and `moderator_client` in
`test_views.py` creates yet another user independently. Pulling these
together would mean any change to how test users are created only
needs to happen in one place.

Concrete changes:

- Remove `user` fixture from `test_models.py`; import it from
  `fixtures.py`.
- Rewrite `posts_triple` to compose the shared `user` fixture via
  `@use(user)` (and import `user` from `fixtures.py`).
- Move `moderator_client` and `unpublished_post` from `test_views.py`
  into `fixtures.py` so they can be shared if further view tests are
  added. `moderator_client` should compose `user` or create its own
  user — currently `moderator_client` creates a `mod` user and
  `unpublished_post` creates a `draftauthor` user; that's fine, but
  both should be defined alongside the other shared fixtures.


## Views: duplicated moderator check

`PostListView.get_queryset()` and `PostDetailView.get_queryset()` are
identical — both check `request.user.groups.filter(name='Moderators')`
and return either all posts or only published ones. Extract a helper:

```python
def _is_moderator(user):
    return (
        user.is_authenticated and
        user.groups.filter(name='Moderators').exists()
    )
```

The `hasattr(self.request, 'user')` guard is also unnecessary — Django's
`AuthenticationMiddleware` guarantees `request.user` is always set.
Remove it from both views.

Use `.exists()` instead of `.count() > 0` — it short-circuits and is
the idiomatic Django form.


## Model: minor cleanups

- The `get_sentinel_user` docstring URL references Django 2.1; update
  to current docs or remove the comment.
- The inline comment `# Convert Markdown to safe HTML. Enable extra
  features. Escape tags.` mentions "Escape tags" which is no longer
  true (safe_mode was removed). Remove the stale comment.
- The slug regex `'(.+?)(?:-\d+)?$'` uses an unescaped backslash
  (`\d`) in a plain string — use a raw string: `r'(.+?)(?:-\d+)?$'`.
- The `TODO` comment about `comments_enabled` has been there since the
  original codebase and has no plan behind it. Remove it.


## URLs: minor cleanups

- `admin.autodiscover()` is called unconditionally at module level in
  `posts/urls.py`. Django calls it automatically since Django 1.7; the
  explicit call is a no-op. Remove it.
- The `MEDIA_ROOT` debug-serve block references `settings.MEDIA_ROOT`
  which is never set, so this would error if triggered. Remove it
  (media files are not a feature of this app).


## Forms: unused import

`posts/forms.py` imports `slugify` from `django.template.defaultfilters`
but never uses it. Remove the import.


## Settings: use `pathlib`

`standalone/settings.py` uses `os.path.dirname(os.path.dirname(__file__))`
for `BASE_DIR`. The modern idiom is:

```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
```

This also makes `STATIC_ROOT` cleaner:
```python
STATIC_ROOT = BASE_DIR / 'standalone' / 'static'
```


## `edit_profile` view: bug

`edit_profile` calls `form.save(commit=False)` but never calls
`form.instance.save()` or `form.save_m2m()` afterwards, so profile
changes are never actually persisted. Fix:

```python
if form.is_valid():
    form.save()
    return HttpResponseRedirect(reverse('post_list_view'))
```
