#!/usr/bin/env python
import sys

from TheHitList.tests import run_tests

warn_msg = """
Warning!...These tests will operate on your current The Hit List database and may have unintended consequences!
You may want to consider Backing up your database first (File-->Backup Database...).
Do you want to run the tests?
"""
print(warn_msg)

go = raw_input('Y(es)/N(o): ')
if go.lower() not in ('y', 'ye', 'yes'):
    sys.exit(1)

run_tests(verbosity=2)

