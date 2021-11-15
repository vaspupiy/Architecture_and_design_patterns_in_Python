class Requests:
    """Класс обработки запроса с параметрами"""

    @staticmethod
    def parse_input_data(data: str) -> dict:
        """Метод преобразует данные запроса в словарь Python"""
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result


class GetRequests(Requests):
    """Класс обработки Get-запроса с параметрами"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_request_param(environ: dict) -> dict:
        """метод получает параметры запроса и возвращает словарь с параметрами"""
        query_string = environ['QUERY_STRING']
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class PostRequests(Requests):
    """Класс обработки Post-запроса с параметрами"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_wsgi_input_data(env: dict) -> bytes:
        """метод возвращает данные в виде байт"""
        content_len_data = env.get('CONTENT_LENGTH')  # получаем длину тела
        content_len = int(content_len_data) if content_len_data else 0 # Приводим к int
        # Считываем данные если они есть
        data = env['wsgi.input'].read(content_len) if content_len > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        """метод преобразует данные из строки байт в словарь Python"""
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ: dict) -> dict:
        """метод получает данные и преобразует данные в словарь"""
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data
