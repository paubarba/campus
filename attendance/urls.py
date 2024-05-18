from django.urls import path

from . import views

app_name = 'attendance'
urlpatterns = [
    # url: /attendance/
    path("", views.index, name="index"),
    # url: /attendance/create
    path("create", views.create, name="create"),
    # url: /attendance/class5/
    path("class<int:class_id>/", views.detail, name="detail"),
    # url: /attendance/store
    path("store", views.store, name="store"),
]
