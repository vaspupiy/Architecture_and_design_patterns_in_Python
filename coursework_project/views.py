"""Модуль, содержащий контроллеры веб-приложения"""
from behavioral_patterns import ListView, CreateView, BaseSerializer, EmailNotifier, SmsNotifier
from patterns.creations_patterns import Engine, Logger
from structural_patterns import AppRoute, Debug
from vaspupiy_framework.templator import render

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        _date = request.get('date', None)
        content = {
            'title': 'Английский',
            'date': _date,
        }
        return '200 OK', render('index.html', content=content)


@AppRoute(routes=routes, url='/admin/')
class IndexAdmin:
    @Debug(name='IndexAdmin')
    def __call__(self, request):
        _date = request.get('date', None)
        objects_list = site.categories
        content = {
            'title': 'Английский',
            'date': _date,
            'objects_list': objects_list
        }
        return '200 OK', render('index-admin.html', content=content)


@AppRoute(routes=routes, url='/courses/')
class Courses:
    # По сути дубль CoursesList, оставлю что-то одно... позже... :)
    @Debug(name='Courses')
    def __call__(self, request):
        _date = request.get('date', None)
        content = {
            'title': 'Список курсов',
            'date': _date,
            'course_names': [
                'Курс 1', 'Курс 2', 'Курс 3', 'Курс 4', 'Курс 5', 'Курс 6'
            ],
        }
        return '200 OK', render('courses.html', content=content)


# Контроллер - список курсов
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='Courses')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            _date = request.get('date', None)
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
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
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
                # Добавляем наблюдателей на курс
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)

            _date = request.get('date', None)
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

                _date = request.get('date', None)
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
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
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
            _date = request.get('date', None)

            content = {
                'title': 'Создать курс',
                'date': _date,
                'name': name,
                'objects_list': objects_list,
            }

            return '200 OK', render('index-admin.html', content=content)
        else:
            categories = site.categories
            _date = request.get('date', None)

            content = {
                'title': 'Создать курс',
                'date': _date,
                'categories': categories,
            }
            return '200 OK', render('create-category.html', content=content)


# Контроллер - список категорий
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')

        _date = request.get('date', None)
        objects_list = site.categories

        content = {
            'title': 'Создать курс',
            'date': _date,
            'objects_list': objects_list,
        }
        return '200 OK', render('category-list.html', content=content)


# контроллер - копировать курс
@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
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

            _date = request.get('date', None)
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


@AppRoute(routes=routes, url='/courses/course/')
class Course:
    @Debug(name='Course')
    def __call__(self, request):
        _date = request.get('date', None)
        content = {
            'title': 'Курс',
            'date': _date
        }
        return '200 OK', render('course.html', content=content)


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        _date = request.get('date', None)
        content = {
            'title': 'Такие дела...',
            'date': _date
        }
        return '200 OK', render('about.html', content=content)


@AppRoute(routes=routes, url='/feedback/')
class Feedback:
    @Debug(name='Feedback')
    def __call__(self, request):
        _date = request.get('date', None)
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


@AppRoute(routes=routes, url='404_not_found')
class NotFound:
    @Debug(name='NotFound')
    def __call__(self, request):
        _date = request.get('date', None)
        content = {
            'title': 'Страница не найдена',
            'date': _date
        }
        return '404 WHAT', render('page404.html', content=content)


# контроллер - Расписания
@AppRoute(routes=routes, url='/study-programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        _date = request.get('date', None)
        content = {
            'title': 'Расписания',
            'date': _date
        }
        return '200 OK', render('study-programs.html', content=content)


# контроллер - отображение студентов
@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student-list.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Список студентов'
        return context


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create-student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Создание студента'
        return context

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        context['title'] = 'Добавление студента на курс'
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
