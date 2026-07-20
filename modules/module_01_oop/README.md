# Module 1: Mastering Object-Oriented Python for AI (Classes, Attributes, and Methods)

## Terminology & Concept

In professional AI engineering, Object-Oriented Programming (OOP) is the standard for building reusable components like model wrappers, data loaders, and agent harnesses. Instead of writing scattered functions, we group data and behavior into Classes.

*   **Class:** A blueprint for creating objects. Think of a `"PromptTemplate"` as a class, while a specific `"EmailGeneratorPrompt"` is an **Instance** of that class.
*   **Attributes:** Variables that belong to an object. In AI, these are often **Stateful**, such as an API key, a model temperature, or a conversation history.
*   **Methods:** Functions defined inside a class that describe what the object can do (e.g., `.generate_response()` or `.calculate_tokens()`).
*   **Dunder Methods (Double Underscore):** Special methods like `__init__` (the **Constructor**), which initializes an instance when it is created.
*   **Self:** The first argument of any instance method, representing the specific object instance being operated on. Professionals always use the name `self` by convention.
*   **Inheritance:** The process where a new class (**Subclass**) takes on the attributes and methods of an existing class (**Base Class**). In AI engineering, you will almost always inherit from Pydantic's `BaseModel` to handle data validation automatically.
*   **Pythonic Naming (PEP 8):** Use `CapWords` for Class names and `snake_case` for methods and attributes.

---

## Tiny Exercise

Write a clean, "Pythonic" class for a basic AI agent configuration. This exercise focuses on Type Hinting and the Constructor.

**Task:** Create a class that stores model settings.  
**Requirements:** Use PEP 8 naming and standard Python type hints.

```python
class AgentConfig:
    def __init__(self, model_name: str, temperature: float = 0.7):
        """
        Initialize the agent configuration.
        model_name: The name of the LLM (e.g., 'gpt-4o')
        temperature: Controls randomness (0.0 to 1.0)
        """
        self.model_name = model_name
        self.temperature = temperature

    def describe_settings(self) -> str:
        return f"Model: {self.model_name} | Temp: {self.temperature}"

# Usage
my_config = AgentConfig(model_name="gpt-4o", temperature=0.5)
print(my_config.describe_settings())
```

> **Practice Tip:** Avoid extraneous whitespace inside parentheses and surround top-level class definitions with two blank lines to follow PEP 8 standards.

---

## Milestone Project: The AI Agent Registry

**Goal:** Build a system that manages multiple "Agent" objects, each with unique configurations, using FastAPI and Pydantic.

### System Architecture
*   **Schema Layer:** Define a `BaseModel` (inheriting from Pydantic) to handle the validation of agent metadata (name, role, tools).
*   **Logic Layer:** Create a custom `AIAgent` class that takes a Pydantic model as an attribute and has a method to "simulate" a response.
*   **API Layer:** A FastAPI endpoint that accepts JSON, converts it into an `AIAgent` instance, and returns the result.

### Core Coding Requirements
*   **Strict Typing:** Every attribute in your Pydantic model must have a type hint (e.g., `role: str`, `max_tokens: int`).
*   **Validation:** Use Pydantic's `PositiveInt` or `Field` to ensure the `max_tokens` attribute is never negative.
*   **Method Logic:** Your `AIAgent` class should have a method called `get_full_prompt(self, user_input: str)` that combines a system prompt (stored as an attribute) with the user input.