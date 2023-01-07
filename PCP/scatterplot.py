import plotly.express as px 
import plotly.graph_objects as go

from data import df_plot
  
customdata = list(
        zip(
            df_plot['host_response_rate'],
            df_plot['accommodates'],
            df_plot['bedrooms'], 
        )
)

fig_scatter = go.Figure()

fig_scatter.add_trace(
    go.Scatter(
        x=df_plot['review_scores_accuracy'],
        y=df_plot['review_scores_checkin'],
        mode='markers',
        marker_color=df_plot['bedrooms'],
        customdata=customdata,
    )
)

fig_scatter.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis_title='review_scores_accuracy',
    yaxis_title='review_scores_checkin',
    title_text='Scatter Plot 1',
    title_x=0.5,
    yaxis_zeroline=False,
    xaxis_zeroline=False,
    dragmode='select',
)

fig_scatter.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
fig_scatter.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey')

scatter2=dict(
    type='Scatter',
    x=df_plot['review_scores_cleanliness'],
    y=df_plot['review_scores_communication'],
    mode='markers',
    marker_color=df_plot['bedrooms'],
    customdata=customdata,
)

layout2 = dict(
    plot_bgcolor='grid',
    paper_bgcolor='white',
    xaxis_title='review_scores_cleanliness',
    yaxis_title='review_scores_communication',
    title=dict(
        text='Scatterplot 2',
        xanchor='center',
        xref='container',
    )
)

fig_scatter2 = dict(
    data=[scatter2],
    layout=layout2,
)

go.Scatter()