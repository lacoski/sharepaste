from django import template
from django.template import Template
from ..models import Paste

register = template.Library()

GROUP_FUNCTION= {'PASTE':
                    {
                        'Paste index':'/'
                    }, 
                'SHARE':
                    {
                        'SHARE TO':'path to share to', 
                        'SHARED BY':'path to shared by',
                    }
                }

@register.inclusion_tag('userzone/partial/sidebar_content.html')
def sidebar_content(request_user):
    main_navigation = 'GROUP FUNCTION'
    if request_user.is_authenticated:
        username = request_user.username
    return {
        'is_authenticated': request_user.is_authenticated,
        'username': request_user.username,
        'group_function': GROUP_FUNCTION,
        'main_navigation': main_navigation
    }

@register.inclusion_tag('userzone/partial/user_account_menu.html')
def User_Account_Menu(request_user):
    if request_user.is_authenticated:
        username = request_user.username
    
    return {
        'is_authenticated': request_user.is_authenticated,
        'username': request_user.username,
    }

@register.inclusion_tag('userzone/partial/public_pastes.html')
def Public_Pastes():
    list_pastes = Paste.objects.filter(user_own="")[:10]
    return {
        'list_pastes' : list_pastes,
    }

@register.inclusion_tag('userzone/partial/logo_base.html')
def Logo():    
    return {
        'none' : 'none',
    }

@register.inclusion_tag('userzone/partial/notification.html')
def Notification():    
    return {
        'none' : 'none',
    }

