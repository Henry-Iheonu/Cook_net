from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.signup_login, name='signup_login'),  # URL for the signup-login page
    path('home/', login_required(views.home), name='home'),
    path('post_food/', login_required(views.post_food), name='post_food'),
    path('signup_login', views.user_logout, name='logout'),
    path('delete_food/<int:id>/', views.delete_food, name='delete_food'),
    path('food/<int:id>/', views.food_detail, name='food_detail'),
]
