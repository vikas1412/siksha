from django.urls import path
from create_exam.views import ExamListView
from create_exam import views

urlpatterns = [
    path("", views.home, name="home"),

    path('list-all/', ExamListView.as_view(), name='exam'),

    # Fetch all questions at once
    path('<int:id>/preview-demo/', views.preview_exam, name='preview-demo'),

    # Fetch one by one using AJAX
    path('<int:id>/fetch-by-one/', views.preview_one_by_one, name='preview-one-by-one'),

    path('save-response/', views.save_user_response, name="save-user-response"),

    path('<int:id>/view/', views.view_exam, name='view'),
    path('upload-in-bulk/<int:id>/', views.upload_in_bulk, name='upload-questions-in-bulk'),

    path('<int:id>/del/', views.delete_all, name='delete-all-questions'),

    path('save-response/', views.save_response, name="save-response"),

    path('testing/', views.save_user_info, name="user_info"),

    path('add-user/', views.add_user, name="add-user"),
]