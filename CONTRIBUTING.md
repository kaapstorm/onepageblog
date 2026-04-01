# Contributing to onepageblog

## Principles

**Simplicity above all.** This is a small codebase and should stay that
way. Prefer the straightforward solution. Avoid abstractions,
indirection, or dependencies unless they earn their keep.

## Development setup

```bash
# Create and activate a virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r standalone/requirements.txt

# Run migrations
./manage-dev migrate

# Run the dev server
./manage-dev runserver
```

## Running tests

```bash
DJANGO_SETTINGS_MODULE=standalone.settings \
  DEPLOY_ENV=dev \
  SECRET_KEY=x \
  ALLOWED_HOSTS=localhost \
  DATABASE_URL='sqlite:///standalone/sqlite3.db' \
  pytest posts/tests/
```

## Testing conventions

Tests use **pytest** with **pytest-unmagic**.

pytest-unmagic replaces pytest's implicit fixture injection with
explicit Python imports. Fixtures are defined with `@fixture` (from
`unmagic`), applied to tests with `@use`, and called explicitly to get
their value. This makes dependencies visible and lets IDE navigation
work naturally.

### Writing a fixture

```python
from unmagic import fixture

@fixture
def my_post():
    post = Post(title="Test")
    post.save()
    yield post
    post.delete()
```

### Using a fixture in a test

```python
from unmagic import use
from posts.tests.fixtures import my_post

@use(my_post)
def test_post_title():
    post = my_post()
    assert post.title == "Test"
```

### Key rules

- **Import fixtures explicitly.** No magic name-matching. If a test
  uses a fixture, it imports it.
- **Apply with `@use`.** Decorate the test (or class) with `@use(fix)`
  to activate setup/teardown.
- **Call to get the value.** Inside the test body, call `fix()` to get
  the fixture's return value.
- **Compose fixtures.** To use one fixture inside another, put `@use`
  before `@fixture`:
  ```python
  @use(database)
  @fixture
  def populated_db():
      db = database()
      db.insert(seed_data)
      yield db
  ```
- **Access pytest built-ins by name.** For things like `tmp_path` or
  the pytest-django `db` marker:
  ```python
  from unmagic import use

  @use("db")
  def test_django_query():
      ...
  ```

## Code style

- Keep it simple. No premature abstractions.
- Follow existing patterns in the codebase.
- License: AGPL-3.0 (see `COPYING`).
