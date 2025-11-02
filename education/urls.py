from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    path('', views.data_man, name='data_man'),
    path('scripts/', views.run_script_view, name='scripts'),

]