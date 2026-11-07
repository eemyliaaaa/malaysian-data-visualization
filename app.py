
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Malaysian Data | Visualization Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. COLOUR PALETTE
# =====================================================

DARK_GREEN = "#183D2B"
GREEN_LIGHT = "#426B50"
GREEN_MID = "#78927B"
GREEN_PALE = "#E5ECE6"

DARK_PINK = "#A62959"
PINK_LIGHT = "#C6537C"
PINK_PALE = "#F3E5EA"

CREAM = "#F7F4EF"
WHITE = "#FFFFFF"
TEXT = "#343434"
MUTED = "#77716F"
BORDER = "#E7DFDA"

STATE_COLORS = [
    "#183D2B", "#A62959", "#426B50", "#C6537C",
    "#315C43", "#8E3158", "#53785B", "#B64B72",
    "#244B35", "#D07896", "#426B50", "#A62959",
    "#315C43", "#C6537C", "#53785B", "#8E3158",
    "#183D2B"
]

# =====================================================
# 3. CUSTOM CSS
# =====================================================

st.markdown(
    f"""
    <style>

    /* Main background */
    .stApp {{
        background-color: {CREAM};
        color: {TEXT};
    }}

    .main .block-container {{
        max-width: 1450px;
        padding: 2rem 3rem 3rem 3rem;
    }}

    /* Hide the old sidebar */
    [data-testid="stSidebar"] {{
        display: none;
    }}

    /* Main headings */
    h1, h2, h3 {{
        color: {DARK_GREEN} !important;
        font-weight: 750 !important;
    }}

    h1 {{
        font-size: 2.15rem !important;
        letter-spacing: -0.7px;
    }}

    h2 {{
        font-size: 1.45rem !important;
    }}

    h3 {{
        font-size: 1.15rem !important;
    }}

    /* Brand */
    .brand-title {{
        color: {DARK_GREEN};
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }}

    .brand-subtitle {{
        color: {MUTED};
        font-size: 0.9rem;
        margin-top: -4px;
    }}

    .eyebrow {{
        color: {DARK_PINK};
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .description {{
        color: {MUTED};
        font-size: 0.98rem;
        margin-bottom: 15px;
    }}

    .section-label {{
        color: {DARK_GREEN};
        font-size: 1.1rem;
        font-weight: 750;
        margin-bottom: 12px;
    }}

    /* Top navigation */
    div[role="radiogroup"] {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }}

    div[role="radiogroup"] label {{
        background-color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 10px 15px;
        transition: 0.2s ease;
    }}

    div[role="radiogroup"] label:hover {{
        border-color: {DARK_PINK};
        background-color: {PINK_PALE};
    }}

    /* KPI cards */
    [data-testid="stMetric"] {{
        background-color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 15px;
        padding: 20px;
        min-height: 120px;
        box-shadow: 0 3px 12px rgba(24,61,43,0.05);
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-size: 0.88rem !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {DARK_GREEN} !important;
        font-size: 1.65rem !important;
        font-weight: 750 !important;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
    }}

    /* Dividers */
    hr {{
        border-color: {BORDER};
        margin: 1.5rem 0;
    }}

    /* Select boxes */
    div[data-baseweb="select"] > div {{
        background-color: {WHITE};
        border-radius: 9px;
        border-color: {BORDER};
    }}

    /* Data tables */
    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
        overflow: hidden;
    }}

    /* Expanders */
    [data-testid="stExpander"] {{
        background-color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}

    /* Download buttons */
    .stDownloadButton button {{
        background-color: {DARK_GREEN};
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
    }}

    .stDownloadButton button:hover {{
        background-color: {DARK_PINK};
        color: white;
    }}

    /* Information boxes */
    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}

    /* Footer */
    .footer {{
        text-align: center;
        color: {MUTED};
        font-size: 0.82rem;
        padding: 20px 0;
        line-height: 1.8;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# 4. LOAD DATASETS
# =====================================================

@st.cache_data
def load_data():

    population = pd.read_csv("population_clean.csv")
    income = pd.read_csv("income_clean.csv")
    marriages = pd.read_csv("marriages_clean.csv")

    for df in [population, income, marriages]:

        df["state"] = (
            df["state"].astype(str).str.strip()
        )

        df["year"] = pd.to_numeric(
            df["year"], errors="coerce"
        )

    return population, income, marriages


try:
    population, income, marriages = load_data()

except Exception as error:
    st.error(f"Unable to load datasets: {error}")
    st.stop()


# =====================================================
# 5. COMMON CHART SETTINGS
# =====================================================

def chart_layout(height=550):

    return {
        "template": "plotly_white",
        "height": height,
        "paper_bgcolor": WHITE,
        "plot_bgcolor": WHITE,
        "font": {
            "family": "Arial, sans-serif",
            "color": TEXT,
            "size": 12
        },
        "margin": dict(l=25, r=25, t=55, b=35)
    }


# =====================================================
# 6. TOP HEADER
# =====================================================

header_left, header_right = st.columns([3, 1])

with header_left:

    st.markdown(
        '<div class="brand-title">🌿 Malaysian Data</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'Interactive Visualization Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        f"""
        <div style="
            text-align:right;
            padding-top:10px;
            color:{DARK_GREEN};
            font-size:0.85rem;
            font-weight:700;">
            MALAYSIA<br>
            2017 – 2023
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")


# =====================================================
# 7. TOP NAVIGATION
# =====================================================

page = st.radio(
    "Select Analysis",
    [
        "🌿 Population",
        "🌸 Household Income",
        "💗 Marriage"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")


# =====================================================
# 8. PAGE HEADER FUNCTION
# =====================================================

def page_header(title, description, objective):

    st.markdown(
        '<div class="eyebrow">'
        'MALAYSIAN DATA VISUALIZATION'
        '</div>',
        unsafe_allow_html=True
    )

    st.title(title)

    st.markdown(
        f'<div class="description">{description}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            background:{GREEN_PALE};
            border-left:4px solid {DARK_GREEN};
            padding:15px 18px;
            border-radius:9px;
            margin:15px 0 25px 0;
            color:{TEXT};">
            <b style="color:{DARK_GREEN};">
                Visualization Objective
            </b><br>
            {objective}
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 9. POPULATION ANALYSIS
# =====================================================

if page == "🌿 Population":

    page_header(
        "Population Analysis",
        "Explore population growth patterns across Malaysian states.",
        "Analyse population growth across Malaysian states "
        "from 2017 to 2023."
    )

    st.markdown(
        '<div class="section-label">Population Overview</div>',
        unsafe_allow_html=True
    )

    years = sorted(
        population["year"].dropna().unique()
    )

    if not years:
        st.warning("No population year data is available.")
        st.stop()

    selected_years = st.slider(
        "Select year range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years))),
        key="population_years"
    )

    population_filtered = population[
        population["year"].between(
            selected_years[0],
            selected_years[1]
        )
    ].copy()

    population_trend = (
        population_filtered
        .groupby(
            ["year", "state"],
            as_index=False
        )["population"].sum()
    )

    total_population = (
        population_trend
        .groupby("year")["population"]
        .sum()
        .sort_index()
    )

    if total_population.empty:
        st.warning("No population data for this period.")
        st.stop()

    start_population = total_population.iloc[0]
    end_population = total_population.iloc[-1]

    growth = (
        (end_population - start_population)
        / start_population * 100
        if start_population != 0 else 0
    )

    # KPI cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Starting Population",
        f"{start_population:,.1f}k"
    )

    col2.metric(
        "Latest Population",
        f"{end_population:,.1f}k"
    )

    col3.metric(
        "Population Growth",
        f"{growth:.2f}%"
    )

    st.caption(
        "Population values are presented in thousands."
    )

    st.markdown("---")

    # Population line chart
    st.subheader("Population Growth by State")

    fig = px.line(
        population_trend,
        x="year",
        y="population",
        color="state",
        markers=True,
        color_discrete_sequence=STATE_COLORS,
        labels={
            "year": "Year",
            "population": "Population (thousands)",
            "state": "Malaysian State"
        }
    )

    fig.update_layout(
        **chart_layout(600),
        hovermode="x unified",
        xaxis=dict(
            title="Year",
            dtick=1
        ),
        yaxis_title="Population (thousands)",
        legend_title="State"
    )

    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=6)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with st.expander("View Population Data"):

        st.dataframe(
            population_trend,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Population Data",
            population_trend.to_csv(index=False),
            file_name="population_analysis.csv",
            mime="text/csv"
        )


# =====================================================
# 10. HOUSEHOLD INCOME ANALYSIS
# =====================================================

elif page == "🌸 Household Income":

    page_header(
        "Household Income Analysis",
        "Compare mean and median monthly household income "
        "across Malaysian states.",
        "Compare mean and median household income across "
        "Malaysian states for available survey years "
        "within 2017–2023."
    )

    st.markdown(
        '<div class="section-label">Income Overview</div>',
        unsafe_allow_html=True
    )

    available_years = sorted(
        income["year"].dropna().unique()
    )

    if not available_years:
        st.warning("No household income year data is available.")
        st.stop()

    selected_year = st.selectbox(
        "Select survey year",
        available_years,
        index=len(available_years) - 1,
        format_func=lambda x: str(int(x))
    )

    income_selected = income[
        income["year"] == selected_year
    ].copy()

    income_chart = (
        income_selected
        .groupby("state", as_index=False)
        .agg({
            "income_mean": "mean",
            "income_median": "mean"
        })
        .sort_values("income_mean")
    )

    if income_chart.empty:
        st.warning("No income data for this year.")
        st.stop()

    highest = income_chart.loc[
        income_chart["income_mean"].idxmax()
    ]

    lowest = income_chart.loc[
        income_chart["income_mean"].idxmin()
    ]

    average_income = income_chart["income_mean"].mean()

    # KPI cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Highest Mean Income",
        f"RM {highest['income_mean']:,.0f}",
        highest["state"]
    )

    col2.metric(
        "Lowest Mean Income",
        f"RM {lowest['income_mean']:,.0f}",
        lowest["state"]
    )

    col3.metric(
        "Average Mean Income",
        f"RM {average_income:,.0f}"
    )

    st.caption(
        f"Household income survey year: {int(selected_year)}"
    )

    st.markdown("---")

    # Dumbbell chart
    st.subheader(
        f"Mean vs Median Household Income ({int(selected_year)})"
    )

    fig = go.Figure()

    # Connecting lines
    for _, row in income_chart.iterrows():

        fig.add_trace(
            go.Scatter(
                x=[
                    row["income_median"],
                    row["income_mean"]
                ],
                y=[
                    row["state"],
                    row["state"]
                ],
                mode="lines",
                line=dict(
                    color="#D7DCD7",
                    width=3
                ),
                showlegend=False,
                hoverinfo="skip"
            )
        )

    # Median income: dark green
    fig.add_trace(
        go.Scatter(
            x=income_chart["income_median"],
            y=income_chart["state"],
            mode="markers",
            name="Median Income",
            marker=dict(
                color=GREEN_LIGHT,
                size=12,
                line=dict(
                    color=WHITE,
                    width=1.5
                )
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Median Income: RM %{x:,.0f}"
                "<extra></extra>"
            )
        )
    )

    # Mean income: dark pink
    fig.add_trace(
        go.Scatter(
            x=income_chart["income_mean"],
            y=income_chart["state"],
            mode="markers",
            name="Mean Income",
            marker=dict(
                color=DARK_PINK,
                size=12,
                line=dict(
                    color=WHITE,
                    width=1.5
                )
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Mean Income: RM %{x:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        **chart_layout(680),
        xaxis_title="Monthly Household Income (RM)",
        yaxis_title="Malaysian State",
        legend_title="Income Measurement",
        hovermode="closest"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("### Understanding the Income Difference")

    st.markdown(
        f"""
        <div style="
            background:{PINK_PALE};
            border-left:4px solid {DARK_PINK};
            padding:16px 18px;
            border-radius:10px;
            color:{TEXT};">
            <b style="color:{DARK_GREEN};">
                Mean Income
            </b><br>
            The average household income.<br><br>

            <b style="color:{DARK_PINK};">
                Median Income
            </b><br>
            The middle value when household incomes are
            arranged from lowest to highest.<br><br>

            <b>Connecting line</b><br>
            Shows the difference between mean and median.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "A mean income higher than the median may indicate "
        "that higher-income households influence the average. "
        "The gap alone does not describe the full income distribution."
    )

    with st.expander("View Household Income Data"):

        st.dataframe(
            income_chart,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Household Income Data",
            income_chart.to_csv(index=False),
            file_name="household_income_analysis.csv",
            mime="text/csv"
        )


# =====================================================
# 11. MARRIAGE ANALYSIS
# =====================================================

elif page == "💗 Marriage":

    page_header(
        "Marriage Analysis",
        "Explore annual female marriage rate patterns "
        "across Malaysian states.",
        "Examine annual marriage trends across Malaysian "
        "states from 2017 to 2023."
    )

    st.markdown(
        '<div class="section-label">Marriage Overview</div>',
        unsafe_allow_html=True
    )

    marriages_female = marriages[
        marriages["sex"].astype(str).str.lower() == "female"
    ].copy()

    marriage_data = (
        marriages_female
        .groupby(
            ["state", "year"],
            as_index=False
        )["rate"].mean()
    )

    marriage_pivot = marriage_data.pivot(
        index="state",
        columns="year",
        values="rate"
    )

    available_years = sorted(
        marriage_data["year"].dropna().unique()
    )

    if not available_years:
        st.warning("No female marriage data available.")
        st.stop()

    selected_years = st.slider(
        "Select year range",
        min_value=int(min(available_years)),
        max_value=int(max(available_years)),
        value=(
            int(min(available_years)),
            int(max(available_years))
        ),
        key="marriage_years"
    )

    selected_columns = [
        year for year in marriage_pivot.columns
        if selected_years[0] <= year <= selected_years[1]
    ]

    marriage_filtered = marriage_pivot[selected_columns]

    if marriage_filtered.empty:
        st.warning("No marriage data for this period.")
        st.stop()

    latest_year = selected_columns[-1]

    latest_rates = marriage_filtered[latest_year].dropna()

    average_rate = latest_rates.mean()
    highest_rate = latest_rates.max()
    lowest_rate = latest_rates.min()

    # KPI cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average State-Level Rate",
        f"{average_rate:.2f}"
    )

    col2.metric(
        "Highest State-Level Rate",
        f"{highest_rate:.2f}"
    )

    col3.metric(
        "Lowest State-Level Rate",
        f"{lowest_rate:.2f}"
    )

    st.caption(
        f"Female marriage rates for {int(latest_year)}. "
        "Summary values are calculated across available states."
    )

    st.markdown("---")

    # Marriage heatmap
    st.subheader("Female Marriage Rates by State and Year")

    fig = px.imshow(
        marriage_filtered,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale=[
            "#E5ECE6",
            "#78927B",
            "#183D2B",
            "#C6537C",
            "#A62959"
        ],
        labels={
            "x": "Year",
            "y": "Malaysian State",
            "color": "Marriage Rate"
        }
    )

    fig.update_layout(
        **chart_layout(680),
        xaxis_title="Year",
        yaxis_title="Malaysian State",
        coloraxis_colorbar_title="Marriage Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "The heatmap uses colour intensity to highlight "
        "differences in female marriage rates across states "
        "and years, based on the supplied dataset."
    )

    with st.expander("View Marriage Rate Data"):

        st.dataframe(
            marriage_filtered,
            use_container_width=True
        )

        st.download_button(
            "Download Marriage Rate Data",
            marriage_filtered.to_csv(),
            file_name="marriage_rate_analysis.csv",
            mime="text/csv"
        )


# =====================================================
# 12. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    f"""
    <div class="footer">
        <b style="color:{DARK_GREEN};">
            🌿 Malaysian Data Visualization Dashboard
        </b><br>
        Population • Household Income • Marriage<br>
        Data Period: 2017–2023
    </div>
    """,
    unsafe_allow_html=True
)
