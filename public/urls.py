from django.urls import path
from public import views

app_name = 'public'

urlpatterns = [
    path('', views.LoginPageView.as_view(), name="login"),
    path('register', views.RegisterPageView.as_view(), name="register"),
    path('dashboard', views.DashboardPageView.as_view(), name="dashboard"),
    path('dologin', views.dologin, name="dologin"),
    path('doregister', views.doregister, name="doregister"),
    path('logout', views.user_logout, name="logout"),
]