import os
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="items")

engine = create_engine('sqlite:///inventory.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_input(field_name, prompt, convert_func, test=False, test_value=None):
    if test:
        return convert_func(test_value)
    else:
        while True:
            try:
                return convert_func(input(prompt))
            except ValueError:
                print(f"Invalid input for {field_name}, please try again.")



def login(username=None, session=None):
    if username is None:
        username = get_input("username", "Enter username: ", str)
    user = session.query(User).filter_by(username=username).first()
    if not user:
        user = User(username=username)
        session.add(user)
        session.commit()
    return user

def log_item(user, item_id=None, action=None, amount=None, session=None):
    try:
        if item_id is None and action is None and amount is None:
            item_id = get_input("Item_ID", "Enter Item_ID: ", int)
            action = get_input("action", "Enter action (add/remove): ", str)
            amount = get_input("amount", "Enter amount: ", int)
        if item_id is None or action is None or amount is None:
            raise ValueError("All log item attributes (item_id, action, amount) must be provided.")

        item = session.query(Item).filter_by(id=item_id, owner=user).first()
        if not item:
            error_msg = "Item not found or you do not have permission."
            print(error_msg)
            return {'status': 'error', 'message': error_msg}

        if action == 'add':
            item.quantity += amount
            print(f"Added {amount} to {item.name}. New quantity: {item.quantity}")
        elif action == 'remove':
            if item.quantity >= amount:
                item.quantity -= amount
                print(f"Removed {amount} from {item.name}. New quantity: {item.quantity}")
            else:
                error_msg = f"Not enough quantity available for {item.name}."
                print(error_msg)
                return {'status': 'error', 'message': error_msg}
        else:
            error_msg = "Invalid action. Please specify 'add' or 'remove'."
            print(error_msg)
            return {'status': 'error', 'message': error_msg}

        session.commit()
        return {'status': 'success', 'message': 'Transaction logged successfully.'}
    except Exception as e:
        session.rollback()
        error_msg = f"Error occurred while logging item transaction: {e}"
        print(error_msg)
        return {'status': 'error', 'message': error_msg}

def create_item(user, name=None, quantity=None, price=None, session=None):
    try:
        if name is None:
            raise ValueError("Item name must be provided.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if not isinstance(price, float) or price <= 0:
            raise ValueError("Price must be a positive float.")

        new_item = Item(name=name, quantity=quantity, price=price, user_id=user.id)
        session.add(new_item)
        session.commit()
        print(f"Item {name} successfully created with ID {new_item.id}.")
    except ValueError as ve:
        session.rollback()
        print(f"Error occurred while creating the item: {ve}")

def list_items(session=None):
    if session is None:
        session = Session()
    items = session.query(Item).all()
    [print(f"Item ID: {item.id}, Name: {item.name}, Quantity: {item.quantity}, Price: ${item.price:.2f}, Owner: ${item.owner.username}") for item in items]
    return len(items)

def update_or_delete_item(user, operation, item_id=None, new_name=None, new_quantity=None, new_price=None, session=None):
    result = {'status': 'success', 'message': ''}

    if operation == 'update' and item_id is None and (new_name is not None or new_quantity is not None or new_price is not None):
        raise ValueError("If any new item attributes are provided, item_id must also be provided.")

    if item_id is None:
        item_id = get_input("item ID", "Enter one you own!\nEnter the item ID: ", int)

    item = session.query(Item).filter_by(id=item_id, owner=user).first()
    if not item:
        result['status'] = 'error'
        result['message'] = "Item not found."
        return result

    if operation == 'update':
        if new_name is None:
            print(f" Current Item: {item.name} {item.quantity} {item.price}")
            new_name = get_input("new_name", "Enter new name: ", str)
        if new_quantity is None:
            new_quantity = get_input("quantity", "Enter the quantity: ", int)
        if new_price is None:
            new_price = get_input("price", "Enter the price: ", float)

        item.name = new_name
        item.quantity = new_quantity
        item.price = new_price
    elif operation == 'delete':
        session.delete(item)

    session.commit()
    return result


def main_menu(user, session=None, input_func=input, output_func=print):
    while True:
        # this allows for testing of the mocked user (in/out)put
        output_func("\nInventory Management System ")
        output_func("\n1. Log Item Transaction\n2. List All Items\n3. Update My Items\n4. Delete My Items\n5. Create New Item\n0. Logout")
        choice = input_func("Enter your choice: ")

        if choice == '1':
            list_items(session=session)
            log_item(user, session=session)
        elif choice == '2':
            list_items(session=session)
        elif choice == '3':
            list_items(session=session)
            update_or_delete_item(user, 'update', session=session)
        elif choice == '4':
            list_items(session=session)
            update_or_delete_item(user, 'delete', session=session)
        elif choice == '5':
            name = get_input("name", "Enter the name: ", str)
            quantity = get_input("quantity", "Enter the quantity: ", int)
            price = get_input("price", "Enter the price: ", float)

            create_item(user, name, quantity, price, session=session)
        elif choice == '0':
            output_func("Logging out...")
            break
        else:
            output_func("Invalid choice, please try again.")

    return "Logged out"

if __name__ == '__main__':
    session = Session()
    user = login(session=session)
    main_menu(user, session)