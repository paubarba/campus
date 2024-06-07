from django.urls import path

from . import views

app_name = 'quizzes'
urlpatterns = [
    # url: /quizzes/
    path("", views.index, name="index"),
    # url: /quizzes/1/attempt
    path("<int:quiz_id>/attempt", views.create, name="create"),
    # url: /quizes/1/store
    path("<int:quiz_id>/store", views.store, name="store"),
    # url: /quizzes/1/0105123
    path("<int:quiz_id>/<int:student_id>", views.detail, name="detail"),
]
