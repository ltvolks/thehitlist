import unittest

import test_tasks


def run_tests(verbosity=2):
    reqs_tests = unittest.TestLoader().loadTestsFromTestCase(test_tasks.RequirementsTestCase)
    thl_tests = unittest.TestLoader().loadTestsFromTestCase(test_tasks.TheHitListTestCase)
    all_tests = unittest.TestSuite([reqs_tests, thl_tests])

    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(all_tests)
