# coding: utf-8
from django.http import HttpResponse

BALANCE_PAGE = u'''
<html>
 <head>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
  <script src="http://code.highcharts.com/highcharts.js"></script>
 </head>
 <body>
<style>
#trellis td {
    width: 200px;
    height: 200px;
}
#trellis td.first {
    width: 300px;
}
</style>

<h1>Balanço Anual</h2>

<div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>

<script type="text/javascript">
$(function() {
    $(document).ready(function() {

    var datasets = [%s, %s];

    $('#container').highcharts({
        chart: {
        },

        title: {
            text: 'Balanço Anual',
        },

        credits: {
            enabled: false
        },

        xAxis: {
            categories: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov', 'Dez'],
        },

        series: datasets

    });
});
});
</script>

</body>  
</html>
'''

PIE_PAGE = u'''
<html>
 <head>
 <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
  <script src="http://code.highcharts.com/highcharts.js"></script>

 </head>
 <body>
   <div id="container" style="min-width: 400px; height: 400px; margin: 0 auto"></div>

  <script type="text/javascript">
$(function() {
    var chart;
    $(document).ready(function() {

        // Radialize the colors
        Highcharts.getOptions().colors = Highcharts.map(Highcharts.getOptions().colors, function(color) {
            return {
                radialGradient: {
                    cx: 0.5,
                    cy: 0.3,
                    r: 0.7
                },
                stops: [
                    [0, color],
                    [1, Highcharts.Color(color).brighten(-0.3).get('rgb')] // darken
                    ]
            };
        });

        // Build the chart
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container',
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: 'Categorias de despesas'
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage}%</b>',
                percentageDecimals: 1
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        connectorColor: '#000000',
                        formatter: function() {
                            return '<b>' + this.point.name + '</b>: ' + Math.round(this.percentage) + ' %';
                        }
                    }
                }
            },
            series: [{
                type: 'pie',
                name: 'Despesas',
                data: ['''

PAGE2 = ''']
}]
});
})
});
 </script>

 </body>  
</html>
'''

from django.contrib.auth.decorators import login_required
from finance.models import *

@login_required
def balance(request, year):
    monthly_expenses = []
    monthly_incomes = []
    for month in range(1,13):
        monthly_incomes.append(sum([i.value for i in Expense.objects.filter(date__year=year).filter(date__month=month).filter(category__lte=7)]))
        monthly_expenses.append(sum([i.value for i in Expense.objects.filter(date__year=year).filter(date__month=month).filter(category__gt=7)]))
    incomes = "{type: 'column', name: 'Receitas', data: %r}" % monthly_incomes
    expenses = "{type: 'column', name: 'Despesas', data: %r}" % monthly_expenses
    return HttpResponse(BALANCE_PAGE % (incomes, expenses))

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
    return HttpResponse(PIE_PAGE+values+PAGE2)

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
    return HttpResponse(PIE_PAGE+values+PAGE2)
