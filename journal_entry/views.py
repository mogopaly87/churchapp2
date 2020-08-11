from django.shortcuts import render
from .models import JournalEntry
from .forms import EntryForm
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib import messages

@login_required
@allowed_users(allowed_roles=['supervisor'])
def journal_entry(request):
    
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid:
            instance = form.save()
            messages.success(request, f'Your entry has been added')
            form= EntryForm()
    else:
        form= EntryForm()
    
    return render(request, 'journal_entry.html', {'form':form})