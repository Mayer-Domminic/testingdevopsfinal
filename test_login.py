import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import User, login, Base

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_login(self):
        session = unittest.mock.Mock()
        session.query().filter_by().first.return_value = None
        user = login(username='test_user', session=session)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'test_user')
        session.add.assert_called_once()
        session.commit.assert_called_once()

    def test_login_create_user(self):
        session = self.Session()
        user = login(username='test_user', session=session)
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(session.query(User).count(), 1)


if __name__ == '__main__':
    unittest.main()