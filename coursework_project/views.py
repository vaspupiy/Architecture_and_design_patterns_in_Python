"""Модуль, содержащий контроллеры веб-приложения"""
from quopri import decodestring

from vaspupiy_framework.templator import render


def decode_value(data: dict) -> dict:
    """функция преобразует данные в удобочитаемы вид"""
    new_data = {}
    for k, v in data.items():
        val = bytes(v.replace('%', '=').replace('+', ' '), 'UTF-8')
        val_decode_str = decodestring(val).decode('UTF-8')
        new_data[k] = val_decode_str
    return new_data


class Index:
    def __call__(self, request):
        date = request.get('data', None)
        data = {
            'title': 'Английский',
            'date': date
        }
        return '200 OK', render('index.html', data=data)


class Courses:
    def __call__(self, request):
        date = request.get('data', None)
        data = {
            'title': 'Список курсов',
            'date': date,
            'course_names': [
                'Курс 1', 'Курс 2', 'Курс 3', 'Курс 4', 'Курс 5', 'Курс 6'
            ]
        }
        return '200 OK', render('courses.html', data=data)


class Course:
    def __call__(self, request):
        date = request.get('data', None)
        data = {
            'title': 'Курс',
            'date': date
        }
        return '200 OK', render('course.html', data=data)


class About:
    def __call__(self, request):
        date = request.get('data', None)
        data = {
            'title': 'Такие дела...',
            'date': date
        }
        return '200 OK', render('about.html', data=data)


class Feedback:
    def __call__(self, request):
        date = request.get('data', None)
        data = {
            'title': 'Обратная связь',
            'date': date
        }
        if request['method'] == 'POST' and request['data']['message']:
            # проверяем, что метод пост и что есть сообщение, иначе игнорируем
            with open('temp_bd.txt', 'a', encoding='utf-8') as f:
                f.write('\n\nновая запись: \n')
                data = decode_value(request['data'])
                for k, v in data.items():
                    str_line = f'{k}: {v}\n'
                    f.write(str_line)
        return '200 OK', render('feedback.html', data=data)


class NotFound:
    def __call__(self, request):
        date = request.get('data', None)
        data = {
            'title': 'Страница не найдена',
            'date': date
        }
        return '404 WHAT', render('page404.html', data=data)
