from django.urls import path
from public import views

app_name = 'public'

urlpatterns = [
    path('', views.LoginPageView.as_view(), name="login"),
    path('register', views.RegisterPageView.as_view(), name="register"),
    path('dashboard', views.DashboardPageView.as_view(), name="dashboard"),
    path('dologin', views.Login.as_view(), name="dologin"),
    path('doregister', views.Register.as_view(), name="doregister"),
    path('logout', views.Logout.as_view(), name="logout"),
    path('delete', views.Delete.as_view(), name="delete"),
    path('customer', views.CustomerPageView.as_view(), name="customer"),
    path('customer/edit', views.EditCustomer.as_view(), name="edit_customer"),
    path('customer/save', views.SaveCustomer.as_view(), name="save_customer"),
]