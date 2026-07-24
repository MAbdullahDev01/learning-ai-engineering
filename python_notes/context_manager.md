# Context Managers

---

## What is a context manager?

> An object that defines setup and teardown logic around a block of code, so resources are acquired and released reliably

Common uses:

- Opening and closing files
- Acquiring and releasing locks
- Starting and stopping timers
- Connecting and disconnecting from a database
- Temporarily changing settings (e.g. working directory, decimal precision)

The `with` statement is Python's built-in way to use a context manager.

---

## The `with` statement

```python
with open("notes.txt", "w") as file:
    file.write("Hello!")
# file is automatically closed here, even if an error occurred inside the block
```

Without a context manager, you would need a `try`/`finally` block to guarantee cleanup:

```python
file = open("notes.txt", "w")
try:
    file.write("Hello!")
finally:
    file.close()
```

The `with` statement is shorter and harder to forget cleanup.

---

## How `with` works

When Python runs a `with` block, it calls two special methods on the context manager:

1. **`__enter__`** — runs at the start (setup)
2. **`__exit__`** — runs at the end (teardown), even if an exception was raised

```text
with context_manager as value:
    # body

# roughly equivalent to:
manager = context_manager
value = manager.__enter__()
try:
    # body
except:
    if not manager.__exit__(*sys.exc_info()):
        raise
else:
    manager.__exit__(None, None, None)
```

The value after `as` is whatever `__enter__` returns. If you omit `as`, `__enter__` still runs — you just do not bind its return value to a name.

---

## Class-based context manager

Implement `__enter__` and `__exit__` on a class:

```python
class Timer:
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        import time
        elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {elapsed:.4f} seconds")
        return False  # do not suppress exceptions

with Timer():
    total = sum(range(1_000_000))
```

### `__exit__` parameters

| Parameter | Meaning |
|-----------|---------|
| `exc_type` | Exception class, or `None` if no error |
| `exc_value` | Exception instance, or `None` |
| `traceback` | Traceback object, or `None` |

If `__exit__` returns `True`, Python **suppresses** the exception (treats it as handled). Returning `False` or `None` lets the exception propagate normally.

```python
class SuppressValueError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return exc_type is ValueError  # suppress only ValueError

with SuppressValueError():
    raise ValueError("this is swallowed")

print("still running")
```

---

## Practical example: managing a file

```python
class ManagedFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
        return False

with ManagedFile("output.txt", "w") as f:
    f.write("Saved safely")
```

Prefer the built-in `open()` in real code — it already is a context manager.

---

## Function-based context manager (`contextlib.contextmanager`)

Instead of a class, you can use a generator with `@contextmanager`:

```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename, mode):
    file = open(filename, mode)
    try:
        yield file          # everything before yield = __enter__
    finally:
        file.close()        # everything after yield = __exit__

with managed_file("output.txt", "w") as f:
    f.write("Saved safely")
```

Pattern:

- Code **before** `yield` = setup (`__enter__`)
- The **yielded value** = what `as` receives
- Code in **`finally` after `yield`** = teardown (`__exit__`)

You cannot suppress exceptions by returning a value from a `@contextmanager` function — use `try`/`except` inside the generator if you need that behaviour.

---

## Practical example: temporary directory change

```python
import os
from contextlib import contextmanager

@contextmanager
def change_dir(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(previous)

with change_dir("/tmp"):
    print(os.getcwd())  # /tmp on Unix

print(os.getcwd())      # back to the original directory
```

---

## Practical example: database-style resource

```python
from contextlib import contextmanager

class Connection:
    def __init__(self, name):
        self.name = name

    def query(self, sql):
        print(f"[{self.name}] Running: {sql}")

@contextmanager
def connect(name):
    print(f"Connecting to {name}...")
    conn = Connection(name)
    try:
        yield conn
    finally:
        print(f"Closing {name}...")

with connect("main_db") as db:
    db.query("SELECT * FROM users")
```

---

## Useful tools in `contextlib`

### `closing`

For objects that have a `.close()` method but no `__enter__`/`__exit__`:

```python
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen("https://example.com")) as response:
    data = response.read()
```

### `suppress`

Ignore specific exceptions inside a block:

```python
from contextlib import suppress
from pathlib import Path

path = Path("maybe_missing.txt")

with suppress(FileNotFoundError):
    path.unlink()
```

### `redirect_stdout` / `redirect_stderr`

Temporarily send output somewhere else:

```python
import io
from contextlib import redirect_stdout

buffer = io.StringIO()

with redirect_stdout(buffer):
    print("hidden from the console")

print(buffer.getvalue())  # hidden from the console\n
```

### Nesting multiple managers

```python
from contextlib import contextmanager

@contextmanager
def tag(label):
    print(f"[{label}] start")
    try:
        yield
    finally:
        print(f"[{label}] end")

with tag("outer"), tag("inner"):
    print("working")
# [outer] start
# [inner] start
# working
# [inner] end
# [outer] end
```

---

## Built-in context managers you already use

| Example | What it manages |
|---------|-----------------|
| `open(...)` | File handles |
| `threading.Lock()` | Lock acquire/release |
| `decimal.localcontext()` | Temporary decimal settings |
| `unittest.mock.patch(...)` | Temporary attribute replacement |
| `tempfile.TemporaryDirectory()` | A folder deleted on exit |

```python
import threading

lock = threading.Lock()

with lock:
    # only one thread runs this block at a time
    pass
```

---

## Quick reference

| Concept | Remember |
|---------|----------|
| Context manager | Defines setup (`__enter__`) and teardown (`__exit__`) |
| `with ... as x` | Calls `__enter__`, binds its return value to `x`, then calls `__exit__` |
| Class-based | Implement `__enter__` and `__exit__` |
| `@contextmanager` | Generator: code before `yield` = enter, `finally` after = exit |
| `__exit__` return `True` | Suppresses the exception raised inside the block |
| `contextlib.suppress` | Ignore specific exceptions without a full `try`/`except` |

---

## Common mistakes

1. **Forgetting cleanup on error** — without `with` or `finally`, an exception can skip your `.close()` call
2. **Using `@contextmanager` without `try`/`finally`** — if an error happens after `yield`, teardown may not run
3. **Returning `True` from `__exit__` by accident** — silently hides bugs
4. **Expecting `__enter__` to receive arguments** — pass data through `__init__` (class) or the decorator's outer function (generator)

```python
# wrong — no guaranteed cleanup if write fails
@contextmanager
def bad_file(name, mode):
    file = open(name, mode)
    yield file
    file.close()

# correct
@contextmanager
def good_file(name, mode):
    file = open(name, mode)
    try:
        yield file
    finally:
        file.close()
```

5. **Reusing a one-shot context manager** — some managers (like an exhausted file iterator) are meant to be used once per `with` block
