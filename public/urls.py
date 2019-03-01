from django.urls import path
from public import views

app_name = 'public'

urlpatterns = [
    path('', views.LoginPageView.as_view(), name="login"),
    path('register', views.RegisterPageView.as_view(), name="register"),
    path('dologin', views.dologin, name="dologin"),
    path('doregister', views.doregister, name="doregister"),
]