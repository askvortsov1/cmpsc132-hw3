from HW3 import Stack, Calculator


class TestStack:
    def test_doctests(self):
        x = Stack()
        x.pop()
        x.push(2)
        x.push(4)
        x.push(6)
        assert repr(x) == "Top:Node(6)\nStack:\n6\n4\n2"
        assert x.pop() == 6
        assert repr(x) == "Top:Node(4)\nStack:\n4\n2"
        assert len(x) == 2
        assert x.peek() == 4


class TestCalculator:
    def test_compare_precendence(self):
        x = Calculator()
        assert x._compare_precedence("^", "^") == 0
        assert x._compare_precedence("^", "*") > 0
        assert x._compare_precedence("*", "+") > 0
        assert x._compare_precedence("-", "^") < 0

    def test_validate_parentheses(self):
        x = Calculator()
        assert x._validate_parentheses("(())") is True
        assert x._validate_parentheses("))(())()((") is False
        assert x._validate_parentheses(")(") is False
        assert x._validate_parentheses("(asdsadsadsadsadsa(asdsadsadds(sadsada)))") is True

    def test_preprocess_and_validate(self):
        x = Calculator(extra_credit=True)
        assert x._preprocess_and_validate('   2 *  (  5   +   3)    ^ 2+(1  +4    ') is None
        assert x._preprocess_and_validate('2*(5 +3)^ 2+)1  +4(    ') is None
        assert x._preprocess_and_validate('25 +') is None
        assert x._preprocess_and_validate('2    5') is None
        assert x._preprocess_and_validate('2 *    5   +   3    ^ -2       +1  +4') == ["2", "*", "5", "+", "3", "^", "-2", "+", "1", "+", "4"]
        assert x._preprocess_and_validate("2(4)") == ["2", "*", "(", "4", ")"]
        x.extra_credit = False
        assert x._preprocess_and_validate('2 *    5   +   3    ^ -2       +1  +4') is None
        assert x._preprocess_and_validate("2(4)") is None

    def test_is_number(self):
        x = Calculator()
        assert x.isNumber('hello') is False
        assert x.isNumber('1.2') is True
        assert x.isNumber('1.2.3') is False
        assert x.isNumber('    13   ') is True
        assert x.isNumber('    12   3') is False

    def test_postfix_doctest(self):
        x = Calculator()
        assert x.postfix(' 2 ^        4') == '2.0 4.0 ^'
        assert x.postfix('2') == '2.0'
        assert x.postfix('2.1*5+3^2+1+4.45') == '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
        assert x.postfix('    2 *       5.34        +       3      ^ 2    + 1+4   ') == '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
        assert x.postfix(' 2.1 *      5   +   3    ^ 2+ 1  +     4') == '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
        assert x.postfix('(2.5)') == '2.5'
        assert x.postfix('((2))') == '2.0'
        assert x.postfix('     -2 *  ((  5   +   3)    ^ 2+(1  +4))    ') == '-2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
        assert x.postfix('  (   2 *  ((  5   +   3)    ^ 2+(1  +4)))    ') == '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
        assert x.postfix('  ((   2 *  ((  5   +   3)    ^ 2+(1  +4))))    ') == '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
        assert x.postfix('   2 *  (  5   +   3)    ^ 2+(1  +4)    ') == '2.0 5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'
        assert x.postfix(' 23 / 12 - 223 +      5.25 * 4    *      3423') == '23.0 12.0 / 223.0 - 5.25 4.0 * 3423.0 * +'
        assert x.postfix('2 *    5   +   3    ^ -2       +1  +4') is None
        assert x.postfix('2    5') is None
        assert x.postfix('25 +') is None
        assert x.postfix('   2 *  (  5   +   3)    ^ 2+(1  +4    ') is None
        assert x.postfix('2*(5 +3)^ 2+)1  +4(    ') is None
        x.extra_credit = True
        assert x.postfix('(2.5)(1)(5)') == '2.5 1.0 * 5.0 *'

    def test_calculate_doctest(self):
        x = Calculator()
        x.expr = '    4  +      3 -2'
        assert x.calculate == 5.0
        x.expr = '  -2  +3.5'
        assert x.calculate == 1.5
        x.expr = '4+3.65-2 /2'
        assert x.calculate == 6.65
        x.expr = ' 23 / 12 - 223 +      5.25 * 4    *      3423'
        assert x.calculate == 71661.91666666667
        x.expr = '   2   - 3         *4'
        assert x.calculate == -10.0
        x.expr = ' 3 *   (        ( (10 - 2*3)))'
        assert x.calculate == 12.0
        x.expr = ' 8 / 4  * (3 - 2.45      * (  4- 2 ^   3)) + 3'
        assert x.calculate == 28.6
        x.expr = ' 2   *  ( 4 + 2 *   (5-3^2)+1)+4'
        assert x.calculate == -2.0
        x.expr = '2.5 + 3 * ( 2 +(3.0) *(5^2 - 2*3^(2) ) *(4) ) * ( 2 /8 + 2*( 3 - 1/ 3) ) - 2/ 3^2'
        assert x.calculate == 1442.7777777777778
        x.expr = "4++ 3 +2"
        assert x.calculate is None
        x.expr = "4    3 +2"
        assert x.calculate is None
        x.expr = '(2)*10 - 3*(2 - 3*2)) '
        assert x.calculate is None
        x.expr = '(2)*10 - 3*/(2 - 3*2) '
        assert x.calculate is None
        x.expr = ')2(*10 - 3*(2 - 3*2) '
        assert x.calculate is None
        x.extra_credit = True
        x.expr = '(2.5)(1)(5)'
        assert x.calculate == 12.5
        x.expr = '3(6)'
        assert x.calculate == 18
        x.expr = '(6)3'
        assert x.calculate == 18
