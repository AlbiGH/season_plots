import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def dynamic_format_dollars(x, pos):
    """ Helper function used to format the y-axis in various plots"""
    
    if x >= 1e9:
        return '${:1.1f}B'.format(x*1e-9)
    elif x >= 1e6:
        return '${:1.1f}M'.format(x*1e-6)
    elif x >= 1e3:
        return '${:1.0f}K'.format(x*1e-3)
    else:
        return '${:1.0f}'.format(x)

def quarterly_plot(df, name=""):
    """ This function produces a plot containing 4 subplots. Each subplot has the sales for a respective
        quarter over the number of years in the dataset. Each subplot also has a dashed line representing the
        average sales for that quarter. Differences in the dashed lines can be interpreted as different seasonal 
        patterns, though this does not always have to be the case
    """

    import matplotlib.ticker as mtick
    
    temp_df = df.copy()
    temp_df['quarter'] = temp_df['date'].dt.quarter
    temp_df['year'] = temp_df['date'].dt.year 
    
    qd = temp_df.groupby(by=['year','quarter'],as_index=False)['total_sales'].sum()
    ymin = qd['total_sales'].min() - qd['total_sales'].std()*0.5
    ymax = qd['total_sales'].max() + qd['total_sales'].std()*0.5

    plt.style.use("fivethirtyeight")
    mpl.rcParams['lines.linewidth'] = 2
    mpl.rcParams['axes.labelsize']='medium'

    fig, axs = plt.subplots(1,4,figsize=(12,6))
    counter = 1
    for ax in axs:
        plot_data = qd[qd['quarter']==counter]
        plot_mean = plot_data['total_sales'].mean()
        
        ax.plot(plot_data['year'],plot_data['total_sales'],color = '#3d5a89', linewidth=3)
        ax.axhline(y=plot_mean,color='#293241',linestyle='--')
        ax.set_ylim(ymin,ymax)
        ax.set_title("Q"+ str(counter) + " Sales", size=14)
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(dynamic_format_dollars))
        if counter > 1:
            ax.set_yticklabels([])
        counter +=1

    if name == "":
        fig.suptitle('Quarterly Sales over Time')
    if name != "":
        fig.suptitle('Quarterly Sales over Time for ' + name)

    return fig

def monthly_plot(df, name=""):
    """ This function produces a plot containing 12 subplots. Each subplot has the sales for a respective
        month over the number of years in the dataset. Each subplot also has a dashed line representing the
        average sales for that month. Differences in the dashed lines can be interpreted as different seasonal 
        patterns, though this does not always have to be the case
    """

    import matplotlib.ticker as mtick
    
    temp_df = df.copy()
    temp_df['month'] = temp_df['date'].dt.month
    temp_df['year'] = temp_df['date'].dt.year 
    
    md = temp_df.groupby(by=['year','month'],as_index=False)['total_sales'].sum()
    ymin = md['total_sales'].min() - md['total_sales'].std()*0.5
    ymax = md['total_sales'].max() + md['total_sales'].std()*0.5

    plt.style.use("fivethirtyeight")
    mpl.rcParams['lines.linewidth'] = 2
    mpl.rcParams['axes.labelsize']='small'
    mpl.rcParams['xtick.labelsize'] = 'small'
    mpl.rcParams['ytick.labelsize'] = 'small'
    
    fig, axs = plt.subplots(1,12,figsize=(20,6))
    
    counter = 1
    for ax in axs:
        plot_data = md[md['month']==counter]
        plot_mean = plot_data['total_sales'].mean()
        
        ax.plot(plot_data['year'],plot_data['total_sales'],color = '#3d5a89', linewidth=3)
        ax.axhline(y=plot_mean,color='#293241',linestyle='--')
        ax.set_ylim(ymin,ymax)
        ax.set_title("M"+ str(counter) + " Sales", size=14)
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(dynamic_format_dollars))
        ax.xaxis.set_major_locator(mtick.MaxNLocator(integer=True,nbins=2))
        
        if counter > 1:
            ax.set_yticklabels([])
            ax.tick_params(axis='y', which='both', length=0)
            ax.set_ylabel('')
        counter +=1

    if name == "":
        fig.suptitle('Monthly Sales over Time')
    if name != "":
        fig.suptitle('Monthly Sales over Time for ' + name)

    
    plt.tight_layout()
    
    return fig
    

def daily_plot(df, name=""):
    
    temp_df = df.copy()
    temp_df['month'] = temp_df['date'].dt.month
    temp_df['year'] = temp_df['date'].dt.year 
    temp_df['day_of_week'] = temp_df['date'].dt.day_of_week
    
    #average out the days by month 
    daily_df = temp_df.groupby(by=['year','month','day_of_week'],as_index=False)['total_sales'].sum()
    daily_df['date'] = daily_df.apply(lambda x: pd.to_datetime(str(x.year)+'-'+str(x.month)+'-1'),axis=1)
    ymin = daily_df['total_sales'].min() - daily_df['total_sales'].std()*0.5
    ymax = daily_df['total_sales'].max() + daily_df['total_sales'].std()*0.5

    plt.style.use("fivethirtyeight")
    mpl.rcParams['lines.linewidth'] = 2
    mpl.rcParams['axes.labelsize']='small'
    mpl.rcParams['xtick.labelsize'] = 'small'
    mpl.rcParams['ytick.labelsize'] = 'small'

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    fig, axs = plt.subplots(1,7,figsize=(15,6))
    
    counter = 0
    for ax in axs:
        plot_data = daily_df[daily_df['day_of_week']==counter]
        plot_mean = plot_data['total_sales'].mean()
        
        ax.plot(plot_data['date'],plot_data['total_sales'],color = '#3d5a89', linewidth=3)
        ax.axhline(y=plot_mean,color='#293241',linestyle='--')
        ax.set_ylim(ymin,ymax)
        ax.set_title(days[counter], size=14)
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(dynamic_format_dollars))
        ax.xaxis.set_major_locator(mtick.MaxNLocator(integer=False,nbins=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        #ax.xaxis.set_major_formatter(mtick.FuncFormatter)
        
        if counter > 0:
            ax.set_yticklabels([])
            ax.tick_params(axis='y', which='both', length=0)
            ax.set_ylabel('')
        counter +=1

    if name == "":
        fig.suptitle('Daily Sales over Time')
    if name != "":
        fig.suptitle('Daily Sales over Time for ' + name)

    
    plt.tight_layout()
    
    return fig
     