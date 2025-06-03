from dash import html, dcc # dash core components
# import dash_bootstrap_components as dbc # For better styling options if needed

# This app will use Tailwind CSS loaded via CDN in app.py,
# so we primarily use className for styling.

def create_main_layout():
    """
    Creates the main layout for the Dash application.
    Uses Tailwind CSS classes for styling.
    """
    layout = html.Div(className="bg-gray-900 text-white min-h-screen p-4 md:p-8 font-sans antialiased", children=[
        # Header
        html.Div(className="mb-8 md:mb-12 text-center", children=[
            html.H1("Polymarket Insight Engine 📈", className="text-4xl sm:text-5xl font-bold text-purple-400 mb-3 sm:mb-4 tracking-tight"),
            html.P("Visualize (Mock) Polymarket Data - For Portfolio & Conceptual Purposes Only!", className="text-gray-400 text-md sm:text-lg")
        ]),

        # Input Section
        html.Div(className="mb-8 md:mb-10 p-4 sm:p-6 bg-gray-800 rounded-xl shadow-2xl max-w-2xl mx-auto", children=[
            html.Label("Enter Polymarket Market ID (e.g., 'market1', 'market2', 'market3'):", htmlFor="market-id-input", className="block text-md sm:text-lg font-medium text-gray-300 mb-2"),
            dcc.Input(
                id="market-id-input",
                type="text",
                placeholder="Enter Market ID (e.g., market1)",
                # value="market1", # Default value for quick testing
                className="w-full p-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition duration-150 ease-in-out shadow-sm text-sm sm:text-base",
                debounce=True # Only trigger callback after user stops typing for a bit (500ms default)
            ),
            html.Button(
                "🔍 Fetch Market Data (Mock)", 
                id="fetch-button", 
                n_clicks=0,
                className="mt-4 w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-4 sm:px-6 rounded-lg shadow-md hover:shadow-lg transition duration-150 ease-in-out transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-opacity-50 text-sm sm:text-base"
            )
        ]),
        
        # Loading component to wrap outputs that depend on callbacks
        dcc.Loading(
            id="loading-indicator",
            type="default", # or "circle", "cube", "dot"
            color="#a855f7", # purple-500
            className="my-4", # Some margin for the spinner itself
            children=[
                html.Div(id="output-container", style={'display': 'none'}, children=[ # A container for all outputs, initially hidden
                    # Market Details Section
                    html.Div(id="market-details-output", className="mb-8 md:mb-10"), # Styling will be applied within the callback

                    # Chart Section
                    html.Div(id="charts-container", className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8 mb-8 md:mb-10", children=[
                        html.Div(className="p-4 sm:p-6 bg-gray-800 rounded-xl shadow-xl", children=[
                            html.H2("Historical Price Trend", className="text-xl sm:text-2xl font-semibold text-purple-300 mb-4 sm:mb-6 text-center"),
                            dcc.Graph(id="price-chart", className="rounded-lg h-64 sm:h-80 md:h-96") # Responsive height
                        ]),
                        html.Div(className="p-4 sm:p-6 bg-gray-800 rounded-xl shadow-xl", children=[
                            html.H2("Trading Volume", className="text-xl sm:text-2xl font-semibold text-purple-300 mb-4 sm:mb-6 text-center"),
                            dcc.Graph(id="volume-chart", className="rounded-lg h-64 sm:h-80 md:h-96") # Responsive height
                        ]),
                    ]),

                    # Additional Processed Data Display (Optional)
                    html.Div(id="processed-data-output", className="mb-8 md:mb-10") # Styling will be applied within the callback
                ])
            ]
        ),

        # Footer
        html.Div(className="mt-12 md:mt-16 pt-6 md:pt-8 border-t border-gray-700 text-center text-gray-500 text-xs sm:text-sm", children=[
            html.P("Disclaimer: This is a conceptual application using MOCK DATA for portfolio demonstration."),
            html.P("It does NOT provide financial advice or real predictions. Use with extreme caution and common sense")
        ])
    ])
    return layout