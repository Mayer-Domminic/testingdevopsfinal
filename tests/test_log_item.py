import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import User, Item, log_item, Base

class TestLogItem(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_log_item(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        item = Item(name='Test Item', quantity=10, price=9.99, owner=user)
        session.add(item)
        session.commit()

        result = log_item(user, item.id, 'add', 5, session=session)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(item.quantity, 15)

        result = log_item(user, item.id, 'remove', 3, session=session)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(item.quantity, 12)



    def test_log_invalid_action(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        item = Item(name='Test Item', quantity=10, price=9.99, owner=user)
        session.add(item)
        session.commit()

        result = log_item(user, item.id, 'invalid_action', 5, session=session)
        self.assertEqual(result['status'], 'error')
        self.assertIn("Invalid action", result['message'])

        session.close()

    def test_log_item_not_found(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        item = Item(name='Test Item', quantity=10, price=9.99, owner=user)
        session.add(item)
        session.commit()

        result = log_item(user, item.id + 1, 'add', 5, session=session)
        self.assertEqual(result['status'], 'error')
        self.assertIn("Item not found", result['message'])

        session.close()

    def test_log_insufficient_quantity(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        item = Item(name='Test Item', quantity=10, price=9.99, owner=user)
        session.add(item)
        session.commit()

        result = log_item(user, item.id, 'remove', 20, session=session)
        self.assertEqual(result['status'], 'error')
        self.assertIn("Not enough quantity available", result['message'])

        session.close()

if __name__ == '__main__':
    unittest.main()
