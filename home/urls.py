from django.urls import path, include
from home.views import  edit_dp,home, about, contact, search, handlesignup, handlelogin, handlelogout, createpost, edituser, custom_password_change, sendEmail
from django.contrib.auth import views as auth_views
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('signup', handlesignup, name='handlesignup'),
    path('login', handlelogin, name='handlelogin'),
    path('logout/', handlelogout, name='handlelogout'),
    path('createpost/', createpost, name='createpost'),
    path('account/', edituser, name='edituser'),
    path('change-password',
    custom_password_change.as_view(), name = 'change-password'),
    path('edit_dp/',edit_dp),

    #forgot password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    #verif email
    path('email/', include(mail_urls)),
    path('send_email/',sendEmail),
]