from django.urls import path
from APP import views

urlpatterns = [
    path('', views.index, name="index"),
    path("index/", views.index, name="index"),
    path('login/', views.login, name='login'),
    path('check_login/', views.check_login, name='check_login'),
    path('register/', views.register, name='register'),
    path('check_register/', views.check_register, name='check_register'),
    path('logout/', views.logout, name="logout"),
    path('all_dishes/', views.all_dishes, name="all_dishes"),
    path('data_visualization/', views.data_visualization, name="data_visualization"),
    path('guess_youlike/', views.guess_youlike, name="guess_youlike"),
    path("like/<str:food_name>/<str:operate>", views.like),
    path("food_drink/", views.food_drink, name="food_drink"),
    path("food_staple/", views.food_staple, name="food_staple"),
    path("food_dishes/", views.food_dishes, name="food_dishes"),
    path("food_dessert/", views.food_dessert, name="food_dessert"),
    path("search/", views.search, name="search"),
    path("food_single/", views.food_single, name="food_single"),
    path("all_user/", views.all_user, name="all_user"),
    path("add_image/", views.add_image, name="add_image"),
    path("receive_image/", views.receive_image, name="receive_image"),

]
