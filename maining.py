from sqlalchemy import create_engine, Column, Integer, String, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# Підключення до бази даних
engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Список груп, які потрібно додати
groups_to_add = ['Group 1', 'Group 2', 'Group 1']

for group_name in groups_to_add:
    # Перевірка, чи існує група з таким ім'ям
    existing_group = session.query(Group).filter_by(name=group_name).first()
    if existing_group:
        print(f"Група з ім'ям {group_name} вже існує.")
    else:
        new_group = Group(name=group_name)
        session.add(new_group)
        print(f"Додано групу з ім'ям {group_name}.")

try:
    session.commit()
except exc.IntegrityError:
    session.rollback()
    print("Виникла помилка при додаванні груп.")

# Закриття сесії
session.close()
