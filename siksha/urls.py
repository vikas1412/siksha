from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    path("exam/", include("create_exam.urls")),
    path("", RedirectView.as_view(url="exam/", permanent=True)),
]
