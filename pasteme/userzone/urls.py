from django.urls import path, re_path

from . import views

urlpatterns = [
    # ex: /userzone/
    #path('', views.index, name='index'),    
    #path('nameform/', views.get_name),
    #path('thanks/', views.thanks),
    #path('paste/<int:paste_id>', views.get_detail_paste),
    #path('paste/<slug:paste_name>/<int:paste_id>', views.get_detail_paste),
    # path('', views.list_paste, name = 'list_pastes'),    
    # path('new', views.create_paste, name = 'create_pastes'),
    # path('update/<int:id>',views.update_paste, name = 'update_paste'),
    # path('delete/<int:id>',views.delete_paste, name = 'delete_paste'),
    path('', views.list_paste_template, name = 'list_paste_template'),
    path('create_paste', views.create_paste_template, name = 'create_paste_template'),    
    path('update_paste/<int:id>', views.update_paste_template, name = 'update_paste_template'),
    path('delete_paste/<int:id>', views.delete_paste_template, name = 'delete_paste_template'),
    path('review_paste_template/<slug:id>', views.review_paste_template, name = 'review_paste_template'),
]
