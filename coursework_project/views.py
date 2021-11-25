"""Модуль, содержащий контроллеры веб-приложения"""
from quopri import decodestring
from datetime import date
from vaspupiy_framework.templator import render
from patterns.creations_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        _date = date.today()
        content = {
            'title': 'Английский',
            'date': _date,
        }
        return '200 OK', render('index.html', content=content)


class IndexAdmin:
    def __call__(self, request):
        _date = date.today()
        objects_list = site.categories
        content = {
            'title': 'Английский',
            'date': _date,
            'objects_list': objects_list
        }
        return '200 OK', render('index-admin.html', content=content)


class Courses:
    # По сути дубль CoursesList, оставлю что-то одно... позже... :)
    def __call__(self, request):
        _date = date.today()
        content = {
            'title': 'Список курсов',
            'date': _date,
            'course_names': [
                'Курс 1', 'Курс 2', 'Курс 3', 'Курс 4', 'Курс 5', 'Курс 6'
            ],
        }
        return '200 OK', render('courses.html', content=content)


# Контроллер - список курсов
class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            _date = date.today()
            objects_list = category.courses
            name = category.name
            _id = category.id
            all_course_list = site.courses
            content = {
                'title': 'Список курсов',
                'date': _date,
                'objects_list': objects_list,
                'name': name,
                'id': _id,
                'all_course_list': all_course_list,
            }
            return '200 OK', render('course-list.html', content=content)

        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                site.courses.append(course)

            _date = date.today()
            objects_list = category.courses
            name = category.name
            _id = category.id

            content = {
                'title': 'Создать курс',
                'date': _date,
                'objects_list': objects_list,
                'name': name,
                'id': _id
            }

            return '200 OK', render('course-list.html', content=content)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                _date = date.today()
                name = category.name
                _id = category.id

                content = {
                    'title': 'Создать курс',
                    'date': _date,
                    'name': name,
                    'id': _id
                }

                return '200 OK', render('create-course.html', content=content)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# Контроллер - создать категорию
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            objects_list = site.categories
            _date = date.today()

            content = {
                'title': 'Создать курс',
                'date': _date,
                'name': name,
                'objects_list': objects_list,
            }

            return '200 OK', render('index-admin.html', content=content)
        else:
            categories = site.categories
            _date = date.today()

            content = {
                'title': 'Создать курс',
                'date': _date,
                'categories': categories,
            }
            return '200 OK', render('create-category.html', content=content)


# Контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')

        _date = date.today()
        objects_list = site.categories

        content = {
            'title': 'Создать курс',
            'date': _date,
            'objects_list': objects_list,
        }
        return '200 OK', render('category-list.html', content=content)


# контроллер - копировать курс
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            name = site.decode_value(name)
            category_id = request_params['id']
            category = site.find_category_by_id(int(category_id))
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.course_clone()
                new_course.name = new_name
                site.courses.append(new_course)

            _date = date.today()
            objects_list = category.courses
            cat_name = category.name
            all_course_list = site.courses

            content = {
                'title': 'Создать курс',
                'date': _date,
                'objects_list': objects_list,
                'id': category_id,
                'name': cat_name,
                'all_course_list': all_course_list,
            }

            return '200 OK', render('course-list.html',
                                    content=content)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


class Course:
    def __call__(self, request):
        _date = date.today()
        content = {
            'title': 'Курс',
            'date': _date
        }
        return '200 OK', render('course.html', content=content)


class About:
    def __call__(self, request):
        _date = date.today()
        content = {
            'title': 'Такие дела...',
            'date': _date
        }
        return '200 OK', render('about.html', content=content)


class Feedback:
    def __call__(self, request):
        _date = date.today()
        content = {
            'title': 'Обратная связь',
            'date': _date
        }
        if request['method'] == 'POST' and request['data']['message']:
            # проверяем, что метод пост и что есть сообщение, иначе игнорируем
            with open('temp_bd.txt', 'a', encoding='utf-8') as f:
                f.write('\n\nновая запись: \n')
                data = site.decode_dict(request['data'])
                for k, v in data.items():
                    str_line = f'{k}: {v}\n'
                    f.write(str_line)
        return '200 OK', render('feedback.html', content=content)


class NotFound:
    def __call__(self, request):
        _date = date.today()
        content = {
            'title': 'Страница не найдена',
            'date': _date
        }
        return '404 WHAT', render('page404.html', content=content)


# контроллер - Расписания
class StudyPrograms:
    def __call__(self, request):
        _date = date.today()
        content = {
            'title': 'Расписания',
            'date': _date
        }
        return '200 OK', render('study-programs.html', content=content)
