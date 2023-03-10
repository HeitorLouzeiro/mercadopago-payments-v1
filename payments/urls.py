from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('removecart/', views.removecart, name='removecart'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
]
