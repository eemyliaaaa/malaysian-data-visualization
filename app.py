
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Malaysian Data | Visualization Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. COLOUR THEME AND CUSTOM CSS
# =====================================================

MAROON = "#702D3A"
DARK_MAROON = "#57212C"
OLIVE = "#87966B"
LIGHT_OLIVE = "#E9EDDF"
CREAM = "#F8F6F0"
WHITE = "#FFFFFF"
TEXT = "#393536"
MUTED = "#77716D"
BORDER = "#E9E3DA"

st.markdown(
    f"""
    <style>

    /* Main application */
    .stApp {{
        background-color: {CREAM};
        color: {TEXT};
    }}

    .main .block-container {{
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {MAROON};
        border-right: none;
    }}

    section[data-testid="stSidebar"] * {{
        color: white;
    }}

    section[data-testid="stSidebar"] [data-testid="stRadio"] label {{
        padding: 8px 10px;
        border-radius: 8px;
    }}

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
        background-color: rgba(255,255,255,0.12);
    }}

    /* Headings */
    h1, h2, h3 {{
        color: {MAROON} !important;
        font-weight: 700 !important;
    }}

    h1 {{
        font-size: 2.15rem !important;
    }}

    h2 {{
        font-size: 1.5rem !important;
    }}

    h3 {{
        font-size: 1.15rem !important;
    }}

    /* KPI metric cards */
    [data-testid="stMetric"] {{
        background-color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 20px 22px;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(60,40,40,0.04);
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {MAROON} !important;
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
    }}

    /* Dividers */
    hr {{
        border-color: {BORDER};
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }}

    /* Select boxes and sliders */
    div[data-baseweb="select"] > div {{
        border-radius: 9px;
    }}

    /* Dataframes */
    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
        overflow: hidden;
    }}

    /* Buttons */
    .stDownloadButton button {{
        background-color: {OLIVE};
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }}

    .stDownloadButton button:hover {{
        background-color: {MAROON};
        color: white;
    }}

    /* Information boxes */
    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}

    /* Custom header */
    .dashboard-tag {{
        color: {OLIVE};
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}

    .page-description {{
        color: {MUTED};
        font-size: 1rem;
        margin-bottom: 1.4rem;
    }}

    .section-label {{
        color: {MAROON};
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 12px;
    }}

    .footer {{
        color: {MUTED};
        font-size: 0.8rem;
        text-align: center;
        padding: 15px 0;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# 3. LOAD DATASETS
# =====================================================

@st.cache_data
def load_data():

    population = pd.read_csv("population_clean.csv")
    income = pd.read_csv("income_clean.csv")
    marriages = pd.read_csv("marriages_clean.csv")

    # Standardise state names
    for df in [population, income, marriages]:
        df["state"] = df["state"].astype(str).str.strip()

    # Ensure year columns are numeric
    for df in [population, income, marriages]:
        df["year"] = pd.to_numeric(
            df["year"], errors="coerce"
        )

    return population, income, marriages


try:
    population, income, marriages = load_data()

except Exception as error:
    st.error(f"Unable to load the datasets: {error}")
    st.stop()


# =====================================================
# 4. COMMON CHART SETTINGS
# =====================================================

CHART_LAYOUT = {
    "template": "plotly_white",
    "font": {
        "family": "Arial, sans-serif",
        "color": TEXT,
        "size": 12
    },
    "paper_bgcolor": WHITE,
    "plot_bgcolor": WHITE,
    "margin": dict(l=25, r=25, t=65, b=35),
    "legend": dict(
        bgcolor="rgba(255,255,255,0.8)"
    )
}

# =====================================================
# 5. SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding:12px 0 22px 0;">
            <div style="font-size:2rem;">📊</div>
            <div style="
                font-size:1.45rem;
                font-weight:800;
                color:white;">
                Malaysian Data
            </div>
            <div style="
                font-size:0.9rem;
                color:#E9DDE0;
                margin-top:5px;">
                Visualization Dashboard
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        "<p style='font-size:0.75rem;"
        "letter-spacing:1px;font-weight:700;'>"
        "ANALYSIS MENU</p>",
        unsafe_allow_html=True
    )

    page = st.radio(
        "Choose analysis",
        [
            "Population Analysis",
            "Household Income Analysis",
            "Marriage Analysis"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="padding-top:8px;">
            <div style="font-size:0.8rem;color:#E9DDE0;">
                DATA COVERAGE
            </div>
            <div style="
                font-size:1rem;
                font-weight:600;
                color:white;
                margin-top:5px;">
                Malaysia | 2017–2023
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.caption("Data Visualization Project")


# =====================================================
# 6. PAGE HEADER FUNCTION
# =====================================================

def page_header(title, description, objective):

    st.markdown(
        '<div class="dashboard-tag">'
        'MALAYSIAN DATA VISUALIZATION'
        '</div>',
        unsafe_allow_html=True
    )

    st.title(title)

    st.markdown(
        f'<div class="page-description">{description}</div>',
        unsafe_allow_html=True
    )

    st.info(f"**Visualization objective:** {objective}")


# =====================================================
# 7. POPULATION ANALYSIS
# =====================================================

if page == "Population Analysis":

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

    # Year filter
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

    # Filter population data
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

    # Total population by year
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
        ((end_population - start_population)
         / start_population * 100)
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
        labels={
            "year": "Year",
            "population": "Population (thousands)",
            "state": "Malaysian State"
        }
    )

    fig.update_layout(
        **CHART_LAYOUT,
        height=560,
        hovermode="x unified",
        xaxis=dict(
            title="Year",
            dtick=1
        ),
        yaxis_title="Population (thousands)",
        legend_title="State"
    )

    fig.update_traces(
        line=dict(width=2),
        marker=dict(size=6)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Data table
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
# 8. HOUSEHOLD INCOME ANALYSIS
# =====================================================

elif page == "Household Income Analysis":

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

    # Survey year filter
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
        st.warning("No income data is available for this year.")
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
                    color="#D8D5CE",
                    width=3
                ),
                showlegend=False,
                hoverinfo="skip"
            )
        )

    # Median income points
    fig.add_trace(
        go.Scatter(
            x=income_chart["income_median"],
            y=income_chart["state"],
            mode="markers",
            name="Median Income",
            marker=dict(
                color=OLIVE,
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

    # Mean income points
    fig.add_trace(
        go.Scatter(
            x=income_chart["income_mean"],
            y=income_chart["state"],
            mode="markers",
            name="Mean Income",
            marker=dict(
                color=MAROON,
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
        **CHART_LAYOUT,
        height=680,
        xaxis_title="Monthly Household Income (RM)",
        yaxis_title="Malaysian State",
        legend_title="Income Measurement",
        hovermode="closest"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Interpretation
    st.markdown("### Understanding the Income Difference")

    st.markdown(
        """
        - **Mean income:** The average household income.
        - **Median income:** The middle value when household
          incomes are arranged from lowest to highest.
        - **Connecting line:** Shows the difference between
          mean and median income for each state.
        """
    )

    st.info(
        "When mean income is higher than median income, "
        "higher-income households may be influencing the average. "
        "The difference between the two measures does not, "
        "by itself, describe the full income distribution."
    )

    # Income data
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
# 9. MARRIAGE ANALYSIS
# =====================================================

elif page == "Marriage Analysis":

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

    # Select female marriage records
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
        st.warning("No female marriage rate data is available.")
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

    # Filter years
    selected_columns = [
        year for year in marriage_pivot.columns
        if selected_years[0] <= year <= selected_years[1]
    ]

    marriage_filtered = marriage_pivot[selected_columns]

    if marriage_filtered.empty:
        st.warning("No marriage data is available for this period.")
        st.stop()

    # Summary metrics
    latest_year = selected_columns[-1]

    latest_rates = marriage_filtered[latest_year].dropna()

    average_rate = latest_rates.mean()
    highest_rate = latest_rates.max()
    lowest_rate = latest_rates.min()

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
            "#F1EBDD",
            "#D4B17A",
            "#87966B",
            "#702D3A"
        ],
        labels={
            "x": "Year",
            "y": "Malaysian State",
            "color": "Marriage Rate"
        }
    )

    fig.update_layout(
        **CHART_LAYOUT,
        height=680,
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
        "and years. It uses the rate values recorded in "
        "the supplied dataset."
    )

    # Marriage data
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
# 10. FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        <b>Malaysian Data Visualization Dashboard</b><br>
        Population • Household Income • Marriage<br>
        Data Period: 2017–2023
    </div>
    """,
    unsafe_allow_html=True
)
