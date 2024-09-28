from mathforlanguage import mathforlenguage, StringBeans, Arrays, Shmuple

"""
Muffasa Programming Language Interpreter

This module implements the Muffasa programming language interpreter, including a lexer, parser, and interpreter.
The language supports basic arithmetic operations, variable assignments, conditional statements, loops,
and custom data structures like Shmuple, Arrays, and StringBeans.

Classes:
    Lexer: converts source code into tokens.
    Parser: converts tokens into an abstract syntax tree.
    Interpreter: executes the AST to run the program.

Author: Lidor Tubul

Date: 20.08.2024

Version: 1.0
"""


# Lexer: Converts code into tokens for parsing
class Lexer:
    """
    the lexer class is responsible for converting a string of code into a list of tokens
    that the parser can use to generate the abstract syntax tree

    attributes:
        code (str): source code to be tokenized
        position (int): current location of char in the source code
    """

    def __init__(self, code: str):
        """
        initialize the lexer with a given source code

        parameter:
            code (str): source code to be tokenized
        """
        self.code = code
        self.position = 0

    def get_next_char(self):
        """
        return the next character in the code or None if the end of the code is reached

        return:
            char (str or None): the next character in the source code or None if at the end
        """
        if self.position >= len(self.code):
            return None
        char = self.code[self.position]
        self.position += 1
        return char

    def tokenize(self):
        """
        convert the source code into a list of tokens

        returns:
            list: a list of tuples, where each tuple represents a token in the format (token_type, token_value)

        raise:
            RuntimeError: if an unexpected character is not recognized during tokenization
        """
        tokens = []
        while (char := self.get_next_char()) is not None:
            if char.isspace():
                continue  # skip whitespace
            elif char.isalpha():  # identifiers and keywords
                start = self.position - 1
                while (char := self.get_next_char()) is not None and (char.isalnum() or char == '_'):
                    continue
                self.position -= 1
                value = self.code[start:self.position]
                if value in ['squareRoot', 'min', 'max']:
                    tokens.append(('FUNC', value))
                elif value in {'True', 'False'}:
                    tokens.append(('BOOL', value))
                elif value == 'if':
                    tokens.append(("IF", value))
                elif value == 'else':
                    tokens.append(("ELSE", value))
                elif value in {'while', "for"}:
                    tokens.append(("LOOP", value))
                elif value == 'break':
                    tokens.append(("Terminate", value))
                elif value == 'continue':
                    tokens.append(("Continue", value))
                elif value in {'Shmuple', 'StringBeans', 'Arrays'}:
                    tokens.append(("Class", value))
                else:
                    tokens.append(('ID', value))  # identifiers (variable names, function names, etc.)
            elif char.isdigit() or (char == '-' and
                                    self.position < len(self.code) and self.code[self.position].isdigit()):  # Numbers
                start = self.position - 1
                while (char := self.get_next_char()) is not None and (char.isdigit() or char == '.'):
                    continue
                self.position -= 1
                tokens.append(('NUMBER', self.code[start:self.position]))
            elif char == '"':  # string literals
                start = self.position
                while (char := self.get_next_char()) != '"':
                    if char is None:
                        raise RuntimeError('Unterminated string literal')
                tokens.append(('CHAR', self.code[start:self.position]))
            elif char in '+-*/=<>!&|(){}^;,~':  # operators and symbols
                if char == '^':
                    tokens.append(('OP', '^'))
                elif char == '=':
                    if self.get_next_char() == '=':
                        tokens.append(('OP', '=='))
                    else:
                        self.position -= 1
                        tokens.append(('ASSIGN', '='))
                elif char == '!':  # check for '!='
                    if self.get_next_char() == '=':
                        tokens.append(('OP', '!='))
                    else:
                        raise RuntimeError(f'Unexpected character {char!r} in char number: {self.position}')
                elif char == '&':
                    if self.get_next_char() == '&':
                        tokens.append(('OP', '&&'))
                    else:
                        raise RuntimeError(f'Unexpected character {char!r} in char number: {self.position}')
                elif char == '|':
                    if self.get_next_char() == '|':
                        tokens.append(('OP', '||'))
                    else:
                        raise RuntimeError(f'Unexpected character {char!r} in char number: {self.position}')
                elif char in '+-*/':
                    tokens.append(('OP', char))
                elif char in '<>':
                    tokens.append(('OP', char))
                elif char in '(){}':
                    tokens.append(('OP', char))
                elif char == ',':
                    tokens.append(('COMMA', ','))
                elif char == '~':
                    tokens.append(('END', '~'))
                elif char == ';':
                    tokens.append(('SEMICOLON', ';'))
                else:
                    raise RuntimeError(f'Unexpected character {char!r} in char number: {self.position}')
            elif char == '.':  # dot operator
                tokens.append(('DOT', '.'))
            else:
                raise RuntimeError(f'Unexpected character {char!r} in char number: {self.position}')
        return tokens


