
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Malaysian Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. COLOUR PALETTE
# =========================================================

DARK_GREEN = "#174C35"
GREEN = "#247A53"
GREEN_LIGHT = "#58A987"
GREEN_PALE = "#E5F0E9"

DARK_PINK = "#A62959"
PINK = "#C87591"

BACKGROUND = "#ECEEEC"
WHITE = "#FFFFFF"
TEXT = "#202722"
MUTED = "#858D87"
BORDER = "#E8ECE8"
GRID = "#EDF0ED"

# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* Main application background */
    .stApp {{
        background: {BACKGROUND};
        color: {TEXT};
    }}

    .main .block-container {{
        max-width: 100%;
        padding: 1.15rem 1.5rem 2rem 1.5rem;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        display: block !important;
        background: {WHITE};
        border-right: 1px solid {BORDER};
        min-width: 235px;
        max-width: 235px;
    }}

    section[data-testid="stSidebar"] > div {{
        padding: 1.1rem 0.9rem;
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {{
        color: {DARK_GREEN} !important;
    }}

    .sidebar-brand {{
        font-size: 1.5rem;
        font-weight: 850;
        color: {DARK_GREEN};
        padding: 10px 5px 2px 5px;
        letter-spacing: -0.5px;
    }}

    .sidebar-subtitle {{
        font-size: 0.78rem;
        color: {MUTED};
        padding: 0 5px 20px 5px;
    }}

    .sidebar-label {{
        font-size: 0.68rem;
        color: {MUTED};
        font-weight: 800;
        letter-spacing: 1.5px;
        padding: 12px 5px 5px 5px;
    }}

    /* Sidebar navigation buttons */
    section[data-testid="stSidebar"]
    div[role="radiogroup"] {{
        gap: 5px;
    }}

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {{
        background: transparent;
        border: none;
        border-radius: 8px;
        padding: 10px 9px;
        color: {MUTED};
        font-weight: 600;
    }}

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {{
        background: {GREEN_PALE};
        color: {DARK_GREEN};
    }}

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:has(input:checked) {{
        background: {GREEN_PALE};
        color: {DARK_GREEN};
        border-left: 4px solid {GREEN};
    }}

    /* Main header */
    .topbar {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 13px;
        padding: 14px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 17px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.025);
    }}

    .topbar-title {{
        color: {DARK_GREEN};
        font-size: 1.25rem;
        font-weight: 800;
    }}

    .topbar-subtitle {{
        color: {MUTED};
        font-size: 0.78rem;
        margin-top: 3px;
    }}

    .topbar-period {{
        color: {DARK_GREEN};
        font-size: 0.78rem;
        font-weight: 750;
        text-align: right;
    }}

    /* Page title */
    .eyebrow {{
        color: {GREEN};
        font-size: 0.68rem;
        font-weight: 850;
        letter-spacing: 1.7px;
        margin-bottom: 5px;
    }}

    h1 {{
        color: {DARK_GREEN} !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.6px;
        margin-bottom: 0 !important;
    }}

    h2 {{
        color: {DARK_GREEN} !important;
        font-size: 1.25rem !important;
        font-weight: 750 !important;
    }}

    h3 {{
        color: {DARK_GREEN} !important;
        font-size: 1rem !important;
        font-weight: 750 !important;
    }}

    .page-description {{
        color: {MUTED};
        font-size: 0.88rem;
        margin: 3px 0 13px 0;
    }}

    /* Objective card */
    .objective-card {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-left: 4px solid {GREEN};
        border-radius: 10px;
        padding: 12px 16px;
        margin: 10px 0 16px 0;
        line-height: 1.5;
    }}

    .objective-label {{
        color: {GREEN};
        font-size: 0.68rem;
        font-weight: 850;
        letter-spacing: 1px;
        margin-bottom: 3px;
    }}

    .objective-text {{
        color: {TEXT};
        font-size: 0.85rem;
    }}

    /* KPI cards */
    [data-testid="stMetric"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 15px 16px;
        min-height: 108px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.025);
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {DARK_GREEN} !important;
        font-size: 1.55rem !important;
        font-weight: 850 !important;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
    }}

    [data-testid="stMetricDelta"] {{
        color: {GREEN} !important;
        font-size: 0.75rem !important;
    }}

    /* Chart card */
    [data-testid="stPlotlyChart"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.025);
    }}

    /* Streamlit bordered containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}

    /* Inputs */
    div[data-baseweb="select"] > div {{
        background: {WHITE};
        border-radius: 8px;
        border-color: {BORDER};
    }}

    /* Select slider accent */
    input[type="range"] {{
        accent-color: {GREEN};
    }}

    /* Insight cards */
    .insight-card {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 12px 14px;
        color: {TEXT};
        font-size: 0.84rem;
        line-height: 1.6;
    }}

    .insight-card strong {{
        color: {DARK_GREEN};
    }}

    .pink-text {{
        color: {DARK_PINK};
        font-weight: 750;
    }}

    /* Expanders */
    [data-testid="stExpander"] {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 9px;
    }}

    /* Download buttons */
    .stDownloadButton button {{
        background: {DARK_GREEN};
        color: {WHITE};
        border: none;
        border-radius: 8px;
        font-weight: 650;
    }}

    .stDownloadButton button:hover {{
        background: {GREEN};
        color: {WHITE};
    }}

    /* Footer */
    .footer {{
        background: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 13px;
        text-align: center;
        color: {MUTED};
        font-size: 0.76rem;
        margin-top: 20px;
        line-height: 1.8;
    }}

    .footer strong {{
        color: {DARK_GREEN};
    }}

    /* Reduce vertical gaps */
    div[data-testid="stVerticalBlock"] {{
        gap: 0.7rem;
    }}

    hr {{
        border-color: {BORDER};
        margin: 0.7rem 0;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 4. LOAD DATASETS
# =========================================================

@st.cache_data
def load_data():

    population = pd.read_csv("population_clean.csv")
    income = pd.read_csv("income_clean.csv")
    marriages = pd.read_csv("marriages_clean.csv")

    for df in [population, income, marriages]:

        df["state"] = df["state"].astype(str).str.strip()

        df["year"] = pd.to_numeric(
            df["year"], errors="coerce"
        )

    return population, income, marriages


try:

    population, income, marriages = load_data()

except Exception as error:

    st.error(
        f"Unable to load datasets. Check the CSV filenames "
        f"and column names. Details: {error}"
    )

    st.stop()


# =========================================================
# 5. COMMON CHART SETTINGS
# =========================================================

def chart_layout(height=420):

    return {
        "template": "plotly_white",
        "height": height,
        "paper_bgcolor": WHITE,
        "plot_bgcolor": WHITE,
        "font": {
            "family": "Arial, sans-serif",
            "color": TEXT,
            "size": 11
        },
        "margin": dict(
            l=35,
            r=25,
            t=35,
            b=35
        ),
        "hoverlabel": {
            "bgcolor": WHITE,
            "font_color": TEXT
        }
    }


# =========================================================
# 6. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">📊 Malaysian Data</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Visualization Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-label">ANALYSIS MENU</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Population Analysis",
            "Household Income",
            "Marriage Analysis"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-label">DATA COVERAGE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            color:{DARK_GREEN};
            font-size:0.85rem;
            font-weight:750;
            padding:5px;">
            Malaysia | 2017–2023
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.caption("DATA SOURCES")

    st.markdown(
        """
        <div style="
            color:#858D87;
            font-size:0.76rem;
            line-height:1.8;">
            Population Dataset<br>
            Household Income Dataset<br>
            Marriage Dataset
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.caption("Malaysian Data Visualization Project")


# =========================================================
# 7. TOP HEADER
# =========================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        f"""
        <div class="topbar">
            <div>
                <div class="topbar-title">
                    {page}
                </div>
                <div class="topbar-subtitle">
                    Malaysian Data Visualization Dashboard
                </div>
            </div>
            <div class="topbar-period">
                MALAYSIA<br>
                2017 – 2023
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 8. PAGE HEADER FUNCTION
# =========================================================

def page_header(title, description, objective):

    st.markdown(
        '<div class="eyebrow">MALAYSIAN DATA VISUALIZATION</div>',
        unsafe_allow_html=True
    )

    st.title(title)

    st.markdown(
        f'<div class="page-description">{description}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="objective-card">
            <div class="objective-label">
                VISUALIZATION OBJECTIVE
            </div>
            <div class="objective-text">
                {objective}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 9. POPULATION ANALYSIS
# =========================================================

if page == "Population Analysis":

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
        )["population"]
        .sum()
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

    # KPI CARDS
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

    # CHART CARD
    st.markdown("### Population Growth by State")

    with st.container(border=True):

        all_states = sorted(
            population_trend["state"].unique()
        )

        default_states = all_states

        selected_states = st.multiselect(
            "Select states to display",
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

            state_colors = [
                DARK_GREEN,
                DARK_PINK,
                GREEN,
                PINK,
                SAGE,
                "#735B68",
                "#55705B",
                "#B36C83",
                "#345B43",
                "#916477",
                "#708A74",
                "#A34A6C",
                "#294B37",
                "#C18A9D",
                "#607665",
                "#88445D",
                "#9BA99B"
            ]

            fig = px.line(
                population_chart,
                x="year",
                y="population",
                color="state",
                markers=True,
                color_discrete_sequence=state_colors,
                labels={
                    "year": "Year",
                    "population": "Population (thousands)",
                    "state": "State"
                }
            )

            fig.update_layout(
                **chart_layout(430),
                hovermode="x unified",
                xaxis_title="Year",
                yaxis_title="Population (thousands)",
                legend_title="State"
            )

            fig.update_xaxes(
                dtick=1,
                gridcolor=GRID
            )

            fig.update_yaxes(
                gridcolor=GRID,
                zeroline=False
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


# =========================================================
# 10. HOUSEHOLD INCOME ANALYSIS
# =========================================================

elif page == "Household Income":

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
        st.warning("No income data is available.")
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

    # KPI CARDS
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

    # DUMBBELL CHART CARD
    st.markdown("### Mean vs Median Household Income")

    with st.container(border=True):

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
                        color="#CBD3CC",
                        width=3
                    ),
                    showlegend=False,
                    hoverinfo="skip"
                )
            )

        # Median
        fig.add_trace(
            go.Scatter(
                x=income_chart["income_median"],
                y=income_chart["state"],
                mode="markers",
                name="Median Income",
                marker=dict(
                    color=DARK_GREEN,
                    size=11,
                    line=dict(color=WHITE, width=1.5)
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Median Income: RM %{x:,.0f}"
                    "<extra></extra>"
                )
            )
        )

        # Mean
        fig.add_trace(
            go.Scatter(
                x=income_chart["income_mean"],
                y=income_chart["state"],
                mode="markers",
                name="Mean Income",
                marker=dict(
                    color=DARK_PINK,
                    size=11,
                    line=dict(color=WHITE, width=1.5)
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Mean Income: RM %{x:,.0f}"
                    "<extra></extra>"
                )
            )
        )

        fig.update_layout(
            **chart_layout(490),
            xaxis_title="Monthly Household Income (RM)",
            yaxis_title="Malaysian State",
            legend_title="Income Measurement",
            hovermode="closest"
        )

        fig.update_xaxes(gridcolor=GRID)

        fig.update_yaxes(
            gridcolor=GRID,
            autorange="reversed"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # EXPLANATION CARDS
    st.markdown("### Understanding the Income Difference")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="insight-card">
                <strong style="color:{DARK_GREEN};">
                    ● Median Income
                </strong><br>
                The middle value when household incomes are
                arranged from lowest to highest.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="insight-card">
                <strong style="color:{DARK_PINK};">
                    ● Mean Income
                </strong><br>
                The average household income across the
                selected state's households.
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


# =========================================================
# 11. MARRIAGE ANALYSIS
# =========================================================

elif page == "Marriage Analysis":

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
        )["rate"]
        .mean()
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

    # KPI CARDS
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

    # HEATMAP CARD
    st.markdown("### Female Marriage Rates by State and Year")

    with st.container(border=True):

        fig = px.imshow(
            marriage_filtered,
            text_auto=".1f",
            aspect="auto",
            color_continuous_scale=[
                "#F1F4F1",
                "#D5E2D8",
                "#A2BBA8",
                "#527F61",
                "#174C35"
            ],
            labels={
                "x": "Year",
                "y": "Malaysian State",
                "color": "Marriage Rate"
            }
        )

        fig.update_layout(
            **chart_layout(500),
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
        """
        <div class="insight-card">
            <strong>Heatmap interpretation:</strong>
            Darker green shades indicate higher female marriage
            rates, while lighter shades indicate lower rates.
            Comparing the rows and columns helps identify
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


# =========================================================
# 12. FOOTER
# =========================================================

st.markdown(
    f"""
    <div class="footer">
        <strong>📊 Malaysian Data Visualization Dashboard</strong><br>
        Population &nbsp; • &nbsp;
        Household Income &nbsp; • &nbsp;
        Marriage<br>
        Data Coverage: Malaysia | 2017–2023
    </div>
    """,
    unsafe_allow_html=True
)
