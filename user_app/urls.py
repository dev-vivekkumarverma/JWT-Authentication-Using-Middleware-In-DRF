from django.urls import path
from .views import register_user,auth_user

urlpatterns = [
    path("register/",register_user,name="create_new_user"),
    path("login/",auth_user,name='login_user'),
    
]
