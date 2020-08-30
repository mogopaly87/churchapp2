from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import RegistrationModel, GivingModel
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, View, UpdateView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.contrib import messages
from django.db.models import Sum
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
from .forms import RegForm
from django.views.decorators.csrf import csrf_exempt
import git
from .filters import GivingFilter
from journal_entry.decorators import allowed_users

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('update_giving.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# This view handles invalid url requests
def error_404_view(request, exception):
    return render(request, '404.html')


@login_required
def home(request):
    return render(request, 'home.html', {'title': 'Home Page'})

#----------------------- REGISTRATION----------------------------

# This view handles the registration of members
@login_required
def register(request):
    form = RegForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name').capitalize()
            last_name = request.POST.get('last_name').capitalize()
            middle_name = request.POST.get('middle_name').capitalize()
            date_of_birth = request.POST.get('date_of_birth')
            street_address = request.POST.get('street_address')
            postal_code = request.POST.get('postal_code')
            province = request.POST.get('province')
            country = request.POST.get('country').capitalize()
            phone = request.POST.get('phone_0')
            email = request.POST.get('email')
            # Use the Registration Model to create entries/objects
            RegistrationModel.objects.create(first_name=first_name, last_name=last_name, middle_name=middle_name,
                                            date_of_birth=date_of_birth, street_address=street_address,
                                            postal_code=postal_code, province=province, country=country, phone=phone,
                                            email=email)
            member = RegistrationModel.objects.filter(first_name=first_name, last_name=last_name, middle_name=middle_name,
                                                    date_of_birth=date_of_birth, street_address=street_address,
                                                    postal_code=postal_code, province=province, country=country, phone=phone,
                                                    email=email).last()
            messages.info(request, f'You have successfully added {member.first_name} {member.last_name}')
            form = RegForm()
            # return render(request, 'register_success.html', {'member': member})      
    return render(request, 'register.html', {'title': 'User Register', 'form': form})

#----------------------- RECORD GIVING----------------------------

# This view handles the logic of searching/filtering members before the
# 'post' view uses the result to post/add record to the GivingModel
@method_decorator(login_required, name='dispatch')
class GiveView(ListView):

    model = RegistrationModel
    context_object_name = 'members_list'
    template_name = 'DbEntry/giving.html'

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)
        title = "Post Giving"
        context["title"] = title
        return context

    def get_queryset(self):
        query = self.request.GET.get('fname')
        print(query)
        # since the page automatically passes 'None' to the 'query' variable
        #..here we check if what is passed is not 'None' before query is run
        if not query == None:
            queryset = RegistrationModel.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
            # if a valid query, check if name entered exists in db
            if queryset.exists():
                # if name exists, retrieve queryset
                return RegistrationModel.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
            else:
                # if name not in db return 'info' message
                messages.info(self.request, 'Sorry, the name you entered cannot be found!')



# This view handles the logic for posting/adding records to the GivingModel
# It first uses the info from the 'GiveView' to select the correct member to post on
# It uses the 'id' field which is a hidden field.
@login_required
def post(request):

    if request.method == 'POST':
        print(request.method)
        member_id2= request.POST.get('member_id2')
        giving_date = request.POST.get('giving_date')
        offering_amount = (request.POST.get('offering_amount'))
        tithe_amount = request.POST.get('tithe_amount')
        building_fund_amount = request.POST.get('building_fund_amount')
        other_amount = request.POST.get('Other_amount')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        print(first_name, giving_date, offering_amount, tithe_amount, building_fund_amount, other_amount)

        GivingModel.objects.create(members_id=member_id2, giving_date=giving_date, offering_amount=offering_amount, tithe_amount=tithe_amount, building_fund_amount=building_fund_amount, Other_amount=other_amount)

        messages.info(request, 'Thank you for giving today') 
    return render(request, 'post_success.html', {'title': 'Successful Giving'})


#----------------------- UPDATE MEMBER INFO----------------------------

# This class view is used to search for member(object) to update
@method_decorator(login_required, name='dispatch')
class UpdateSearch(ListView):

    model = RegistrationModel
    context_object_name = 'members_list'
    template_name = 'DbEntry/update.html'

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)
        title = "Update Member Info"
        context["title"] = title
        return context

    def get_queryset(self):
        query = self.request.GET.get('fname')
        print(query)
        # since the page automatically passes 'None' to the 'query' variable
        #..here we check if what is passed is not 'None' before query is run
        if not query == None:
            queryset = RegistrationModel.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
            # if a valid query, check if name entered exists in db
            if queryset.exists():
                # if name exists, return queryset
                return RegistrationModel.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
            else:
                # if name not in db, return 'info' message
                messages.info(self.request, 'Sorry, the name you entered cannot be found!')

