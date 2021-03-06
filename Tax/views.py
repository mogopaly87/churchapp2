from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from DbEntry.models import RegistrationModel, GivingModel
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
from django.template import loader, RequestContext
import pdfkit
from datetime import date
import os
# from .models import Tithely


# Create your views here.

#-------------------------------PRINT TAX SLIP ------------------------------------
@method_decorator(login_required, name='dispatch')
class Search_For_Tax(ListView):

    model = RegistrationModel
    context_object_name = 'members_list'
    template_name = 'search_for_tax.html'

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)
        title = "Tax Slip"
        context["title"] = title
        return context

    def get_queryset(self):
        if self.request.method == 'GET':
            query = self.request.GET.get('entry')
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

@login_required
def generate_tax_slip(request, member_id):
    tax_year = request.GET.get('tax_year')
    queryset = GivingModel.objects.all()
    queryset2 = RegistrationModel.objects.get(id=member_id)
    today = date.today()
    date_issued = today.strftime("%B %d, %Y")
    if not tax_year == None:
        # query = get_list_or_404(GivingModel, members_id=member_id, giving_date__year=int(tax_year))
        query2 = queryset.filter(members_id=member_id, giving_date__year=int(tax_year)).aggregate(
            total_giving = Sum('offering_amount') + 
                            Sum('tithe_amount') + 
                            Sum('building_fund_amount') + 
                            Sum('Other_amount')
                            )
        total_giving = (query2['total_giving'])
        print(total_giving)
        #------------to view tax receipt as web page, run this:---------------------
        return render(request, 'tax_receipt_print.html', {'total_giving': total_giving, 
                                                    'tax_year': tax_year,
                                                    'date_issued': date_issued    ,
                                                    'member': queryset2})
        #--------------to view tax receipt as PDF, run any of the two options-----------------
        # html = loader.render_to_string('tax_receipt_print.html', {'total_giving': total_giving, 
        #                                                     'tax_year': tax_year,
        #                                                     'date_issued': date_issued,
        #                                                     'member': queryset2})
        # path_wkhtmltopdf = os.environ.get('PATH_WKHTMLTOPDF') #r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        # output = pdfkit.from_string(html, output_path=False, configuration=config)
        # OPTION 1---------to auto generate and download receipt, use:-----------
        # response = HttpResponse(output)
        # response['Content-Type'] = 'application/pdf'
        # response['Content-Disposition'] = 'attachment; filename = file.pdf'
        # return response
        # OPTION 2---------to generate receipt in browser, use:-------------------
        # response = HttpResponse(content_type="application/pdf")
        # response.write(output)
        # return response
    return render(request, 'generate_tax_slip.html', {'title': 'Print Tax Slip'})


"""USED TO TEST CUSTOM MANAGEMENT COMMAND FOR UPLOADING TITHELY CSV FILE"""
# import pandas as pd
# def tithely(request):
    
#     df = pd.read_csv(r'C:\Users\mogon\OneDrive\Documents\Django\churchapp2\Tax\tithely_donations.csv', sep=',')
#     df.columns = ['net_amount', 'fees', 'amount', 'cover_fee', 'first_name',
#             'last_name', 'giving_type', 'deposit_date', 'trans_date']
#     df_new = df[['net_amount', 'first_name', 'last_name', 'giving_type', 'trans_date']]
#     df_new.net_amount.apply(str)
#     df_new.dropna(inplace=True)
#     df_new['net_amount'] = df_new['net_amount'].map(lambda x: x.lstrip('$'))
#     df_new2 = df_new.astype({'net_amount':'float'})
#     df_new2 = df_new2.astype({'trans_date':'datetime64'})
    
#     givings = []
#     for i in range(len(df_new2)):
#         givings.append(
#             Tithely(
#                 net_amount = df_new2.iloc[i][0],
#                 first_name = df_new2.iloc[i][1],
#                 last_name = df_new2.iloc[i][2],
#                 giving_type = df_new2.iloc[i][3],
#                 trans_date = df_new2.iloc[i][4]
#             )
#         )
#     Tithely.objects.bulk_create(givings)