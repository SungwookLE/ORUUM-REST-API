import pandas as pd
import pymysql.cursors
from plotly.offline import plot
import plotly.graph_objs as go

def plotly_plot(mysql_connection):
    """
    This function plots plotly plot
    """
    #Create SQL command string
    sql = """SELECT * FROM api_stock_list"""

    #Get table from SQL result       
    with mysql_connection.cursor() as cursor:
      cursor.execute(sql)
      row = cursor.fetchall()
      
    result_table = pd.DataFrame(row, columns=["ticker",'update_date','name_english','name_korea','market','price','price_open','prevclose','price_high','price_low','volume','update_dt','create_dt']).iloc[700:750]
    result_table2 = pd.DataFrame(row, columns=["ticker",'update_date','name_english','name_korea','market','price','price_open','prevclose','price_high','price_low','volume','update_dt','create_dt']).iloc[700:750]
    
    #Create graph object Figure object with data
    fig = go.Figure(
                    data = [go.Scatter(name = 'ORUUM1', x = result_table['ticker'], y = result_table['prevclose']),
                    go.Scatter(name = 'ORUUM2', x = result_table['ticker'], y = result_table['price_high'])]
                   )

    #Update layout for graph object Figure
    fig.update_layout(title_text = 'ORUUM',
                      xaxis_title = 'Kind',
                      yaxis_title = 'Price')
    
    #Turn graph object into local plotly graph
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj