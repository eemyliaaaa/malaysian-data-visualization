
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Malaysian Data Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. COLOUR PALETTE
# =====================================================

GREEN = "#174C35"
GREEN_2 = "#26734D"
GREEN_3 = "#6B967A"
PINK = "#A62959"
PINK_LIGHT = "#D98BA5"

BACKGROUND = "#F1F2F0"
WHITE = "#FFFFFF"
TEXT = "#202722"
MUTED = "#7B847E"
BORDER = "#E5E9E5"
GRID = "#EDF0ED"

# =====================================================
# 3. CUSTOM CSS
# =====================================================

st.markdown(f"""
<style>

/* Hide sidebar completely */
section[data-testid="stSidebar"] {{
    display: none;
}}

button[data-testid="collapsedControl"] {{
    display: none;
}}

/* Main background */
.stApp {{
    background: {BACKGROUND};
    color: {TEXT};
}}

.main .block-container {{
    max-width: 1440px;
    padding: 1.1rem 2rem 2rem 2rem;
}}

/* Remove excessive spacing */
div[data-testid="stVerticalBlock"] {{
    gap: 0.65rem;
}}

/* Brand header */
.brand-header {{
    background: {GREEN};
    color: white;
    border-radius: 14px;
    padding: 17px 23px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 13px;
    border-bottom: 4px solid {PINK};
}}

.brand-name {{
    font-size: 1.45rem;
    font-weight: 850;
    letter-spacing: -0.5px;
}}

.brand-caption {{
    font-size: 0.78rem;
    color: #D5E3DA;
    margin-top: 3px;
}}

.brand-period {{
    text-align: right;
    font-size: 0.75rem;
    font-weight: 750;
    line-height: 1.6;
    color: #E5EEE8;
}}

/* Horizontal navigation */
div[role="radiogroup"] {{
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin: 4px 0 13px 0;
}}

div[role="radiogroup"] label {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 9px;
    padding: 8px 16px;
    color: {TEXT};
    font-weight: 650;
    font-size: 0.84rem;
}}

div[role="radiogroup"] label:has(input:checked) {{
    background: {GREEN};
    color: white;
    border-color: {GREEN};
}}

div[role="radiogroup"] label:hover {{
    border-color: {GREEN_2};
}}

/* Page heading */
.eyebrow {{
    font-size: 0.67rem;
    font-weight: 850;
    color: {PINK};
    letter-spacing: 1.8px;
    margin-bottom: 3px;
}}

h1 {{
    color: {GREEN} !important;
    font-size: 1.85rem !important;
    font-weight: 850 !important;
    letter-spacing: -0.7px;
    margin: 0 !important;
}}

h2, h3 {{
    color: {GREEN} !important;
    font-weight: 750 !important;
}}

h3 {{
    font-size: 1.02rem !important;
}}

/* Description */
.description {{
    color: {MUTED};
    font-size: 0.85rem;
    margin: 3px 0 10px 0;
}}

/* Objective */
.objective {{
    background: {WHITE};
    border-left: 4px solid {GREEN};
    border-radius: 9px;
    padding: 11px 15px;
    margin: 9px 0 13px 0;
    font-size: 0.84rem;
    line-height: 1.5;
}}

.objective strong {{
    color: {GREEN};
}}

/* KPI cards */
[data-testid="stMetric"] {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 11px;
    padding: 13px 15px;
    min-height: 100px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.025);
}}

[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
}}

[data-testid="stMetricValue"] {{
    color: {GREEN} !important;
    font-size: 1.5rem !important;
    font-weight: 850 !important;
    overflow-wrap: anywhere;
}}

[data-testid="stMetricDelta"] {{
    color: {PINK} !important;
    font-size: 0.74rem !important;
}}

/* Chart containers */
[data-testid="stPlotlyChart"] {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 11px;
    padding: 5px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.025);
}}

/* Other bordered containers */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 11px;
    padding: 7px;
}}

/* Select boxes */
div[data-baseweb="select"] > div {{
    background: {WHITE};
    border-radius: 8px;
    border-color: {BORDER};
}}

/* Insight card */
.insight {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 12px 15px;
    font-size: 0.83rem;
    line-height: 1.6;
    color: {TEXT};
}}

.insight strong {{
    color: {GREEN};
}}

/* Expanders */
[data-testid="stExpander"] {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 9px;
}}

/* Download buttons */
.stDownloadButton button {{
    background: {GREEN};
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 650;
}}

.stDownloadButton button:hover {{
    background: {GREEN_2};
    color: white;
}}

/* Footer */
.footer {{
    text-align: center;
    padding: 15px;
    margin-top: 16px;
    background: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    color: {MUTED};
    font-size: 0.75rem;
    line-height: 1.8;
}}

.footer strong {{
    color: {GREEN};
}}

/* Dividers */
hr {{
    border-color: {BORDER};
    margin: 0.55rem 0;
}}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 4. LOAD CLEANED DATASETS
# =====================================================

@st.cache_data
def load_data():

    population = pd.read_csv("population_clean.csv")
    income = pd.read_csv("income_clean.csv")
    marriages = pd.read_csv("marriages_clean.csv")

    datasets = [population, income, marriages]

    for df in datasets:

        df.columns = df.columns.str.strip()

        df["state"] = df["state"].astype(str).str.strip()

        if "year" not in df.columns:
            if "date" in df.columns:
                df["year"] = pd.to_datetime(
                    df["date"], errors="coerce"
                ).dt.year
            else:
                raise ValueError(
                    "A year or date column is missing."
                )

        df["year"] = pd.to_numeric(
            df["year"], errors="coerce"
        )

    return population, income, marriages


try:

    population, income, marriages = load_data()

except Exception as e:

    st.error(f"Dataset loading error: {e}")
    st.stop()


# =====================================================
# 5. COMMON CHART SETTINGS
# =====================================================

def chart_layout(height=400):

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
            l=35,
            r=25,
            t=30,
            b=35
        )
    )


# =====================================================
# 6. TOP HEADER
# =====================================================

st.markdown("""
<div class="brand-header">
    <div>
        <div class="brand-name">📊 Malaysian Data</div>
        <div class="brand-caption">
            Interactive Data Visualization Dashboard
        </div>
    </div>
    <div class="brand-period">
        MALAYSIA<br>
        2017 – 2023
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# 7. HORIZONTAL NAVIGATION
# =====================================================

page = st.radio(
    "Navigation",
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
        '<div class="eyebrow">MALAYSIAN DATA VISUALIZATION</div>',
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
            <strong>Visualization Objective</strong><br>
            {objective}
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 9. POPULATION PAGE
# =====================================================

if page == "🌿 Population":

    page_header(
        "Population Analysis",
        "Explore population growth patterns across Malaysian states.",
        "Analyse population growth across Malaysian states "
        "from 2017 to 2023."
    )

    years = sorted(
        population["year"].dropna().unique()
    )

    if not years:
        st.warning("No population data available.")
        st.stop()

    selected_range = st.slider(
        "Select year range",
        int(min(years)),
        int(max(years)),
        (int(min(years)), int(max(years))),
        key="pop_range"
    )

    pop_filtered = population[
        population["year"].between(
            selected_range[0],
            selected_range[1]
        )
    ].copy()

    pop_trend = (
        pop_filtered.groupby(
            ["year", "state"],
            as_index=False
        )["population"].sum()
    )

    yearly_total = (
        pop_trend.groupby("year")["population"]
        .sum().sort_index()
    )

    if yearly_total.empty:
        st.warning("No data for this year range.")
        st.stop()

    start_value = yearly_total.iloc[0]
    end_value = yearly_total.iloc[-1]

    growth = (
        (end_value - start_value) / start_value * 100
        if start_value else 0
    )

    st.markdown("### Population Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Starting Population", f"{start_value:,.1f}k")
    c2.metric("Latest Population", f"{end_value:,.1f}k")
    c3.metric("Population Growth", f"{growth:.2f}%")

    st.caption("Population values are presented in thousands.")

    st.markdown("### Population Growth by State")

    with st.container(border=True):

        states = sorted(pop_trend["state"].unique())

        selected_states = st.multiselect(
            "Choose states",
            states,
            default=states,
            key="pop_states"
        )

        chart_data = pop_trend[
            pop_trend["state"].isin(selected_states)
        ]

        if not chart_data.empty:

            palette = [
                GREEN, PINK, GREEN_2, PINK_LIGHT,
                "#526E5B", "#8C526A", "#75917C",
                "#B35B7D", "#345A42", "#A67A8A"
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
                **chart_layout(440),
                hovermode="x unified",
                legend_title="State"
            )

            fig.update_xaxes(
                dtick=1,
                gridcolor=GRID
            )

            fig.update_yaxes(gridcolor=GRID)

            fig.update_traces(
                line=dict(width=2.3),
                marker=dict(size=6)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:
            st.info("Select at least one state.")

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


# =====================================================
# 10. HOUSEHOLD INCOME PAGE
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

    years = sorted(
        income["year"].dropna().unique()
    )

    if not years:
        st.warning("No income data available.")
        st.stop()

    selected_year = st.selectbox(
        "Select survey year",
        years,
        index=len(years) - 1,
        format_func=lambda x: str(int(x))
    )

    income_selected = income[
        income["year"] == selected_year
    ].copy()

    income_chart = (
        income_selected.groupby("state", as_index=False)
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

    average = income_chart["income_mean"].mean()

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
                        color="#D5DDD6",
                        width=3
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
                    size=11
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Median: RM %{x:,.0f}"
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
                    size=11
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Mean: RM %{x:,.0f}"
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

        fig.update_xaxes(gridcolor=GRID)

        fig.update_yaxes(
            autorange="reversed",
            gridcolor=GRID
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("### Understanding the Income Difference")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="insight">
                <strong style="color:{GREEN};">
                    ● Median Income
                </strong><br>
                The middle value when household incomes are
                arranged from lowest to highest.
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="insight">
                <strong style="color:{PINK};">
                    ● Mean Income
                </strong><br>
                The average household income across households.
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


# =====================================================
# 11. MARRIAGE PAGE
# =====================================================

elif page == "💗 Marriage":

    page_header(
        "Marriage Analysis",
        "Explore annual female marriage rate patterns "
        "across Malaysian states.",
        "Examine annual female marriage rate trends "
        "across Malaysian states from 2017 to 2023."
    )

    marriages_female = marriages[
        marriages["sex"].astype(str).str.strip().str.lower()
        == "female"
    ].copy()

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

    years = sorted(
        marriage_data["year"].dropna().unique()
    )

    if not years:
        st.warning("No female marriage rate data available.")
        st.stop()

    selected_range = st.slider(
        "Select year range",
        int(min(years)),
        int(max(years)),
        (int(min(years)), int(max(years))),
        key="marriage_range"
    )

    selected_columns = [
        year for year in marriage_pivot.columns
        if selected_range[0] <= year <= selected_range[1]
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

    st.markdown("### Marriage Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Average State-Level Rate", f"{average_rate:.2f}")
    c2.metric("Highest State-Level Rate", f"{highest_rate:.2f}")
    c3.metric("Lowest State-Level Rate", f"{lowest_rate:.2f}")

    st.caption(
        f"Female marriage rates for {int(latest_year)}."
    )

    st.markdown("### Female Marriage Rates by State and Year")

    with st.container(border=True):

        fig = px.imshow(
            marriage_filtered,
            text_auto=".1f",
            aspect="auto",
            color_continuous_scale=[
                "#F1F3F1",
                "#B8CDBD",
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
            **chart_layout(480),
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
        <div class="insight">
            <strong>Heatmap interpretation:</strong>
            Darker green shades represent higher female marriage
            rates, while lighter shades represent lower rates.
            Comparing states and years helps identify differences
            and changes over time.
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
