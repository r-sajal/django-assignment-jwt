from django.urls import path
from . import views 

urlpatterns = [
    # path(r'',),
    # path(r'register',),
    # path('hello/', views.HelloView.as_view(), name ='hello'), 
    path('', views.loginpage, name ='loginpage'), 
    path(r'loginrequest', views.loginrequest, name ='loginrequest'), 
    path(r'showdata', views.Showdata, name ='showdata'),
    path(r'register', views.register, name ='register'),

]