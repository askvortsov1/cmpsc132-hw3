# HW3
# Due Date: 11/03/2019, 11:59PM
'''
Team members:

Collaboration Statement:             

'''
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
        if self.top == None:
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
    def __init__(self):
        self.expr = None

    def isNumber(self, txt):
        txt = re.sub(r'^\s+|\s+$', "", txt)
        try:
            float(txt)
            return True
        except Exception:
            return False


    def postfix(self, txt):
        if not isinstance(txt, str) or len(txt) <= 0:
            print("Argument error in postfix")
            return None

        postStack = Stack()
        # YOUR CODE STARTS HERE

    @property
    def calculate(self):
        if not isinstance(self.expr, str) or len(self.expr) <= 0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()

        # YOUR CODE STARTS HERE
