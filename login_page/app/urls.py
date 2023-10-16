
from . import views
from django.urls import path


urlpatterns = [
    path('',views.login_page,name="login_page"),
    path('signup/',views.signup_page,name="signup_page"),
    path('home/',views.home_page,name="home_page"),
    path('admin_dashboard/',views.admin_dashboard_page,name="admin_dashboard_page"),
    path('logout/', views.logout_page, name='logout_page'),
    path('save/', views.save_data, name='save_data'),
    path('delete/<int:user_id>', views.delete_data, name='delete_data'),
    # path('edit/<int:user_id>', views.edit_data, name='edit_data'),
    path('search/', views.search_data, name='search_data'),
]
