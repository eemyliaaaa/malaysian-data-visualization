
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Malaysian Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT = Path(__file__).parent

# Dataset files are expected beside app.py.
POPULATION_FILE = ROOT / "population_clean.csv"
INCOME_FILE = ROOT / "income_clean.csv"
MARRIAGE_FILE = ROOT / "marriages_clean.csv"


# =========================================================
# 2. COLOUR PALETTE
# =========================================================

GREEN = "#174C35"
GREEN_DARK = "#103B29"
GREEN_MEDIUM = "#26734D"
GREEN_LIGHT = "#8AA995"

PINK = "#A62959"
PINK_LIGHT = "#D98BA5"

BACKGROUND = "#E8E9E7"
WHITE = "#FFFFFF"
TEXT = "#202722"
MUTED = "#737C75"
BORDER = "#252B27"
GRID = "#E9EDE9"


# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    /* -----------------------------------------
       FULL SCREEN LAYOUT
    ----------------------------------------- */

    .stApp {{
        background: {BACKGROUND};
        color: {TEXT};
    }}

    .main .block-container {{
        width: 100% !important;
        max-width: 100% !important;
        padding: 0.8rem 1.5rem 1.2rem 1.5rem !important;
        margin: 0 !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
        height: 0;
    }}

    footer {{
        visibility: hidden;
    }}

    /* Remove sidebar completely */

    section[data-testid="stSidebar"] {{
        display: none !important;
    }}

    button[data-testid="collapsedControl"] {{
        display: none !important;
    }}

    /* -----------------------------------------
       GENERAL SPACING
    ----------------------------------------- */

    div[data-testid="stVerticalBlock"] {{
        gap: 0.65rem;
    }}

    h1, h2, h3 {{
        color: {GREEN} !important;
        font-weight: 800 !important;
    }}

    h1 {{
        font-size: 1.9rem !important;
        letter-spacing: -0.7px;
    }}

    h2 {{
        font-size: 1.2rem !important;
    }}

    h3 {{
        font-size: 1rem !important;
    }}

    p {{
        color: {TEXT};
    }}

    hr {{
        border-color: #D2D7D2;
        margin: 0.5rem 0;
    }}

    /* -----------------------------------------
       HEADER
    ----------------------------------------- */

    .brand-header {{
        width: 100%;
        background: {GREEN};
        color: white;
        border: 1.5px solid {BORDER};
        border-bottom: 5px solid {PINK};
        border-radius: 15px;
        padding: 17px 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
    }}

    .brand-name {{
        font-size: 1.5rem;
        font-weight: 850;
        letter-spacing: -0.5px;
        color: white;
    }}

    .brand-caption {{
        font-size: 0.8rem;
        color: #DCE8E0;
        margin-top: 4px;
    }}

    .brand-period {{
        text-align: right;
        font-size: 0.78rem;
        font-weight: 750;
        line-height: 1.7;
        color: white;
    }}

    /* -----------------------------------------
       HORIZONTAL NAVIGATION
    ----------------------------------------- */

    div[role="radiogroup"] {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 5px 0 12px 0;
    }}

    div[role="radiogroup"] label {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 10px;
        padding: 10px 21px;
        color: {TEXT};
        font-size: 0.87rem;
        font-weight: 650;
        transition: all 0.2s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.035);
    }}

    div[role="radiogroup"] label:hover {{
        background: #E6EEE8;
        border-color: {GREEN};
        color: {GREEN};
        transform: translateY(-2px);
    }}

    div[role="radiogroup"] label:has(input:checked) {{
        background: {GREEN};
        color: white;
        border: 1.5px solid {BORDER};
        border-bottom: 4px solid {PINK};
    }}

    div[role="radiogroup"] label:has(input:checked) p {{
        color: white !important;
    }}

    /* -----------------------------------------
       PAGE HEADING
    ----------------------------------------- */

    .eyebrow {{
        color: {PINK};
        font-size: 0.68rem;
        font-weight: 850;
        letter-spacing: 1.8px;
        margin-bottom: 4px;
    }}

    .page-description {{
        color: {MUTED};
        font-size: 0.88rem;
        margin-top: -7px;
        margin-bottom: 10px;
    }}

    /* -----------------------------------------
       OBJECTIVE CARD
    ----------------------------------------- */

    .objective-card {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-left: 5px solid {GREEN};
        border-radius: 10px;
        padding: 12px 16px;
        margin: 8px 0 13px 0;
        line-height: 1.6;
        font-size: 0.85rem;
    }}

    .objective-card strong {{
        color: {GREEN};
    }}

    /* -----------------------------------------
       KPI CARDS
    ----------------------------------------- */

    [data-testid="stMetric"] {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 12px;
        padding: 15px 17px;
        min-height: 105px;
        box-shadow: 0 3px 9px rgba(0,0,0,0.045);
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {GREEN} !important;
        font-size: 1.65rem !important;
        font-weight: 850 !important;
        overflow-wrap: anywhere;
    }}

    [data-testid="stMetricDelta"] {{
        color: {PINK} !important;
        font-size: 0.75rem !important;
    }}

    /* -----------------------------------------
       CHART CARDS
    ----------------------------------------- */

    [data-testid="stPlotlyChart"] {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 13px;
        padding: 7px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.045);
    }}

    /* -----------------------------------------
       INSIGHT CARDS
    ----------------------------------------- */

    .insight-card {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-left: 4px solid {PINK};
        border-radius: 10px;
        padding: 13px 16px;
        font-size: 0.84rem;
        line-height: 1.65;
        color: {TEXT};
    }}

    .insight-card strong {{
        color: {GREEN};
    }}

    /* -----------------------------------------
       SELECT BOXES
    ----------------------------------------- */

    div[data-baseweb="select"] > div {{
        background: {WHITE};
        border-radius: 8px;
        border-color: {BORDER};
    }}

    /* -----------------------------------------
       EXPANDERS
    ----------------------------------------- */

    [data-testid="stExpander"] {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 10px;
    }}

    /* -----------------------------------------
       DOWNLOAD BUTTONS
    ----------------------------------------- */

    .stDownloadButton button {{
        background: {GREEN};
        color: white;
        border: 1px solid {BORDER};
        border-radius: 8px;
        font-weight: 650;
    }}

    .stDownloadButton button:hover {{
        background: {GREEN_MEDIUM};
        color: white;
    }}

    /* -----------------------------------------
       FOOTER
    ----------------------------------------- */

    .dashboard-footer {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 11px;
        padding: 13px;
        margin-top: 15px;
        text-align: center;
        color: {MUTED};
        font-size: 0.76rem;
        line-height: 1.8;
    }}

    .dashboard-footer strong {{
        color: {GREEN};
    }}

    /* -----------------------------------------
       SMALL SCREENS
    ----------------------------------------- */

    @media (max-width: 768px) {{

        .main .block-container {{
            padding: 0.6rem !important;
        }}

        .brand-header {{
            padding: 14px;
        }}

        .brand-name {{
            font-size: 1.2rem;
        }}

        div[role="radiogroup"] label {{
            padding: 8px 11px;
            font-size: 0.78rem;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 4. DATA LOADING AND PREPROCESSING
# =========================================================

@st.cache_data
def load_data():

    # Load cleaned datasets
    population = pd.read_csv(POPULATION_FILE)
    income = pd.read_csv(INCOME_FILE)
    marriages = pd.read_csv(MARRIAGE_FILE)

    # Standardise column names
    for df in [population, income, marriages]:
        df.columns = df.columns.str.strip()

    # Standardise state names
    for df in [population, income, marriages]:
        if "state" not in df.columns:
            raise ValueError("Missing state column.")

        df["state"] = df["state"].astype(str).str.strip()

    # Extract year if not already available
    for df in [population, income, marriages]:

        if "year" not in df.columns:

            if "date" not in df.columns:
                raise ValueError("Missing year/date column.")

            df["year"] = pd.to_datetime(
                df["date"],
                errors="coerce"
            ).dt.year

        df["year"] = pd.to_numeric(
            df["year"],
            errors="coerce"
        )

        df.dropna(
            subset=["year", "state"],
            inplace=True
        )

        df["year"] = df["year"].astype(int)

        # Keep the study period
        df.drop(
            df[~df["year"].between(2017, 2023)].index,
            inplace=True
        )

    # Convert numerical fields
    numeric_columns = {
        "population": population,
        "income_mean": income,
        "income_median": income,
        "rate": marriages
    }

    for column, df in numeric_columns.items():

        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Remove unusable records
    population = population.dropna(
        subset=["population"]
    ).copy()

    income = income.dropna(
        subset=["income_mean", "income_median"]
    ).copy()

    marriages = marriages.dropna(
        subset=["rate"]
    ).copy()

    # Remove exact duplicates
    population = population.drop_duplicates()
    income = income.drop_duplicates()
    marriages = marriages.drop_duplicates()

    return population, income, marriages


try:

    population, income, marriages = load_data()

except Exception as error:

    st.error(
        f"Unable to load the datasets: {error}"
    )

    st.info(
        "Check that all three cleaned CSV files are "
        "uploaded in the same GitHub folder as app.py."
    )

    st.stop()


# =========================================================
# 5. CHART LAYOUT FUNCTION
# =========================================================

def chart_layout(height=420):

    return dict(
        template="plotly_white",
        height=height,
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        font=dict(
            family="Arial",
            color=TEXT,
            size=11
        ),
        margin=dict(
            l=45,
            r=35,
            t=35,
            b=45
        ),
        hoverlabel=dict(
            bgcolor=WHITE,
            font_color=TEXT
        )
    )


# =========================================================
# 6. BRAND HEADER
# =========================================================

st.markdown(
    """
    <div class="brand-header">

        <div>
            <div class="brand-name">
                📊 Malaysian Data
            </div>

            <div class="brand-caption">
                Interactive Data Visualization Dashboard
            </div>
        </div>

        <div class="brand-period">
            MALAYSIA<br>
            2017 – 2023
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 7. HORIZONTAL NAVIGATION
# =========================================================

page = st.radio(
    "Navigation",
    [
        "Population",
        "Household Income",
        "Marriage"
    ],
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation"
)

st.markdown("---")


# =========================================================
# 8. PAGE HEADER FUNCTION
# =========================================================

def page_header(title, description, objective):

    st.markdown(
        '<div class="eyebrow">'
        'MALAYSIAN DATA VISUALIZATION'
        '</div>',
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
            <strong>Visualization Objective</strong><br>
            {objective}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 9. POPULATION ANALYSIS
# =========================================================

if page == "Population":

    page_header(
        "Population Analysis",
        "Explore population growth patterns across "
        "Malaysian states.",
        "Analyse population growth across Malaysian "
        "states from 2017 to 2023."
    )

    # Select year range
    available_years = sorted(
        population["year"].unique()
    )

    selected_range = st.slider(
        "Select year range",
        min_value=int(min(available_years)),
        max_value=int(max(available_years)),
        value=(
            int(min(available_years)),
            int(max(available_years))
        ),
        key="population_year_range"
    )

    pop_filtered = population[
        population["year"].between(
            selected_range[0],
            selected_range[1]
        )
    ].copy()

    # Aggregate population by state and year
    pop_trend = (
        pop_filtered.groupby(
            ["year", "state"],
            as_index=False
        )["population"].sum()
    )

    yearly_total = (
        pop_trend.groupby("year")["population"]
        .sum()
        .sort_index()
    )

    if yearly_total.empty:

        st.warning("No population records for this period.")

    else:

        start_value = yearly_total.iloc[0]
        end_value = yearly_total.iloc[-1]

        growth = (
            (end_value - start_value) / start_value * 100
            if start_value != 0 else 0
        )

        # KPI section
        st.markdown("### Population Overview")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Starting Population",
            f"{start_value:,.1f}k"
        )

        c2.metric(
            "Latest Population",
            f"{end_value:,.1f}k"
        )

        c3.metric(
            "Population Growth",
            f"{growth:.2f}%"
        )

        st.caption(
            "Population values are presented in thousands."
        )

        # Line chart
        st.markdown("### Population Growth by State")

        with st.container(border=True):

            states = sorted(
                pop_trend["state"].unique()
            )

            selected_states = st.multiselect(
                "Select states to display",
                states,
                default=states,
                key="population_states"
            )

            chart_data = pop_trend[
                pop_trend["state"].isin(selected_states)
            ]

            if not chart_data.empty:

                palette = [
                    GREEN,
                    PINK,
                    GREEN_MEDIUM,
                    PINK_LIGHT,
                    "#52735E",
                    "#87445E",
                    "#75917C",
                    "#B45D7B",
                    "#345A42",
                    "#A67A8A"
                ]

                fig = px.line(
                    chart_data,
                    x="year",
                    y="population",
                    color="state",
                    markers=True,
                    color_discrete_sequence=palette,
                    labels={
                        "year": "Year",
                        "population": "Population (thousands)",
                        "state": "State"
                    }
                )

                fig.update_layout(
                    **chart_layout(480),
                    hovermode="x unified",
                    legend_title="State"
                )

                fig.update_xaxes(
                    dtick=1,
                    gridcolor=GRID
                )

                fig.update_yaxes(
                    gridcolor=GRID
                )

                fig.update_traces(
                    line=dict(width=2.5),
                    marker=dict(size=6)
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    "Select at least one state to display."
                )

        # Data table
        with st.expander("View Population Data"):

            st.dataframe(
                pop_trend,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download Population Data",
                pop_trend.to_csv(index=False),
                "population_analysis.csv",
                "text/csv"
            )


# =========================================================
# 10. HOUSEHOLD INCOME ANALYSIS
# =========================================================

elif page == "Household Income":

    page_header(
        "Household Income Analysis",
        "Compare mean and median monthly household "
        "income across Malaysian states.",
        "Compare mean and median household income across "
        "Malaysian states for available survey years "
        "within 2017–2023."
    )

    available_years = sorted(
        income["year"].unique()
    )

    default_index = (
        available_years.index(2022)
        if 2022 in available_years
        else len(available_years) - 1
    )

    selected_year = st.selectbox(
        "Select survey year",
        available_years,
        index=default_index,
        format_func=lambda x: str(int(x))
    )

    income_selected = income[
        income["year"] == selected_year
    ].copy()

    # Aggregate state-level values
    income_chart = (
        income_selected.groupby(
            "state",
            as_index=False
        ).agg(
            income_mean=("income_mean", "mean"),
            income_median=("income_median", "mean")
        )
    )

    income_chart = income_chart.sort_values(
        "income_mean",
        ascending=False
    )

    if income_chart.empty:

        st.warning("No household income data available.")

    else:

        highest = income_chart.loc[
            income_chart["income_mean"].idxmax()
        ]

        lowest = income_chart.loc[
            income_chart["income_mean"].idxmin()
        ]

        average = income_chart["income_mean"].mean()

        # KPI section
        st.markdown("### Income Overview")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Highest Mean Income",
            f"RM {highest['income_mean']:,.0f}",
            highest["state"]
        )

        c2.metric(
            "Lowest Mean Income",
            f"RM {lowest['income_mean']:,.0f}",
            lowest["state"]
        )

        c3.metric(
            "Average Mean Income",
            f"RM {average:,.0f}"
        )

        st.caption(
            f"Household income survey year: {int(selected_year)}"
        )

        # Dumbbell chart
        st.markdown(
            "### Mean vs Median Household Income"
        )

        with st.container(border=True):

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
                            color="#C9D1CB",
                            width=4
                        ),
                        showlegend=False,
                        hoverinfo="skip"
                    )
                )

            # Median points
            fig.add_trace(
                go.Scatter(
                    x=income_chart["income_median"],
                    y=income_chart["state"],
                    mode="markers",
                    name="Median Income",
                    marker=dict(
                        color=GREEN,
                        size=11,
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

            # Mean points
            fig.add_trace(
                go.Scatter(
                    x=income_chart["income_mean"],
                    y=income_chart["state"],
                    mode="markers",
                    name="Mean Income",
                    marker=dict(
                        color=PINK,
                        size=11,
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
                **chart_layout(510),
                xaxis_title="Monthly Household Income (RM)",
                yaxis_title="Malaysian State",
                legend_title="Income Measurement",
                hovermode="closest"
            )

            fig.update_xaxes(
                gridcolor=GRID,
                tickformat=",.0f"
            )

            fig.update_yaxes(
                autorange="reversed",
                gridcolor=GRID
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # Explanation section
        st.markdown("### Understanding the Income Difference")

        left, right = st.columns(2)

        with left:

            st.markdown(
                f"""
                <div class="insight-card">
                    <strong style="color:{GREEN};">
                        ● Median Income
                    </strong><br>
                    The middle value when household incomes
                    are arranged from lowest to highest.
                </div>
                """,
                unsafe_allow_html=True
            )

        with right:

            st.markdown(
                f"""
                <div class="insight-card">
                    <strong style="color:{PINK};">
                        ● Mean Income
                    </strong><br>
                    The average household income calculated
                    across households.
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
                "income_analysis.csv",
                "text/csv"
            )


# =========================================================
# 11. MARRIAGE ANALYSIS
# =========================================================

elif page == "Marriage":

    page_header(
        "Marriage Analysis",
        "Explore annual female marriage rate patterns "
        "across Malaysian states.",
        "Examine annual female marriage rate trends "
        "across Malaysian states from 2017 to 2023."
    )

    # Select female records
    if "sex" not in marriages.columns:

        st.error(
            "The marriage dataset does not contain a sex column."
        )

        st.stop()

    marriages_female = marriages[
        marriages["sex"].astype(str).str.strip().str.lower()
        == "female"
    ].copy()

    if marriages_female.empty:

        st.error(
            "No female records found. Check the values "
            "in the sex column of marriages_clean.csv."
        )

        st.stop()

    # Aggregate rate by state and year
    marriage_data = (
        marriages_female.groupby(
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
        marriage_data["year"].unique()
    )

    selected_range = st.slider(
        "Select year range",
        min_value=int(min(available_years)),
        max_value=int(max(available_years)),
        value=(
            int(min(available_years)),
            int(max(available_years))
        ),
        key="marriage_year_range"
    )

    selected_columns = [
        year for year in marriage_pivot.columns
        if selected_range[0] <= year <= selected_range[1]
    ]

    marriage_filtered = marriage_pivot[
        selected_columns
    ]

    if marriage_filtered.empty:

        st.warning(
            "No female marriage rate data available."
        )

    else:

        latest_year = selected_columns[-1]

        latest_rates = marriage_filtered[
            latest_year
        ].dropna()

        average_rate = latest_rates.mean()
        highest_rate = latest_rates.max()
        lowest_rate = latest_rates.min()

        # KPI section
        st.markdown("### Marriage Overview")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Average State-Level Rate",
            f"{average_rate:.2f}"
        )

        c2.metric(
            "Highest State-Level Rate",
            f"{highest_rate:.2f}"
        )

        c3.metric(
            "Lowest State-Level Rate",
            f"{lowest_rate:.2f}"
        )

        st.caption(
            f"Female marriage rates for {int(latest_year)}. "
            "Summary values are calculated across available states."
        )

        # Heatmap
        st.markdown(
            "### Female Marriage Rates by State and Year"
        )

        with st.container(border=True):

            fig = px.imshow(
                marriage_filtered,
                text_auto=".1f",
                aspect="auto",
                color_continuous_scale=[
                    "#F0F2EF",
                    "#B7C9BC",
                    "#6F967B",
                    GREEN
                ],
                labels={
                    "x": "Year",
                    "y": "Malaysian State",
                    "color": "Marriage Rate"
                }
            )

            fig.update_layout(
                **chart_layout(490),
                xaxis_title="Year",
                yaxis_title="Malaysian State",
                coloraxis_colorbar_title="Marriage Rate"
            )

            fig.update_traces(
                textfont=dict(
                    size=11,
                    color=TEXT
                ),
                hovertemplate=(
                    "State: %{y}<br>"
                    "Year: %{x}<br>"
                    "Rate: %{z:.2f}"
                    "<extra></extra>"
                )
            )

            fig.update_xaxes(
                dtick=1,
                gridcolor=GRID
            )

            fig.update_yaxes(
                gridcolor=GRID
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.markdown(
            """
            <div class="insight-card">
                <strong>Heatmap Interpretation</strong><br>
                Darker green shades represent higher female
                marriage rates, while lighter shades represent
                lower rates. The colour intensity helps compare
                differences across Malaysian states and years.
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
                "marriage_rate_analysis.csv",
                "text/csv"
            )


# =========================================================
# 12. FOOTER
# =========================================================

st.markdown(
    """
    <div class="dashboard-footer">

        <strong>📊 Malaysian Data Visualization Dashboard</strong>
        <br>

        Population &nbsp; • &nbsp;
        Household Income &nbsp; • &nbsp;
        Marriage

        <br>

        Data Period: 2017–2023

    </div>
    """,
    unsafe_allow_html=True
)
