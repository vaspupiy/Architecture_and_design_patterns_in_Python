"""
Полностью перенесен в creations_pattern.py
"""

import sqlite3
from creations_patterns import Student, FeedbackModel


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = 'student'

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():  # все записи
            id_, name = item
            student = Student(name)
            student.id = id_
            result.append(student)
        return result

    def find_by_id(self, id_):
        statement = f"SELECT id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id_,))
        result = self.cursor.fetchone()  # возвращает первую запись
        if result:
            return Student(*result)  # объект класса
        else:
            raise RecordNotFoundException(f'record with id={id_} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class FeedbackMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = 'feedback'

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id_, name, email, message = item
            feedback = FeedbackModel(name, email, message)
            feedback.id = id_
            result.append(feedback)
        return result

    def find_by_id(self, id_):
        statement = f"SELECT id, name, email, message FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id_,))
        result = self.cursor.fetchone()
        print(*result)
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?) (email) VALUE (?) (message) VALUE (?)"
        self.cursor.execute(statement, (obj.name, obj.email, obj.message,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=?, email=?, message=?  WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.email, obj.message, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

"""
connection = sqlite3.connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        print(f"ой ой{obj.__class__}")
        if isinstance(obj, Student):
            print("да-да-да")
            #return StudentMapper(connection)
        #if isinstance(obj, Category):
            #return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)



"""
