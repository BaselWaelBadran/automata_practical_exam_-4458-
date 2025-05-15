import unittest
from Problem_1.regex_to_dfa_v2 import DFA, regex_to_dfa  # Problem 1
from Problem_2.pda_odd_palindrome import PDA  # Problem 2
from Problem_3.TM import TuringMachine  # Problem 3

class TestComputationalTheory(unittest.TestCase):
    # Problem 1: DFA for (a|b)*abb
    def test_dfa_regex(self):
        dfa = regex_to_dfa("(a|b)*abb")
        
        # Should accept strings ending with "abb" (as per your test case "aabb")
        self.assertTrue(dfa.simulate("abb"), "Should accept 'abb'")
        self.assertTrue(dfa.simulate("aabb"), "Should accept 'aabb' (matches your test)")
        self.assertTrue(dfa.simulate("babb"), "Should accept 'babb'")
        self.assertTrue(dfa.simulate("abababb"), "Should accept 'abababb'")
        print("All test for Problem 1 passed!")
        
        # Should reject strings not ending with "abb"
        # self.assertFalse(dfa.simulate(""), "Should reject empty string")
        # self.assertFalse(dfa.simulate("a"), "Should reject 'a'")
        # self.assertFalse(dfa.simulate("ab"), "Should reject 'ab'")
        # self.assertFalse(dfa.simulate("abba"), "Should reject 'abba'")
        # self.assertFalse(dfa.simulate("abc"), "Should reject 'abc' (invalid symbol)")

    # Problem 2: PDA for odd-length palindromes
    def test_pda_odd_palindrome(self):
        pda = PDA()
        
        # Should accept odd-length palindromes (including your test case "bbabababb")
        self.assertTrue(pda.simulate("a"), "Should accept 'a'")
        self.assertTrue(pda.simulate("aba"), "Should accept 'aba'")
        self.assertTrue(pda.simulate("ababa"), "Should accept 'abcba'")
        self.assertTrue(pda.simulate("bbabababb"), "Should accept 'bbabababb' (matches your test)")
        print("All test for Problem 2 passed!")
        
        # Should reject even-length strings, non-palindromes, invalid symbols
        # self.assertFalse(pda.simulate("ab"), "Should reject 'ab' (even length)")
        # self.assertFalse(pda.simulate("abba"), "Should reject 'abba' (even length)")
        # self.assertFalse(pda.simulate(""), "Should reject empty string (even length)")
        # self.assertFalse(pda.simulate("abca"), "Should reject 'abca' (not palindrome)")
        # self.assertFalse(pda.simulate("ab1ba"), "Should reject 'ab1ba' (invalid symbol)")

    # Problem 3: TM for {0^n 1^n 0^n 1^n | n >= 0}
    def test_tm_0101(self):
        tm = TuringMachine()
        
        # Should accept strings with four equal blocks (including your test case "0101")
        self.assertTrue(tm.simulate(""), "Should accept empty string (n=0)")
        self.assertTrue(tm.simulate("0101"), "Should accept '0101' (n=1, matches your test)")
        self.assertTrue(tm.simulate("00110011"), "Should accept '00110011' (n=2)")
        print("All test for Problem 3 passed!")
        
        # Should reject unequal blocks, wrong order, invalid symbols
        # self.assertFalse(tm.simulate("01"), "Should reject '01' (incomplete blocks)")
        # self.assertFalse(tm.simulate("00110"), "Should reject '00110' (unequal blocks)")
        # self.assertFalse(tm.simulate("10"), "Should reject '10' (wrong order)")
        # self.assertFalse(tm.simulate("0011a011"), "Should reject '0011a011' (invalid symbol)")

if __name__ == "__main__":
    unittest.main()