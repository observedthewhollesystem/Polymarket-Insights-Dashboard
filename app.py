import dash
from dash import html
# import dash_bootstrap_components as dbc # If you prefer Bootstrap components

# Import layout and callback registration functions
from layout import create_main_layout
from callbacks import register_callbacks # This is the critical import

# --- Initialize the Dash App ---
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True, 
    assets_folder='assets' 
)
app.title = "Polymarket Insight Engine" # Browser tab title

# --- Add Tailwind CSS via CDN & Custom Font ---
app.index_string = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body { 
                font-family: 'Inter', sans-serif; 
                background-color: #111827; /* Tailwind's bg-gray-900 */
            }
            /* Custom scrollbar for webkit browsers */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: #1f2937; /* Tailwind's gray-800 */
            }
            ::-webkit-scrollbar-thumb {
                background: #4b5563; /* Tailwind's gray-600 */
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #6b7280; /* Tailwind's gray-500 */
            }
            /* Ensure Plotly chart backgrounds are transparent if not set in figure layout */
            .js-plotly-plot .plotly .bg {
                fill: transparent !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# --- App Layout ---
app.layout = create_main_layout()

# --- Register Callbacks ---
register_callbacks(app) # Call the function to set up callbacks

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=8051) # Changed port to 8051 and to app.run()