import unittest
from CSP import CSP


# run with: python3 csp_tests.py
class TestSolValidation(unittest.TestCase):
    def setUp(self):
        self.csp1 = CSP(3, 6)
        self.csp2 = CSP(4, 6)

    def test_empty_csp(self):
        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 4, 1])), "Empty guess, all should be valid")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([5, 4, 1])), "Empty guess, all should be valid")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([2, 4, 3])), "Empty guess, all should be valid")

    def test_basic_single_guess_full(self):
        # After one guess with only bulls and full solution suggestion

        self.csp1.insert_guess([1, 2, 3], 1, 0)

        self.assertFalse(self.csp1._is_sol_valid(to_guess([1, 4, 3])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([2, 4, 3])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([3, 1, 2])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([4, 5, 6])), "Invalid guess")

        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 1, 1])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([2, 2, 2])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 4, 5])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([6, 5, 3])), "Valid guess")

    def test_single_guess_full(self):
        # After one guess and full solution suggestion

        self.csp1.insert_guess([1, 2, 3], 1, 1)

        self.assertFalse(self.csp1._is_sol_valid(to_guess([1, 4, 3])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([2, 3, 1])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([3, 3, 3])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([2, 1, 3])), "Invalid guess")

        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 3, 1])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([3, 2, 2])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 3, 5])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([2, 5, 3])), "Valid guess")

    def test_basic_single_guess_partial(self):
        # After one guess with only bulls and partial solution suggestion

        self.csp1.insert_guess([1, 2, 3], 1, 0)

        self.assertFalse(self.csp1._is_sol_valid({0: 1, 2: 3}), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid({1: 1, 2: 2}), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid({0: 3, 2: 2}), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid({0: 2, 2: 3}), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid({1: 2, 2: 3}), "Invalid guess")
        # self.assertFalse(self.csp1._is_sol_valid({0: 3, 2: 4}), "Kaka")#TODO: not sure could be solved in O(1)

        self.assertTrue(self.csp1._is_sol_valid({0: 1}), "valid guess")
        self.assertTrue(self.csp1._is_sol_valid({0: 1, 2: 6}), "valid guess")
        self.assertTrue(self.csp1._is_sol_valid({0: 3, 2: 3}), "valid guess")
        self.assertTrue(self.csp1._is_sol_valid({0: 1, 1: 1}), "valid guess")  # 1, 1, 1/4/5/6
        self.assertTrue(self.csp1._is_sol_valid({0: 2, 2: 4}), "valid guess")  # 2, 2, 4

    # combinations of guesses
    def test_basic_multi_guesses_full(self):
        self.csp1.insert_guess([1, 1, 1], 1, 0)
        self.csp1.insert_guess([1, 2, 3], 1, 0)

        self.assertFalse(self.csp1._is_sol_valid(to_guess([1, 4, 3])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([2, 4, 3])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([3, 1, 2])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([4, 5, 6])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([2, 2, 2])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([3, 2, 5])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([6, 2, 5])), "Invalid guess")
        self.assertFalse(self.csp1._is_sol_valid(to_guess([4, 5, 6])), "Invalid guess")

        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 4, 5])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 6, 6])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 5, 6])), "Valid guess")

    def test_basic_multi_guesses_partial2(self):
        # 4, 0, 3
        self.csp1.insert_guess([0, 0, 1], 1, 0)
        self.csp1.insert_guess([0, 2, 4], 0, 2)

        self.assertTrue(self.csp1._is_sol_valid({0: 4}), "Valid guess")

    def test_basic_multi_guesses_partial3(self):
        # 4, 0, 3
        self.csp1.insert_guess([2, 0, 2], 1, 0)
        self.csp1.insert_guess([0, 0, 3], 2, 0)

        self.assertTrue(self.csp1._is_sol_valid({0: 4}), "Valid guess")

    def test_zero_result(self):
        self.csp2.insert_guess((0,0,2,3),0,0)
        for domain in self.csp2._domains:
            self.assertEqual(domain, [1,4,5])


"""
    def test_complex_guesses_partial(self):
        self.csp1.insert_guess([1, 1, 1], 1, 0)
        self.csp1.insert_guess([1, 2, 3], 1, 0)

        self.assertFalse(self.csp1._is_sol_valid({}), "Invalid guess")

        self.assertTrue(self.csp1._is_sol_valid({}), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 6, 6])), "Valid guess")
        self.assertTrue(self.csp1._is_sol_valid(to_guess([1, 5, 6])), "Valid guess")
"""

def to_guess(list_sol):
    res = {}
    for k, v in enumerate(list_sol):
        res[k] = v
    return res


if __name__ == '__main__':
    unittest.main()
