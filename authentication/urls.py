from django.urls import path

from .views import user, Login, Signup, logout

app_name = 'authentication'

urlpatterns = [
    path('user', user, name='user'),
    path('logout', logout, name='logout'),

    path('login', Login.as_view(), name='login'),
    path('signup', Signup.as_view(), name='signup'),
]