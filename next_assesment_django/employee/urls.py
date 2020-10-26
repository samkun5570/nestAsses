from django.contrib import admin
from django.urls import include, path
from .views import *

urlpatterns = [
    path('upload_sheet_link/<str:id>', upload_sheet_link, name='upload_sheet_link'),
    path('upload_sheet_api/<str:id>', upload_sheet_api, name='upload_sheet_api'),
    path('login/', login_request, name='login'),
    path('register/', register_request, name='register'),
    path("logout/", logout_request, name="logout"),
    path('', base, name='base'),
    path('employee/', create_employee, name='employee'),
]