class Parser:
    """
    the parser class is responsible for converting a list of tokens into an abstract syntax tree that
    represents the structure of the source code

    attributes:
        tokens (list of tuples): list of tokens generated by the lexer
        position (int): current position in the list of tokens
        tokenSize (int): size of the tokens generated by the lexer
    """
    def __init__(self, tokens: list):
        """
        initialize parser with a list of tokens

        parameter:
            tokens (list of tuples): list of tokens to be parsed
        """
        self.tokens = tokens
        self.position = 0
        self.tokenSize = len(tokens)

    def current_token(self):
        """
        return current token in the list of tokens.

        return:
            token (tuple or None): current token as a tuple (token_type, token_value) or None if reached to the end
        """
        return self.tokens[self.position] if self.position < self.tokenSize else None

    def consume(self, expected_type):
        """
        consume a current token if it matched the expected type and goes to the next token

        parameter:
            expected_type (str): expected type of the current token

        return:
            token_value (str): value of the token

        raise:
            RuntimeError: if the current token does not match the expected type
        """
        token = self.current_token()
        if token and token[0] == expected_type:
            self.position += 1
            return token[1]
        raise RuntimeError(f'Expected {expected_type} but got {token} in position number {self.position}')

    def parse(self):
        """
        parse the list of tokens into abstract syntax tree

        return:
            ast (list): a list of parsed statements, each represented as a tuple
        """
        ast = []
        while self.position < self.tokenSize:
            ast.append(self.parse_statement())
        return ast

    def parse_statement(self):
        """
        parse a single statement from the current position in the token list

        return:
            tuple: tuple representing the parsed statement

        raise:
            RuntimeError: if unexpected token found or if the statement isn't terminated properly
        """
        token = self.current_token()
        if token[0] == 'CHAR':  # handle string literals (comments)
            self.consume('CHAR')
            return 'COMMENT', token[1]  # return comments as a special type of statement
        elif token[0] == 'Terminate':  # handle break statements
            self.consume('Terminate')
            if self.current_token() and self.current_token()[0] in ['END', 'SEMICOLON']:
                self.consume(self.current_token()[0])
            return ('BREAK',)
        elif token[0] == 'Continue':  # handle continue statements
            self.consume('Continue')
            if self.current_token() and self.current_token()[0] in ['END', 'SEMICOLON']:
                self.consume(self.current_token()[0])
            return ('CONTINUE',)
        elif token[0] == 'ID':
            var_name = self.consume('ID')
            if self.current_token()[0] == 'ASSIGN':
                self.consume('ASSIGN')
                expr = self.parse_expression()
                if self.current_token() and self.current_token()[0] in ['END', 'SEMICOLON']:
                    self.consume(self.current_token()[0])
                else:
                    raise RuntimeError(f"Expected '~' or ';' at the end of statement, got {self.current_token()}")
                return 'ASSIGN', var_name, expr
            elif self.current_token()[0] == 'DOT':
                method_call = self.parse_method_call(var_name)
                if self.current_token() and self.current_token()[0] in ['END', 'SEMICOLON']:
                    self.consume(self.current_token()[0])
                else:
                    raise RuntimeError(f"Expected '~' or ';' at the end of statement, got {self.current_token()}")
                return method_call
            else:
                expr = self.parse_expression()
                if self.current_token() and self.current_token()[0] in ['END', 'SEMICOLON']:
                    self.consume(self.current_token()[0])
                else:
                    raise RuntimeError(f"Expected '~' or ';' at the end of statement, got {self.current_token()}")
                return expr
        elif token[0] == 'IF':
            return self.parse_if_statement()
        elif token[0] == 'LOOP':
            if token[1] == 'while':
                return self.parse_while_statement()
            elif token[1] == 'for':
                return self.parse_for_statement()
        else:
            expr = self.parse_expression()
            if self.current_token() and self.current_token()[0] in ['END', 'SEMICOLON']:
                self.consume(self.current_token()[0])
            else:
                raise RuntimeError(f"Expected '~' or ';' at the end of statement, got {self.current_token()}")
            return expr

    def parse_expression(self):
        """
        parse expression that can be a combination of terms and operators

        return:
            tuple: tuple representing the parsed expression
        """
        left = self.parse_term()
        while self.current_token() and self.current_token()[0] == 'OP' and self.current_token()[1] in ['+', '-', '<',
                                                                                                       '>', '==', '!=',
                                                                                                       '&&', '||']:
            op = self.consume('OP')
            right = self.parse_term()
            left = (op, left, right)
        return left

    def parse_term(self):
        """
        parse a term that can be a combination of factors and operators

        return:
            tuple: tuple representing the parsed term
        """
        left = self.parse_factor()
        while self.current_token() and self.current_token()[0] == 'OP' and self.current_token()[1] in ['*', '/', '^']:
            op = self.consume('OP')
            right = self.parse_factor()
            left = (op, left, right)
        return left

    def parse_factor(self):
        """
        parse factor that can be a number, boolean, identifier, function call or nested expression

        return:
            tuple: tuple representing the parsed factor

        Raise:
            RuntimeError: if reached to unexpected token
        """
        if self.current_token()[0] == 'NUMBER':
            return 'NUMBER', self.consume('NUMBER')
        elif self.current_token()[0] == 'BOOL':
            return 'BOOL', self.consume('BOOL')
        elif self.current_token()[0] == 'ID':
            return self.parse_id_or_call()
        elif self.current_token()[0] == 'OP' and self.current_token()[1] == '(':
            self.consume('OP')
            expr = self.parse_expression()
            self.consume('OP')
            return expr
        elif self.current_token()[0] == 'Class':
            return self.parse_class_instantiation()
        elif self.current_token()[0] == 'CHAR':
            return 'CHAR', self.consume('CHAR')
        elif self.current_token()[0] == 'FUNC':
            return self.parse_function_call()  # could have pass current_token()[1] if I want to pass arg into func
        else:
            raise RuntimeError(f"Unexpected token {self.current_token()} in parse_factor")

    def parse_id_or_call(self):
        """
        parse identifier that could be a variable or a function call

        return:
            tuple: tuple representing either identifier or a function call
        """
        var_name = self.consume('ID')
        if self.current_token()[0] == 'OP' and self.current_token()[1] == '(':
            return self.parse_function_call()  # var_name to func
        elif self.current_token()[0] == 'DOT':
            return self.parse_method_call(var_name)
        return 'ID', var_name

    def parse_function_call(self):
        """
        parse a function call including its arguments

        return:
            tuple: tuple representing the function call including the function name and its arguments
        """
        func_name = self.consume('FUNC')
        self.consume('OP')  # '('
        args = []
        if self.current_token()[0] != 'OP' or self.current_token()[1] != ')':
            args.append(self.parse_expression())
            while self.current_token() and self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
                args.append(self.parse_expression())
        self.consume('OP')  # ')'
        return 'CALL', func_name, args

    def parse_method_call(self, obj_name):
        """
        parse a method call on an object including its arguments

        parameter:
            obj_name (str): name of the object on which the method is called

        return:
            tuple: tuple representing the method call including the object name, method name and arguments
        """
        self.consume('DOT')
        method_name = self.consume('ID')
        self.consume('OP')  # '('
        args = []
        if self.current_token()[0] != 'OP' or self.current_token()[1] != ')':
            args.append(self.parse_expression())
            while self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
                args.append(self.parse_expression())
        self.consume('OP')  # ')'
        return 'METHOD_CALL', obj_name, method_name, args

    def parse_class_instantiation(self):
        """
        parse a class instantiation including its arguments

        return:
            tuple: tuple representing the class instantiation including the class name and its arguments
        """
        class_name = self.consume('Class')
        self.consume('OP')  # '('
        args = []
        if self.current_token()[0] != 'OP' or self.current_token()[1] != ')':
            args.append(self.parse_expression())
            while self.current_token()[0] == 'COMMA':
                self.consume('COMMA')
                args.append(self.parse_expression())
        self.consume('OP')  # ')'
        return 'CLASS_INST', class_name, args

    def parse_bool_statement(self):
        """
        parse a boolean statement from the tokens

        return:
            bool_statement (tuple): tuple representing the parsed boolean statement
        """
        bool_expr = self.parse_expression()
        return 'BOOL', bool_expr

    def parse_if_statement(self):
        """
        parse if statement including the condition, if-body, and optional else-body
        handle both cases of if (alone) and if-else

        return:
            tuple: tuple representing the if statement structure
        """
        self.consume('IF')
        self.consume('OP')  # '('
        condition = self.parse_expression()
        self.consume('OP')  # ')'
        self.consume('OP')  # '{'
        if_body = []
        while self.current_token() and not (self.current_token()[0] == 'OP' and self.current_token()[1] == '}'):
            if_body.append(self.parse_statement())
        self.consume('OP')  # '}'

        if self.current_token() and self.current_token()[0] == 'ELSE':
            self.consume('ELSE')
            self.consume('OP')  # '{'
            else_body = []
            while self.current_token() and not (self.current_token()[0] == 'OP' and self.current_token()[1] == '}'):
                else_body.append(self.parse_statement())
            self.consume('OP')  # '}'
            return 'IF_ELSE', condition, if_body, else_body

        return 'IF', condition, if_body

    def parse_while_statement(self):
        """
        parse a while loop including the condition and loop body

        return:
            tuple: tuple representing the while loop structure
        """
        self.consume('LOOP')  # 'while'
        self.consume('OP')  # '('
        condition = self.parse_expression()
        self.consume('OP')  # ')'
        self.consume('OP')  # '{'
        while_body = []
        while self.current_token() and not (self.current_token()[0] == 'OP' and self.current_token()[1] == '}'):
            stmt = self.parse_statement()
            if stmt is not None:  # This line ensures that comments (which are None) are not added to the body
                while_body.append(stmt)
        self.consume('OP')  # '}'
        return 'WHILE', condition, while_body

    def parse_for_statement(self):
        """
        parse a for loop including initialization, condition, increment and loop body

        return:
            tuple: tuple representing for loop structure
        """
        self.consume('LOOP')  # 'for'
        self.consume('OP')  # '('

        # Parse initialization
        init_var = self.consume('ID')
        self.consume('ASSIGN')
        init_expr = self.parse_expression()
        self.consume('SEMICOLON')

        # Parse condition
        condition = self.parse_expression()
        self.consume('SEMICOLON')

        # Parse increment
        incr_var = self.consume('ID')
        self.consume('ASSIGN')
        incr_expr = self.parse_expression()

        self.consume('OP')  # ')'
        self.consume('OP')  # '{'

        for_body = []
        while self.current_token() and not (self.current_token()[0] == 'OP' and self.current_token()[1] == '}'):
            for_body.append(self.parse_statement())
        self.consume('OP')  # '}'

        init = ('ASSIGN', init_var, init_expr)
        increment = ('ASSIGN', incr_var, incr_expr)
        return 'FOR', init, condition, increment, for_body


