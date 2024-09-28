# Muffasa Programming Language Interpreter

Muffasa is a custom-built programming language interpreter that supports various features, including custom data structures, string manipulation, arithmetic operations and more. This README will guide you through the rules and features of the language, how to use the interpreter, and provide examples of usage.

## Table of Contents
- [Language Rules](#language-rules)
- [Features](#features)
- [Example](#example)
- [Contributing](#contributing)


## Language Rules

### 1. **Identifiers and Keywords**
   - Identifiers (e.g., variable names) must start with a letter and can include letters, numbers, and underscores.
   - Reserved keywords include: `if`, `else`, `while`, `for`, `True`, `False`, `Shmuple`, `StringBeans`, `Arrays`, etc.
   - Identifiers are case-sensitive.

### 2. **Data Types**
   - **Numbers**: Supports integers and floating-point numbers. Negative numbers are allowed.
   - **Strings**: Enclosed in double quotes (`" "`). Strings can also be used as comments when placed alone on a line.
   - **Booleans**: Uses `True` and `False`.

### 3. **Operators**

- **Arithmetic**:
  - `+`: Addition (Implemented by the `Add` function in `mathforlanguage`)
  - `-`: Subtraction (Implemented by the `Subtract` function in `mathforlanguage`)
  - `*`: Multiplication (Implemented by the `Multiply` function in `mathforlanguage`)
  - `/`: Division (Implemented by the `Divide` function in `mathforlanguage`)
  - `^`: Exponentiation (Implemented by the `Pow` function in `mathforlanguage`)

- **Comparison**:
  - `==`: Equal to (Implemented by the `Equal` function in `mathforlanguage`)
  - `!=`: Not equal to (Implemented by the `notEqual` function in `mathforlanguage`)
  - `<`: Less than (Implemented by the `less` function in `mathforlanguage`)
  - `>`: Greater than (Implemented by the `greater` function in `mathforlanguage`)

- **Logical**:
  - `&&`: Logical AND (Implemented by the `And` function in `mathforlanguage`)
  - `||`: Logical OR (Implemented by the `Or` function in `mathforlanguage`)

- **Assignment**:
  - `=`: Assignment (Handled by the `assign` function in `mathforlanguage`)



### 4. **Control Structures**
   - **Conditional Statements**:
     - `if` conditionals, optionally followed by `else`. No support for `else-if`.
   - **Loops**:
     - `while` and `for` loops.
     - Supports `break` to exit loops and `continue` to skip to the next iteration.

### 5. **Custom Data Structures**

- **Shmuple**:
  - A custom tuple-like structure.
  - **Methods**:
    - `sortuple`: Sorts the elements in the Shmuple and returns a new sorted Shmuple.
    - `Add`: Combines two Shmuples into one.
    - `getitem`: Retrieves an item at a specific index.
    - `Index`: Finds the index of a specific item.
    - `Length`: Returns the number of elements in the Shmuple.

- **Arrays**:
  - A custom array structure.
  - **Methods**:
    - `add`: Adds an element to the end of the array.
    - `insert`: Inserts an element at a specific index in the array.
    - `at`: Return an element at a given index.
    - `remove`: Removes an element from the array at a specific index.
    - `length`: Returns the size of the array.
    - `display`: Displays the contents of the array.
    - `check_index`: Checks if an index is within the range of the array.

- **StringBeans**:
  - A custom string manipulation class.
  - **Methods**:
    - `Replace`: Replaces all instances of a substring with another substring.
    - `allUpper`: Checks if all characters in the string are uppercase.
    - `allLower`: Checks if all characters in the string are lowercase.
    - `Conjoin`: Concatenates the string with another string.
    - `show`: Displays the string.
    - `splitBeans`: Returns a Array of StringBeans that were separated by given String.



### 6. **Functions**
   - **Mathematical Functions**:
     - `min(a, b)`: Returns the minimum of `a` and `b`.
     - `max(a, b)`: Returns the maximum of `a` and `b`.
     - `squareRoot(x)`: Returns the square root of `x`.

### 7. **Comments**
   - Strings can serve as comments if placed alone on a line, e.g., `"This is a comment"`.

### 8. **End of Statement**
   - Statements are terminated by the tilde (`~`) or semicolon (`;`) symbol.

### 9. **Program Termination**
   - Programs can be explicitly terminated using the tilde (`~`) symbol at the end of the program.

## Features
### 1. **Lexer**
The Lexer (Lexical Analyzer) is responsible for converting the source code written in the Muffasa language into a series of tokens. Tokens are the smallest units of meaning, such as keywords, operators, identifiers, and literals (numbers, strings, etc.).

- **Implementation**: The Lexer processes the input string character by character, grouping sequences of characters into tokens. It handles various token types, such as:
  - **Identifiers** (e.g., variable names)
  - **Keywords** (`if`, `else`, `while`, etc.)
  - **Operators** (`+`, `-`, `*`, `/`, `==`, etc.)
  - **Literals** (numbers, strings)
  - **Punctuation** (parentheses, braces, semicolons, etc.)

### 2. **Parser**
The Parser takes the tokens generated by the Lexer and organizes them into an Abstract Syntax Tree (AST). The AST is a tree-like structure that represents the grammatical structure of the source code.

- **Implementation**: The Parser follows the rules of the Muffasa language's grammar to build the AST. It ensures that expressions, control structures, and other constructs are properly formed. For instance:
  - For an if statement node, the Interpreter evaluates the condition. If the condition is True, it executes the subtree corresponding to the if branch. If the condition is False, it skips this branch, or, if an else branch exists, it executes the statements in the else subtree.
  - A `while` loop node will have a condition node and a body node.

The AST is a simplified version of the program that the Interpreter can easily execute.

### 3. **Interpreter**
The Interpreter traverses the AST generated by the Parser and executes the program. It evaluates expressions, executes statements, and manages the program's state (variables and control flow).

- **Implementation**: The Interpreter processes the AST by executing functions associated with the custom classes defined in mathforlanguage.py. Depending on the type of node, it may perform arithmetic calculations, logical comparisons, or execute control structures (loops, conditionals). Key components include:
  - **Evaluation of Expressions**: Arithmetic and logical operations are implemented using custom functions like `Add`, `Subtract`, `Equal`, `And`, etc., defined in the `mathforlanguage` module.
  - **Control Flow**: The Interpreter handles `if` statements, `while` loops, and `for` loops by conditionally executing code based on the evaluated expressions.
  - **Variable Management**: Variables are stored in a symbol table or environment, allowing the Interpreter to track and update variable values throughout execution. Variables defined within control structures such as `if`, `for` and `while` loops are contained within those blocks and are deleted as soon as the block ends, unless the variable was created before entering the block, in which case it persists.

### 4. **Error Handling**
The Muffasa interpreter includes mechanisms for handling errors at various stages of interpretation:
- **Lexical Errors**: Detected during tokenization by the Lexer (e.g., unrecognized characters).
- **Syntax Errors**: Identified by the Parser when the structure of the code doesn't conform to the language's grammar (e.g., missing parentheses).
- **Runtime Errors**: Caught by the Interpreter when executing operations that fail (e.g., division by zero, undefined variables).


## Example
      x = 520156~
      y = 3~
      if (x != 5)
      {
         z = x + y~
      }
      else
      {
         p = x - y~
      }

      while (y < 10)
      {
         y = y + 1~
         q = 5~
      }
      for (i = 1; i < 10 ; i = i + 1)
      {
         y = y + i~
         p = y~
      }
      
      l = y < x;
      n = z > y;
      c =  l && n;
      e = False;
      f = True;
      t = e || f;

## Contributing
   Name: Lidor Tubul
