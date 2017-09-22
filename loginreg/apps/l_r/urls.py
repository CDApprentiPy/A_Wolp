from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="main"),
    url(r'^add/$', views.process, name="process"),
    url(r'^login/$', views.login, name="login"),
    url(r'^success/$', views.success, name="success"),
    url(r'^logout/$', views.logout, name="peace"),
    
    
    

]