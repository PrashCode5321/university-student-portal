from django.contrib.auth.views import LoginView
from .forms import LoginForm


# Create your views here.
class MyLoginView(LoginView):
    authentication_form = LoginForm
    template_name = "registration/login.html"
