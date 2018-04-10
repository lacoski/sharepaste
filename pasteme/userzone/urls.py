from django.urls import path, re_path
from django.conf.urls import handler404, handler500

from . import views

urlpatterns = [
    # path('', views.list_paste_template, name = 'list_paste_template'),
    path('', views.index, name = 'index_page'),
    path('list_paste', views.list_paste_template, name = 'list_paste_template'),
    path('create_paste', views.create_paste_template, name = 'create_paste_template'),    
    path('update_paste/<int:id>', views.update_paste_template, name = 'update_paste_template'),
    path('delete_paste/<int:id>', views.delete_paste_template, name = 'delete_paste_template'),
    path('review_paste/<slug:id>', views.review_paste_template, name = 'review_paste_template'),
    path('go_to_paste/', views.go_to_paste_template, name = 'go_to_paste_template'),
    path('search_paste/', views.search_paste_template, name = 'search_paste_template'),
    path('create_paste_guest/', views.create_paste_guest_template, name = 'create_paste_guest_template'),
    path('create_tool_guest/', views.create_paste_tool_guest_template, name = 'create_paste_tool_guest_template'),
    path('review_paste_guest/<slug:id>', views.review_paste_guest_template, name = 'review_paste_guest_template'),
    path('go_to_paste_guest/', views.go_to_paste_guest_template, name = 'go_to_paste_guest_template'),    
    path('upload/', views.simple_upload, name = 'simple_upload'),
    path('read/', views.read_content_file, name = 'read_content_file'),
    
    
]
