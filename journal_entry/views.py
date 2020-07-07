from django.shortcuts import render
from .models import JournalEntry
from .forms import EntryForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users

# @login_required
# @allowed_users(allowed_roles=['supervisor'])
# def journal_entry(request):
#     JournalFormset = modelformset_factory(JournalEntry, fields='__all__', extra=1)
    

#     if request.method == 'POST':
#         form = JournalFormset(request.POST, queryset=JournalEntry.objects.none())
#         instance = form.save()
    
#     form = JournalFormset(queryset=JournalEntry.objects.none())
#     return render(request, 'journal_entry.html', {'form':form})