import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import User, Item, list_items, Base

class TestListItems(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_list_items(self):
        session = self.Session()
        user1 = User(username='test_user1')
        user2 = User(username='test_user2')
        session.add(user1)
        session.add(user2)
        item1 = Item(name='Item 1', quantity=5, price=10.0, owner=user1)
        item2 = Item(name='Item 2', quantity=3, price=15.0, owner=user2)
        session.add(item1)
        session.add(item2)
        session.commit()

        self.assertEqual(list_items(session=session), 2)

        session.close()

if __name__ == '__main__':
    unittest.main()