class Interpreter:
    """
    the interpreter class is responsible for executing the abstract syntax tree
    generated by the parser. It handles variable assignment, control flow, and
    expression evaluation.

    Attributes:
        variables (dict): stores variable names and their values
        math (mathforlenguage): instance of math operations class
        current_statement: keep track of the statement being executed
    """
    def __init__(self):
        """
        initializes the interpreter with an empty variable dictionary and a
        math operations instances.
        """
        self.variables = {}
        self.math = mathforlenguage()
        self.current_statement = None

    def interpret(self, ast):
        """
        interprets the entire AST by executing each statement in order.

        parameter:
            ast (list): The abstract syntax tree to be interpreted
        """
        for statement in ast:
            if statement is not None:
                self.execute_statement(statement)

    def execute_statement(self, statement):
        """
        Executes a single statment based on its type.

        parameter:
            statement (tuple): a tuple representing the statement to be executed

        Returns:
            the result of the statement execution, if applicable
        """
        self.current_statement = statement
        statement_type = statement[0]
        if statement_type == 'ASSIGN':
            self.execute_assignment(statement)
        elif statement_type == 'IF_ELSE':
            self.execute_if_else(statement)
        elif statement_type == 'WHILE':
            self.execute_while(statement)
        elif statement_type == 'FOR':
            self.execute_for(statement)
        elif statement_type == 'METHOD_CALL':
            return self.execute_method_call(statement)
        elif statement_type == 'CLASS_INST':
            return self.execute_class_instantiation(statement)
        elif statement_type == 'ID':
            var_name = statement[1]
            if var_name not in self.variables:
                raise NameError(f"Name '{var_name}' is not defined")
            return self.variables[var_name]
        elif statement_type == 'BREAK':
            return 'BREAK'
        elif statement_type == 'CONTINUE':
            return 'CONTINUE'
        elif statement_type == 'COMMENT':
            pass  # Do nothing for comments

    def execute_assignment(self, statement):
        """
        executes an assignment statement, storing the value in the variables' dictionary.

        Parameter:
            statement (tuple): the assignment statement to execute

        This method handles different types of assignments
        and variable references.
        """
        _, var_name, expr = statement
        if isinstance(expr, tuple) and expr[0] == 'CLASS_INST':
            value = self.execute_class_instantiation(expr)
        elif isinstance(expr, tuple) and expr[0] == 'ID':
            var_name_expr = expr[1]
            if var_name_expr not in self.variables:
                raise NameError(f"Name '{var_name_expr}' is not defined")
            value = self.variables[var_name_expr]
        else:
            value = self.evaluate_expression(expr)
        if isinstance(value, StringBeans):
            self.variables[var_name] = value.__copy__()
        elif isinstance(value, bool):
            self.variables[var_name] = value
        else:
            self.variables[var_name] = value
        self.math.assign(var_name, value)

    def execute_if_else(self, statement): 
        """
        executes an if-else statement, handling both if and if-else constructs.

        parameter:
            statement (tuple): the if or if-else statement to execute

        this method manages the scope of variables created within the if and else blocks,
        removing them after execution.
        """
        if_variables = set()  # track variables assigned in the if block
        else_variables = set()  # track variables assigned in the else block

        if statement[0] == 'IF':
            _, condition, if_body = statement
            else_body = []
        else:  # IF_ELSE
            _, condition, if_body, else_body = statement

        if self.evaluate_expression(condition):
            for stmt in if_body:
                if isinstance(stmt, tuple) and stmt[0] == 'ASSIGN':
                    var_name = stmt[1]
                    if_variables.add(var_name)
                result = self.execute_statement(stmt)
                if result in ['BREAK', 'CONTINUE']:
                    return result
        else:
            for stmt in else_body:
                if isinstance(stmt, tuple) and stmt[0] == 'ASSIGN':
                    var_name = stmt[1]
                    else_variables.add(var_name)
                result = self.execute_statement(stmt)
                if result in ['BREAK', 'CONTINUE']:
                    return result

        # remove variables assigned in the if block that are not used outside the block
        for var_name in if_variables:
            if var_name not in self.current_statement and var_name not in else_variables:
                del self.variables[var_name]

        # remove variables assigned in the else block that are not used outside the block
        for var_name in else_variables:
            if var_name not in self.current_statement and var_name not in if_variables:
                del self.variables[var_name]

        return None

    def execute_while(self, statement):
        """
        executes a while loop statement.

        parameter:
            statement (tuple): while loop statement to execute

        this method manages the execution of the loop body, handling break and continue
        statements, and removes variables created within the loop after execution.
        """
        _, condition, body = statement
        loop_variables = set()  # track variables created in the loop

        while self.evaluate_expression(condition):
            should_break = False
            should_continue = False
            for stmt in body:
                if isinstance(stmt, tuple):
                    if stmt[0] == 'ASSIGN':
                        var_name = stmt[1]
                        if var_name not in self.variables:
                            loop_variables.add(var_name)
                    elif stmt[0] == 'BREAK':
                        should_break = True
                        break
                    elif stmt[0] == 'CONTINUE':
                        should_continue = True
                        break
                    elif stmt[0] == 'COMMENT':
                        continue  # skip comments
                    elif stmt[0] in ['IF', 'IF_ELSE']:
                        result = self.execute_if_else(stmt)
                        if result == 'BREAK':
                            should_break = True
                            break
                        elif result == 'CONTINUE':
                            should_continue = True
                            break
                        continue
                result = self.execute_statement(stmt)
                if result == 'BREAK':
                    should_break = True
                    break
                elif result == 'CONTINUE':
                    should_continue = True
                    break
            if should_break:
                break
            if should_continue:
                continue

        # remove variables created inside the loop
        for var_name in loop_variables:
            if var_name in self.variables:
                del self.variables[var_name]

    def execute_for(self, statement):
        """
        executes a for loop statement.

        parameter:
            statement (tuple): for a loop statement to execute

        this method manages the execution of the loop body, handling break and continue
        statements and removes variables created within the loop after execution.
        """
        _, init, condition, increment, body = statement
        loop_variables = set()  # Track variables created inside the loop

        # check if the loop counter-variable already exists in the global scope
        loop_counter = init[1]
        loop_counter_exists = loop_counter in self.variables

        self.execute_statement(init)

        while self.evaluate_expression(condition):
            should_break = False
            should_continue = False
            for stmt in body:
                if isinstance(stmt, tuple):
                    if stmt[0] == 'ASSIGN':
                        var_name = stmt[1]
                        if var_name not in self.variables:
                            loop_variables.add(var_name)
                    elif stmt[0] == 'BREAK':
                        should_break = True
                        break
                    elif stmt[0] == 'CONTINUE':
                        should_continue = True
                        break
                    elif stmt[0] in ['IF', 'IF_ELSE']:
                        result = self.execute_if_else(stmt)
                        if result == 'BREAK':
                            should_break = True
                            break
                        elif result == 'CONTINUE':
                            should_continue = True
                            break
                        continue
                result = self.execute_statement(stmt)
                if result == 'BREAK':
                    should_break = True
                    break
                elif result == 'CONTINUE':
                    should_continue = True
                    break

            if should_break:
                break

            # execute the increment statement even if continue was encountered
            self.execute_statement(increment)

            if should_continue:
                continue

        # Remove variables created inside the loop
        for var_name in loop_variables:
            del self.variables[var_name]

        # Remove the loop counter variable if it was created within the loop
        if not loop_counter_exists:
            del self.variables[loop_counter]

    def execute_method_call(self, statement):
        """
        executes a method call.

        parameter:
            statement (tuple): The method call statement to execute

        """
        _, obj_name, method_name, args = statement
        obj = self.variables.get(obj_name)
        if obj is None:
            raise NameError(f"Name '{obj_name}' is not defined")

        method = getattr(obj, method_name, None)
        if method is None:
            raise AttributeError(f"'{type(obj).__name__}' object has no attribute '{method_name}'")

        evaluated_args = [self.evaluate_expression(arg) for arg in args]
        result = method(*evaluated_args)

        if isinstance(self.current_statement, tuple) and self.current_statement[0] == 'ASSIGN':
            var_name = self.current_statement[1]
            self.variables[var_name] = result
        elif method_name == 'display':
            print(f"{obj_name} = {result}")
        elif method_name == 'splitBeans':
            # when splitBeans is called without assignment we'll print the result
            print(f"{result.display()}")

        return result

    def evaluate_expression(self, expr):
        """
        evaluates an expression and returns its value.

        parameter:
            expr: The expression to evaluate

        this method handles various types of expressions, including math
        operations, functions, and variables.
        """
        if isinstance(expr, tuple):
            if expr[0] in {'+', '-', '*', '/', '==', '<', '>', '^', 'CALL', 'METHOD_CALL', '!=', '&&', '||'}:
                if expr[0] == 'CALL':
                    return self.execute_function_call(expr)
                elif expr[0] == 'METHOD_CALL':
                    return self.execute_method_call(expr)
                elif expr[0] in {'&&', '||'}:
                    left = self.to_bool(self.evaluate_expression(expr[1]))
                    right = self.to_bool(self.evaluate_expression(expr[2]))
                    return self.apply_operator(expr[0], left, right)
                else:
                    left = self.evaluate_expression(expr[1])
                    right = self.evaluate_expression(expr[2])
                    return self.apply_operator(expr[0], left, right)
            elif expr[0] == 'ID':
                return self.variables.get(expr[1], 0)
            elif expr[0] == 'NUMBER':
                return int(expr[1])
            elif expr[0] == 'BOOL':
                return expr[1] == 'True'
            elif expr[0] == 'CHAR':
                return expr[1].strip('"')
        return expr

    def to_bool(self, value):
        """
        converts a value to a boolean.

        parameter:
            value: value to convert

        returns:
            bool: boolean representation of the value
        """

        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return bool(value)
        elif isinstance(value, str):
            return value.lower() == 'true'
        else:
            return bool(value)

    def execute_function_call(self, expr):
        """
        executes a function call.

        parameter:
            expr (tuple): The function / class call expression
        """
        _, func_name, args = expr
        if func_name == 'Shmuple':
            return Shmuple(*[self.evaluate_expression(arg) for arg in args])
        elif func_name == 'Arrays':
            return Arrays(self.evaluate_expression(args[0]))
        elif func_name == 'StringBeans':
            return StringBeans(self.evaluate_expression(args[0]))
        elif func_name == 'squareRoot':
            return self.math.squareRoot(self.evaluate_expression(args[0]))
        elif func_name == 'min':
            return self.math.Min(self.evaluate_expression(args[0]), self.evaluate_expression(args[1]))
        elif func_name == 'max':
            return self.math.Max(self.evaluate_expression(args[0]), self.evaluate_expression(args[1]))
        else:
            raise NameError(f"Function '{func_name}' is not defined")

    def execute_class_instantiation(self, statement):
        """
        executes a class instantiation.

        parameter:
            statement (tuple): The class instantiation statement

        this method creates new instances of Shmuple, Arrays, or StringBeans classes.
        """
        _, class_name, args = statement
        evaluated_args = [self.evaluate_expression(arg) for arg in args]
        if class_name == 'Shmuple':
            return Shmuple(*evaluated_args)
        elif class_name == 'Arrays':
            return Arrays(*evaluated_args)
        elif class_name == 'StringBeans':
            return StringBeans(*evaluated_args)
        else:
            raise NameError(f"Class '{class_name}' is not defined")

    def apply_operator(self, op, left, right):
        """
        applies a binary operator to two operands.

        parameters:
            op (str): the operator
            left: the left operand
            right: the right operand

        returns:
            the result of the operation
        """
        if op == '+':
            return self.math.Add(left, right)
        elif op == '-':
            return self.math.Subtract(left, right)
        elif op == '*':
            return self.math.Multiply(left, right)
        elif op == '/':
            return self.math.Divide(left, right)
        elif op == '^':
            return self.math.Pow(left, right)
        elif op == '==':
            return self.math.Equal(left, right)
        elif op == '!=':
            return self.math.notEqual(left, right)
        elif op == '<':
            return self.math.less(left, right)
        elif op == '>':
            return self.math.greater(left, right)
        elif op == '&&':
            return self.math.And(self.to_bool(left), self.to_bool(right))
        elif op == '||':
            return self.math.Or(self.to_bool(left), self.to_bool(right))

    def print_variables(self):
        """
        prints all variables in the current scope.

        displays the contents of the variables, this function only for the project tester
        """
        print("Variables:")
        for var, value in self.variables.items():
            if isinstance(value, Shmuple):
                print(f"{var} = {value}")
            elif isinstance(value, Arrays):
                print(f"{var} = {value.display()}")
            elif isinstance(value, StringBeans):
                print(f"{var} = {value}")
            elif isinstance(value, str):
                print(f"{var} = \"{value}\"")
            else:
                print(f"{var} = {value}")


