from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from Tax.views import Search_For_Tax, generate_tax_slip

app_name='taxes'


urlpatterns = [
    path('search_for_tax/', Search_For_Tax.as_view(), name='search_for_tax'),
    path('<int:member_id>/generate_tax_slip/', generate_tax_slip, name='generate_tax_slip'),
]