# This view is used to update member info

@login_required
def updateForm(request, member_id):
    record = get_object_or_404(RegistrationModel, id=member_id)
    if request.method == 'POST':   
        print(request.method)
        first_name = request.POST.get('first_name').capitalize()
        middle_name = request.POST.get('middle_name').capitalize()
        last_name = request.POST.get('last_name') .capitalize()
        date_of_birth = request.POST.get('date_of_birth')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        postal_code = request.POST.get('postal_code')
        province = request.POST.get('province')
        country = request.POST.get('country').capitalize()

        update_query = RegistrationModel.objects.filter(id=member_id).update(
                                first_name=first_name, last_name=last_name,
                                middle_name=middle_name, date_of_birth=date_of_birth,
                                street_address=street_address, postal_code=postal_code,
                                province=province, country=country, phone=phone,
                                email=email)
        return redirect(reverse('update_search'))

    return render(request, 'update_form.html', {'record': record, 'title': 'Update Info Form'})


#----------------------- CORRECT GIVING AMOUNT RECEIVED ----------------------------#


# This view is used to ssearch for members giving to delete

@method_decorator(login_required, name='dispatch')
class Correct_Giving_Search(ListView):

    model = RegistrationModel
    context_object_name = 'members_list'
    template_name = 'DbEntry/correct_giving.html'

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)
        title = "Update Giving"
        context["title"] = title
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            query = self.request.GET.get('fname')
            print('The name is >>', query)
            # since the page automatically passes 'None' to the 'query' variable
            #..here we check if what is passed is not 'None' before query is run
            if not query == None:
                queryset = RegistrationModel.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
                # if a valid query, check if name entered exists in db
                if queryset.exists():
                    # if name exists, return queryset
                    return RegistrationModel.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
                else:
                    # if name not in db, return 'info' message
                    messages.info(self.request, 'Sorry, the name you entered cannot be found!')
            elif query == None:
                pass

@login_required
def get_transactions(request, member_id):
    transactions = get_list_or_404(GivingModel, members=member_id)
    paginator = Paginator(transactions, 7)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except  PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # if request.method == ''
    return render(request, 'update_giving_list.html', {'page': page, 'posts':posts, 'title': 'Giving Record', 'member_id':member_id})

@login_required
def get_transaction_object(request, giving_id):
    post = get_object_or_404(GivingModel, id=giving_id)
    print(post.members_id) # sanity check
    print(giving_id) # sanity check
    print('user is >>> ',request.user.first_name, request.user.last_name)

    if request.method == 'POST':
        offering = request.POST.get('offering')
        tithe = request.POST.get('tithe')
        building = request.POST.get('building')
        other = request.POST.get('other')

        GivingModel.objects.filter(id=giving_id).update(
                                offering_amount=offering,
                                tithe_amount=tithe,
                                building_fund_amount=building,
                                Other_amount=other)
        post = get_object_or_404(GivingModel, id=giving_id)
        logger.info('{} {} CHANGED: id:{} - O:{} - T:{} - B:{} - Ot:{}'.format(request.user.username, 
                                                                        request.user.last_name, 
                                                                        post.id, post.offering_amount,
                                                                        post.tithe_amount, post.building_fund_amount,
                                                                        post.Other_amount))
        return redirect(reverse('update_giving_list', args=(post.members_id,)))
    logger.info('{} {} ACCESSED: id:{} - O:{} - T:{} - B:{} - Ot:{}'.format(request.user.username, 
                                                                            request.user.last_name, 
                                                                            post.id, post.offering_amount,
                                                                            post.tithe_amount, post.building_fund_amount,
                                                                            post.Other_amount))
    return render(request, 'update_giving_object.html', {'post': post, 'title': 'Update This Record', 'member_id':post.members_id})


@login_required
@allowed_users(allowed_roles=['supervisor'])
def filterGivings(request):
    """This view is used to search for givings by date range,
    member, and/or the various giving types (offering, tithe,
    building funds, Other)"""
    giving_list = GivingModel.objects.all()
    giving_filter = GivingFilter(request.GET, queryset=giving_list)
    return render(request, 'giving_search_list.html', {'filter': giving_filter})

@csrf_exempt
def update(request):
    """ This function is used to link my github repo to my
    deployment server. Enables auto update after I push 
    to git."""
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        repo = git.Repo("mogononso.pythonanywhere.com/") 
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")