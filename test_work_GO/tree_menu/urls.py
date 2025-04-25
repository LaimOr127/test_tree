from django.urls import path
from . import views

app_name = 'tree_menu'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('page/<path:page_path>/', views.page_view, name='page'),
] 