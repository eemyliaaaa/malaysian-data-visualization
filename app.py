
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
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. COLOUR PALETTE
# =====================================================

DARK_GREEN = "#183D2B"
GREEN = "#28583D"
GREEN_LIGHT = "#52775C"

DARK_PINK = "#A62959"
PINK = "#C13C70"
PINK_LIGHT = "#D96A91"

BACKGROUND = "#EAE6DE"
WHITE = "#FFFFFF"
TEXT = "#252A26"
MUTED = "#686D68"
BORDER = "#D6D0C6"

# =====================================================
# 3. CUSTOM CSS
# =====================================================

st.markdown(
    f"""
    <style>

    /* Overall page */
    .stApp {{
        background: {BACKGROUND};
        color: {TEXT};
    }}

    .main .block-container {{
        max-width: 1500px;
        padding: 1.2rem 2.5rem 2rem 2.5rem;
    }}

    /* Hide sidebar */
    [data-testid="stSidebar"] {{
        display: none;
    }}

    /* Reduce vertical spacing */
    div[data-testid="stVerticalBlock"] {{
        gap: 0.8rem;
    }}

    h1, h2, h3 {{
        color: {DARK_GREEN} !important;
        font-weight: 800 !important;
    }}

    h1 {{
        font-size: 2.2rem !important;
        letter-spacing: -0.8px;
        margin-bottom: 0.2rem !important;
    }}

    h2 {{
        font-size: 1.45rem !important;
    }}

    h3 {{
        font-size: 1.1rem !important;
    }}

    /* Header branding */
    .top-header {{
        background: {DARK_GREEN};
        padding: 20px 25px;
        border-radius: 14px;
        border-bottom: 5px solid {DARK_PINK};
        color: white;
        margin-bottom: 12px;
    }}

    .top-header h2 {{
        color: white !important;
        margin: 0;
        font-size: 1.65rem !important;
    }}

    .top-header p {{
        color: #E7EDE8;
        margin: 3px 0 0 0;
        font-size: 0.88rem;
    }}

    .header-right {{
        color: white;
        text-align: right;
        font-size: 0.8rem;
        font-weight: 700;
        line-height: 1.7;
        padding-top: 7px;
    }}

    /* Page title */
    .eyebrow {{
        color: {DARK_PINK};
        font-size: 0.73rem;
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 4px;
    }}

    .description {{
        color: {MUTED};
        font-size: 0.96rem;
        margin-bottom: 10px;
    }}

    /* Objective panel */
    .objective {{
        background: {DARK_GREEN};
        color: white;
        padding: 14px 18px;
        border-radius: 9px;
        border-left: 6px solid {DARK_PINK};
        margin: 10px 0 15px 0;
        line-height: 1.55;
    }}

    .objective strong {{
        color: #F5B6CE;
        display: block;
        margin-bottom: 3px;
        font-size: 0.9rem;
    }}

    /* Section headings */
    .section-heading {{
        color: {DARK_GREEN};
        font-size: 1.15rem;
        font-weight: 800;
        border-left: 5px solid {DARK_PINK};
        padding-left: 10px;
        margin: 12px 0 8px 0;
    }}

    /* KPI cards */
    [data-testid="stMetric"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-top: 4px solid {DARK_GREEN};
        border-radius: 10px;
        padding: 14px 17px;
        min-height: 105px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {DARK_GREEN} !important;
        font-size: 1.55rem !important;
        font-weight: 850 !important;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
    }}

    [data-testid="stMetricDelta"] {{
        color: {DARK_PINK} !important;
    }}

    /* Navigation */
    div[role="radiogroup"] {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }}

    div[role="radiogroup"] label {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 8px 14px;
        font-weight: 650;
    }}

    div[role="radiogroup"] label:hover {{
        border-color: {DARK_PINK};
        background: #F4E6EB;
    }}

    /* Inputs */
    div[data-baseweb="select"] > div {{
        background: {WHITE};
        border-radius: 8px;
        border-color: {BORDER};
    }}

    /* Slider */
    input[type="range"] {{
        accent-color: {DARK_PINK};
    }}

    /* Charts */
    [data-testid="stPlotlyChart"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 11px;
        padding: 7px;
        box-shadow: 0 3px 9px rgba(0,0,0,0.04);
    }}

    /* Expander */
    [data-testid="stExpander"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 9px;
    }}

    /* Download button */
    .stDownloadButton button {{
        background: {DARK_GREEN};
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        padding: 8px 16px;
    }}

    .stDownloadButton button:hover {{
        background: {DARK_PINK};
        color: white;
    }}

    /* Custom insight panels */
    .insight {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-left: 5px solid {DARK_PINK};
        border-radius: 9px;
        padding: 13px 16px;
        color: {TEXT};
        line-height: 1.6;
        margin: 8px 0;
    }}

    .insight strong {{
        color: {DARK_GREEN};
    }}

    /* Footer */
    .footer {{
        background: {DARK_GREEN};
        color: white;
        text-align: center;
        padding: 16px;
        border-radius: 10px;
        border-top: 4px solid {DARK_PINK};
        font-size: 0.82rem;
        line-height: 1.8;
        margin-top: 20px;
    }}

    .footer strong {{
        color: #F5B6CE;
    }}

    /* Reduce default divider space */
    hr {{
        border-color: {BORDER};
        margin: 0.8rem 0;
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

def chart_layout(height=480):

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
        "margin": dict(l=35, r=35, t=45, b=35),
        "legend": {
            "bgcolor": "rgba(255,255,255,0.85)",
            "borderwidth": 0
        }
    }


# =====================================================
# 6. TOP HEADER
# =====================================================

left, right = st.columns([4, 1])

with left:

    st.markdown(
        f"""
        <div class="top-header">
            <h2>📊 Malaysian Data</h2>
            <p>Interactive Data Visualization Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:

    st.markdown(
        """
        <div class="header-right">
            MALAYSIA<br>
            2017 – 2023
        </div>
        """,
        unsafe_allow_html=True
    )


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
        <div class="objective">
            <strong>VISUALIZATION OBJECTIVE</strong>
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
        '<div class="section-heading">Population Overview</div>',
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

    # Interactive state selection
    st.markdown(
        '<div class="section-heading">Population Trend by State</div>',
        unsafe_allow_html=True
    )

    latest_state_population = (
        population_trend[
            population_trend["year"] == population_trend["year"].max()
        ]
        .sort_values("population", ascending=False)
    )

    default_states = latest_state_population["state"].head(6).tolist()

    all_states = sorted(population_trend["state"].unique())

    selected_states = st.multiselect(
        "Select states to compare",
        options=all_states,
        default=default_states,
        key="population_states"
    )

    population_chart = population_trend[
        population_trend["state"].isin(selected_states)
    ]

    if population_chart.empty:
        st.warning("Please select at least one state.")
    else:

        fig = px.line(
            population_chart,
            x="year",
            y="population",
            color="state",
            markers=True,
            color_discrete_sequence=[
                DARK_GREEN,
                DARK_PINK,
                GREEN,
                PINK,
                GREEN_LIGHT,
                PINK_LIGHT,
                "#73516A",
                "#647A64",
                "#8F3158",
                "#345E4A",
                "#D07896",
                "#476B58",
                "#B64B72",
                "#244B35",
                "#A65C7C",
                "#547C69",
                "#7C274B"
            ],
            labels={
                "year": "Year",
                "population": "Population (thousands)",
                "state": "Malaysian State"
            }
        )

        fig.update_layout(
            **chart_layout(490),
            hovermode="x unified",
            xaxis=dict(
                title="Year",
                dtick=1
            ),
            yaxis_title="Population (thousands)",
            legend_title="State"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
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
        '<div class="section-heading">Income Overview</div>',
        unsafe_allow_html=True
    )

    available_years = sorted(
        income["year"].dropna().unique()
    )

    if not available_years:
        st.warning("No household income data is available.")
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
        .sort_values("income_mean", ascending=False)
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

    st.markdown(
        '<div class="section-heading">Mean vs Median Income</div>',
        unsafe_allow_html=True
    )

    # Dumbbell chart
    fig = go.Figure()

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
                    color="#B9C3BA",
                    width=3
                ),
                showlegend=False,
                hoverinfo="skip"
            )
        )

    # Median income
    fig.add_trace(
        go.Scatter(
            x=income_chart["income_median"],
            y=income_chart["state"],
            mode="markers",
            name="Median Income",
            marker=dict(
                color=DARK_GREEN,
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

    # Mean income
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
        **chart_layout(560),
        xaxis_title="Monthly Household Income (RM)",
        yaxis_title="Malaysian State",
        legend_title="Income Measurement",
        hovermode="closest"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Explanation panel
    st.markdown(
        '<div class="section-heading">Understanding the Income Difference</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight">
            <strong style="color:{DARK_GREEN};">
                ● Median Income
            </strong><br>
            The middle value when household incomes are
            arranged from lowest to highest.
            <br><br>

            <strong style="color:{DARK_PINK};">
                ● Mean Income
            </strong><br>
            The average household income.
            <br><br>

            <strong>Connecting line</strong><br>
            Shows the difference between mean and median
            income for each state.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight">
            When mean income is higher than median income,
            higher-income households may influence the average.
            The difference alone does not describe the full
            income distribution.
        </div>
        """,
        unsafe_allow_html=True
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
        '<div class="section-heading">Marriage Overview</div>',
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

    st.markdown(
        '<div class="section-heading">Female Marriage Rates by State and Year</div>',
        unsafe_allow_html=True
    )

    # Marriage heatmap
    fig = px.imshow(
        marriage_filtered,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale=[
            "#EAE6DE",
            "#78927B",
            "#28583D",
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
        **chart_layout(560),
        xaxis_title="Year",
        yaxis_title="Malaysian State",
        coloraxis_colorbar_title="Marriage Rate"
    )

    fig.update_traces(
        textfont=dict(
            size=11,
            color=TEXT
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        f"""
        <div class="insight">
            <strong>How to interpret the heatmap</strong><br>
            Dark green and dark pink shades indicate different
            levels of female marriage rates. Comparing the
            colours across rows and columns helps identify
            differences between states and changes over time.
        </div>
        """,
        unsafe_allow_html=True
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

st.markdown(
    f"""
    <div class="footer">
        <strong>📊 Malaysian Data Visualization Dashboard</strong><br>
        Population &nbsp; • &nbsp;
        Household Income &nbsp; • &nbsp;
        Marriage<br>
        Data Period: 2017–2023
    </div>
    """,
    unsafe_allow_html=True
)