if __name__ == "__main__":
    # test code
    code1 = """
    "בשפה הזאת אפשר לכתוב הערות כסטרינג רגיל בשורה נפרדת"
    "כאן בדיקה לשמאפל"
    sh = Shmuple(1, 3, 2, 0, -7)~
    sh_sorted = sh.sortuple()~
    sh2 = Shmuple(-8, 6)~
    sh1 = sh.Add(sh2)~
    sh1 = sh1.sortuple()~
    item = sh1.getitem(5)~
    shin = sh1.Index(0)~
    shlen = sh1.Length()~ 
    
    "כאן בדיקה למערכים"
    arr = Arrays(5)~
    arr.add(10)~
    arr.insert(0, "5")~
    arr_len = arr.length()~
    item_arr = arr.at(0)~
    arr.remove(1)~
    arr.display()~
    
    "בדיקה לסטרינגים"
    strb = StringBeans("hello");
    strb.show();
    newstrb = strb;
    strb.Replace("h", "hi");
    strb.show();
    newstrb.show();
    a = newstrb.allUpper();
    b = newstrb.allLower();
    newstrb.Conjoin(" ast");
    
    "קצת פעולות אריתמטיות, תנאים ולולאות בקוד 2"
    c = 5;
    t = 7;
    c = c - t;
    u = 5*2;
    U = t*c;
    "add min max functionality"
    T = min(10, 2)~
    P = max(10, 2)~
    L = squareRoot(100)~
    O = c^4~
    """

    code2 = """
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
    "There is no else-if duo to the fact there was no requirement"
    "need to fix break and comments in loops"
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
    """

    # this code supposed to fail
    code3 = """
    x = 1~
    else
    {
        x = x + 1~
    }
    """

    code4 = """
    str1 = StringBeans("Hello,World,How,Are,You")~
    arr1 = str1.splitBeans(",")~
    arr1.display()~
    
    str2 = StringBeans("This is a test")~
    arr2 = str2.splitBeans(" ")~
    arr2.display()~
    
    "Test splitBeans without assignment"
    str3 = StringBeans("One|Two|Three")~
    str3.splitBeans("|")~
    
    y = 0~
    sum = 0~
    z = 0~
    while (y < 10)
    {
        "comment1"
        y = y + 2~
        sum = sum + 1~
        "comment2"
        if (y > 3)
        {
            p = 400~
        }
        break;
        
    }
    for (i = 4; i < 10 ; i = i + 1)
    {
        y = i + i~
        p = y~
        if(y < 3)
        {
            continue;
        }
        else
        {
            break;
        }
    }
    
"""

    # create interpreter instance
    interpreter = Interpreter()

    # initialize lexer and parser for code1
    lexer1 = Lexer(code1)
    tokens1 = lexer1.tokenize()
    print("Testing code1:")
    print("Tokens:", tokens1)

    parser1 = Parser(tokens1)
    try:
        # parse and interpreter code1
        ast1 = parser1.parse()
        print("AST:", ast1)
        interpreter.interpret(ast1)
        interpreter.print_variables()
    except RuntimeError as e:
        print(f"Error: {e}")

    # initialize lexer and parser for code2
    lexer2 = Lexer(code2)
    tokens2 = lexer2.tokenize()
    print("Testing code2:")
    print("Tokens:", tokens2)

    parser2 = Parser(tokens2)

    # create new interpreter instance for code2
    interpreter2 = Interpreter()
    try:
        # parse and interprit code2
        ast2 = parser2.parse()
        print("AST:", ast2)
        interpreter2.interpret(ast2)
        interpreter2.print_variables()
    except RuntimeError as e:
        print(f"Error: {e}")

    # initialize lexer and parser for code3
    lexer3 = Lexer(code3)
    tokens3 = lexer3.tokenize()
    print("Testing code3:")
    print("Tokens:", tokens3)

    # we did not create interpreter for code3 because parser ment to fail
    parser3 = Parser(tokens3)
    try:
        # attempt to parse code3 (expected to fail)
        ast3 = parser3.parse()
        print("AST:", ast3)
    except RuntimeError as e:
        print(f"Error: {e}")

    # create a new interpreter instance for code4
    int3 = Interpreter()
    lexer4 = Lexer(code4)
    tokens4 = lexer4.tokenize()
    parser4 = Parser(tokens4)
    print("Testing code4:")
    print("Tokens:", tokens4)
    try:
        # parse and interpreter code4
        ast4 = parser4.parse()
        print("AST:", ast4)
        int3.interpret(ast4)
        int3.print_variables()
    except RuntimeError as e:
        print(f"Error: {e}")
