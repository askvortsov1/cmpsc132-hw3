# HW3
# Due Date: 11/03/2019, 11:59PM
########################################
#
# Team members: Alexander Skvortsov, Vibudh Bhardwaj
# Collaboration Statement: We completed this assignment using only this semester's course materials and official python documentation.
#
########################################
import re


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return "Node({})".format(self.value)

    __repr__ = __str__


# =============================================== Part I ==============================================

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0

    def __str__(self):
        temp = self.top
        out = []
        while temp:
            out.append(str(temp.value))
            temp = temp.next
        out = '\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top, out))

    __repr__ = __str__

    def isEmpty(self):
        if self.top is None:
            return True
        else:
            return False

    def __len__(self):
        return self.count

    def push(self, value):
        self.count += 1
        if self.top is None:
            self.top = Node(value)
        else:
            new_node = Node(value)
            new_node.next = self.top
            self.top = new_node

    def pop(self):
        if self.isEmpty():
            return
        self.count -= 1
        popped_node = self.top
        self.top = self.top.next
        popped_node.next = None
        return popped_node.value

    def peek(self):
        if self.isEmpty():
            return None
        else:
            return self.top.value


# =============================================== Part II ==============================================
class Calculator:
    def __init__(self, extra_credit=False):
        self.expr = None
        self.extra_credit = extra_credit

    def _compare_precedence(self, op1, op2):
        precedence_mapping = {
            None: 0,
            "(": 0,
            ")": 0,
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3
        }
        return precedence_mapping.get(op1) - precedence_mapping.get(op2)

    def _validate_parentheses(self, txt):
        counter = 0
        for i in txt:
            if i == "(":
                counter += 1
            elif i == ")":
                counter -= 1
            if counter < 0:
                return False
        return counter == 0

    def _preprocess_and_validate(self, txt):
        # Validate for balanced parentheses
        if not self._validate_parentheses(txt):
            return None
        # Validate against unsupported characters
        reg_invalid = re.compile(r"""
            [^\(\)\+\*\-\^/\d\.\s]  # Any character that's not a digit, operator, period, or whitespace
            | (?<!\d)\.(?!\d)  # Any period without a digit on either end
        """, re.VERBOSE)
        if re.search(reg_invalid, txt):
            return None
        # Extract all relevant characters from whitespace into list
        reg = re.compile(r"""
            \s* \d*\.?\d+ \s*  # number wrapped by possible whitespace
            | \s* [\(\)\+\*\-\^/] \s*  # Operator wrapped by possible whitespace
        """, re.VERBOSE)
        elements = [re.sub(r'\s*', "", i) for i in re.findall(reg, txt)]  # Comprehension to remove whitespace
        # Ensure that expression has elements, and that doesn't end or start with improper operator
        if len(elements) == 0 or elements[0] in "^*/+-" or elements[-1] in "^*/+-":
            # If starts with - but followed by number, means negative number
            if elements[0] == "-" and self.isNumber(elements[1]):
                elements[0] += elements[1]
                elements.pop(1)
            else:
                return None
        # Iterate through and validate against consequent operators, consequent numbers
        i = 1
        while i < len(elements):
            # If start or open parenthese followed by minus then number, that means negative number
            if i > 1 and elements[i - 2] == "(" and elements[i - 1] == "-" and self.isNumber(elements[i]):
                elements[i - 1] += elements[i]
                elements.pop(i)
            # Check for consequent operators
            if elements[i - 1] in "(^*/+-" and elements[i] in "^*/+-":
                # If extra credit and second operator is minus followed by number, merge into negative
                if self.extra_credit and elements[i] == "-" and i < len(elements) - 1 and self.isNumber(elements[i + 1]):
                    elements[i] += elements[i + 1]
                    elements.pop(i + 1)
                else:
                    return None
            # If extra credit, support parenthesis multiplication
            if any([
                elements[i - 1] == ")" and elements[i] == "(",
                self.isNumber(elements[i - 1]) and elements[i] == "(",
                elements[i - 1] == ")" and self.isNumber(elements[i])
            ]):
                if self.extra_credit:
                    elements.insert(i, "*")
                else:
                    return None
            # Consequent numbers invalid.
            if self.isNumber(elements[i - 1]) and self.isNumber(elements[i]):
                return None
            i += 1
        return elements

    def isNumber(self, txt):
        txt = re.sub(r'^\s+|\s+$', "", txt)
        try:
            float(txt)
            return True
        except Exception:
            return False

    def isOperator(self, txt):
        return txt.strip() in "()^*/+-"

    def postfix(self, txt):
        if not isinstance(txt, str) or len(txt) <= 0:
            print("Argument error in postfix")
            return None

        elements = self._preprocess_and_validate(txt)
        if elements is None:
            return None

        postStack = Stack()
        postList = []
        for element in elements:
            # Append numbers to list immediately
            if self.isNumber(element):
                postList.append(str(float(element)))
            # Process operators
            elif self.isOperator(element):
                if element == "(":
                    postStack.push(element)
                elif self._compare_precedence(element, postStack.peek()) <= 0:
                    while not self._compare_precedence(element, postStack.peek()) > 0:
                        if postStack.peek() == "(":
                            if element == ")":
                                postStack.pop()
                            break
                        else:
                            postList.append(postStack.pop())
                    if element != ")":
                        postStack.push(element)
                else:
                    postStack.push(element)
            else:
                return None
        while not postStack.isEmpty():
            if postStack.peek() == "(":
                postStack.pop()
            else:
                postList.append(postStack.pop())
        return " ".join(postList)

    @property
    def calculate(self):
        if not isinstance(self.expr, str) or len(self.expr) <= 0:
            print("Argument error in calculate")
            return None

        postfix_str = self.postfix(self.expr)
        if postfix_str is None:
            return None

        postList = postfix_str.split(" ")

        op_mapping = {
            "^": lambda x, y: y ** x,
            "*": lambda x, y: y * x,
            "/": lambda x, y: y / x,
            "+": lambda x, y: y + x,
            "-": lambda x, y: y - x
        }

        calcStack = Stack()

        for element in postList:
            if self.isNumber(element):
                calcStack.push(element)
            elif self.isOperator(element):
                calcStack.push(op_mapping[element](float(calcStack.pop()), float(calcStack.pop())))
        return calcStack.pop()
