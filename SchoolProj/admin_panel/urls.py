from . import views
from django.urls import path
from .views import HomePage, StudentForms


app_name = "admin_panel"
urlpatterns = [
    path("home/", HomePage.as_view(), name="homepage"),
    path("register/student/", StudentForms.as_view(), name="form")
]
