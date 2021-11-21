from datetime import date
from views import Index, About, Courses, Feedback, NotFound, Course


# front controller
def secret_front(request):
    request['data'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

# Набор привязок: путь-контроллер
routes = {
    '/': Index(),
    '/courses/': Courses(),
    '/courses/course/': Course(),
    '/about/': About(),
    '/feedback/': Feedback(),
    #  добавил возможность выводить 404 ошибку, оставляя навигационную панель(футер и хедер)
    '404_not_found': NotFound(),  # да простят меня все...
}
