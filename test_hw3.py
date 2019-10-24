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
        assert x.pop() == 4
        assert repr(x) == "Top:Node(2)\nStack: \n2"
        assert x.pop() == 2
        assert repr(x) == "Top:None\nStack:\n"
        assert len(x) == 0
        assert x.peek() is None


class TestCalculator:
    def test_compare_precendence(self):
        x = Calculator()
        assert x._compare_precedence("^", "^") == 0
        assert x._compare_precedence("^", "*") > 0
        assert x._compare_precedence("*", "+") > 0
        assert x._compare_precedence("-", "^") < 0
        assert x._compare_precedence("*","^") < 0

    def test_validate_parentheses(self):
        x = Calculator()
        assert x._validate_parentheses("(())") is True
        assert x._validate_parentheses("))(())()((") is False
        assert x._validate_parentheses(")(") is False
        assert x._validate_parentheses("(asdsadsadsadsadsa(asdsadsadds(sadsada)))") is True
        assert x._validate_parentheses("hifhsv())()))()(((") is False
        assert x._validate_parentheses("314314") is True
        assert x._validate_parentheses("-0-909r viurvpu()9efi cd()") is True
        assert x._validate_parentheses("[][]{}{][]()()") is True
        assert x._validate_parentheses("[()][()]][") is True


    def test_preprocess_and_validate(self):
        x = Calculator(extra_credit=True)
        assert x._preprocess_and_validate('   2 *  (  5   +   3)    ^ 2+(1  +4    ') is None
        assert x._preprocess_and_validate('2*(5 +3)^ 2+)1  +4(    ') is None
        assert x._preprocess_and_validate('25 +') is None
        assert x._preprocess_and_validate('2    5') is None
        assert x._preprocess_and_validate('2 *    5   +   3    ^ -2       +1  +4') == ["2", "*", "5", "+", "3", "^", "-2", "+", "1", "+", "4"]
        assert x._preprocess_and_validate("2(4)") == ["2", "*", "(", "4", ")"]
        assert x._preprocess_and_validate("5(3*7+25-2187^78)") == ['5', '*', '(', '3', '*', '7', '+', '25', '-', '2187', '^', '78', ')']
        assert x._preprocess_and_validate("543(90-78)(") is None
        assert x._preprocess_and_validate("65 +  (4) - 13 ^7-(-1) + 31-69") == ['65', '+', '(', '4', ')', '-', '13', '^', '7', '-', '(', '-1', ')', '+', '31', '-', '69']
        x.extra_credit = False
        assert x._preprocess_and_validate('2 *    5   +   3    ^ -2       +1  +4') is None
        assert x._preprocess_and_validate("2(4)") is None
        assert x._preprocess_and_validate(' 2*2+6-34^78') == ['2', '*', '2', '+', '6', '-', '34', '^', '78']
        assert x._preprocess_and_validate("5(3*7+25-2187^78)") is None
        assert x._preprocess_and_validate("543(90-78)(") is None
        assert x._preprocess_and_validate("65 +  (4) - 13 ^7-(-1) + 31-69") is None


    def test_is_number(self):
        x = Calculator()
        assert x.isNumber('hello') is False
        assert x.isNumber('1.2') is True
        assert x.isNumber('1.2.3') is False
        assert x.isNumber('    13   ') is True
        assert x.isNumber('    12   3') is False
        assert x.isNumber('4/5') is False
        assert x.isNumber('9-8') is False
        assert x.isNumber('9.978879824578798') is True
        assert x.isNumber('-0970785') is True
        assert x.isNumber('43$') is False

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
        assert x.postfix('42  + 41 - 4892798*42 - a 42') is None
        assert x.postfix('42  + 41 - 4892798*42 - 12') == '42.0 41.0 + 4892798.0 42.0 * - 12.0 -'
        x.extra_credit = True
        assert x.postfix('(2.5)(1)(5)') == '2.5 1.0 * 5.0 *'
        assert x.postfix('42  + 41 - 4892798*42 - 12') == '42.0 41.0 + 4892798.0 42.0 * - 12.0 -'
        assert x.postfix('42  + 41 - 4892798*42 - a 42') is None
        assert x.postfix('7*0-(799) - (-7) +56 ^ 90') == '7.0 0.0 * 799.0 - -7.0 - 56.0 90.0 ^ +'
        assert x.postfix('4 - (9) -905 35 +24 ^77') is None


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
        x.expr = '9-(-9) + 79-27'
        assert x.calculate == 70.0
        x.expr = '1.9 ^1 -2'
        assert x.calculate == -0.10000000000000009
        x.expr = '4^^2-4'
        assert x.calculate is None
        x.expr = '1(3-3)^0-0*(24-12)'
        assert x.calculate == 1.0
        x.expr = '0^1 - 90 + 9^2-(9*(9))-(-9)'
        assert x.calculate == -81.0
        x.expr = '0^(2-2)+50-5*2  + 2(9)+ 3   ^ 2 + 5309 ^ (0)'
        assert x.calculate == 69.0



