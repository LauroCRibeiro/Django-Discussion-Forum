from django.urls import path
from . import views
from .views import SignUpView
urlpatterns=[
    path('',views.home,name='home'),
    path('tag/<str:tag>',views.get_by_tag,name='via_tag'),
    path('user/<str:user>',views.get_by_user,name='via_user'),
    path('thread/<int:id>',views.thread_detail,name='thread-detail'),
    path('create-thread/',views.create_thread,name='create-thread'),
    path('submit-thread/',views.submit_thread,name='submit-thread'),
    path('reply/<int:thread_id>',views.submit_reply,name='reply'),
    path('login/',views.user_login,name='login'),
    path('register/',SignUpView.as_view(),name='register'),
    path('profile',views.user_profile,name='profile'),
    path('change-password',views.change_password,name='change-password'),
    path('setting',views.user_setting,name='setting'),
    path('threads',views.user_threads,name='threads'),
    path('replies',views.user_replies,name='replies'),
]