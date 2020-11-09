from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('user/<int:u_id>', views.user_quotes),
    path('quote/add', views.add),
    path('myaccount/<int:u_id>', views.profile),
    path('update/<int:u_id>', views.update),
    path('delete/<int:q_id>', views.delete),
    path('like/<int:q_id>', views.like),
]