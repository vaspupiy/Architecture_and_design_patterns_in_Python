from views import Index, About, Courses, Feedback, NotFound

# Набор привязок: путь-контроллер
routes = {
    '/': Index(),
    '/courses/': Courses(),
    '/about/': About(),
    '/feedback/': Feedback(),
    #  добавил возможность выводить 404 ошибку, оставляя навигационную панель(футтер и хедер)
    '404_not_found': NotFound(),  # да простят меня все...
}
