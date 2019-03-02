from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from shop import woocommerce
from django.http import HttpResponseRedirect


class BaseTemplateView(TemplateView):
    """Base for client Template View to make sure the user is authenticated"""
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(BaseTemplateView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('public:login')

class BaseView(View):
    """Base for client Template View to make sure the user is authenticated"""
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(BaseView, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('public:login')


class LoginPageView(TemplateView):
    template_name = "login.html"


class RegisterPageView(TemplateView):
    template_name = "register.html"


class DashboardPageView(BaseTemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardPageView, self).get_context_data(**kwargs)
        context['customers'] = woocommerce.get_all_customers()
        return context

class CustomerPageView(BaseTemplateView):
    template_name = "admin/customer.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerPageView, self).get_context_data(**kwargs)
        return context

class EditCustomer(BaseTemplateView):
    template_name = "admin/customer.html"
    def get_context_data(self, **kwargs):
        context = super(EditCustomer, self).get_context_data(**kwargs)
        customer_id = self.request.GET.get('id', 0)
        context['customer'] = woocommerce.get_customer(customer_id)
        return context

class Delete(BaseView):
    def get(self, request, *args, **kwargs):
        customer_id = request.GET["id"]
        data = woocommerce.delete_customer(customer_id)
        if data.get('data', {}).get('status', []) == 400:
            messages.error(request, "An error occurred deleting the user")
        else:
            messages.error(request, "User successfully deleted")
        return redirect('public:dashboard')

class SaveCustomer(BaseView):
    def post(self, request, *args, **kwargs):
        customer_dict = dict()
        billing = dict()
        shipping = dict()
        customer_id = request.POST.get('id', None)
        customer_dict['email'] = request.POST.get('email')
        customer_dict['first_name'] = request.POST.get('first_name')
        customer_dict['last_name'] = request.POST.get('last_name')
        customer_dict['username'] = request.POST.get('username')
        billing['first_name'] = request.POST.get('billing_first_name')
        billing['last_name'] = request.POST.get('billing_last_name')
        billing['company'] = request.POST.get('billing_company')
        billing['address_1'] = request.POST.get('billing_address_1')
        billing['address_2'] = request.POST.get('billing_address_2')
        billing['city'] = request.POST.get('billing_city')
        billing['state'] = request.POST.get('billing_state')
        billing['postcode'] = request.POST.get('billing_postcode')
        billing['country'] = request.POST.get('billing_country')
        billing['email'] = request.POST.get('billing_email')
        billing['phone'] = request.POST.get('billing_phone')
        shipping['first_name'] = request.POST.get('shipping_first_name')
        shipping['last_name'] = request.POST.get('shipping_last_name')
        shipping['company'] = request.POST.get('shipping_company')
        shipping['address_1'] = request.POST.get('shipping_address_1')
        shipping['address_2'] = request.POST.get('shipping_address_2')
        shipping['city'] = request.POST.get('shipping_city')
        shipping['state'] = request.POST.get('shipping_state')
        shipping['postcode'] = request.POST.get('shipping_postcode')
        shipping['country'] = request.POST.get('shipping_country')
        shipping['email'] = request.POST.get('shipping_email')
        shipping['phone'] = request.POST.get('shipping_phone')

        customer_dict['billing'] = billing
        customer_dict['shipping'] = shipping

        response = None
        if customer_id:
            response = woocommerce.update_customer(customer_id, customer_dict)
            if response.get('data', {}).get('status', []) == 400:
                message = response.get('data', {}).get('params', 'An error occurred updating')
                messages.error(request, message)
            else:
                messages.success(request, "Customer successfully updated")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            response = woocommerce.create_customer(customer_dict)
            if response.get('data', {}).get('status', []) == 400:
                message = response.get('data', {}).get('params', 'An error occurred updating')
                messages.error(request, message)
            else:
                messages.success(request, "Customer successfully created")
            return redirect('public:dashboard')


class Login(View):
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('public:dashboard')
        else:
            messages.error(request, "Wrong password or email combination")
            return redirect('public:login')

class Register(View):
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['repeatPassword']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        if password != re_password:
            messages.error(request, "Passwords don't match")
            return redirect('public:register')
        else:
            try:
                User.objects.create_user(
                    email=email,
                    username=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.error(request, "Account successfully created, please login")
                return redirect('public:login')
            except Exception as ex:
                if 'already exists' in str(ex):
                    messages.error(request, "Account already exists")
                else:
                    messages.error(request, "An error occurred please try again")
                return redirect('public:register')

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('public:login')


