from django.urls import path
from create_exam.views import ExamListView
from create_exam import views

urlpatterns = [
    path("", views.home, name="home"),

    path('list-all/', ExamListView.as_view(), name='exam'),

    # Fetch one by one using AJAX
    path('<int:exam_id>/fetch/', views.preview_one_by_one, name='preview-one-by-one'),

    path('<int:exam_id>/submit/', views.submit_exam, name="submit-exam"),

    path('save-response/', views.save_user_response, name="save-user-response"),

    path('<int:exam_id>/view/', views.view_exam, name='view'),
    path('bulk-upload/<int:exam_id>/', views.bulk_upload, name='upload-questions-in-bulk'),

    path('<int:exam_id>/del/', views.delete_all, name='delete-all-questions'),

    path('save-response/', views.save_response, name="save-response"),


    path('user/create/', views.save_user_info, name="new-user"),
    path('new/user/', views.save_new_user, name="save-new-user"),

    path('new/exam/', views.new_exam, name="new-exam"),
    path('new/batch/', views.new_batch, name="new-batch"),

    # Depriciating
    path('testing/', views.save_user_info, name="user_info"),
    path('add-user/', views.add_user, name="add-user"),
]