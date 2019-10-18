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
        assert x.postfix('2 *    5   +   3    ^ -2       +1  +4') == 'error message'
        assert x.postfix('2    5') == 'error message'
        assert x.postfix('25 +') == 'error message'
        assert x.postfix('   2 *  (  5   +   3)    ^ 2+(1  +4    ') == 'error message'
        assert x.postfix('2*(5 +3)^ 2+)1  +4(    ') == 'error message'

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
        assert x.calculate == 'error message'
        x.expr = "4    3 +2"
        assert x.calculate == 'error message'
        x.expr = '(2)*10 - 3*(2 - 3*2)) '
        assert x.calculate == 'error message'
        x.expr = '(2)*10 - 3*/(2 - 3*2) '
        assert x.calculate == 'error message'
        x.expr = ')2(*10 - 3*(2 - 3*2) '
        assert x.calculate == 'error message'
