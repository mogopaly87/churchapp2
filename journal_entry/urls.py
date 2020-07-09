from django.urls import path
from .views import journal_entry

app_name='journal_entry'


urlpatterns = [
    path('entry/', journal_entry, name='journal-entry'),
]