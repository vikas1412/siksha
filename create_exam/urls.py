from django.urls import path
from create_exam.views import ExamListView
from create_exam import views

urlpatterns = [
    path("", views.home, name="home"),

    path('list-all/', ExamListView.as_view(), name='exam'),
    path('<int:id>/preview-demo/', views.preview_exam, name='preview-demo'),

    path('<int:id>/view/', views.view_exam, name='view'),
    path('upload-in-bulk/<int:id>/', views.upload_in_bulk, name='upload-questions-in-bulk'),

    path('<int:id>/del/', views.delete_all, name='delete-all-questions'),

    path('save-response/', views.save_response, name="save-response"),

    path('check-to-do/', views.save_todo, name="todo"),
]

