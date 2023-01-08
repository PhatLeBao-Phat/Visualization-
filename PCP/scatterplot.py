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

def make_scatter(feature, color_by, title):
    fig_scatter = go.Figure()

    fig_scatter.add_trace(
        go.Scatter(
            x=df_plot[feature[0]],
            y=df_plot[feature[1]],
            mode='markers',
            marker_color=df_plot[color_by],
            customdata=customdata,
        )
    )

    fig_scatter.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title=feature[0],
        yaxis_title=feature[1],
        title_text=title,
        title_x=0.5,
        yaxis_zeroline=False,
        xaxis_zeroline=False,
        dragmode='select',
    )

    fig_scatter.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
    fig_scatter.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey')

    return fig_scatter

fig_scatter = make_scatter(
    feature=['review_scores_checkin', 'review_scores_accuracy'],
    color_by='bedrooms',
    title='Scatter Plot 1',
)

fig_scatter2 = make_scatter(
    feature=['review_scores_checkin', 'review_scores_accuracy'],
    color_by='bedrooms',
    title='Scatter Plot 2',
)
