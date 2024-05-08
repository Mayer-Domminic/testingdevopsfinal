import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import User, create_item, Item, Base

class TestCreateItem(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_create_item_valid(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        session.commit()

        create_item(user, name='Test Item', quantity=10, price=9.99, session=session)
        self.assertEqual(session.query(Item).count(), 1)
        item = session.query(Item).first()
        self.assertEqual(item.name, 'Test Item')
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.price, 9.99)
        self.assertEqual(item.owner, user)
        session.close()

    def test_create_item_missing_name(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        session.commit()

        create_item(user, quantity=10, price=9.99, session=session)
        self.assertEqual(session.query(Item).count(), 0)
        session.close()

    def test_create_item_invalid_quantity(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        session.commit()

        create_item(user, name='Invalid Quantity Item', quantity=-5, price=9.99, session=session)
        self.assertEqual(session.query(Item).count(), 0)

        create_item(user, name='Invalid Quantity Item', quantity=0, price=9.99, session=session)
        self.assertEqual(session.query(Item).count(), 0)

        session.close()

    def test_create_item_invalid_price(self):
        session = self.Session()
        user = User(username='test_user')
        session.add(user)
        session.commit()

        create_item(user, name='Invalid Price Item', quantity=10, price=-9.99, session=session)
        self.assertEqual(session.query(Item).count(), 0)

        create_item(user, name='Invalid Price Item', quantity=10, price=0, session=session)
        self.assertEqual(session.query(Item).count(), 0)

        session.close()

if __name__ == '__main__':
    unittest.main()
