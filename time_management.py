# pylance: ignore
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

import sqlite3

def create_database():
    # Connect to the database (creates it if it doesn't exist)
    connection = sqlite3.connect('time_management.db')
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Commit changes and close the connection
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_database()

Base = declarative_base()

# User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    tasks = relationship('Task', back_populates='user')
    reminders = relationship('Reminder', back_populates='user')

# Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='tasks')

# Reminder model
class Reminder(Base):
    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True)
    time_str = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='reminders')

# Database setup
engine = create_engine('sqlite:///time_management.db')
#create the tables in the database
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_data():
    user1 = User(name='Annet')

    # Use Datetime objects for start_time and end_time
    task1 = Task(
        name='Work on project',
        start_time=DateTime(2024, 9, 24, 10, 0, 0),
        end_time=DateTime(2024, 9, 24, 12, 0, 0),
        user=user1
    )
    reminder1 = Reminder(
        time_str=DateTime(2024, 9, 24, 9, 0, 0),
        message='Morning meeting reminder',
        user=user1
    )

    session.add(user1)
    session.add(task1)
    session.add(reminder1)
    session.commit()

def get_data():
    users = session.query(User).all()
    for user in users:
        print(f"User: {user.name}")
        for task in user.tasks:
            print(f"  Task: {task.name}, Start: {task.start_time}, End: {task.end_time}")
        for reminder in user.reminders:
            print(f"  Reminder: {reminder.message}, Time: {reminder.time_str}")

if __name__ == "__main__":
    get_data()  # Call get_data to print the current data in the database


