import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import io
import base64

# Import your custom logic scripts
from src import cleaner, classifier, analyzer, visualize

# 1. INITIALIZE THE APP
# suppress_callback_exceptions=True is required when using Tabs!
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], suppress_callback_exceptions=True)
server = app.server

# 2. DEFINE THE LAYOUT
app.layout = dbc.Container([
    html.Br(),
    html.H2("Danki Genetic Triangulation Toolkit", className="text-center", style={"color": "#33FFA2", "fontWeight": "bold" }),
    html.P("Give a chance to triangulation to discover hidden genetic connections", className="text-center text-muted"),
    html.Hr(),
    
    dbc.Row([
        # --- LEFT COLUMN: CONTROLS ---
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("1. Upload Data", className="fw-bold"),
                dbc.CardBody([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div(['Drag and Drop or ', html.A('Select Excel File')]),
                        style={
                            'width': '100%', 'height': '60px', 'lineHeight': '60px',
                            'borderWidth': '2px', 'borderStyle': 'dashed',
                            'borderRadius': '5px', 'textAlign': 'center', 'marginBottom': '10px'
                        },
                        multiple=False
                    ),
                    html.Div(id='upload-status', className="text-info small fw-bold"),
                ])
            ], className="mb-3 shadow-sm"),
            
            dbc.Card([
                dbc.CardHeader("2. Filters & Analysis", className="fw-bold"),
                dbc.CardBody([
                    html.Label("Filter by Cluster:"),
                    dcc.Dropdown(id='cluster-filter', multi=True, placeholder="Select clusters..."),
                    
                    dbc.Button(
                        "Run Triangulation", 
                        id='btn-analyze', 
                        color="primary", 
                        size="lg",
                        className="mt-4 w-100 shadow-sm"
                    )
                ])
            ], className="shadow-sm")
        ], width=12, md=3),
        
        # --- RIGHT COLUMN: RESULTS (TABS) ---
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Tabs(id="tabs", value="tab-map", children=[
                        
                        # TAB 1: CHROMOSOME BROWSER
                        dcc.Tab(label="Chromosome Map", value="tab-map", children=[
                            html.Br(),
                            dcc.Loading(
                                id="loading-map",
                                type="default",
                                children=dcc.Graph(id='genome-map', style={"height": "75vh"})
                            )
                        ]),
                        
                        # TAB 2: TRIANGULATION DATA TABLE
                        dcc.Tab(label="Triangulation Table", value="tab-table", children=[
                            html.Br(),
                            dash_table.DataTable(
                                id='tri-table',
                                page_size=15,
                                style_table={'overflowX': 'auto'},
                                style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'sans-serif'},
                                style_header={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'}
                            )
                        ])
                    ])
                ])
            ], className="shadow-sm")
        ], width=12, md=9)
    ])
], fluid=True, className="bg-light pb-5")


# 3. DEFINE CALLBACKS

# --- Callback 1: File Upload & Auto-Classification ---
@app.callback(
    [Output('upload-status', 'children'), 
     Output('cluster-filter', 'options')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')],
    prevent_initial_call=True # Prevents errors on page load
)
def handle_upload(contents, filename):
    if not contents:
        return dash.no_update, dash.no_update
        
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Run through the src/ pipelines
        df = cleaner.clean_genetic_data(io.BytesIO(decoded))
        df = classifier.apply_classification(df)
        
        # Populate the dropdown with unique clusters found
        unique_clusters = sorted([str(c) for c in df['CLUSTER'].unique() if pd.notna(c)])
        cluster_options = [{'label': c, 'value': c} for c in unique_clusters]
        
        return f"✅ Successfully loaded {filename} ({len(df)} segments).", cluster_options
        
    except Exception as e:
        return f"❌ Error processing file: {str(e)}", []


# --- Callback 2: Run Analysis (Math & Graph) ---
@app.callback(
    [Output('genome-map', 'figure'), 
     Output('tri-table', 'data')],
    [Input('btn-analyze', 'n_clicks')],
    [State('upload-data', 'contents'), 
     State('cluster-filter', 'value')],
    prevent_initial_call=True # Prevents errors on page load
)
def run_analysis(n_clicks, contents, selected_clusters):
    if not contents:
        return dash.no_update, dash.no_update
        
    try:
        # Re-read file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Process
        df = cleaner.clean_genetic_data(io.BytesIO(decoded))
        df = classifier.apply_classification(df)
        
        # Filter dataframe if user selected specific clusters
        if selected_clusters:
            df = df[df['CLUSTER'].isin(selected_clusters)]
        
        # Run Triangulation Math
        tri_data = analyzer.find_triangulation_groups(df)
        
        # Generate Plotly Chart
        fig = visualize.plot_chromosome_segments(df)
        
        # Return updated chart and table
        return fig, tri_data.to_dict('records')
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return dash.no_update, dash.no_update


# 4. RUN SERVER
if __name__ == '__main__':
    app.run_server(debug=True)