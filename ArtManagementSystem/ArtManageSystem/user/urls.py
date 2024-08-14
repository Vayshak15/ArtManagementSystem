from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path,include
from user.views import signup

urlpatterns=[
    path('signup',signup,name='signup'),
    #path('login',LoginView.as_view(),name='signin'),
    #path('logout',LogoutView.as_view(),name='signout'),
    path('',include('django.contrib.auth.urls'))
]