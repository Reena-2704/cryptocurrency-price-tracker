import streamlit as st
import pandas as pd
import plotly.express as px
import os
import importlib.util
import requests

# Load the supplied compact crypto tracker as the dashboard's data engine.
# Keep crypto_tracker_compact(1).py in the same folder as this dashboard.
TRACKER_FILE = "crypto_tracker_compact.py"

def load_tracker():
    spec = importlib.util.spec_from_file_location("crypto_tracker", TRACKER_FILE)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {TRACKER_FILE}")
    tracker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tracker)
    return tracker

st.set_page_config(
    page_title="CryptoCurrency Tracker",
    page_icon="₿",
    layout="wide"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .main, .stApp {
        background-color: #f8fafc;
    }

    header[data-testid="stHeader"] {
        background-color: #ffffff;
        border-bottom: 1px solid #e5e7eb;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1240px;
    }

    .title {
        font-size: 46px;
        font-weight: 800;
        letter-spacing: -0.5px;
        text-align: center;
        margin-bottom: 4px;
        color: #2563eb;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 15px;
        margin-bottom: 36px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        color: #1e293b;
        margin-top: 48px;
        margin-bottom: 18px;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 12px;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08);
        transform: translateY(-1px);
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }

    button[kind="secondary"], .stDownloadButton button, .stButton button {
        background-color: #2563eb;
        border: 1px solid #2563eb;
        color: #ffffff;
        border-radius: 8px;
        font-weight: 600;
        padding: 6px 16px;
        transition: background-color 0.15s ease, box-shadow 0.15s ease;
    }

    button[kind="secondary"]:hover, .stDownloadButton button:hover, .stButton button:hover {
        background-color: #1d4ed8;
        border: 1px solid #1d4ed8;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }

    .coin-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 18px;
        background-color: #ffffff;
        border-radius: 10px;
        overflow: hidden;
    }

    .coin-table th {
        text-align: left;
        color: #64748b;
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 14px 18px;
        background-color: #f8fafc;
        border-bottom: 1px solid #e5e7eb;
    }

    .coin-table td {
        padding: 16px 18px;
        color: #1e293b;
        font-size: 18px;
        border-bottom: 1px solid #f1f5f9;
    }

    .coin-row {
        transition: transform 0.18s ease, background-color 0.18s ease, box-shadow 0.18s ease;
    }

    .coin-row:hover {
        background-color: #eff6ff;
        transform: scale(1.01);
        box-shadow: 0 0 0 1px #dbeafe, 0 6px 16px rgba(37, 99, 235, 0.10);
    }

    .coin-row:hover td:first-child {
        border-left: 3px solid #2563eb;
    }

    .positive {
        color: #059669;
        font-weight: 600;
    }

    .negative {
        color: #dc2626;
        font-weight: 600;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        padding: 12px 16px;
        margin-top: 10px;
        margin-bottom: 10px;
        background-color: #ffffff !important;
    }

    div[data-testid="stAlert"] p {
        color: #0f172a !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    body, p, span, label, div {
        color: #0f172a;
    }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #d1d5db !important;
        color: #0f172a !important;
    }

    div[data-testid="stMultiSelect"] div[data-baseweb="select"] {
        background-color: #ffffff !important;
    }

    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
    }

    div[data-baseweb="select"] span {
        color: #0f172a !important;
    }

    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
    }

    div[data-baseweb="popover"] * {
        background-color: #ffffff;
    }

    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #ffffff !important;
    }

    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }

    ul[role="listbox"], div[role="listbox"] {
        background-color: #ffffff !important;
    }

    li[role="option"], div[role="option"] {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }

    li[role="option"] *, div[role="option"] * {
        color: #0f172a !important;
    }

    li[role="option"]:hover, div[role="option"]:hover {
        background-color: #eff6ff !important;
    }

    div[data-baseweb="popover"] [aria-selected="true"] {
        background-color: #eff6ff !important;
        color: #0f172a !important;
    }

    span[data-baseweb="tag"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
    }

    span[data-baseweb="tag"] * {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    div[data-baseweb="tag"] {
        background-color: #2563eb !important;
    }

    div[data-baseweb="tag"] span {
        color: #ffffff !important;
    }

    div[data-baseweb="tag"] svg {
        fill: #ffffff !important;
    }

    input {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }

    .stCaption, div[data-testid="stCaptionContainer"] {
        color: #6b7280 !important;
    }

    .stMarkdown, .stMarkdown p {
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<style>
.crypto-title {
    color: #0066FF !important;
    font-family: "Arial Rounded MT Bold", Arial, sans-serif !important;
    font-size: 110px !important;
    font-weight: bold !important;
    text-align: center;
    line-height: 0.9;
    margin: 0;
    padding: 0;
}
</style>

<div class="crypto-title">
    CRYPTOCURRENCY<br>
    PRICE TRACKER
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="
    text-align: center;
    font-size: 22px;
    margin-top: 0px;
">
    Real-Time Cryptocurrency Market Intelligence Dashboard
</p>
""", unsafe_allow_html=True)


# --------------------------------------------------
# REFRESH BUTTON
# --------------------------------------------------

if st.button("Refresh Market Data"):

    with st.spinner("Collecting latest cryptocurrency data..."):
        try:
            tracker = load_tracker()
            driver = tracker.get_driver()
            try:
                data = tracker.scrape_coins(driver)
            finally:
                driver.quit()

            if not data:
                st.error("No data scraped — CoinMarketCap's layout may have changed.")
            else:
                tracker.save_csv(data)
                st.success("Market data updated successfully.")
                st.rerun()

        except Exception as e:
            st.error("Error while updating market data.")
            st.exception(e)


# --------------------------------------------------
# CHECK CSV
# --------------------------------------------------

if not os.path.exists("crypto_price_history.csv"):
    st.error("crypto_price_history.csv not found.")
    st.stop()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("crypto_price_history.csv")

df.columns = df.columns.str.strip()

# The supplied tracker uses snake_case column names.
# Normalize them to the exact column names expected by the original dashboard.
column_aliases = {
    "timestamp": "Date & Time",
    "name": "Name",
    "symbol": "Symbol",
    "price": "Price",
    "change_24h": "24h Change",
    "market_cap": "Market Cap",
}

df = df.rename(columns=column_aliases)

# The compact tracker intentionally supplies the fields it scrapes.
# Keep the dashboard specification intact by providing safe fallbacks
# for fields that are not present in that tracker version.
for required_column in [
    "Date & Time", "Name", "Symbol", "Price", "24h Change", "Market Cap"
]:
    if required_column not in df.columns:
        st.error(f"Required column '{required_column}' is missing from tracker output.")
        st.stop()

if "Rank" not in df.columns:
    df["Rank"] = (
        df.groupby("Date & Time")["Market Cap"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

if "1h Change" not in df.columns:
    df["1h Change"] = "N/A"

if "7d Change" not in df.columns:
    df["7d Change"] = "N/A"

if "Volume (24h)" not in df.columns:
    df["Volume (24h)"] = "N/A"


# --------------------------------------------------
# CLEAN NUMERIC VALUES
# --------------------------------------------------

df["Price Numeric"] = (
    df["Price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

df["24h Numeric"] = pd.to_numeric(
    df["24h Change"].astype(str).str.replace("%", "", regex=False).str.replace("+", "", regex=False),
    errors="coerce"
).fillna(0.0)

df["7d Numeric"] = pd.to_numeric(
    df["7d Change"].astype(str).str.replace("%", "", regex=False),
    errors="coerce"
).fillna(0.0)

df["1h Numeric"] = pd.to_numeric(
    df["1h Change"].astype(str).str.replace("%", "", regex=False),
    errors="coerce"
).fillna(0.0)


# --------------------------------------------------
# LATEST DATA
# --------------------------------------------------

latest = (
    df
    .groupby("Symbol", as_index=False)
    .tail(1)
    .reset_index(drop=True)
)


# --------------------------------------------------
# MARKET STATISTICS
# --------------------------------------------------

btc = latest[latest["Symbol"] == "BTC"]

if not btc.empty:
    btc_price = btc.iloc[0]["Price Numeric"]
    btc_change = btc.iloc[0]["24h Numeric"]
else:
    btc_price = 0
    btc_change = 0


top_gainer = latest.loc[
    latest["24h Numeric"].idxmax()
]

top_loser = latest.loc[
    latest["24h Numeric"].idxmin()
]


# --------------------------------------------------
# MARKET SENTIMENT
# --------------------------------------------------

positive = len(
    latest[latest["24h Numeric"] > 0]
)

negative = len(
    latest[latest["24h Numeric"] < 0]
)

if positive > negative:
    sentiment = "Bullish"

elif negative > positive:
    sentiment = "Bearish"

else:
    sentiment = "Neutral"


# --------------------------------------------------
# MARKET OVERVIEW
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Market Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Bitcoin Price",
        f"${btc_price:,.2f}",
        f"{btc_change:.2f}%"
    )

with col2:

    st.metric(
        "Top Gainer",
        top_gainer["Name"],
        f"+{top_gainer['24h Numeric']:.2f}%"
    )

with col3:

    st.metric(
        "Top Loser",
        top_loser["Name"],
        f"{top_loser['24h Numeric']:.2f}%"
    )

with col4:

    st.metric(
        "Market Sentiment",
        sentiment
    )


# --------------------------------------------------
# CSV EXPORT
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Export Market Data</div>',
    unsafe_allow_html=True
)

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Crypto Price History as CSV",
    data=csv_data,
    file_name="crypto_price_history.csv",
    mime="text/csv"
)


# --------------------------------------------------
# TOP 10 TABLE
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Top 10 Cryptocurrencies</div>',
    unsafe_allow_html=True
)


def change_class(value):

    return "positive" if value >= 0 else "negative"


table_rows = ""

for _, coin in latest.sort_values("Rank").head(10).iterrows():

    row_html = (
        "<tr class='coin-row'>"

        f"<td>{coin['Rank']}</td>"

        f"<td>{coin['Name']}</td>"

        f"<td>{coin['Symbol']}</td>"

        f"<td>{coin['Price']}</td>"

        f"<td class='{change_class(coin['1h Numeric'])}'>"
        f"{coin['1h Change']}</td>"

        f"<td class='{change_class(coin['24h Numeric'])}'>"
        f"{coin['24h Change']}</td>"

        f"<td class='{change_class(coin['7d Numeric'])}'>"
        f"{coin['7d Change']}</td>"

        f"<td>{coin['Market Cap']}</td>"

        f"<td>{coin['Volume (24h)']}</td>"

        "</tr>"
    )

    table_rows += row_html


table_header = (
    "<thead><tr>"

    "<th>Rank</th>"
    "<th>Name</th>"
    "<th>Symbol</th>"
    "<th>Price</th>"
    "<th>1h</th>"
    "<th>24h</th>"
    "<th>7d</th>"
    "<th>Market Cap</th>"
    "<th>Volume (24h)</th>"

    "</tr></thead>"
)


table_html = (
    f"<table class='coin-table'>"
    f"{table_header}"
    f"<tbody>{table_rows}</tbody>"
    f"</table>"
)

st.markdown(
    table_html,
    unsafe_allow_html=True
)


# --------------------------------------------------
# TOP 10 MARKET SHARE PIE CHART
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Top 10 Cryptocurrency Market Share</div>',
    unsafe_allow_html=True
)

top10 = latest.sort_values("Rank").head(10).copy()


def parse_market_cap_for_chart(value):

    text = str(value).replace("$", "").replace(",", "").strip()

    multiplier = 1

    if text.endswith("T"):

        multiplier = 1_000_000_000_000
        text = text[:-1]

    elif text.endswith("B"):

        multiplier = 1_000_000_000
        text = text[:-1]

    elif text.endswith("M"):

        multiplier = 1_000_000
        text = text[:-1]

    elif text.endswith("K"):

        multiplier = 1_000
        text = text[:-1]

    try:

        return float(text) * multiplier

    except ValueError:

        return 0.0


top10["Market Cap Numeric"] = top10["Market Cap"].apply(
    parse_market_cap_for_chart
)

total_market_cap = top10["Market Cap Numeric"].sum()


if total_market_cap > 0:

    fig_market_share = px.pie(
        top10,
        names="Symbol",
        values="Market Cap Numeric",
        title="Market Share of Top 10 Cryptocurrencies",
        hole=0.35
    )

    fig_market_share.update_traces(
        textinfo="label+percent",
        textfont=dict(
            color="#000000",
            size=18
        ),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Market Share: %{percent}<br>"
            "Market Cap: $%{value:,.0f}"
            "<extra></extra>"
        )
    )

    fig_market_share.update_layout(
        template="plotly_white",
        height=520,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",

        font=dict(
            color="#000000",
            size=18
        ),

        title_font=dict(
            size=26,
            color="#000000"
        ),

        legend_title_text="Cryptocurrency",

        legend=dict(
            font=dict(
                color="#000000",
                size=18
            ),
            title_font=dict(
                color="#000000",
                size=18
            )
        ),

        xaxis=dict(
            tickfont=dict(
                color="#000000",
                size=18
            ),
            title_font=dict(
                color="#000000",
                size=19
            )
        ),

        yaxis=dict(
            tickfont=dict(
                color="#000000",
                size=18
            ),
            title_font=dict(
                color="#000000",
                size=19
            )
        )
    )

    st.plotly_chart(
        fig_market_share,
        width="stretch"
    )

else:

    st.info(
        "Market share data is not available yet."
    )


# --------------------------------------------------
# PREVIOUS DAY VALUE DISTRIBUTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Previous Day Value Distribution</div>',
    unsafe_allow_html=True
)


def parse_market_cap(value):

    text = (
        str(value)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )

    multiplier = 1

    if text.endswith("T"):

        multiplier = 1_000_000_000_000
        text = text[:-1]

    elif text.endswith("B"):

        multiplier = 1_000_000_000
        text = text[:-1]

    elif text.endswith("M"):

        multiplier = 1_000_000
        text = text[:-1]

    elif text.endswith("K"):

        multiplier = 1_000
        text = text[:-1]

    try:

        return float(text) * multiplier

    except ValueError:

        return 0.0


history_all = df.copy()

history_all["Date & Time"] = pd.to_datetime(
    history_all["Date & Time"]
)

previous_day = (
    history_all["Date & Time"].max()
    - pd.Timedelta(days=1)
).date()


previous_day_data = history_all[
    history_all["Date & Time"].dt.date == previous_day
]


if not previous_day_data.empty:

    previous_day_latest = (
        previous_day_data
        .sort_values("Date & Time")
        .groupby("Symbol", as_index=False)
        .tail(1)
    )

    previous_day_latest["Market Cap Numeric"] = (
        previous_day_latest["Market Cap"]
        .apply(parse_market_cap)
    )

    fig_pie = px.pie(
        previous_day_latest,
        names="Name",
        values="Market Cap Numeric",
        title=(
            f"Market Cap Distribution — "
            f"{previous_day.strftime('%b %d, %Y')}"
        ),
        hole=0.4
    )

    fig_pie.update_traces(
        textinfo="label+percent",
        textfont=dict(
            color="#000000",
            size=18
        )
    )

    fig_pie.update_layout(
        template="plotly_white",
        height=480,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",

        font=dict(
            color="#000000",
            size=18
        ),

        title_font=dict(
            size=24,
            color="#000000"
        ),

        legend=dict(
            font=dict(
                color="#000000",
                size=18
            ),
            title_font=dict(
                color="#000000",
                size=18
            )
        ),

        xaxis=dict(
            tickfont=dict(
                color="#000000",
                size=18
            )
        ),

        yaxis=dict(
            tickfont=dict(
                color="#000000",
                size=18
            )
        )
    )

    st.plotly_chart(
        fig_pie,
        width="stretch"
    )

else:

    st.info(
        f"No data recorded for "
        f"{previous_day.strftime('%b %d, %Y')} yet. "
        "Run the tracker across multiple days to populate this chart."
    )


# --------------------------------------------------
# CUSTOM ALERTS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Custom Alerts</div>',
    unsafe_allow_html=True
)

st.info(
    "Set a metric and threshold below. "
    "Matching coins will appear immediately as alerts."
)

alert_col1, alert_col2, alert_col3 = st.columns(3)


metric_map = {
    "Price (USD)": "Price Numeric",
    "1h Change (%)": "1h Numeric",
    "24h Change (%)": "24h Numeric",
    "7d Change (%)": "7d Numeric"
}


with alert_col1:

    metric_label = st.selectbox(
        "Metric",
        list(metric_map.keys()),
        index=2
    )


with alert_col2:

    condition = st.selectbox(
        "Condition",
        ["Above", "Below"]
    )


with alert_col3:

    default_value = (
        5.0
        if "Change" in metric_label
        else 100000.0
    )

    threshold = st.number_input(
        "Threshold",
        value=default_value,
        step=1.0
    )


metric_column = metric_map[metric_label]


if condition == "Above":

    triggered = latest[
        latest[metric_column] > threshold
    ]

else:

    triggered = latest[
        latest[metric_column] < threshold
    ]


if not triggered.empty:

    for _, coin in triggered.iterrows():

        st.warning(
            f"{coin['Name']} ({coin['Symbol']}) — "
            f"{metric_label}: "
            f"{coin[metric_column]:,.2f} "
            f"is {condition.lower()} "
            f"{threshold:,.2f}"
        )

else:

    st.success(
        f"No coins currently have "
        f"{metric_label} {condition.lower()} "
        f"{threshold:,.2f}."
    )


# --------------------------------------------------
# HISTORICAL GROWTH TRACKING
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Historical Growth Tracking</div>',
    unsafe_allow_html=True
)

history = df.copy()

history["Date & Time"] = pd.to_datetime(
    history["Date & Time"]
)

all_symbols = sorted(
    history["Symbol"].unique()
)


selected_coins = st.multiselect(
    "Select Cryptocurrencies to Compare",
    all_symbols,
    default=(
        all_symbols[:3]
        if len(all_symbols) >= 3
        else all_symbols
    )
)


if selected_coins:

    growth_frames = []

    for symbol in selected_coins:

        coin_data = history[
            history["Symbol"] == symbol
        ].sort_values("Date & Time").copy()

        if len(coin_data) > 1:

            baseline_price = (
                coin_data["Price Numeric"].iloc[0]
            )

            coin_data["Growth %"] = (
                (
                    coin_data["Price Numeric"]
                    - baseline_price
                )
                / baseline_price
            ) * 100

            growth_frames.append(
                coin_data
            )


    if growth_frames:

        growth_data = pd.concat(
            growth_frames,
            ignore_index=True
        )

        fig6 = px.line(
            growth_data,
            x="Date & Time",
            y="Growth %",
            color="Symbol",
            markers=True,
            title="Cryptocurrency Growth Over Time (% Change)"
        )

        fig6.update_layout(
            template="plotly_white",
            height=500,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",

            xaxis_title="Time",
            yaxis_title="Growth (%)",

            font=dict(
                color="#000000",
                size=18
            ),

            title_font=dict(
                size=26,
                color="#000000"
            ),

            legend_title_text="Coin",

            legend=dict(
                font=dict(
                    color="#000000",
                    size=18
                ),
                title_font=dict(
                    color="#000000",
                    size=18
                )
            ),

            xaxis=dict(
                tickfont=dict(
                    color="#000000",
                    size=18
                ),
                title_font=dict(
                    color="#000000",
                    size=20
                )
            ),

            yaxis=dict(
                tickfont=dict(
                    color="#000000",
                    size=18
                ),
                title_font=dict(
                    color="#000000",
                    size=20
                )
            )
        )

        fig6.add_hline(
            y=0,
            line_dash="dot",
            line_color="#9ca3af"
        )

        st.plotly_chart(
            fig6,
            width="stretch"
        )

    else:

        st.info(
            "Not enough historical data yet for the selected coins. "
            "Run the tracker multiple times to build growth history."
        )

else:

    st.info(
        "Select at least one cryptocurrency to view its growth."
    )


st.caption(
    "This chart reflects only the data your tracker has scraped so far — "
    "the more times you run it over time, the more history it will show. "
    "For growth over months or years, see the section below."
)


# --------------------------------------------------
# LONG-TERM GROWTH
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Long-Term Growth History</div>',
    unsafe_allow_html=True
)

st.caption(
    "Pulls real multi-year price history from CoinGecko's public API, "
    "independent of your local tracker's CSV."
)


coingecko_ids = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "USDT": "tether",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "USDC": "usd-coin",
    "SOL": "solana",
    "TRX": "tron",
    "HYPE": "hyperliquid",
    "ZEC": "zcash"
}


available_longterm = [
    symbol
    for symbol in all_symbols
    if symbol in coingecko_ids
]


if available_longterm:

    longterm_col1, longterm_col2 = st.columns(2)

    with longterm_col1:

        longterm_symbol = st.selectbox(
            "Select Cryptocurrency",
            available_longterm
        )

    with longterm_col2:

        range_map = {
            "Last 7 Days": 7,
            "Last 30 Days": 30,
            "Last 90 Days": 90,
            "Last 1 Year": 365,
            "Max Available": "max"
        }

        selected_range = st.selectbox(
            "Time Range",
            list(range_map.keys()),
            index=3
        )


    if longterm_symbol:

        coin_id = coingecko_ids[
            longterm_symbol
        ]

        days = range_map[
            selected_range
        ]

        try:

            response = requests.get(
                f"https://coinmarketcap.com/"
                f"{coin_id}/market_chart",
                params={
                    "vs_currency": "usd",
                    "days": days
                },
                timeout=10
            )


            if response.status_code == 200:

                price_points = (
                    response.json()
                    .get("prices", [])
                )


                if price_points:

                    longterm_df = pd.DataFrame(
                        price_points,
                        columns=[
                            "Timestamp",
                            "Price"
                        ]
                    )


                    longterm_df["Date"] = pd.to_datetime(
                        longterm_df["Timestamp"],
                        unit="ms"
                    )


                    baseline = (
                        longterm_df["Price"].iloc[0]
                    )


                    longterm_df["Growth %"] = (
                        (
                            longterm_df["Price"]
                            - baseline
                        )
                        / baseline
                    ) * 100


                    fig_longterm = px.line(
                        longterm_df,
                        x="Date",
                        y="Growth %",
                        title=(
                            f"{longterm_symbol} Growth — "
                            f"{selected_range}"
                        )
                    )


                    fig_longterm.update_traces(
                        line_color="#2563eb"
                    )


                    fig_longterm.update_layout(
                        template="plotly_white",
                        height=480,
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#ffffff",

                        xaxis_title="Date",
                        yaxis_title="Growth (%)",

                        font=dict(
                            color="#000000",
                            size=18
                        ),

                        title_font=dict(
                            size=26,
                            color="#000000"
                        ),

                        xaxis=dict(
                            tickfont=dict(
                                color="#000000",
                                size=18
                            ),
                            title_font=dict(
                                color="#000000",
                                size=20
                            )
                        ),

                        yaxis=dict(
                            tickfont=dict(
                                color="#000000",
                                size=18
                            ),
                            title_font=dict(
                                color="#000000",
                                size=20
                            )
                        )
                    )


                    fig_longterm.add_hline(
                        y=0,
                        line_dash="dot",
                        line_color="#9ca3af"
                    )


                    st.plotly_chart(
                        fig_longterm,
                        width="stretch"
                    )

                else:

                    st.info(
                        "No historical data returned for this coin."
                    )

            else:

                st.warning(
                    "Could not fetch long-term data right now "
                    "(the public API may be rate-limiting or unreachable). "
                    "Try again in a moment."
                )

        except requests.exceptions.RequestException:

            st.warning(
                "Could not reach the historical data service. "
                "Check your internet connection and try again."
            )

else:

    st.info(
        "No supported cryptocurrency is available for long-term history."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "CryptoCurrency Tracker • Built with Python, "
    "Selenium, Pandas, Plotly & Streamlit"
)

#python -m streamlit run dashboard_ss.py