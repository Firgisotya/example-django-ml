from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import BpdOc1
from .forms import OC1Filter
import plotly.express as px
import pandas as pd
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.metrics import mean_absolute_percentage_error



def index(request):
    chart_div = None
    chart_predict = None
    mape = None
    rmse = None

    if 'reset_filter' in request.GET:
        # Redirect to the same view without any filters
        return redirect('index')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    column = request.GET.get('column')
    parameters = request.GET.get('parameters')
    timesteps = request.GET.get('timesteps')
    p = request.GET.get('p')
    q = request.GET.get('q')
    d = request.GET.get('d')
    iterations = request.GET.get('iterations')

    if start_date and end_date:
        # Assuming your model has a 'date' field
        bpd_oc1 = BpdOc1.objects.filter(time__range=[start_date, end_date])

        #Convert queryset to Pandas DataFrame
        bpd_oc1_df = pd.DataFrame.from_records(bpd_oc1.values())

        fig = px.line(bpd_oc1_df, x=bpd_oc1_df['time'], y=bpd_oc1_df['min'], title='Data')
        chart_div = fig.to_html(full_html=False)

        if parameters == 'auto':
            
            # Split data into train / test sets
            train = bpd_oc1_df[:int(0.8*(len(bpd_oc1_df)))]
            test = bpd_oc1_df[int(0.8*(len(bpd_oc1_df))):]

            # Fit a SARIMAX(0, 1, 1)x(2, 1, 1, 12) on the training set
            model = auto_arima(train[column], start_p=1, start_q=1,
                                max_p=3, max_q=3, m=12,
                                start_P=0, seasonal=False,
                                d=1, D=1, trace=True,
                                error_action='ignore',  
                                suppress_warnings=True, 
                                stepwise=True)
            
            # Forecast
            n_periods = len(test)
            fitted, confint = model.predict(n_periods=n_periods, return_conf_int=True)
            index_of_fc = pd.date_range(train[column].index[-1], periods = n_periods, freq='MS')

            # make series for plotting purpose
            fitted_series = pd.Series(fitted, index=index_of_fc)
            lower_series = pd.Series(confint[:, 0], index=index_of_fc)
            upper_series = pd.Series(confint[:, 1], index=index_of_fc)

            # Plot
            fig = px.line(bpd_oc1_df, x=bpd_oc1_df['time'], y=bpd_oc1_df['min'], title='Data Forecast')
            fig.add_trace(px.line(fitted_series, x=fitted_series.index, y=fitted_series).data[0])
            fig.add_trace(px.line(lower_series, x=lower_series.index, y=lower_series).data[0])
            fig.add_trace(px.line(upper_series, x=upper_series.index, y=upper_series).data[0])
            chart_predict = fig.to_html(full_html=False)

            
            
            

        

    else:
        bpd_oc1 = BpdOc1.objects.none()
        chart_div = "No data available for the selected filter."
        chart_predict = "No data available for the selected filter."
        mape = "No data available for the selected filter."
        rmse = "No data available for the selected filter."


    context = {
        'title': 'OC1',
        'bpd_oc1': bpd_oc1,
        'chart_div': chart_div,
        'chart_predict': chart_predict,
        'mape': mape,
        'rmse': rmse,
    }

    return render(request, 'OC1/index.html', context)
    
