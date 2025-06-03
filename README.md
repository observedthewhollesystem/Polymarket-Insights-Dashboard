# Polymarket-Insights-Dashboard
Interactive dashboard concept for tracking Polymarket trends using Dash (simulated data). Portfolio project.

# Polymarket-Insights-Dashboard 

## Project Overview

This project is a conceptual web application designed to visualize and track data from Polymarket (using **mock data** for demonstration purposes). It serves as a portfolio piece to showcase skills in full-stack Python development, data processing, and interactive data visualization using the Dash framework.

**Disclaimer:** This application uses MOCK (simulated) data for Polymarket interactions. It does **NOT** connect to live Polymarket data, does **NOT** make real financial predictions, and should **NOT** be used for any actual trading decisions. It is intended for educational and portfolio demonstration purposes only.

## Features
Market Data Display Input a (mock) market ID to view simulated details such as current 'Yes'/'No' prices, liquidity, and volume.
* Historical Price Visualization: Interactive line charts display the (mock) historical price trends for 'Yes' and 'No' outcomes, including moving averages.
* Volume Charting: Bar charts visualize (mock) historical trading volume for the selected market.
* Descriptive Analytics: Displays basic processed data insights (e.g., moving averages, percentage changes, high volume days) based on the mock historical data.
* Interactive UI: Built with Dash and styled with Tailwind CSS for a modern and responsive user experience.

## Technologies Used

 Backend & Data Processing:
    * Python
    * Pandas (for data manipulation)
    * NumPy (for numerical operation)
* Frontend & Visualization
    * Dash (core framework for the web application)
    * Plotly (for interactive charting)
    * Tailwind CSS (for styling, via CDN)
* Data Source (Simulated):
    * Custom Python scripts generate mock market data to simulate API responses from Polymarket.

## Project Structure

polymarket_fancy_tracker/
├── app.py                  Main Dash application
├── polymarket_client_mock.py  Generates MOCK Polymarket data
├── data_processor.py       Processes the mock data for display
├── layout.py               Defines the Dash app layout structure
├── callbacks.py            Handles Dash app interactivity
├── utils.py                Utility/helper functions
├── requirements.txt        Python library dependencies
└── assets/                 For local CSS (if used)
    └── style.css

## How to Run Locally

1.  Clone the repository:
    ```bash
    git clone my repo
    cd repository name
    ```
2.  Create and activate a Python virtual environment
    * Ensure you have Python 3 installed.
    ```bash
    python3 -m venv venv
    ```
    * Activate the environment:
        * On macOS/Linux:
            ```bash
            source venv/bin/activate
            ```
        * On Windows (Command Prompt/PowerShell):
            ```bash
            venv\Scripts\activate
            ```
3.  **Install dependencies:**
    * Make sure you are in the project's root directory (where `requirements.txt` is located) and your virtual environment is active.
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python3 app.py
    ```
5.  Open your web browser and navigate to `http://127.0.0.1:8051` (or the port specified in `app.py`).

## Limitations

* MOCK DATA: This application uses simulated data for all Polymarket interactions. It does **NOT** connect to any live Polymarket data feeds.
* NO PREDICTIONS: The tool is for visualization of historical (mock) data and does **NOT** provide any predictive capabilities or financial advice.
* CONCEPTUAL DEMONSTRATION: This is a portfolio piece to demonstrate application structure and UI/UX design with Dash. It is not a production-ready financial tool.

## Purpose & Learning

This project was developed to:
* Demonstrate proficiency in building interactive web dashboards with Python and Dash.
* Practice structuring a multi-file application.
* Explore data visualization techniques for time-series data.
* Simulate the frontend and basic backend logic for a financial data tracking application (using mock data).

## Future Development (Conceptual)

If this were to be developed into a live application, potential future steps would include:
* Integrating with a live Polymarket API or a reliable data provider for real-time market data.
* Implementing robust error handling and data validation for live data.
* Adding user authentication and personalized watchlists.
* Expanding the range of descriptive analytical tools and indicators.

---
*This project is for demonstration and educational purposes only and is not intended for financial decision-making.*
