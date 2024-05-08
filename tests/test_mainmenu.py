import unittest
from unittest.mock import Mock
from main import main_menu, login

class TestMainMenu(unittest.TestCase):
    def test_logout(self):
        session_mock = Mock()
        input_mock = Mock(side_effect=['0'])
        output_mock = Mock()
        # the user for now is just my username as a test
        user = login('dom', session_mock)

        result = main_menu(user, session=session_mock, input_func=input_mock, output_func=output_mock)
        output_mock.assert_called_with("Logging out...")
        self.assertEqual(result, "Logged out")

if __name__ == '__main__':
    unittest.main()
