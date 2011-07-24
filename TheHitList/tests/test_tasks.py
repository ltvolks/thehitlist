import sys
import unittest

import TheHitList



class RequirementsTestCase(unittest.TestCase):
    """Test basic requirements are met."""

    def test_requirements(self):
        """
        appscript - http://appscript.sourceforge.net/py-appscript/install.html
        The Hit List must be installed
        """
        failures = []

        # Test for appscript
        try:
            import appscript
        except ImportError, msg:
            err = 'py-appscript - http://appscript.sourceforge.net/py-appscript/install.html'
            failures.append(err)

        # Test for The Hit List
        from appscript import app, ApplicationNotFoundError, CantLaunchApplicationError
        try:
            thl = app('The Hit List')
        except ApplicationNotFoundError, msg:
            err = 'The Hit List - http://www.potionfactory.com/thehitlist/'
            failures.append(err)
        except CantLaunchApplicationError, msg:
            failures.append(str(msg))
            
        if failures:
            if len(failures) > 1:
                fail_msg = '%d requirements are missing: %s' % (len(failures), '\n'.join(failures))
            else:
                fail_msg = '1 requirement is missing: %s' % (failures[0],)
            self.fail(fail_msg)



class TheHitListTestCase(unittest.TestCase):
    """Test interaction with The Hit List
    TODO: Create a test database to avoid issues with current hitlist
    """
    
    def setUp(self):
        self.thl = TheHitList.Application()


    def test_tasks(self):
        
        # New task in Inbox
        #thl.new_task('New Inbox Task')
        
        # Print Today list
        #thl.today().rprint()

        # Print Upcoming list
        
        # Print all Folders
        #thl.folders().rprint()

        # Create List
        self.thl.new_list('THL Test List')
        found_list = self.thl.find_list('THL Test List')
        if not found_list:
            self.assert_(found_list is not None, "Unable to create a new List 'THL Test List'")
        else:
            task = TheHitList.Task()
            task.title = "Test Title"
            task.notes = "Test Notes"

            found_list.add_task(task)
            found_task = self.thl.find_task('Test Title')
            self.assert_(found_task is not None, "Unable to find created Task 'Test Title'")

if __name__ == '__main__':
    warn_msg = """
    Warning!...These tests will operate on your current The Hit List database and may have unintended consequences!
    You may want to consider Backing up your database first (File-->Backup Database...).
    Do you want to run the tests?
    """
    print(warn_msg)
    
    go = raw_input('Y(es)/N(o): ')

    if go.lower() in ('y', 'ye', 'yes'):
        unittest.main()
    else:
        sys.exit(1)

