from django.urls import path
from . import views

# NO LEADING SLASHES
urlpatterns = [
    path('', views.index, name='index'),
    path('createuser', views.createuser),
    path('login', views.login),
    path('success', views.dashboard),
    path('logout', views.logout),
    path('post', views.post),
    path('<int:messageid>/comment', views.comment),
]
