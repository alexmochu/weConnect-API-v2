
""" File to handle Unit Test for User accounts """
import unittest
from api.models import User

class TestUserAccountsTestCases(unittest.TestCase):
    """ Users accounts tests case """

    def setUp(self):
        """ Setup Users Class test case """

        self.user = User()

    def tearDown(self):
        """ Teardown Users Class test case  """

        del self.user

if __name__ == '__main__':
    unittest.main()