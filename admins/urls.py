from django.urls import path
from admins.views import *

urlpatterns = [
    path('register1/',Register,name="register1"),
    path('login1/',Login1,name='login1'),
    path('dashboard/',Dashboard,name="dashboard"),
    path('add-center/', add_center, name='add_center'),
    path('update-center/<int:center_id>/', update_center, name='update_center'),
    path('delete-center/<int:center_id>/', delete_center, name='delete_center'),
    path('centers/',center_list, name='center_list'),
    path('dosage-details/', dosage_details, name='dosage_details'),
    path('booked-slots/', view_booked_slots, name='admin_booked_slots'),
    path('logout1/',logout1,name="logout1")
]
