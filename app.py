
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Malaysian Data Visualization Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
    .main {
        background-color: #F8F7F2;
    }

    h1, h2, h3 {
        color: #702D3A;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E8E3DC;
    }

    section[data-testid="stSidebar"] {
        background-color: #702D3A;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATASETS
# ==========================================

@st.cache_data
def load_data():

    population = pd.read_csv("population_clean.csv")
    income = pd.read_csv("income_clean.csv")
    marriages = pd.read_csv("marriages_clean.csv")

    return population, income, marriages


population, income, marriages = load_data()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("📊 Malaysian Data")
st.sidebar.markdown("### Visualization Dashboard")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "ANALYSIS",
    [
        "Population Analysis",
        "Household Income Analysis",
        "Marriage Analysis"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Malaysian State Data | 2017–2023")

# ==========================================
# PAGE 1: POPULATION ANALYSIS
# ==========================================

if page == "Population Analysis":

    st.title("Population Analysis")
    st.write(
        "Analysis of population growth across Malaysian "
        "states from 2017 to 2023."
    )

    st.markdown("### Population Overview")

    # Filter year
    years = sorted(population["year"].dropna().unique())

    selected_years = st.slider(
        "Select year range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years)))
    )

    population_filtered = population[
        population["year"].between(
            selected_years[0],
            selected_years[1]
        )
    ]

    population_trend = (
        population_filtered
        .groupby(["year", "state"], as_index=False)
        ["population"].sum()
    )

    total_population = (
        population_trend.groupby("year")["population"].sum()
    )

    start_population = total_population.iloc[0]
    end_population = total_population.iloc[-1]

    growth = (
        (end_population - start_population)
        / start_population * 100
        if start_population != 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Starting Population",
        f"{start_population:,.1f} thousand"
    )

    col2.metric(
        "Latest Population",
        f"{end_population:,.1f} thousand"
    )

    col3.metric(
        "Population Growth",
        f"{growth:.2f}%"
    )

    st.markdown("---")

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
            "state": "State"
        }
    )

    fig.update_layout(
        template="plotly_white",
        height=600,
        hovermode="x unified",
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Population Data")

    st.dataframe(
        population_trend,
        use_container_width=True
    )

# ==========================================
# PAGE 2: HOUSEHOLD INCOME ANALYSIS
# ==========================================

elif page == "Household Income Analysis":

    st.title("Household Income Analysis")

    st.write(
        "Comparison of mean and median monthly household "
        "income across Malaysian states."
    )

    st.markdown("### Income Overview")

    available_years = sorted(
        income["year"].dropna().unique()
    )

    selected_year = st.selectbox(
        "Select survey year",
        available_years,
        index=len(available_years) - 1
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

    highest = income_chart.loc[
        income_chart["income_mean"].idxmax()
    ]

    lowest = income_chart.loc[
        income_chart["income_mean"].idxmin()
    ]

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
        "States Analysed",
        f"{income_chart['state'].nunique()}"
    )

    st.markdown("---")

    st.subheader(
        f"Mean vs Median Household Income ({selected_year})"
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
                    color="lightgray",
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
                color="#87966B",
                size=11
            ),
            hovertemplate=(
                "State: %{y}<br>"
                "Median: RM %{x:,.0f}"
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
                color="#8B2635",
                size=11
            ),
            hovertemplate=(
                "State: %{y}<br>"
                "Mean: RM %{x:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=700,
        xaxis_title="Monthly Household Income (RM)",
        yaxis_title="Malaysian State",
        legend_title="Income Measurement"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "A larger gap between mean and median income indicates "
        "a greater difference between these two measures. "
        "The mean may be influenced by higher-income households."
    )

    st.subheader("Household Income Data")

    st.dataframe(
        income_chart,
        use_container_width=True
    )

# ==========================================
# PAGE 3: MARRIAGE ANALYSIS
# ==========================================

elif page == "Marriage Analysis":

    st.title("Marriage Analysis")

    st.write(
        "Analysis of female marriage rates across "
        "Malaysian states from 2017 to 2023."
    )

    # Select female records
    marriages_female = marriages[
        marriages["sex"].str.lower() == "female"
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
        marriage_data["year"].unique()
    )

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

    marriage_filtered = marriage_pivot.loc[
        :,
        (marriage_pivot.columns >= selected_years[0]) &
        (marriage_pivot.columns <= selected_years[1])
    ]

    # Summary metrics
    latest_year = selected_years[1]

    latest_rates = marriage_filtered[latest_year].dropna()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average State-Level Rate",
        f"{latest_rates.mean():.2f}"
    )

    col2.metric(
        "Highest State-Level Rate",
        f"{latest_rates.max():.2f}"
    )

    col3.metric(
        "Lowest State-Level Rate",
        f"{latest_rates.min():.2f}"
    )

    st.markdown("---")

    st.subheader("Female Marriage Rates by State")

    fig = px.imshow(
        marriage_filtered,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="YlOrRd",
        labels={
            "x": "Year",
            "y": "State",
            "color": "Marriage Rate"
        }
    )

    fig.update_layout(
        template="plotly_white",
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "The heatmap highlights differences in female "
        "marriage rates between Malaysian states and years."
    )

    st.subheader("Marriage Rate Data")

    st.dataframe(
        marriage_filtered,
        use_container_width=True
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Malaysian Data Visualization Dashboard | "
    "Data period: 2017–2023"
)
