"""Модуль, содержащий контроллеры веб-приложения"""
from vaspupiy_framework.templator import render


class Index:
    def __call__(self):
        return '200 OK', render('index.html')


class Courses:
    def __call__(self):
        return '200 OK', render('courses.html')


class About:
    def __call__(self):
        return '200 OK', render('about.html')


class Feedback:
    def __call__(self):
        return '200 OK', render('feedback.html')


class NotFound:
    def __call__(self):
        return '404 WHAT', render('page404.html')
