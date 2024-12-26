from django.contrib import admin
from django.urls import path
from geekfeed import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('home/',views.home, name="home"),
    path('technology/',views.technology,name="technology"),
    path('technology/<int:tech_id>/', views.technology_detail, name='technology_detail'),
    path('games/',views.games,name="games"),
    path('games/<int:game_id>/',views.games_detail, name='games_detail'),
    path('contact/',views.contact,name="contact"),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('change_password', views.change_password, name='change_password'),
    path('inbox/', views.inbox, name='inbox'),
    path('send/', views.send_message, name='send_message'),
    path('mark_as_read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('responder/<int:recipient_id>/', views.responder_mensaje, name='responder_mensaje'),
    
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
