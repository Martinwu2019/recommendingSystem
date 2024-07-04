from django.contrib import admin
from django.urls import path, include
from APP import views

urlpatterns = [
    # 直接使用跟路由
    # path('', views.index),
    # path('book/', views.book),
    # path('book/detail/<book_id>/', views.book_detail),
    # path('book/author/detail/', views.author_detail)

    # 使用子路由（一个应用对应一个子路由）命名空间namespace（可以解决屌用时有多个重名html问题）
    path('', include(('APP.urls', 'APP'), namespace='APP')),

    path('admin/', admin.site.urls),
]
