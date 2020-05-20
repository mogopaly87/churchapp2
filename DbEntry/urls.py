from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from DbEntry.views import register, post, GiveView, UpdateSearch, updateForm, error_404_view, get_transactions, get_transaction_object, Correct_Giving_Search, update


urlpatterns = [
     path("update_server/", views.update, name="update"),
     path('post/', post, name='post_page'),
     path('giving/', GiveView.as_view(), name='search_member'),
     #     path('correct_giving/', correct_giving_search, name='correct_giving'),
     path('correct_giving/', Correct_Giving_Search.as_view(), name= 'correct_giving'),
     path('update_search/', UpdateSearch.as_view(), name='update_search'),
     path('<int:member_id>/update_giving_list/', get_transactions, name='update_giving_list'),
     path('<int:giving_id>/update_giving_object/',get_transaction_object, name='update_giving_object'),
     path('<int:member_id>/update_submit/', updateForm, name='update-submit'),
     path('register/', register, name='register_page'),
     path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
     path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
          name='password_reset'),
     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
          name='password_reset_done'),
     path('password-reset/confirm/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
          name='password_reset_confirm'),
     path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
          name='password_reset_complete'),
     path('home/', views.home, name='home_page'),
     path('', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
]

handler404 = 'DbEntry.views.error_404_view'