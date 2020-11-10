from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('user/', views.userPage, name="user-page"),

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('account/', views.accountSettings, name="account"),


    path('create_order/<str:pk>', views.createOrder, name="createOrder"),
    path('update_order/<str:pk>/', views.updateOrder, name="updateOrder"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="deleteOrder"),
]