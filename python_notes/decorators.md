# Decorators

---

## What is a decorator?

> A function that wraps another function to extend its behaviour **without changing the original function's code**

Common uses:

- Logging when a function runs
- Measuring how long a function takes
- Checking permissions before a function runs
- Reusing the same setup/teardown logic

You will also see built-in decorators in Python and in OOP notes, such as `@staticmethod`, `@classmethod`, and `@property`.

---

## How `@` works

The `@` syntax is shorthand. These two versions do the same thing:

```python
def greet():
    print("Hello!")

# long form
greet = decorator_name(greet)

# short form (preferred)
@decorator_name
def greet():
    print("Hello!")
```

When Python sees `@decorator_name` above a function, it:

1. Defines the function
2. Passes that function into `decorator_name`
3. Replaces the function name with whatever the decorator returns (usually a wrapper)

---

## Basic decorator

```python
def shout(func):
    def wrapper():
        print("--- before ---")
        func()
        print("--- after ---")
    return wrapper

@shout
def greet():
    print("Hello!")

greet()
# --- before ---
# Hello!
# --- after ---
```

The decorator runs extra code **around** the original function.

---

## Functions with arguments

If the wrapped function takes arguments, the wrapper must accept and pass them through using `*args` and `**kwargs`:

```python
def shout(func):
    def wrapper(*args, **kwargs):
        print("--- before ---")
        result = func(*args, **kwargs)
        print("--- after ---")
        return result
    return wrapper

@shout
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")
```

Without `*args` and `**kwargs`, calling `greet("Alice")` would fail because `wrapper()` takes no arguments.

---

## Preserve the original function name (`functools.wraps`)

A wrapper replaces the original function. Without `@wraps`, tools like `help()` may show the wrapper's name instead of the real function:

```python
from functools import wraps

def shout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("--- before ---")
        return func(*args, **kwargs)
    return wrapper

@shout
def greet(name):
    """Says hello to someone."""
    print(f"Hello, {name}!")

print(greet.__name__)  # greet (not wrapper)
print(greet.__doc__)   # Says hello to someone.
```

**Always use `@wraps(func)` inside custom decorators** — it is a small habit that saves confusion later.

---

## Practical example: timing a function

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timer
def slow_task():
    time.sleep(1)
    return "done"

slow_task()
```

---

## Practical example: logging

```python
from functools import wraps

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, 3)
```

---

## Decorators with their own arguments

Sometimes the decorator itself needs settings. That requires **one extra nested function**:

```python
from functools import wraps

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hi():
    print("Hi!")

say_hi()
# Hi!
# Hi!
# Hi!
```

Pattern:

```text
@decorator(arg)
def func():
    pass

# is roughly equivalent to:
func = decorator(arg)(func)
```

---

## Stacking decorators

You can apply more than one decorator. They run **from bottom to top** (closest to the function first):

```python
@decorator_a
@decorator_b
def func():
    pass

# same as:
func = decorator_a(decorator_b(func))
```

```python
from functools import wraps

def bold(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"**{result}**"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"*{result}*"
    return wrapper

@bold
@italic
def greet(name):
    return name

print(greet("Alice"))  # **Alice**  (italic runs first, then bold)
```

---

## Quick reference

| Concept | Remember |
|---------|----------|
| Decorator | A function that takes a function and returns a new function |
| `@decorator` | Syntactic sugar for `func = decorator(func)` |
| `wrapper(*args, **kwargs)` | Passes arguments through to the original function |
| `@wraps(func)` | Keeps the original function's name and docstring |
| Decorator with args | Three levels: outer (args) → decorator (func) → wrapper |
| Multiple decorators | Applied bottom-up, closest to the function first |

---

## Common mistakes

1. **Forgetting to `return wrapper`** — the decorator must return the wrapper function, not call it
2. **Forgetting `*args, **kwargs`** — breaks functions that take arguments
3. **Forgetting `@wraps`** — debugging and `help()` become harder
4. **Calling the wrapper at definition time** — use `return wrapper`, not `return wrapper()`

```python
# wrong
def bad_decorator(func):
    def wrapper():
        func()
    return wrapper()  # calls wrapper immediately — don't do this

# correct
def good_decorator(func):
    def wrapper():
        func()
    return wrapper
```
