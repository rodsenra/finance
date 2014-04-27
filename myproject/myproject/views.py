# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from finance.models import *

@login_required
def root(request):
    return render(request, 'root.html')

@login_required
def balance(request, year):
    monthly_expenses = []
    monthly_incomes = []
    for month in range(1, 13):
        monthly_incomes.append(sum([i.value for i in Expense.objects.filter(date__year=year).filter(date__month=month).filter(category__lte=7)]))
        monthly_expenses.append(sum([i.value for i in Expense.objects.filter(date__year=year).filter(date__month=month).filter(category__gt=7)]))
    incomes = "{type: 'column', name: 'Receitas', data: %r}" % monthly_incomes
    expenses = "{type: 'column', name: 'Despesas', data: %r}" % monthly_expenses
    return render(request, 'balance.html', {'incomes': incomes, 'expenses': expenses})

@login_required
def pie_macro(request, year, month):
    despesas = Expense.objects.filter(date__year=year).filter(date__month=month)
    macros = {}
    total = 0
    for i in despesas:
        category = i.category.macro.name
        if category==u"Renda":
            continue
        if category not in macros:
            macros[category]=0
        macros[category] += i.value
        total += i.value
    values = ",".join([u"['%s = R$ %.2f', %f]" % (k,v,v/total*100)  for k,v in macros.items() ])
    return render(request, 'pie.html', {'values': values})

@login_required
def pie_micro(request, year, month):
    despesas = Expense.objects.filter(date__year=year).filter(date__month=month)
    macros = {}
    total = 0
    for i in despesas:
        category = i.category.name
        if category==u"Renda":
            continue
        if category not in macros:
            macros[category]=0
        macros[category] += i.value
        total += i.value
    values = ",".join([u"['%s = R$ %.2f', %f]" % (k,v,v/total*100)  for k,v in macros.items() ])
    return render(request, 'pie.html', {'values': values})
