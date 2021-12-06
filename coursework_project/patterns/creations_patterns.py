import sqlite3
from copy import deepcopy
from quopri import decodestring
import sqlite3

# Абстрактный пользователь
from architectural_system_pattern_unit_of_work import DomainObject
from behavioral_patterns import Subject, ConsoleWriter


class User:
    def __init__(self, name):
        self.name = name


# Преподаватель
class Teacher(User):
    pass


#  Студент
class Student(User, DomainObject):

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


#  Администратор
class Admin(User):
    pass


#  Порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
        'admin': Admin,
    }

    # Порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# Порождающий паттерн Прототип - Курс
class CoursePrototype:
    # Прототип курсов обучения
    def course_clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


# Категория
class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# Порождающий паттерн Абстрактная фабрика - фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # Порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []
        self.feedbacks = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id_):
        for item in self.categories:
            print('item', item.id)
            if item.id == id_:
                return item
        raise Exception(f'Нет категории с id = {id_}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    @staticmethod
    def create_feedback(name, email, message):
        return FeedbackModel(name, email, message)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val: str) -> str:
        val_b = bytes(val.replace('%', '=').replace('+', " "), "UTF-8")
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    @staticmethod
    def decode_dict(data: dict) -> dict:
        """функция преобразует данные в удобочитаемы вид"""
        new_data = {}
        for k, v in data.items():
            new_data[k] = Engine.decode_value(v)
        return new_data


# Порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)


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

    def __init__(self, _connection):
        self.connection = _connection
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


# класс Feedback
class FeedbackModel(DomainObject):

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message


class FeedbackMapper:

    def __init__(self, _connection):
        self.connection = _connection
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
        statement = f"INSERT INTO {self.table_name} (name, email, message) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.name, obj.email, obj.message,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=?, email=?, message=?  WHERE id=?"
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


connection = sqlite3.connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'feedback': FeedbackMapper,
        # 'category': CategoryMapper и т.д.
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        if isinstance(obj, FeedbackModel):
            return FeedbackMapper(connection)
        # if isinstance(obj, Category):
        # return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
