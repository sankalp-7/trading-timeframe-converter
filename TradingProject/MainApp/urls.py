from django.urls import path
from.views import home,download
app_name='MainApp'
urlpatterns=[ 
    path('',home,name='home'),
    path('download/',download,name='get'),
]