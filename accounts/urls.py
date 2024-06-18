from django.urls import path

from . import views

urlpatterns = [
    path("register_home", views.register_home, name="register"),
    path("register_labour", views.register_labour, name="register_labour"),
    path("register_contractor", views.register_contractor, name="register_contractor"),
    path("login_home", views.login_home, name="login_home"),
    path("login_contractor", views.login_contractor, name="login_contractor"),
    path("login_labour", views.login_labour, name="login_labour"),
    path('logout', views.logout, name="logout"),
    path("contractor_home", views.contractor_home, name="contractor_home"),
    path("labour_home", views.labour_home, name="labour_home"),
    path("contractor_records", views.contractor_records, name="contractor_records"),
    path("labour_records", views.labour_records, name="labour_records"),
    path("labour_profile", views.labour_profile, name="labour_profile"),
    path("postjob", views.postjob, name="postjob"),
    path('update_labour/<int:id>',views.update_labour,name= 'update_labour'),
    path('do_update_labour/<int:id>/', views.do_update_labour, name='do_update_labour'),
    path('company_details',views.company_details, name='company_details'),
    path('company_form',views.company_form, name='company_form')
]