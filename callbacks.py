from dash import Input, Output, State, html, no_update, ctx # ctx for callback context
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px # For potentially simpler charts if needed

# Import mock client and processor functions
from polymarket_client_mock import get_mock_market_details, get_mock_historical_prices
from data_processor import process_market_data

# Define a default empty figure layout for when there's no data or an error
empty_fig_layout = dict(
    template="plotly_dark", 
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(31, 41, 55, 0.7)', # bg-gray-800 with some opacity
    font_color="white",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False), # Hide axis for empty
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, visible=False), # Hide axis for empty
    annotations=[dict(text="Enter Market ID & Fetch Data", xref="paper", yref="paper", showarrow=False, font=dict(size=16, color="grey"))]
)

def register_callbacks(app):
    """
    Registers all callbacks for the Dash application.
    """

    @app.callback(
        [Output("market-details-output", "children"),
         Output("price-chart", "figure"),
         Output("volume-chart", "figure"),
         Output("processed-data-output", "children")],
        [Input("fetch-button", "n_clicks")],
        [State("market-id-input", "value")],
        prevent_initial_call=True 
    )
    def update_market_info_on_click(n_clicks, market_id_state):
        """
        Callback to fetch and display market information ONLY when the button is clicked.
        """
        market_id = market_id_state

        # Default empty/error states for outputs
        details_output_children = html.Div()
        # Initialize with empty layout but specific titles
        price_fig = go.Figure().update_layout(**empty_fig_layout, title_text="Price Chart")
        volume_fig = go.Figure().update_layout(**empty_fig_layout, title_text="Volume Chart")
        processed_data_table_div = html.Div()
        
        if not market_id:
            details_output_children = html.Div("Please enter a Market ID to fetch data.", className="text-yellow-400 text-center p-4 bg-gray-800 rounded-lg shadow")
            # Keep figures empty but with titles
            return details_output_children, price_fig, volume_fig, processed_data_table_div

        # --- 1. Fetch Market Details (Mock) ---
        details = get_mock_market_details(market_id)
        
        if not details or details.get("error") or details.get("warning"):
            error_msg = "Could not fetch valid market details."
            if details:
                error_msg = details.get("error", details.get("warning", "Problem fetching market details."))
            
            details_output_children = html.Div([
                html.H3(f"Market: {market_id}", className="text-xl sm:text-2xl font-semibold text-red-400 mb-2 sm:mb-3"),
                html.P(error_msg, className="text-red-300 text-sm sm:text-base")
            ], className="p-4 sm:p-6 bg-red-900 bg-opacity-20 rounded-xl shadow-xl text-center")
            # Return empty figs on error here as well
            return details_output_children, price_fig, volume_fig, processed_data_table_div
        else:
            details_output_children = html.Div([
                html.H3(details.get('name', 'N/A'), className="text-xl sm:text-2xl font-semibold text-purple-300 mb-2 sm:mb-3 text-center"),
                html.P(f"Category: {details.get('category', 'N/A')}", className="text-gray-400 text-sm text-center mb-4"),
                html.P(details.get('description', 'No description available.'), className="text-gray-300 text-xs sm:text-sm mb-4 italic px-2 leading-relaxed"),
                html.Div(className="grid grid-cols-2 sm:grid-cols-3 gap-3 sm:gap-4 text-center", children=[
                    html.Div(className="p-3 bg-gray-700 rounded-lg shadow", children=[
                        html.P("YES Price", className="text-xs sm:text-sm font-medium text-purple-400 mb-1"),
                        html.P(f"${details.get('current_yes_price', 0):.2f}", className="text-lg sm:text-xl font-bold")
                    ]),
                    html.Div(className="p-3 bg-gray-700 rounded-lg shadow", children=[
                        html.P("NO Price", className="text-xs sm:text-sm font-medium text-purple-400 mb-1"),
                        html.P(f"${details.get('current_no_price', 0):.2f}", className="text-lg sm:text-xl font-bold")
                    ]),
                    html.Div(className="p-3 bg-gray-700 rounded-lg shadow", children=[
                        html.P("Liquidity", className="text-xs sm:text-sm font-medium text-purple-400 mb-1"),
                        html.P(f"${details.get('liquidity_usd', 0):,}", className="text-lg sm:text-xl font-bold")
                    ]),
                    html.Div(className="p-3 bg-gray-700 rounded-lg shadow", children=[
                        html.P("24h Volume", className="text-xs sm:text-sm font-medium text-purple-400 mb-1"),
                        html.P(f"${details.get('volume_24h_usd', 0):,}", className="text-lg sm:text-xl font-bold")
                    ]),
                    html.Div(className="p-3 bg-gray-700 rounded-lg shadow col-span-2 sm:col-span-1", children=[
                        html.P("Resolution Date", className="text-xs sm:text-sm font-medium text-purple-400 mb-1"),
                        html.P(f"{details.get('resolution_date', 'N/A')}", className="text-lg sm:text-xl font-bold")
                    ]),
                ])
            ], className="p-4 sm:p-6 bg-gray-800 rounded-xl shadow-xl")
        
        # --- 2. Fetch and Process Historical Prices (Mock) ---
        historical_df = get_mock_historical_prices(market_id, days=180)
        
        if historical_df.empty:
            price_fig.update_layout(title_text=f"No Historical Price Data for {market_id}", annotations=[dict(text="No historical price data available", showarrow=False, font=dict(color="grey"))])
            volume_fig.update_layout(title_text=f"No Historical Volume Data for {market_id}", annotations=[dict(text="No historical volume data available", showarrow=False, font=dict(color="grey"))])
            processed_data_table_div = html.Div(className="p-4 sm:p-6 bg-gray-800 rounded-xl shadow-xl", children=[
                                        html.P("No historical data to process or display.", className="text-gray-400 text-center")])
            return details_output_children, price_fig, volume_fig, processed_data_table_div

        processed_df = process_market_data(historical_df.copy(), market_id)
            
        if not processed_df.empty:
            # --- 3. Create Price Chart ---
            yes_price_col = f'{market_id}_yes_price'
            no_price_col = f'{market_id}_no_price'
            yes_7d_ma_col = f'{yes_price_col}_7d_ma'
            yes_30d_ma_col = f'{yes_price_col}_30d_ma'

            price_fig.data = [] # Clear previous traces
            price_fig.add_trace(go.Scatter(
                x=processed_df['date'], y=processed_df.get(yes_price_col, pd.Series(dtype='float64')), 
                mode='lines', name='YES Price', line=dict(color='#4ade80', width=2.5), marker=dict(size=5)
            ))
            price_fig.add_trace(go.Scatter(
                x=processed_df['date'], y=processed_df.get(no_price_col, pd.Series(dtype='float64')), 
                mode='lines', name='NO Price', line=dict(color='#f87171', width=2.5), marker=dict(size=5)
            ))
            if yes_7d_ma_col in processed_df.columns and not processed_df[yes_7d_ma_col].isnull().all():
                price_fig.add_trace(go.Scatter(
                    x=processed_df['date'], y=processed_df[yes_7d_ma_col], mode='lines', 
                    name='YES 7D MA', line=dict(color='#c084fc', width=1.5, dash='dash')
                ))
            if yes_30d_ma_col in processed_df.columns and not processed_df[yes_30d_ma_col].isnull().all():
                price_fig.add_trace(go.Scatter(
                    x=processed_df['date'], y=processed_df[yes_30d_ma_col], mode='lines', 
                    name='YES 30D MA', line=dict(color='#60a5fa', width=1.5, dash='dot')
                ))

            price_fig.update_layout( # Update existing figure
                title=dict(text=f"Price History", x=0.5, font=dict(size=16, color='white')),
                xaxis_title="Date", yaxis_title="Price (Mock USD)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
                margin=dict(l=50, r=20, t=60, b=40), hovermode="x unified",
                xaxis=dict(showgrid=True, zeroline=False, showticklabels=True, gridcolor='rgba(107, 114, 128, 0.3)', visible=True), # Show axis
                yaxis=dict(showgrid=True, zeroline=False, showticklabels=True, gridcolor='rgba(107, 114, 128, 0.3)', visible=True), # Show axis
                annotations=[] # Clear previous annotations
            )

            # --- 4. Create Volume Chart ---
            volume_col = f'{market_id}_volume'
            if volume_col in processed_df.columns:
                volume_fig.data = [] # Clear previous traces
                volume_fig.add_trace(go.Bar(
                    x=processed_df['date'], y=processed_df[volume_col], 
                    name='Volume', marker_color='#60a5fa'
                ))
                volume_fig.update_layout( # Update existing figure
                    title=dict(text=f"Trading Volume", x=0.5, font=dict(size=16, color='white')),
                    xaxis_title="Date", yaxis_title="Volume (Mock Units)",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
                    margin=dict(l=50, r=20, t=60, b=40), hovermode="x unified",
                    xaxis=dict(showgrid=True, zeroline=False, showticklabels=True, gridcolor='rgba(107, 114, 128, 0.3)', visible=True), # Show axis
                    yaxis=dict(showgrid=True, zeroline=False, showticklabels=True, gridcolor='rgba(107, 114, 128, 0.3)', visible=True), # Show axis
                    annotations=[] # Clear previous annotations
                )
            
            # --- 5. Display some processed data (e.g., last few days) ---
            display_cols_map = {
                'date': 'Date', yes_price_col: 'YES Price', yes_7d_ma_col: '7D MA (Yes)',
                f'{yes_price_col}_1d_pct_change': '1D %Chg (Yes)',
                f'{yes_price_col}_14d_volatility': '14D Volatility', 'high_volume_day': 'High Volume?'
            }
            existing_display_cols = [col for col in display_cols_map.keys() if col in processed_df.columns]
            
            if not processed_df.empty and existing_display_cols:
                recent_data_df = processed_df[existing_display_cols].tail(7).iloc[::-1]
                table_header_content = [html.Th(display_cols_map.get(col, col), className="px-3 py-2 text-left text-xs font-medium text-purple-300 uppercase tracking-wider") for col in existing_display_cols]
                table_header = [html.Thead(html.Tr(table_header_content, className="bg-gray-750"))]
                table_rows = []
                for i in range(len(recent_data_df)):
                    row_cells = []
                    for col in existing_display_cols:
                        val = recent_data_df.iloc[i][col]
                        formatted_val = ""
                        if isinstance(val, pd.Timestamp): formatted_val = val.strftime('%Y-%m-%d')
                        elif 'pct_change' in col and isinstance(val, (float, np.floating)): formatted_val = f"{val:.2f}%" if pd.notna(val) else "N/A"
                        elif 'volatility' in col and isinstance(val, (float, np.floating)): formatted_val = f"{val:.4f}" if pd.notna(val) else "N/A"
                        elif isinstance(val, (float, np.floating)): formatted_val = f"{val:.2f}" if pd.notna(val) else "N/A"
                        elif isinstance(val, (bool, np.bool_)): formatted_val = "Yes" if val else "No"
                        else: formatted_val = str(val) if pd.notna(val) else "N/A"
                        row_cells.append(html.Td(formatted_val, className="px-3 py-2 whitespace-nowrap text-xs text-gray-300"))
                    table_rows.append(html.Tr(row_cells, className="border-b border-gray-700 hover:bg-gray-700 transition-colors duration-150"))
                table_body = [html.Tbody(table_rows)]
                processed_data_table_div = html.Div([
                    html.H3("Recent Data Insights (Last 7 Days - Mock)", className="text-lg sm:text-xl font-semibold text-purple-300 mb-3 sm:mb-4"),
                    html.Div(html.Table(table_header + table_body, className="min-w-full divide-y divide-gray-700 bg-gray-800 rounded-lg shadow-md overflow-hidden"), className="overflow-x-auto")
                ], className="p-4 sm:p-6 bg-gray-800 rounded-xl shadow-xl")
        
        return details_output_children, price_fig, volume_fig, processed_data_table_div

    # This callback controls the visibility of the entire output container
    @app.callback(
        Output("output-container", "style"),
        [Input("fetch-button", "n_clicks")]
    )
    def toggle_output_visibility(n_clicks):
        if n_clicks > 0:
            return {'display': 'block'} # Show when button has been clicked at least once
        return {'display': 'none'} # Initially hidden