from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd


from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, date, time, timedelta

from .forms import AddIncome, AddSpendings, AddMoneySource, AddSpendingKind, AddCash, AddCashKind, Analysing

# Create your views here.

from .models import Income, Spendings, MoneySource, SpendingKind, Cash, CashKind
from django.utils import timezone, dateformat

from django.core.mail import EmailMessage


@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    
    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    num_operations_income = Income.objects.all().count()
    if num_operations_income:
        
        num_operations_income_today = Income.objects.all().filter(date_field= date_today).count()
    else:
        num_operations_income_today = 0

    num_operations_spendings = Spendings.objects.all().count()
    if num_operations_spendings:
        
        num_operations_spendings_today = Spendings.objects.all().filter(date_field= date_today).count()
    else:
        num_operations_spendings_today = 0
    
    num_source = str(MoneySource.objects.all().count())
    
    num_kinds = str(SpendingKind.objects.all().count())

    date_t = datetime.strptime(date_today, "%Y-%m-%d")
    date_t = date_t.date()
    
    delta_week = timedelta(days=7)
    week_before = date_t-delta_week
    
    delta_month = timedelta(days=30)
    month_before = date_t-delta_month
        
    income_week = Income.objects.all().filter(date_field__range=[str(week_before), str(date_t)])
    
    week_income_ammount = 0
    for p in income_week:
        week_income_ammount = week_income_ammount + p.ammount

    income_month = Income.objects.all().filter(date_field__range=[str(month_before), str(date_t)])
    
    month_income_ammount = 0
    for p in income_month:
        month_income_ammount = month_income_ammount + p.ammount

    
    spendings_week = Spendings.objects.all().filter(date_field__range=[str(week_before), str(date_t)])
    week_spendings_ammount = 0
    for p in spendings_week:
        week_spendings_ammount = week_spendings_ammount + p.ammount


    spendings_month = Spendings.objects.all().filter(date_field__range=[str(month_before), str(date_t)])
    month_spendings_ammount = 0
    for p in spendings_month:
        month_spendings_ammount = month_spendings_ammount + p.ammount

    week_income_ammount = round(week_income_ammount, 2)
    month_income_ammount = round(month_income_ammount, 2)
    week_spendings_ammount = round(week_spendings_ammount, 2)
    month_spendings_ammount = round(month_spendings_ammount, 2)
    week_balance = round(week_income_ammount - week_spendings_ammount, 2)
    month_balance = round(month_income_ammount - month_spendings_ammount, 2)
    #balance_week = datetime.date(date_t.year, date_t.month, date_t.day-6)
    #balance_month = datetime.date(date_t.year, date_t.month-1, date_t.day-1)      
    context = {
        'num_operations_income':num_operations_income,
        'num_operations_income_today':num_operations_income_today,
        'num_operations_spendings':num_operations_spendings,
        'num_operations_spendings_today':num_operations_spendings_today,
        'num_source':num_source,
        'num_kinds':num_kinds,
        'date_today': date_today,
        'week_income_ammount': week_income_ammount,
        'month_income_ammount': month_income_ammount,
        'week_spendings_ammount': week_spendings_ammount,
        'month_spendings_ammount': month_spendings_ammount,
        'week_balance': week_balance,
        'month_balance': month_balance,
        }
    
    return render(request, 'index.html', context)

