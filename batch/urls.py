from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView

from batch import views

urlpatterns = [
  path("<int:batch_id>/", views.batch_detail, name="batch-detail"),

]