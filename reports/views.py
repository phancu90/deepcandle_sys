import json

from django.shortcuts import render
import pandas as pd

# Create your views here.
from deepcandle import settings
from .Helpers import Helper


def report_page(request):
    data_report = {}
    data_candle = {}
    if request.method == 'POST':
        step = int(request.POST.get('step', 10))
        symbol = request.POST.get('symbol', 'audusd')
        time_frame = request.POST.get('time_frame', 'audusd')
        group = request.POST.get('group', 'FX_Majors')
        digits = 10000
        if 'jpy' in symbol:
            digits = 100
        helper = Helper()
        path_c = 'static/data_candles/' + group.replace(' ','_') + '/' + symbol + '/' + time_frame + '.csv'
        df = helper.load_csv(path_c)
        max_HL = df['HL'].max()
        step_start = 0
        jump = step
        jump = jump / digits
        while step_start < max_HL:
            min_hl = step_start
            step_start = step_start + jump
            list_candles = helper.get_candles_by_range(df=df, min=min_hl, max=step_start)
            percent = (len(list_candles) / len(df)) * 100
            data_report[str(int(step_start * digits))] = round(percent, 2)
            pd.options.display.float_format = '{:, .6f}'.format
            #index=False, header=True, float_format='%.6f'
            list_candles = list_candles.drop(['HL','BODY'],axis=1)
            data_candle[str(int(step_start * digits))] = list_candles.values.tolist()

    return render(request, 'single_chart.html', {'SYMBOLS': settings.SYMBOL.items(),'years':range(2000,2021),'data_report': data_report, 'data_candle': json.dumps(data_candle)})
