from sqlmodel import SQLModel, Session
from db.database import engine, create_db_and_tables, drop_db_and_tables
from models.user import User
from models.task import Task
from models.task_status import TaskStatus
from models.todo_list import TodoList
from auth.hashing import hash_password  # Importamos la función para hashear contraseñas

def seed_data():
    # Borrar la base de datos y las tablas existentes
    drop_db_and_tables() 
    # Crear la base de datos y las tablas
    create_db_and_tables()

    with Session(engine) as session:
        # Create task statuses
        try:
            task_status_1 = TaskStatus(name="Open", color="White")
            task_status_2 = TaskStatus(name="In Progress", color="Yellow")
            task_status_3 = TaskStatus(name="Done", color="Green")
            session.add_all([task_status_1, task_status_2, task_status_3])
            session.commit()
        except Exception as e:
            print(f"Error creating task statuses: {e}")

        # Crear usuarios
        try:
            user0 = User(username="anonymous", email="anonymous@example.com", hashed_password=hash_password("anonymous"))
            user1 = User(username="user1", email="user1@example.com", hashed_password=hash_password("password1"))
            user2 = User(username="user2", email="user2@example.com", hashed_password=hash_password("password2"))
            session.add_all([user0, user1, user2])
            session.commit()
        except Exception as e:
            print(f"Error creating users: {e}")

        # Crear entradas de todo_lists
        try:
            todo_list1 = TodoList(title="Project One", description="This is the todo-list for project one", owner_id=user1.id, owner_username=user1.username)
            todo_list2 = TodoList(title="Project Two", description="A new todo-list for the new project of the team", owner_id=user2.id, owner_username=user2.username)
            todo_list3 = TodoList(title="Agile Project Three", description="This is the first agile project we manage", owner_id=user1.id, owner_username=user1.username)
            session.add_all([todo_list1, todo_list2, todo_list3])
            session.commit()
        except Exception as e:
            print(f"Error creating todo lists: {e}")


        # Crear tasks
        try:
            task1 = Task(title="Task One", description="This is the first task", due_date='2025-05-20', is_completed=False, todo_list_id=todo_list1.id, status_id=task_status_1.id)
            task2 = Task(title="Task Two", description="This is the second task", due_date='2025-05-20', is_completed=True, todo_list_id=todo_list1.id, status_id=task_status_2.id)
            task3 = Task(title="Task Three", description="This is the first task of another todoList", due_date='2025-05-20', is_completed=False, todo_list_id=todo_list2.id, status_id=task_status_1.id)
            session.add_all([task1, task2, task3])
            session.commit()
        except Exception as e:
            print(f"Error creating todo lists: {e}")

if __name__ == "__main__":
    seed_data()
