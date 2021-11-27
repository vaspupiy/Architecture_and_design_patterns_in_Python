from wsgiref.simple_server import make_server

from vaspupiy_framework.main import Framework
from urls import fronts
from views import routes

# from urls import routes

# Создаем объект WSGI-приложения
application = Framework(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
