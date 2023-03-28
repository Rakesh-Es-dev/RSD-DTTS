from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name="account/login.html"),name="login"),
    path('login/',auth_views.LoginView.as_view(template_name="account/login.html"),name="login"),
    path('logout/',auth_views.LogoutView.as_view(),name="logout"),
    path('signup/',views.Signup.as_view(),name="signup"),
    path('profile/',views.Profile.as_view(),name="profile"),
    path('update/<pk>',views.UserUpdateView.as_view(),name='update'),
    path('cities/',views.cities,name="cities"),
    path('accept/',views.accept,name="accept"),
]