@login_required
def income_view(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    
    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    num_operations = str(Income.objects.all().count())
    if num_operations:
        num_operations_today = Income.objects.all().filter(date_field= date_today).count()
    else:
        num_operations_today = 0
    
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddIncome(request.POST)


        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            income_item = Income()

            income_item.date_field = form.cleaned_data['date_field']
            income_item.source = form.cleaned_data['source']
            income_item.ammount = form.cleaned_data['ammount']
            income_item.cash_kind_income = form.cleaned_data['cash_kind_income']
            income_item.comment = form.cleaned_data['comment']
                   
            income_item.save()

            cash_item = Cash()
            cash_item.date_field = form.cleaned_data['date_field']

            cash_item.cash_kind = form.cleaned_data['cash_kind_income']
            cash_item.ammount = form.cleaned_data['ammount']
            cash_item.comment = form.cleaned_data['comment']

            cash_item.save()


            # redirect to a new URL:
            return HttpResponseRedirect('success_add')

    # If this is a GET (or any other method) create the default form.
    else:
        
        form = AddIncome(initial={'date_field': date_today, 'comment': '0'})


    money_source_objects = MoneySource.objects.all()
    context = {
        'form': form,
        'money_source_objects': money_source_objects,
        'num_operations':num_operations, 
        'num_operations_today':num_operations_today, 
        'date_today': date_today
    }

    return render(request, 'income.html', context)

def income_success_add(request):

    

    return render(request, 'success_add.html')


def add_new_source(request):

    errors = 0
    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    num_operations = str(Income.objects.all().count())
    if num_operations:
        num_operations_today = Income.objects.all().filter(date_field= date_today).count()
    else:
        num_operations_today = 0

    if request.method == 'POST':
        
        form = AddMoneySource(request.POST)

        if form.is_valid():
            new_source = MoneySource()

            new_source.first_level_source = form.cleaned_data['first_level_source']
            
            new_source.second_level_source = form.cleaned_data['second_level_source']

            

            new_source.save()

            # redirect to a new URL:
            return HttpResponseRedirect('success_add')
        else:
            errors = form.errors

    else:
        
        form = AddMoneySource()

    

    all_entries = MoneySource.objects.all()
    first_level = []
    for p in all_entries:
        if p.first_level_source not in first_level:
            first_level.append(p.first_level_source)

    second_level = []
    for d in all_entries:
        if d.second_level_source not in second_level:
            second_level.append(d.second_level_source)
      
    context = {
        'errors': errors,
        'form': form,
        'first_level': first_level,
        'second_level': second_level,
        'num_operations':num_operations, 
        'num_operations_today':num_operations_today, 
        'date_today': date_today
    }

    return render(request, 'add_new_source.html', context)
    
    
def add_new_spending_kind(request):

    errors = 0
    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    num_operations = str(Spendings.objects.all().count())
    if num_operations:
        num_operations_today = Spendings.objects.all().filter(date_field= date_today).count()
    else:
        num_operations_today = 0

    if request.method == 'POST':
        
        form = AddSpendingKind(request.POST)

        if form.is_valid():
            new_spending_kind = SpendingKind()

            new_spending_kind.first_level_kind = form.cleaned_data['first_level_kind']
            
            new_spending_kind.second_level_kind = form.cleaned_data['second_level_kind']

            

            new_spending_kind.save()

            # redirect to a new URL:
            return HttpResponseRedirect('success_add')
        else:
            errors = form.errors

    else:
        
        form = AddSpendingKind()
    
    all_entries = SpendingKind.objects.all()
    first_level = []
    for p in all_entries:
        if p.first_level_kind not in first_level:
            first_level.append(p.first_level_kind)

    second_level = []
    for d in all_entries:
        if d.second_level_kind not in second_level:
            second_level.append(d.second_level_kind)
    
    context = {
        'errors': errors,
        'form': form,
        'first_level': first_level,
        'second_level': second_level,
        'num_operations':num_operations, 
        'num_operations_today':num_operations_today, 
        'date_today': date_today
    }

    return render(request, 'add_new_spending_kind.html', context) 
   

@login_required
def spendings_view(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    
    spendings_kind_objects = SpendingKind.objects.all()
    
    first_level_kind_unique = [p.first_level_kind for p in spendings_kind_objects]
    
    second_level_kind_unique = [p.second_level_kind for p in spendings_kind_objects]
    
    first_level_kind_unique_tuple = []
    second_level_kind_unique_tuple = []
    
    increment = 0
    for i in first_level_kind_unique:
        increment +=1
        to_add = [increment, i]
        to_add = tuple(to_add)
        first_level_kind_unique_tuple.append(to_add)
        
    first_level_kind_unique_tuple = tuple(first_level_kind_unique_tuple)
        
    increment_1 = 0
    for i in second_level_kind_unique:
        increment_1 +=1
        to_add = [increment_1, i]
        to_add = tuple(to_add)
        second_level_kind_unique_tuple.append(to_add)


    second_level_kind_unique_tuple = tuple(second_level_kind_unique_tuple)
    




    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    num_operations = str(Spendings.objects.all().count())
    if num_operations:
        num_operations_today = Spendings.objects.all().filter(date_field= date_today).count()
    else:
        num_operations_today = 0
    
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddSpendings(request.POST)
        

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            spendings_item = Spendings()
            
            

            spendings_item.date_field = form.cleaned_data['date_field']
            
            spendings_item_kind_to_add = form.cleaned_data['kind']
            spendings_item.kind = spendings_item_kind_to_add
            
            cash_kind_in_spending = form.cleaned_data['cash_kind_spending']
            spendings_item.cash_kind_spending = cash_kind_in_spending
            spendings_item.ammount = form.cleaned_data['ammount']
            spendings_item.comment = form.cleaned_data['comment']
            spendings_item.save()

            spendings_item_cash = Cash()
            spendings_item_cash.date_field = form.cleaned_data['date_field']
            spendings_item_cash.cash_kind = cash_kind_in_spending
            spendings_item_cash.ammount = - float(form.cleaned_data['ammount'])
            spendings_item_cash.purpose = False
            spendings_item_cash.comment = 'Учтен расход'
            spendings_item_cash.save()


            # redirect to a new URL:
            return HttpResponseRedirect('success_add')
        

    # If this is a GET (or any other method) create the default form.
    else:
        
        form = AddSpendings(initial={'date_field': date_today, 'comment': '0'})
    
    spendingkind_objects = SpendingKind.objects.all()

    spendingkind_first_level = []
    spendingkind_second_level = []

    for p in spendingkind_objects:
        if p.first_level_kind not in spendingkind_first_level:
            spendingkind_first_level.append(p.first_level_kind)
        if p.second_level_kind not in spendingkind_second_level:
            spendingkind_second_level.append(p.second_level_kind)
    
    structure_spendingkind = {}
    second_levei_in_dict = []

    for p in spendingkind_objects:
        if p.first_level_kind not in structure_spendingkind.keys():
            second_levei_in_dict = [{'id': a.id, 'name': a.second_level_kind} for a in spendingkind_objects.filter(first_level_kind=p.first_level_kind)]

            structure_spendingkind[p.first_level_kind] = second_levei_in_dict
        
    tuple_structured_spendingkind = []
    
    for i in structure_spendingkind.keys():
        tuple_to_add = []
        tuple_to_add.append(i)
        tuple_to_add.append(structure_spendingkind[i])
        tuple_to_add = tuple(tuple_to_add)
        tuple_structured_spendingkind.append(tuple_to_add)

    print (tuple_structured_spendingkind)

    context = {
        'form': form,
        'num_operations':num_operations, 
        'num_operations_today':num_operations_today, 
        'date_today': date_today,
        'spendingkind_objects': spendingkind_objects,
        'spendingkind_first_level': spendingkind_first_level,
        'spendingkind_second_level': spendingkind_second_level,
        'structure_spendingkind': structure_spendingkind,
        'tuple_structured_spendingkind': tuple_structured_spendingkind

    }

    return render(request, 'spendings.html', context)

def spending_success_add(request):

    return render(request, 'success_add_spendings.html')



@login_required
def cash_view(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    
    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    num_operations_cash = Cash.objects.all().count()
    if num_operations_cash:
        
        num_operations_cash_today = Cash.objects.all().filter(date_field= date_today).count()
    else:
        num_operations_cash_today = 0

    num_cash_kind = str(CashKind.objects.all().count())
    

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = AddCash(request.POST)


        # Check if the form is valid:
        if form.is_valid() and form.cleaned_data['purpose']:
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            cash_item = Cash()
            cash_item.date_field = form.cleaned_data['date_field']

            cash_item.cash_kind = form.cleaned_data['cash_kind']
            cash_item.ammount = form.cleaned_data['ammount']
            cash_item.purpose = form.cleaned_data['purpose']
            cash_item.comment = form.cleaned_data['comment']
                   
            cash_item.save()

            # redirect to a new URL:
            return HttpResponseRedirect('success_add')

        elif form.is_valid() and form.cleaned_data['purpose']==False:

            
            cash_item = Cash()
            cash_item.date_field = form.cleaned_data['date_field']
            cash_item.cash_kind = form.cleaned_data['cash_kind']
            cash_item.purpose = form.cleaned_data['purpose']
            
            
            cash_to_check = [p.ammount for p in Cash.objects.all().filter(cash_kind= form.cleaned_data['cash_kind'])]
            cash_to_check_sum = 0

            for i in cash_to_check:
                cash_to_check_sum = cash_to_check_sum + i
            cash_to_check_sum = round(cash_to_check_sum, 2)

            cash_fact = form.cleaned_data['ammount']

            cash_checking_result = cash_fact - cash_to_check_sum
            cash_checking_result = round(cash_checking_result, 2)
            cash_item.ammount = round(cash_checking_result, 2)

            cash_kind_analise = form.cleaned_data['cash_kind']
            

            cash_item.comment = 'Учтено расхождение'


            if cash_item.ammount != 0:
                cash_item.save()
            
            context = {
                'cash_fact': cash_fact,
                'cash_to_check_sum': cash_to_check_sum,
                'cash_checking_result': cash_checking_result,
                'cash_kind_analise':cash_kind_analise, 
                'date_today': date_today,
            }



            return render(request, 'cash_mistake_accounting.html', context)



    # If this is a GET (or any other method) create the default form.
    else:
        
        form = AddCash(initial={'date_field': date_today, 'purpose': False, 'comment': '0'})

    cash_kind_objects = CashKind.objects.all()
    all_entries_cash = Cash.objects.all()
    
    last_cash_entries = []
    for p in cash_kind_objects:
        filtered = all_entries_cash.filter(cash_kind_id=p.id)
        if filtered:
            last_cash_entries.append(filtered.latest('id'))

        
    cash_kind_in_cash_on_today = []
    for p in all_entries_cash:
        if str(p.cash_kind) not in cash_kind_in_cash_on_today:
            cash_kind_in_cash_on_today.append(str(p.cash_kind))

    print(cash_kind_in_cash_on_today)
    cash_on_today = cash_kind_in_cash_on_today.copy()
    increment = 0
    for c in cash_on_today:
        cash_on_today[increment] = [c, 0]
        increment = increment + 1

    for p in all_entries_cash:
        if str(p.cash_kind) in cash_kind_in_cash_on_today:
            index = cash_kind_in_cash_on_today.index(str(p.cash_kind))
            cash_on_today[index][1] = cash_on_today[index][1] + p.ammount
            cash_on_today[index][1] = round(cash_on_today[index][1], 2)
    
    print(cash_on_today)


          
    context = {
        'form': form,
        'cash_on_today': cash_on_today,
        'cash_kind_objects': cash_kind_objects,
        'num_operations_cash':num_operations_cash, 
        'num_operations_cash_today':num_operations_cash_today,
        'num_cash_kind':num_cash_kind,
        'date_today': date_today
    }

    return render(request, 'cash.html', context)


def cash_success_add(request):

    return render(request, 'success_add_cash.html')


def add_new_cashkind(request):

    errors = 0
    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    num_operations_cash = Cash.objects.all().count()
    if num_operations_cash:
        
        num_operations_cash_today = Cash.objects.all().filter(date_field= date_today).count()
    else:
        num_operations_cash_today = 0

    num_cash_kind = str(CashKind.objects.all().count())

    if request.method == 'POST':
        
        form = AddCashKind(request.POST)

        if form.is_valid():
            new_source = CashKind()

            new_source.first_level_cashkind = form.cleaned_data['first_level_cashkind']
            
            new_source.second_level_cashkind = form.cleaned_data['second_level_cashkind']

            

            new_source.save()

            # redirect to a new URL:
            return HttpResponseRedirect('success_add')
        else:
            errors = form.errors

    else:
        
        form = AddCashKind()

    

    all_entries = CashKind.objects.all()
    first_level = []
    for p in all_entries:
        if p.first_level_cashkind not in first_level:
            first_level.append(p.first_level_cashkind)

    second_level = []
    for d in all_entries:
        if d.second_level_cashkind not in second_level:
            second_level.append(d.second_level_cashkind)
        

    context = {
        'errors': errors,
        'form': form,
        'first_level': first_level,
        'second_level': second_level,
        'num_operations_cash':num_operations_cash, 
        'num_operations_cash_today':num_operations_cash_today,
        'num_cash_kind':num_cash_kind,
        'date_today': date_today
    }

    return render(request, 'add_new_cashkind.html', context)

@login_required
def analysing(request):

    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    num_operations_income = Income.objects.all().count()
    
    num_operations_spendings = Spendings.objects.all().count()
    
    num_operations_cash = Cash.objects.all().count()

    first_operation_income = 0
    last_operation_income = 0
    if Income.objects.all().count():
        first_operation_income = Income.objects.all().earliest('id').date_field.strftime("%Y-%m-%d")
        last_operation_income = Income.objects.latest('id').date_field.strftime("%Y-%m-%d")
    
    first_operation_spending = 0
    last_operation_spending = 0
    if Spendings.objects.all().count():
        first_operation_spending = Spendings.objects.all().earliest('id').date_field.strftime("%Y-%m-%d")
        last_operation_spending = Spendings.objects.latest('id').date_field.strftime("%Y-%m-%d")
    
    first_operation_cash = 0
    last_operation_cash = 0
    if Cash.objects.all().count():
        first_operation_cash = Cash.objects.all().earliest('id').date_field.strftime("%Y-%m-%d")
        last_operation_cash = Cash.objects.latest('id').date_field.strftime("%Y-%m-%d")
        
   

    def structured_tuple(model_name):
        first_lev = []
        second_lev = []
        all_field_names = [f.name for f in model_name._meta.fields]
        obj = model_name.objects.all()
        
        for i in obj.values_list(all_field_names[1], flat=True):
            if i not in first_lev:
                first_lev.append(i)
        
        for i in obj.values_list(all_field_names[2], flat=True):
            if i not in second_lev:
                second_lev.append(i)
    
        structure_form = {}
        second_level_in = []
         
        for i in first_lev:
            if i not in structure_form.keys():
                second_level_in =  [a for a in obj.all().filter(**{all_field_names[1]:i}).values_list(all_field_names[2], flat=True)]
                structure_form[i] = second_level_in
        
        tuple_structured = []
    
        for i in structure_form.keys():
            tuple_to_add = []
            tuple_to_add.append(i)
            tuple_to_add.append(structure_form[i])
            tuple_to_add = tuple(tuple_to_add)
            tuple_structured.append(tuple_to_add)

        return tuple_structured

    def result_analising(result):
        
        result_represent = []
        date_result = []
        
        for c in result:
            if date_result and str(c.date_field) == str(date_result[0]):
                date_result[1] = date_result[1] + c.ammount
                date_result[1] = round(date_result[1], 2)
            else:
                if date_result:
                    result_represent.append(date_result)
                    date_result = []
                date_result.append(str(c.date_field))
                date_result.append(c.ammount)




        return result_represent





   
    tuple_structured_spendingkind = structured_tuple(SpendingKind)
    tuple_structured_moneysource = structured_tuple(MoneySource)
    tuple_structured_cashkind = structured_tuple(CashKind)

    if request.method == 'POST':
                
        form = Analysing(request.POST)

        if form.is_valid():
            
            date_begin = form.cleaned_data['date_begin']
            date_end = form.cleaned_data['date_end']
            main = form.cleaned_data['main']
            firstLEV = form.cleaned_data['firstLEV']
            secondLEV = form.cleaned_data['secondLEV']

            
            result =[]

            if main == 'income':
                                
                if firstLEV:
                    if secondLEV:
                        result = Income.objects.all().filter(source__second_level_source=secondLEV).filter(date_field__range=[date_begin, date_end])
                        result = result_analising(result)

                    else:
                        result = Income.objects.all().filter(source__first_level_source=firstLEV).filter(date_field__range=[date_begin, date_end])
                        result = result_analising(result)

                else:
                    result = Income.objects.all().filter(date_field__range=[date_begin, date_end])
                    result = result_analising(result)

            elif main =='spendings':
                if firstLEV:
                    if secondLEV:
                        result = Spendings.objects.all().filter(kind__second_level_kind=secondLEV).filter(date_field__range=[date_begin, date_end])
                        result = result_analising(result)

                    else:
                        result = Spendings.objects.all().filter(kind__first_level_kind=firstLEV).filter(date_field__range=[date_begin, date_end])
                        result = result_analising(result)

                else:
                    result = Spendings.objects.all().filter(date_field__range=[date_begin, date_end])
                    result = result_analising(result)
                #result = Spendings.objects.all().filter(**{a:1})

            elif main =='cash':

                if firstLEV:
                    if secondLEV:
                        result = Cash.objects.all().filter(cash_kind__second_level_cashkind=secondLEV).filter(date_field__range=[date_begin, date_end])
                        result = result_analising(result)

                    else:
                        result = Cash.objects.all().filter(cash_kind__first_level_cashkind=firstLEV).filter(date_field__range=[date_begin, date_end])
                        result = result_analising(result)

                else:
                    result = Cash.objects.all().filter(date_field__range=[date_begin, date_end])
                    result = result_analising(result)
                #result = Cash.objects.all().filter(**{a:1}) 

            elif main == 'common':
                print('common')
                result_income = {}
                query_result_income = Income.objects.all().filter(date_field__range=[date_begin, date_end])
                for q in query_result_income:
                    
                    if result_income:
                        
                        for res in result_income:
                            print(res)
                            
                            if str(q.date_field) in result_income.keys():
                                print(res[0])
                                result_income[str(q.date_field)].append([str(q.source), q.ammount])
                                break
                            else:
                                result_income[str(q.date_field)] = [[str(q.source), q.ammount]]
                                break
                            
                    else:
                        result_income[str(q.date_field)] = [[str(q.source), q.ammount]]


                result_spending = {}
                query_result_spending = Spendings.objects.all().filter(date_field__range=[date_begin, date_end])
                for q in query_result_spending:
                    if result_spending:
                        
                        for res in result_spending:
                            if str(q.date_field) in result_spending.keys():

                                result_spending[str(q.date_field)].append([str(q.kind), q.ammount])
                                break
                            else:
                                result_spending[str(q.date_field)] = [[str(q.kind), q.ammount]]
                                break
                            
                    else:
                        result_spending[str(q.date_field)] = [[str(q.kind), q.ammount]]

                print(result_income)
                print(result_spending)

                result = result_income.copy()

                for d in result:
                    print(d)
                    result[d] = {'income': result_income[d], 'spending':[]}

                for d in result_spending:
                    if d in result.keys():
                        result[d]['spending'] = result_spending[d]
                    else:
                        result[d] = {'income': [], 'spending': result_spending[d]}

                print(result)
                delta = date_end - date_begin
                delta = delta.days + 1

                context_common = {
                            'date_begin': date_begin, 
                            'date_end': date_end,
                            'delta': delta,
                            'main': main,
                            'result': result,
                            'date_today': date_today,
                            }
                return render(request, 'analysing_result_common.html', context_common)

            print(result)


            
            if main == 'income':
                main ='Доходы'
            elif main == 'spendings':
                main = 'Расходы'
            elif main == 'cash':
                main = 'Имеющиеся средства'
            elif main == 'common':
                main = 'Операции по порядку'
            
            delta = date_end - date_begin
            delta = delta.days + 1
            
            

            context_inner = {
                            'date_begin': date_begin, 
                            'date_end': date_end,
                            'delta': delta,
                            'main': main,
                            'firstLEV': firstLEV,
                            'secondLEV': secondLEV,
                            'result': result,
                            'date_today': date_today,
                            }


            return render(request, 'analysing_result.html', context_inner)

        else:
            print(form.errors)
    else:
        form = Analysing()
        
        

    context={
            'form': form,
            'num_operations_income':num_operations_income,
            'num_operations_spendings':num_operations_spendings, 
            'num_operations_cash': num_operations_cash,
            'date_today': date_today,
            'first_operation_income': first_operation_income,
            'last_operation_income': last_operation_income,
            'first_operation_spending': first_operation_spending,
            'last_operation_spending': last_operation_spending,
            'first_operation_cash': first_operation_cash,
            'last_operation_cash': last_operation_cash,
            'tuple_structured_spendingkind': tuple_structured_spendingkind,
            'tuple_structured_moneysource': tuple_structured_moneysource,
            'tuple_structured_cashkind': tuple_structured_cashkind,
            }

    return render(request, 'analysing.html', context)



@login_required
def sending_excel(request):

    date_today = dateformat.format(timezone.now(), 'Y-m-d')

    dict_info = request.GET

    email = dict_info['email']    
    date_begin = dict_info['date_begin']
    date_end = dict_info['date_end']
   
    date_begin = datetime.strptime(date_begin, "%b. %d, %Y")
    
    date_end = datetime.strptime(date_end, "%b. %d, %Y")
    
    

    result_income = {}
    query_result_income = Income.objects.all().filter(date_field__range=[date_begin, date_end])
    for q in query_result_income:
        if result_income:
            for res in result_income:
                
                if str(q.date_field) in result_income.keys():
                    
                    result_income[str(q.date_field)].append([str(q.source), q.ammount])
                    break
                else:
                    result_income[str(q.date_field)] = [[str(q.source), q.ammount]]
                    break
                            
        else:
            result_income[str(q.date_field)] = [[str(q.source), q.ammount]]


    result_spending = {}
    query_result_spending = Spendings.objects.all().filter(date_field__range=[date_begin, date_end])
    for q in query_result_spending:
        if result_spending:
            for res in result_spending:
                if str(q.date_field) in result_spending.keys():
                    result_spending[str(q.date_field)].append([str(q.kind), q.ammount])
                    break
                else:
                    result_spending[str(q.date_field)] = [[str(q.kind), q.ammount]]
                    break
                            
        else:
            result_spending[str(q.date_field)] = [[str(q.kind), q.ammount]]
    
    result = result_income.copy()

    for d in result:
        
        result[d] = {'income': result_income[d], 'spending':[]}

    for d in result_spending:
        if d in result.keys():
            result[d]['spending'] = result_spending[d]
        else:
            result[d] = {'income': [], 'spending': result_spending[d]}

    date_DF = [d for d in result.keys()]
    
    income_DF = []
    for d in result:
        to_add_str = ''
        for item in result[d]['income']:
            to_add_str = to_add_str+item[0]+' '+str(item[1])+', '
        
        to_add_str = to_add_str[:-2]
        
        income_DF.append(to_add_str)

      
    spending_DF = []
    for d in result:
        to_add_str = ''
        for item in result[d]['spending']:
            to_add_str = to_add_str+item[0]+' '+str(item[1])+', '
        
        to_add_str = to_add_str[:-2]
        
        spending_DF.append(to_add_str)
    
    df = pd.DataFrame({
        'Дата': date_DF,
        'Доходы':income_DF,
        'Расходы': spending_DF,
        })
    print(df)
    date_begin = str(date_begin.date())
    date_end = str(date_end.date())
    date_now = dateformat.format(timezone.now(), 'Y-m-d H-i')
    name_new_file = 'money_move/emails/Analysing_com'+ date_begin+'--'+date_end+' '+date_now+'.xlsx'
    
    export_excel = df.to_excel(name_new_file, index = None)

    message = EmailMessage('money_move', 'Analysing result', 'MoneyMoveApp@gmail.com', [email])
    message.attach_file(name_new_file)
    message.send()
    #send_mail('Analysing result', email, "Yasoob",
    #          [email], fail_silently=False)



    context={
        'date_begin': date_begin,
        'date_end': date_end,
        'date_today': date_today,
        'email': email,         

        }

    return render(request, 'analysing_excel_email.html', context)



