# Object Oriented Programming (OOP)

---

## What is an object?

- An object is a bundle of related attributes (variables) and methods (functions)
- Objects can be anything — for example: a phone, cup, or book

## What is a class?

- A blueprint used to design and structure an object

---

## How to create a class?

```python
# header for creating a class
class Car:

    # initialising a class using __init__ with self and any attributes as parameters
    def __init__(self, model: str, year: int, colour: str, for_sale: bool):

        # setting attributes
        self.model = model
        self.year = year
        self.colour = colour
        self.for_sale = for_sale

    # creating a method (must have self as a parameter)
    def drive(self):
        print(f"{self.model} is driving")

    def stop(self):
        print(f"{self.model} stopped")


# creating an object
car1 = Car("BMW M5", 2024, "black", False)

print(car1)  # prints the memory address of the object

# accessing attributes
print(car1.model)

# calling a method
car1.drive()
```

## Class variables and instance variables

> Class variables are shared by every object created from that class

> Instance variables are defined inside the constructor (`__init__`)

```python
class Student:

    class_year: int = 2026       # class variable
    num_of_students: int = 0

    def __init__(self, name: str, age: int):
        self.name = name         # instance variable
        self.age = age
        Student.num_of_students += 1

student1 = Student("Abdullah", 17)
student2 = Student("Muhammad", 18)

print(student1.class_year)       # prints class variable
print(student2.age)              # prints instance variable

# printing a class's class variable
print(Student.class_year)
```

---

## Inheritance

> Allows a class to inherit attributes and methods from another class

Syntax:

```text
class Child(Parent):
```

Example:

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating")

    def sleep(self):
        print(f"{self.name} is sleeping")

class Dog(Animal):
    def speak(self):
        print("Woof!")

dog = Dog("Scooby")
dog.eat()
dog.speak()
```

---

## Multiple and multilevel inheritance

> **Multiple inheritance** — a class inherits from more than one parent class

```text
class Child(Parent1, Parent2):
```

> **Multilevel inheritance** — a class inherits from a parent, which itself inherited from another parent

```text
class Parent1:
    pass

class Parent2(Parent1):
    pass

class Child(Parent2):
    pass

# inheritance chain: Child -> Parent2 -> Parent1
```

Example (multilevel: `Rabbit`/`Hawk`; multiple: `Fish`):

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating")

class Prey(Animal):
    def flee(self):
        print(f"{self.name} is fleeing")

class Predator(Animal):
    def hunt(self):
        print(f"{self.name} is hunting")

class Rabbit(Prey):
    pass

class Hawk(Predator):
    pass

class Fish(Prey, Predator):  # multiple inheritance
    pass

rabbit = Rabbit("Bugs")
hawk = Hawk("Tony")
fish = Fish("Nemo")

rabbit.flee()
rabbit.hunt()  # AttributeError — Rabbit has no hunt method

hawk.hunt()

fish.flee()
fish.hunt()    # Fish inherits from both Prey and Predator

rabbit.eat()
hawk.eat()
fish.eat()
```

---

## Abstract classes

> A class that cannot be instantiated on its own; meant to be subclassed

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):

    @abstractmethod
    def drive(self):
        pass


class Car(Vehicle):

    # all abstract methods must be implemented in the child class
    def drive(self):
        print("Driving the car")

# Vehicle()  # TypeError — cannot instantiate an abstract class
car = Car()
car.drive()
```

Used to enforce that every child class implements the same interface as the parent

---

## `super()` function

> `super()` is used to call methods from the parent class

```python
class Shape:
    def __init__(self, color: str, is_filled: bool):
        self.color = color
        self.is_filled = is_filled

class Circle(Shape):
    def __init__(self, color: str, is_filled: bool, radius: float):
        super().__init__(color, is_filled)
        self.radius = radius

class Square(Shape):
    def __init__(self, color: str, is_filled: bool, width: float):
        super().__init__(color, is_filled)
        self.width = width

class Triangle(Shape):
    def __init__(self, color: str, is_filled: bool, base: float, height: float):
        super().__init__(color, is_filled)
        self.base = base
        self.height = height

circle = Circle("red", True, 5.0)
```

---

## Aggregation

> Classes that are independent of one another, but related (a "has-a" relationship)

```python
class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

library = Library("New York Public Library")

book1 = Book("Harry Potter...", "J.K. Rowling")
book2 = Book("The Hobbit", "J. R. R. Tolkien")

library.add_book(book1)
library.add_book(book2)
# Books exist independently of the library
```

## Composition

> A "has-a" relationship where the parts are created and owned by the parent — they don't exist independently

```python
class Engine:
    def __init__(self, horse_power):
        self.horse_power = horse_power

class Wheel:
    def __init__(self, size):
        self.size = size

class Car:
    def __init__(self, make, model, horse_power, size):
        self.make = make
        self.model = model
        self.engine = Engine(horse_power)              # created inside the class
        self.wheels = [Wheel(size) for _ in range(4)]  # created inside the class
```

---

## Nested classes

```python
class Company:
    class Employee:
        def __init__(self, name, position):
            self.name = name
            self.position = position

    def __init__(self, company_name):
        self.company_name = company_name
        self.employees = []

    def add_employee(self, name, position):
        new_employee = self.Employee(name, position)
        self.employees.append(new_employee)

company = Company("Acme Corp")
company.add_employee("Alice", "Engineer")
```

---

## Static methods

> A method for general utility — does not receive `self` or `cls`

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

MathUtils.add(2, 3)  # call on the class
```

---

## Class methods

> A method bound to the class rather than an instance; receives `cls` as the first argument

```python
class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    @classmethod
    def margherita(cls):
        return cls(["tomato", "mozzarella", "basil"])

pizza = Pizza.margherita()
```

---

## Magic methods (dunder methods)

| Method | Purpose |
|--------|---------|
| `__str__` | Custom string representation when `print(obj)` is called |
| `__eq__` | Custom equality check for `obj1 == obj2` |
| `__lt__` | Less-than comparison for `obj1 < obj2` (used by `sorted()`) |
| `__gt__` | Greater-than comparison for `obj1 > obj2` |
| `__add__` | Custom behaviour for `obj1 + obj2` |
| `__contains__` | Custom behaviour for `item in obj` |
| `__getitem__` | Custom behaviour for `obj[key]` indexing |

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"{self.title} ({self.pages} pages)"

    def __eq__(self, other):
        return self.title == other.title and self.pages == other.pages

book = Book("1984", 328)
print(book)  # 1984 (328 pages)
```

---

## `@property`

> Decorator used to define a method as an attribute-like property, with optional getter, setter, and deleter

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @radius.deleter
    def radius(self):
        del self._radius

circle = Circle(5)
print(circle.radius)  # getter — no parentheses needed
circle.radius = 10    # setter
```
