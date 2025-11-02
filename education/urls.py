from django.urls import path
from . import views


app_name = 'education'

urlpatterns = [
    path('', views.data_man, name='data_man'),
    path('scripts/', views.run_script_view, name='scripts'),
    # path('<int:tutor_id>/', views.tutor, name='tutor'),
    # path('<int:school_id>/', views.school, name='school'),
    # path('<int:course_id>/', views.course, name='course'),

]