"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pixel.views import loginView,regView,index, upload_avatar
from pixel.views import process_data,get_label_data,search,biaoqian, isFollow, add_button
# from django.conf.urls import url ##新增
from django.urls import re_path
from django.conf import settings
from django.views import static
from django.conf.urls.static import static as ss

# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginView, name='login'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', loginView),  # 假设您有一个名为 home 的视图
    # path('/', loginView),
    path('reg/', regView),
    path('index/', index),
    path('api/process_data/<int:id>/', process_data, name='process_data'),
    path('api/add_button/<int:id>/', add_button, name='add_button'),
    path('api/get_label_data/<int:pixel_id>/', get_label_data, name='get_label_data'),
    path('search/', search, name='search'),
    path('api/followed_data/', isFollow, name='isFollow'),
    path('upload_avatar/', upload_avatar, name='upload_avatar'),

    path('biaoqian/', biaoqian, name='biaoqian'),
    re_path(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT},
        name='static'),

    # path('your_search_view/', your_search_view, name='your_search_view'),


]
if settings.DEBUG:
    urlpatterns += ss(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

