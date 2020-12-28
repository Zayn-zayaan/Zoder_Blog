from django.urls import path
from home.views import home, about, contact, search, handlesignup, handlelogin, handlelogout, createpost

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('signup', handlesignup, name='handlesignup'),
    path('login', handlelogin, name='handlelogin'),
    path('logout', handlelogout, name='handlelogout'),
    path('createpost/', createpost, name='createpost'),
]