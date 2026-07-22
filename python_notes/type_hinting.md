# Type Hinting
---

## Why use type hinting?

As python is a dynamic typed language, type hinting is used to inform other developers which variable stores which data type.

## How to type hint?

```python

# Use a colon and add data type
name : str = "Abdullah"

# Stating what a function returns
def myfunction(myparameter : int) -> str:
    return f"{myparameter}"

# Multiple data types (can be either)
data : int | str = "123"

# list
names : list[str] = ["Muhammad", "Abdullah"]

# dictionary
scores : dict[str, float] = {"math": 95.5}

# Not limiting any data type
my_var : any = True
```

## All data types:

1. int (integer)
2. float
3. complex
4. str (string)
5. list
6. tuple (ordered and immutable )
7. range (convert a number to a iterable object)
8. dict
9. set (a mutable collection of unique items)
10. frozenset (immutable collection of items)
11. bool (boolean)
12. bytes (immutable array of bytes)
13. bytearray (mutable version of a bytes)
14. memoryview (access the internal data of an object that supports the buffer protocol)
15. NoneType
16. Any