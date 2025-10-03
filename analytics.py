# analytics.py
import os
from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import ColorScaleRule, Rule
from openpyxl.utils import get_column_letter
from openpyxl.styles.differential import DifferentialStyle


# import DB_URI from config.py
from config import DB_URI

# directories
CHARTS_DIR = "charts"
EXPORTS_DIR = "exports"
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

# engine
engine = create_engine(DB_URI)

# --------------------------
# Queries (each uses JOINs)
# --------------------------
def load_queries(filepath):
    queries = {}
    with open(filepath, 'r') as f:
        content = f.read()
    # Split queries by -- name: <query_name>
    parts = content.split('-- name:')
    for part in parts[1:]:  # skip everything before first -- name:
        lines = part.strip().split('\n')
        query_name = lines[0].strip()
        query_sql = '\n'.join(lines[1:]).strip()
        queries[query_name] = query_sql
    return queries


# --------------------------
# Helpers
# --------------------------
QUERIES = load_queries('queries.sql')

def run_query(query_key):
    q = QUERIES[query_key]
    df = pd.read_sql_query(text(q), con=engine)
    return df


def print_chart_report(df, chart_type, explanation, path=None):
    rows = len(df)
    s = f"[REPORT] {chart_type} — rows: {rows}. What it shows: {explanation}"
    if path:
        s += f" Saved: {path}"
    print(s)

# --------------------------
# Chart creators (matplotlib)
# --------------------------
plt.rcParams.update({
    "figure.facecolor": (1,1,1),
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "legend.fontsize": 10
})

