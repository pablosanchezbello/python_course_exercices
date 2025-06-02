from sqlmodel import SQLModel, Session
from db.database import engine, create_db_and_tables, drop_db_and_tables
from models.user import User
from auth.hashing import hash_password
from models.order import Order
from models.order_item import OrderItem

def seed_data():
    # Delete database and existing tables
    drop_db_and_tables() 
    # Create database and tables
    create_db_and_tables()

    with Session(engine) as session:

        # Create users
        try:
            user0 = User(username="anonymous", email="anonymous@example.com", hashed_password=hash_password("anonymous"))
            user1 = User(username="user1", email="user1@example.com", hashed_password=hash_password("password1"))
            user2 = User(username="user2", email="user2@example.com", hashed_password=hash_password("password2"))
            session.add_all([user0, user1, user2])
            session.commit()
        except Exception as e:
            print(f"Error creating users: {e}")
        
        # Create orders
        try:
            order_1 = Order(status="in progress", user_id=user1.id)
            order_2 = Order(status="in progress", user_id=user2.id)
            session.add_all([order_1, order_2])
            session.commit()
        except Exception as e:
            print(f"Error creating orders: {e}")

        # Create order items
        try:
            order_item_1 = OrderItem(order_id=order_1.id, product_id=1, quantity=2)
            order_item_2 = OrderItem(order_id=order_1.id, product_id=2, quantity=1)
            order_item_3 = OrderItem(order_id=order_2.id, product_id=1, quantity=3)
            order_item_4 = OrderItem(order_id=order_2.id, product_id=3, quantity=1)
            session.add_all([order_item_1, order_item_2, order_item_3, order_item_4])
            session.commit()
        except Exception as e:
            print(f"Error creating order items: {e}")

if __name__ == "__main__":
    seed_data()
