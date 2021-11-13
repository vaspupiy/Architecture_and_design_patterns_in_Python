class PageNotFound404:
    def __call__(self):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа WSGI-фреймворка"""

    def __init__(self, routes_obj):
        self.routes_lst = routes_obj

    def __call__(self, environ, start_response):
        # Получаем адрес, по которому пользователь выполнил переход
        path = environ['PATH_INFO']

        # Добавляем закрывающий слеш
        if not path.endswith('/'):
            path = f'{path}/'

        # Находим нужный контроллер
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            if '404_not_found' in self.routes_lst:
                view = self.routes_lst['404_not_found']
            else:
                view = PageNotFound404()

        # Запускаем контроллер
        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
