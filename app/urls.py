from django.urls import path
from .views import(
	registration_view,
    data_display_view,
    add_subject_view,
    add_class_view
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'app'

urlpatterns = [
	path('register', registration_view, name="register"),
    path('login', obtain_auth_token, name="login"),
    path('/<username>', data_display_view, name="display"),
    path('/<username>/add-subject', add_subject_view, name="add-subject"),
    path('/<username>/<classname>/add-class', add_class_view, name="add-class"),

]