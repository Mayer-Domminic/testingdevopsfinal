import unittest
from unittest.mock import patch


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import User, Item, update_or_delete_item, Base, get_input

class TestUpdateOrDeleteItem(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_update_item_valid(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        item = Item(name='Test Item', quantity=10, price=9.99, owner=user)
        session.add(item)
        session.commit()

        update_or_delete_item(user, 'update', item_id=item.id, new_name='New Name', new_quantity=20, new_price=19.99, session=session)
        self.assertEqual(item.name, 'New Name')
        self.assertEqual(item.quantity, 20)
        self.assertEqual(item.price, 19.99)

        session.close()

    def test_delete_item(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        item = Item(name='Test Item', quantity=10, price=9.99, owner=user)
        session.add(item)
        session.commit()

        update_or_delete_item(user, 'delete', item_id=item.id, session=session)
        self.assertIsNone(session.query(Item).filter_by(id=item.id).first())

        session.close()

    def test_update_delete_missing_item(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        session.commit()

        update_or_delete_item(user, 'update', item_id=12345, new_name='New Name', session=session)
        update_or_delete_item(user, 'delete', item_id=12345, session=session)

        session.close()

    @patch('builtins.input', return_value='123')
    def test_get_input_normal_int(self, mock_input):
        result = get_input('quantity', 'Enter quantity: ', int)
        self.assertEqual(result, 123)

    @patch('builtins.print')
    def test_get_input_failure_int(self, mock_print):
        with patch('builtins.input', side_effect=['invalid', '123']):
            result = get_input('quantity', 'Enter quantity: ', int)
            mock_print.assert_called_with("Invalid input for quantity, please try again.")
            self.assertEqual(result, 123)

    def test_get_input_test_mode(self):
        result = get_input('price', 'Enter price: ', float, test=True, test_value='19.99')
        self.assertAlmostEqual(result, 19.99)


if __name__ == '__main__':
    unittest.main()
