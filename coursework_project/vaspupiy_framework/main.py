from quopri import decodestring
from framework_requests import PostRequests, GetRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    """Класс Framework - основа WSGI-фреймворка"""

    def __init__(self, routes_obj, front_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = front_obj

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path = environ['PATH_INFO']

        # Добавляем закрывающий слеш
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            print(f'Нам пришел post-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_param(environ)
            request['request_params'] = request_params
            print(f'Нам пришли GET-параметры: {request_params}')

        # Находим нужный контроллер
        # Обработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]

        else:
            if '404_not_found' in self.routes_lst:
                view = self.routes_lst['404_not_found']
            else:
                view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)

        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data: dict) -> dict:
        """Метод преобразует данные в удобочитаемы вид"""
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data


# Новый вид WSGI-application.
class DebugApplication(Framework):
    """
    Первый - логирующий ( такой же как основной,
    только для каждого запроса выводит информацию
    (тип запроса и параметры) в консоль
    """

    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI-application.
class FakeApplication(Framework):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
