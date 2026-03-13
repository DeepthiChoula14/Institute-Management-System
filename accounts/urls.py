from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('signup/',views.signup_page,name='signup'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('mystudents/',views.mystudents_view,name='mystudents'),
    path('addstudents/',views.addstudents_view,name='addstudents'),
    path('updatestudent/<int:id>',views.updatestudent_view,name='updatestudent'),
    path('deletestudent/<int:id>',views.deletestudent_view,name='deletestudent'),

    # employee urls
    path('myemployees/',views.myemployee_view,name='myemployees'),
    path('deleteemployee/<int:id>', views.delete_employee_view, name='deleteemployee'),
    path('addemployee/',views.addemployees_view,name='addemployee'),
    path('updateemployee/<int:id>',views.updateemployee_view,name='updateemployee'),
]