def create_pie_passengers_by_class():
    df = run_query("pie_passengers_by_class")
    series = df.set_index('fare_conditions')['passengers']
    fig, ax = plt.subplots(figsize=(7,7))
    series.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax)
    ax.set_ylabel("")  # no y label for pie
    ax.set_title("Passenger distribution by class (fare_conditions)")
    ax.legend(title="Class", loc="best")
    path = os.path.join(CHARTS_DIR, "pie_passengers_by_class.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print_chart_report(df, "Pie chart", "Distribution of passengers by travel class (Economy/Business/etc.)", path)
    return df

def create_bar_top_destinations():
    df = run_query("bar_top_destinations")
    fig, ax = plt.subplots(figsize=(9,6))
    df.plot.bar(x='city_name', y='total_passengers', legend=False, ax=ax)
    ax.set_xlabel("Arrival city")
    ax.set_ylabel("Number of passengers")
    ax.set_title("Top 5 busiest arrival cities by passenger count")
    for p in ax.patches:
        ax.annotate(int(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=9)
    path = os.path.join(CHARTS_DIR, "bar_top_destinations.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print_chart_report(df, "Bar chart", "Top 5 arrival cities by number of passengers", path)
    return df

def create_hbar_most_used_models():
    df = run_query("hbar_most_used_models")
    fig, ax = plt.subplots(figsize=(9,6))
    df.plot.barh(x='aircraft_model', y='usage_count', legend=False, ax=ax)
    ax.set_xlabel("Number of flights")
    ax.set_ylabel("Aircraft model")
    ax.set_title("Top 5 most used aircraft models (by number of flights)")
    for p in ax.patches:
        ax.annotate(int(p.get_width()), (p.get_width(), p.get_y() + p.get_height()/2),
                    ha='left', va='center', fontsize=9)
    path = os.path.join(CHARTS_DIR, "hbar_most_used_models.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print_chart_report(df, "Horizontal bar chart", "Most-used aircraft models by flight count", path)
    return df

def create_line_flights_over_time():
    df_raw = run_query("line_flights_with_dates")
    # convert datetimes in pandas, group by date and count
    df = df_raw.copy()
    df['scheduled_departure'] = pd.to_datetime(df['scheduled_departure'])
    df['date'] = df['scheduled_departure'].dt.date
    grouped = df.groupby('date').size().reset_index(name='flights_count').sort_values('date')
    fig, ax = plt.subplots(figsize=(10,5))
    grouped.plot.line(x='date', y='flights_count', marker='o', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of flights")
    ax.set_title("Number of flights by departure date")
    ax.grid(True, linestyle='--', alpha=0.4)
    path = os.path.join(CHARTS_DIR, "line_flights_over_time.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print_chart_report(grouped, "Line chart", "Flight counts per date (based on scheduled_departure)", path)
    return grouped

def create_hist_flight_durations():
    df = run_query("hist_flight_durations")
    # drop nulls & negative durations
    df2 = df[df['duration_minutes'].notna() & (df['duration_minutes'] > 0)].copy()
    fig, ax = plt.subplots(figsize=(9,6))
    ax.hist(df2['duration_minutes'], bins=20)
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of flights")
    ax.set_title("Distribution of flight durations (minutes)")
    path = os.path.join(CHARTS_DIR, "hist_flight_durations.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print_chart_report(df2, "Histogram", "Distribution of flight durations (minutes)", path)
    return df2

def create_scatter_seats_vs_business():
    df = run_query("scatter_seats_vs_business")
    # safe conversion and drop zeros if desired
    df2 = df.copy()
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(df2['total_seats'], df2['business_seats'])
    for i, row in df2.iterrows():
        ax.annotate(row['model'], (row['total_seats'], row['business_seats']), fontsize=8, alpha=0.8)
    ax.set_xlabel("Total seats (per aircraft model)")
    ax.set_ylabel("Business seats booked (per model)")
    ax.set_title("Total seats vs Business seats per aircraft model")
    path = os.path.join(CHARTS_DIR, "scatter_seats_vs_business.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print_chart_report(df2, "Scatter plot", "Total seats vs business seats by aircraft model", path)
    return df2

# --------------------------
# Plotly time slider (interactive)
# --------------------------
def create_time_slider_plotly():
    df = run_query("time_slider_base")
    df['scheduled_departure'] = pd.to_datetime(df['scheduled_departure'])
    # create month frame (YYYY-MM)
    df['month'] = df['scheduled_departure'].dt.to_period('M').astype(str)
    agg = df.groupby(['month', 'arrival_city']).size().reset_index(name='passengers')
    # keep top N cities to avoid overcrowding slider frames
    top_cities = agg.groupby('arrival_city')['passengers'].sum().nlargest(8).index.tolist()
    agg = agg[agg['arrival_city'].isin(top_cities)]
    fig = px.bar(agg, x='arrival_city', y='passengers',
                 animation_frame='month',
                 range_y=[0, agg['passengers'].max() * 1.2],
                 title="Passengers per arrival city over time (use the slider)")
    # Note: during defense, call fig.show()
    print("[INFO] Plotly figure created. Call fig.show() to open the interactive slider in a browser.")
    return fig

# --------------------------
# Excel export with formatting
# --------------------------
def export_to_excel(dataframes_dict, filename):
    path = os.path.join(EXPORTS_DIR, filename)
    # write sheets
    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for sheet_name, df in dataframes_dict.items():
            safe_name = sheet_name[:31]  # Excel sheet name limit
            df.to_excel(writer, sheet_name=safe_name, index=False)

    # open workbook and add formatting
    wb = load_workbook(path)
    for sheet_name, df in dataframes_dict.items():
        ws = wb[sheet_name[:31]]
        # freeze header row
        ws.freeze_panes = "A2"
        # auto-filter all columns
        ws.auto_filter.ref = ws.dimensions
        last_row = ws.max_row

        # apply gradient + highlight min/max for numeric columns
        for col_idx, col_name in enumerate(df.columns, start=1):
            if pd.api.types.is_numeric_dtype(df[col_name]):
                col_letter = get_column_letter(col_idx)
                cell_range = f"{col_letter}2:{col_letter}{last_row}"

                # gradient color scale
                cs_rule = ColorScaleRule(
                    start_type="min", start_color="FFAA0000",
                    mid_type="percentile", mid_value=50, mid_color="FFFFFF00",
                    end_type="max", end_color="FF00AA00"
                )
                ws.conditional_formatting.add(cell_range, cs_rule)

                # max (Top 1) and min (Bottom 1) highlight
                top_fill = PatternFill(start_color="FFFFFF00", end_color="FFFFFF00", fill_type="solid")
                bottom_fill = PatternFill(start_color="FF00FF00", end_color="FF00FF00", fill_type="solid")

                top_dxf = DifferentialStyle(fill=top_fill)
                bottom_dxf = DifferentialStyle(fill=bottom_fill)

                top_rule = Rule(type="top10", rank=1, percent=False, bottom=False, dxf=top_dxf)
                bottom_rule = Rule(type="top10", rank=1, percent=False, bottom=True, dxf=bottom_dxf)

                ws.conditional_formatting.add(cell_range, top_rule)
                ws.conditional_formatting.add(cell_range, bottom_rule)

    wb.save(path)
    total_rows = sum(len(df) for df in dataframes_dict.values())
    print(f"Created file {path}, {len(dataframes_dict)} sheets, {total_rows} rows")

# --------------------------
# Insert demo row helper (for defense)
# --------------------------
def insert_row(table, row_dict):
    """
    Generic insert helper. Example:
      insert_row('ticket_flights', {'ticket_id': 99999, 'flight_id': 123, 'fare_conditions': 'Economy', 'seat_no':'12A'})
    Adapt columns/values to your schema. Use this during defense to show a live change.
    """
    cols = ", ".join(row_dict.keys())
    vals = ", ".join([f":{k}" for k in row_dict.keys()])
    sql = text(f"INSERT INTO {table} ({cols}) VALUES ({vals})")
    with engine.begin() as conn:
        conn.execute(sql, **row_dict)
    print(f"[DB] Inserted demo row into {table} (you must ensure values respect constraints).")

# --------------------------
# main runner
# --------------------------
def run_all():
    # create charts
    df_pie = create_pie_passengers_by_class()
    df_bar = create_bar_top_destinations()
    df_hbar = create_hbar_most_used_models()
    df_line = create_line_flights_over_time()
    df_hist = create_hist_flight_durations()
    df_scatter = create_scatter_seats_vs_business()

    # interactive
    fig_time = create_time_slider_plotly()
    # Keep the fig object if you want to show it:
    # fig_time.show()

    # Export a few reports to Excel
    reports = {
        "Passengers_by_class": df_pie,
        "Top_destinations": df_bar,
        "Aircraft_usage": df_hbar,
        "Flights_overt_time":df_line,
        "Flight_durations": df_hist,
        "Seats_vs_business": df_scatter
    }
    export_to_excel(reports, "airline_report.xlsx")
    print("[DONE] All charts created and saved under /charts/ ; exports saved under /exports/")

if __name__ == "__main__":
    run_all()
