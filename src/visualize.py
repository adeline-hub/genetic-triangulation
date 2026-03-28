import plotly.express as px
import plotly.graph_objects as go

def plot_chromosome_segments(df):
    """
    Renders a Chromosome Browser:
    Each segment is a bar; color-coded by the Cluster.
    """
    # Create the figure
    fig = go.Figure()

    # Get unique clusters to assign colors consistently
    clusters = df['CLUSTER'].unique()
    colors = px.colors.qualitative.Plotly[:len(clusters)]
    color_map = dict(zip(clusters, colors))

    # Add each segment as a horizontal bar
    for _, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row['End'] - row['Start']],
            y=[row['Chromosome']],
            base=row['Start'],
            orientation='h',
            name=row['ID'],
            marker_color=color_map.get(row['CLUSTER'], 'grey'),
            hovertext=f"ID: {row['ID']}<br>Cluster: {row['CLUSTER']}<br>cM: {row['cM']}",
            hoverinfo="text"
        ))

    # Update layout to look like a Genome Browser
    fig.update_layout(
        title="Chromosome Segment Triangulation Map",
        xaxis_title="Base Pair Position (B37)",
        yaxis=dict(tickmode='linear', title="Chromosome"),
        barmode='overlay', # Crucial: Allows overlaps to be visible
        height=800,
        plot_bgcolor='white'
    )
    
    # Grid lines to help the eye
    fig.update_xaxes(showgrid=True, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey')
    
    return fig