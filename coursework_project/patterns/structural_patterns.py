from time import time


# добавление подкатегорий(доделаю, когда перестану отставать)
# from abc import abstractmethod, ABCMeta
#
# from creations_patterns import CoursePrototype
#
#
# class Component(metaclass=ABCMeta):
#
#     @abstractmethod
#     def get_components(self):
#         pass
#
#
# class Course(CoursePrototype, Component):
#
#     def __init__(self, name, category):
#         self.name = name
#         self.category = category
#
#     def get_components(self):
#         return self
#
#
# class Category(Component):
#     # реестр?
#     auto_id = 0
#
#     def __init__(self, name, category=None):
#         self.id = Category.auto_id
#         Category.auto_id += 1
#         self.name = name
#         self.category = category
#         self._child = set()
#
#     def get_components(self):
#         result = {self.name: {'sub_category_lst': set(), 'course_lst': set()}}
#         for child in self._child:
#             if isinstance(child, Category):
#                 result[self.name]['sub_category_lst'].add(child)
#                 child_result = child.get_components()
#                 result[self.name]['course_lst'].union(child_result[child.name]['course_lst'])
#             else:
#                 child_result = child.get_components()
#                 result[self.name]['course_lst'].add(child_result)
#         return result
#
#     def append(self, component):
#         self._child.add(component)
#
#     def remove(self, component):
#         self._child.discard(component)


# структурный паттерн - Декоратор
class AppRoute:
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Сам декоратор
        """
        self.routes[self.url] = cls()


# структурный паттерн - Декоратор
class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        """
        Сам декоратор
        """

        # это вспомогательная ф-я будет декорировать каждый отдельный метод класса, см. ниже
        def timeit(method):
            """
            нужен для того, что бы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            """

            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name} выполняется {delta:2.2f} мс')
                return result

            return timed

        return timeit(cls)
