from django.urls import path
from users import views

urlpatterns=[
     path("",views.home,name="home"),
     path('register/',views.Registration,name="register"),
     path('login/',views.login,name='login'),
     path('dashboard1/',views.dashboard1,name="dashboard1"),
     path('search-centers/', views.search_centers, name='search_centers'),
    path('book-slot/<int:center_id>/', views.book_slot, name='book_slot'),
    path('logout/',views.logout,name='logout')
]