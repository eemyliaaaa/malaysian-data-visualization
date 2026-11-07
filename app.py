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

BASE_DIR = Path(__file__).parent

POPULATION_FILE = BASE_DIR / "population_clean.csv"
INCOME_FILE = BASE_DIR / "income_clean.csv"
MARRIAGE_FILE = BASE_DIR / "marriages_clean.csv"


# =========================================================
# 2. COLOUR PALETTE
# =========================================================

GREEN = "#174C35"
GREEN_DARK = "#103B29"
GREEN_MID = "#26734D"

PINK = "#A62959"

WHITE = "#FFFFFF"
BACKGROUND = "#D4D8D5"
TEXT = "#202722"
MUTED = "#68736C"
BORDER = "#303A33"
GRID = "#E7ECE8"


# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    html, body, [data-testid="stAppViewContainer"] {{
        background: {BACKGROUND} !important;
        color: {TEXT};
    }}

    .stApp {{
        background: {BACKGROUND} !important;
    }}

    .main .block-container {{
        width: 100% !important;
        max-width: 100% !important;
        padding: 0.45rem 0.65rem 0.8rem 0.65rem !important;
        margin: 0 !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent;
    }}

    footer {{
        visibility: hidden;
    }}

    section[data-testid="stSidebar"] {{
        display: none !important;
    }}

    button[data-testid="collapsedControl"] {{
        display: none !important;
    }}

    div[data-testid="stVerticalBlock"] {{
        gap: 0.35rem;
    }}

    h1, h2, h3 {{
        color: {GREEN} !important;
        font-weight: 800 !important;
    }}

    h1 {{
        font-size: 1.9rem !important;
        margin-bottom: 0.1rem !important;
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

    /* HEADER */

    .brand-header {{
        width: 100%;
        box-sizing: border-box;
        background: {GREEN};
        color: {WHITE};
        border: 1.5px solid {BORDER};
        border-bottom: 5px solid {PINK};
        border-radius: 14px;
        padding: 16px 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 15px;
        margin: 0 0 5px 0;
    }}

    .brand-name {{
        color: {WHITE};
        font-size: 1.5rem;
        font-weight: 850;
    }}

    .brand-caption {{
        color: {WHITE};
        font-size: 0.82rem;
        margin-top: 4px;
    }}

    .brand-period {{
        color: {WHITE};
        text-align: right;
        font-size: 0.78rem;
        font-weight: 750;
        line-height: 1.7;
        white-space: nowrap;
    }}

    /* NAVIGATION */

    div[role="radiogroup"] {{
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin: 2px 0 5px 0;
    }}

    div[role="radiogroup"] label {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 9px;
        padding: 8px 17px;
        color: {TEXT};
        font-size: 0.86rem;
        font-weight: 650;
    }}

    div[role="radiogroup"] label:hover {{
        border-color: {GREEN};
    }}

    div[role="radiogroup"] label:has(input:checked) {{
        background: {GREEN};
        color: {WHITE};
        border: 1.5px solid {BORDER};
        border-bottom: 4px solid {PINK};
    }}

    div[role="radiogroup"] label:has(input:checked) p {{
        color: {WHITE} !important;
    }}

    /* BLACK DIVIDER */

    .black-divider {{
        width: 100%;
        height: 1.5px;
        background: #111111;
        margin: 5px 0 10px 0;
    }}

    /* PAGE INTRODUCTION */

    .eyebrow {{
        color: {PINK};
        font-size: 0.68rem;
        font-weight: 850;
        letter-spacing: 1.7px;
        margin: 0 0 3px 0;
    }}

    .page-description {{
        color: {MUTED};
        font-size: 0.88rem;
        margin-bottom: 8px;
    }}

    .objective-card {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-left: 5px solid {GREEN};
        border-radius: 9px;
        padding: 10px 15px;
        margin: 5px 0 10px 0;
        font-size: 0.85rem;
        line-height: 1.55;
    }}

    .objective-card strong {{
        color: {GREEN};
    }}

    /* KPI CARDS */

    [data-testid="stMetric"] {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 11px;
        padding: 13px 16px;
        min-height: 95px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-size: 0.78rem !important;
    }}

    [data-testid="stMetricValue"] {{
        color: {GREEN} !important;
        font-size: 1.5rem !important;
        font-weight: 850 !important;
        overflow-wrap: anywhere;
    }}

    [data-testid="stMetricDelta"] {{
        color: {PINK} !important;
    }}

    /* CHART CONTAINERS */

    [data-testid="stPlotlyChart"] {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 11px;
        padding: 5px;
    }}

    /* INSIGHT CARDS */

    .insight-card {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-left: 4px solid {PINK};
        border-radius: 9px;
        padding: 12px 15px;
        font-size: 0.84rem;
        line-height: 1.6;
        color: {TEXT};
    }}

    .insight-card strong {{
        color: {GREEN};
    }}

    /* EXPANDER */

    [data-testid="stExpander"] {{
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-radius: 9px;
    }}

    /* SELECT BOX */

    div[data-baseweb="select"] > div {{
        background: {WHITE};
        border-radius: 8px;
        border-color: {BORDER};
    }}

    /* DOWNLOAD BUTTON */

    .stDownloadButton button {{
        background: {GREEN};
        color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        font-weight: 650;
    }}

    .stDownloadButton button:hover {{
        background: {GREEN_MID};
        color: {WHITE};
    }}

    /* FOOTER */

    .dashboard-footer {{
        width: 100%;
        box-sizing: border-box;
        background: {WHITE};
        border: 1.5px solid {BORDER};
        border-top: 4px solid {GREEN};
        border-radius: 10px;
        padding: 12px;
        margin-top: 12px;
        text-align: center;
        color: {MUTED};
        font-size: 0.76rem;
        line-height: 1.8;
    }}

    .dashboard-footer strong {{
        color: {GREEN};
    }}

    /* MOBILE */

    @media (max-width: 768px) {{

        .main .block-container {{
            padding: 0.4rem !important;
        }}

        .brand-header {{
            padding: 13px;
        }}

        .brand-name {{
            font-size: 1.2rem;
        }}

        div[role="radiogroup"] label {{
            padding: 7px 10px;
            font-size: 0.77rem;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 4. LOAD AND PREPROCESS DATA
# =========================================================

@st.cache_data
def load_data():

    required_files = [
        POPULATION_FILE,
        INCOME_FILE,
        MARRIAGE_FILE
    ]

    for file_path in required_files:

        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing file: {file_path.name}. "
                "Upload all three CSV files to the GitHub repository."
            )

    population = pd.read_csv(POPULATION_FILE)
    income = pd.read_csv(INCOME_FILE)
    marriages = pd.read_csv(MARRIAGE_FILE)

    datasets = [population, income, marriages]

    for df in datasets:

        df.columns = df.columns.str.strip()

        if "state" not in df.columns:
            raise ValueError("Missing state column.")

        df["state"] = df["state"].astype(str).str.strip()

        if "year" not in df.columns:

            if "date" not in df.columns:
                raise ValueError("Missing date/year column.")

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

        df.drop(
            df[~df["year"].between(2017, 2023)].index,
            inplace=True
        )

        df.drop_duplicates(inplace=True)

    # Population preprocessing
    if "population" not in population.columns:
        raise ValueError("Missing population column.")

    population["population"] = pd.to_numeric(
        population["population"],
        errors="coerce"
    )

    population.dropna(
        subset=["population"],
        inplace=True
    )

    for column, target in [
        ("sex", "both"),
        ("age", "overall"),
        ("ethnicity", "overall")
    ]:

        if column in population.columns:

            values = (
                population[column]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            if target in values.unique():

                population = population[
                    values == target
                ].copy()

    # Income preprocessing
    for column in ["income_mean", "income_median"]:

        if column not in income.columns:
            raise ValueError(
                f"Missing income column: {column}"
            )

        income[column] = pd.to_numeric(
            income[column],
            errors="coerce"
        )

    income.dropna(
        subset=["income_mean", "income_median"],
        inplace=True
    )

    # Marriage preprocessing
    if "rate" not in marriages.columns:
        raise ValueError("Missing marriage rate column.")

    marriages["rate"] = pd.to_numeric(
        marriages["rate"],
        errors="coerce"
    )

    marriages.dropna(
        subset=["rate"],
        inplace=True
    )

    return population, income, marriages


try:

    population, income, marriages = load_data()

except Exception as error:

    st.error(f"Dataset loading error: {error}")
    st.stop()


# =========================================================
# 5. CHART STYLE
# =========================================================

def chart_layout(height=430):

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
        )
    )


# =========================================================
# 6. HEADER
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
# 7. NAVIGATION
# =========================================================

page = st.radio(
    "Dashboard section",
    [
        "🌿 Population",
        "🌸 Household Income",
        "💗 Marriage"
    ],
    horizontal=True,
    label_visibility="collapsed",
    key="dashboard_navigation"
)

st.markdown(
    '<div class="black-divider"></div>',
    unsafe_allow_html=True
)


# =========================================================
# 8. PAGE HEADER FUNCTION
# =========================================================

def show_page_header(title, description, objective):

    st.markdown(
        """
        <div class="eyebrow">
            MALAYSIAN DATA VISUALIZATION
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title(title)

    st.markdown(
        f"""
        <div class="page-description">
            {description}
        </div>

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

if page == "🌿 Population":

    show_page_header(
        "Population Analysis",
        "Explore population growth patterns across Malaysian states.",
        "Analyse population growth across Malaysian states from 2017 to 2023."
    )

    years = sorted(population["year"].unique())

    year_range = st.slider(
        "Select year range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years))),
        key="population_year_range"
    )

    pop_filtered = population[
        population["year"].between(
            year_range[0],
            year_range[1]
        )
    ].copy()

    pop_trend = (
        pop_filtered
        .groupby(
            ["year", "state"],
            as_index=False
        )["population"]
        .sum()
    )

    yearly_total = (
        pop_trend
        .groupby("year")["population"]
        .sum()
        .sort_index()
    )

    if yearly_total.empty:

        st.warning("No population data available.")

    else:

        start_value = yearly_total.iloc[0]
        end_value = yearly_total.iloc[-1]

        growth = (
            ((end_value - start_value) / start_value) * 100
            if start_value != 0 else 0
        )

        st.markdown("### Population Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Starting Population",
            f"{start_value:,.1f}k"
        )

        col2.metric(
            "Latest Population",
            f"{end_value:,.1f}k"
        )

        col3.metric(
            "Population Growth",
            f"{growth:.2f}%"
        )

        st.caption(
            "Population values are presented in thousands."
        )

        st.markdown("### Population Growth by State")

        all_states = sorted(
            pop_trend["state"].unique()
        )

        selected_states = st.multiselect(
            "Select states to display",
            options=all_states,
            default=all_states,
            key="population_states"
        )

        plot_data = pop_trend[
            pop_trend["state"].isin(selected_states)
        ]

        if plot_data.empty:

            st.info("Select at least one state.")

        else:

            palette = [
                GREEN, PINK, GREEN_MID, "#D47A98",
                "#52735E", "#87445E", "#75917C",
                "#B45D7B", "#345A42", "#A67A8A",
                "#47785A", "#C15B7B", "#718A78",
                "#8C3B5C", "#A8B8AC", "#D19BAE"
            ]

            fig = px.line(
                plot_data,
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
                **chart_layout(470),
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
                line=dict(width=2.4),
                marker=dict(size=6)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with st.expander("View Population Data"):

            st.dataframe(
                pop_trend,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download Population Data",
                data=pop_trend.to_csv(index=False),
                file_name="population_analysis.csv",
                mime="text/csv"
            )


# =========================================================
# 10. HOUSEHOLD INCOME ANALYSIS
# =========================================================

elif page == "🌸 Household Income":

    show_page_header(
        "Household Income Analysis",
        "Compare mean and median monthly household income across Malaysian states.",
        "Compare mean and median household income across Malaysian states "
        "for available survey years within 2017–2023."
    )

    available_years = sorted(
        income["year"].unique()
    )

    default_year = (
        2022 if 2022 in available_years
        else int(available_years[-1])
    )

    selected_year = st.selectbox(
        "Select survey year",
        available_years,
        index=available_years.index(default_year),
        format_func=lambda value: str(int(value))
    )

    income_selected = income[
        income["year"] == selected_year
    ].copy()

    income_chart = (
        income_selected
        .groupby("state", as_index=False)
        .agg(
            income_mean=("income_mean", "mean"),
            income_median=("income_median", "mean")
        )
        .sort_values(
            "income_mean",
            ascending=False
        )
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

        st.markdown("### Income Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Highest Mean Income",
            f"RM {highest['income_mean']:,.0f}",
            str(highest["state"])
        )

        col2.metric(
            "Lowest Mean Income",
            f"RM {lowest['income_mean']:,.0f}",
            str(lowest["state"])
        )

        col3.metric(
            "Average Mean Income",
            f"RM {average:,.0f}"
        )

        st.caption(
            f"Household income survey year: {int(selected_year)}"
        )

        st.markdown(
            "### Mean vs Median Household Income"
        )

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
                        color="#C8D1CA",
                        width=4
                    ),
                    showlegend=False,
                    hoverinfo="skip"
                )
            )

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
            **chart_layout(490),
            xaxis_title="Monthly Household Income (RM)",
            yaxis_title="Malaysian State",
            legend_title="Income Measurement"
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

        st.markdown(
            "### Understanding the Income Difference"
        )

        left, right = st.columns(2)

        with left:

            st.markdown(
                f"""
                <div class="insight-card">
                    <strong style="color:{GREEN};">
                        ● Median Income
                    </strong><br>
                    The middle value when household incomes are
                    arranged from lowest to highest.
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
                data=income_chart.to_csv(index=False),
                file_name="income_analysis.csv",
                mime="text/csv"
            )


# =========================================================
# 11. MARRIAGE ANALYSIS
# =========================================================

elif page == "💗 Marriage":

    show_page_header(
        "Marriage Analysis",
        "Explore annual female marriage rate patterns across Malaysian states.",
        "Examine annual female marriage rate trends across Malaysian states "
        "from 2017 to 2023."
    )

    if "sex" not in marriages.columns:

        st.error(
            "The marriage dataset does not contain a sex column."
        )

        st.stop()

    female_values = (
        marriages["sex"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    marriages_female = marriages[
        female_values.isin(["female", "f"])
    ].copy()

    if marriages_female.empty:

        st.error(
            "No female records found. Check the sex column "
            "in marriages_clean.csv."
        )

        st.stop()

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
        marriage_data["year"].unique()
    )

    year_range = st.slider(
        "Select year range",
        min_value=int(min(available_years)),
        max_value=int(max(available_years)),
        value=(
            int(min(available_years)),
            int(max(available_years))
        ),
        key="marriage_year_range"
    )

    selected_years = [
        year for year in marriage_pivot.columns
        if year_range[0] <= year <= year_range[1]
    ]

    marriage_filtered = marriage_pivot[
        selected_years
    ]

    if marriage_filtered.empty:

        st.warning("No marriage data available.")

    else:

        latest_year = selected_years[-1]

        latest_rates = marriage_filtered[
            latest_year
        ].dropna()

        average_rate = latest_rates.mean()
        highest_rate = latest_rates.max()
        lowest_rate = latest_rates.min()

        st.markdown("### Marriage Overview")

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

        st.markdown(
            "### Female Marriage Rates by State and Year"
        )

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
            **chart_layout(470),
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
                lower rates. Colour intensity helps compare
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
                data=marriage_filtered.to_csv(),
                file_name="marriage_rate_analysis.csv",
                mime="text/csv"
            )


# =========================================================
# 12. FOOTER
# =========================================================

st.markdown(
    """
    <div class="dashboard-footer">
        <strong>
            📊 Malaysian Data Visualization Dashboard
        </strong>
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
