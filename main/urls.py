from django.urls import path
from .views import main_page, info, sign_up, sign_in, secret_view, login_view


urlpatterns = [
    path("", main_page, name='main'),
    path("info", info, name='info'),
    path("sign_up", sign_up, name='sign_up'),
    path("sign_in", sign_in, name='sign_in'),
    path("secret", secret_view, name='secret'),
    path('login/', login_view, name='login'),
]
