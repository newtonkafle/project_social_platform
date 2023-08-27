from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.home, name='home'),
    path('create-room/', views.createRoom, name='create-room'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:id>/', views.userProfile, name='user-profile'),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot-password', views.forgotPassword, name='forgot-password'),
    path('reset-password-validate/<uidb64>/<token>/',
         views.resetPasswordValidate, name='reset-password-validate'),
    path('reset-password', views.resetPassword, name='reset-password'),

]
