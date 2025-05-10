import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm

df = pd.read_csv('vehicles.csv')
st.header('Used Car Market Analysis')

# --- 1. How Are Used Cars Priced? ---
st.subheader("1. How Are Used Cars Priced?")

if st.checkbox('Show only cars under $40,000'):
    df_filtered = df[df['price'] < 40000]
else:
    df_filtered = df

# Plotting histogram of car prices
fig1 = px.histogram(
    df_filtered,
    x='price',
    title='How Are Used Cars Priced?',
    labels={'price': 'Price (USD)', 'count': 'Number of Cars'},
    nbins=50,
    color_discrete_sequence=['darkgreen']
)
fig1.update_layout(xaxis_tickangle=45)  
st.plotly_chart(fig1)

# Summary for "How Are Used Cars Priced?"
pricing_summary = """
This histogram represents the distribution of car prices with a realistic cutoff of 40,000, focusing on what an average buyer might expect. 
Since 75% of cars are priced below 16,839, excluding listings above 40,000 helps remove luxury or rare vehicles, which make up only about 4%-5% of the data. 
This cutoff still provides a broad but relevant view. The distribution is right-skewed, with most cars priced between 3,000 and 10,000, followed by a gradual decline in frequency as prices increase.
"""
st.markdown(pricing_summary)

# --- 2. How Does Mileage Affect Price Across Fuel Types? ---
st.subheader("2. How Does Mileage Affect Price Across Fuel Types?")

if st.checkbox("Show Scatterplot: Mileage vs Price"):
    df_filtered2 = df[
    (df['price'] < 40000) & 
    (df['odometer'] < 250000)  # Filter cars with reasonable mileage
    ]

    # Creating scatter plot with trendline
    fig2 = px.scatter(
        df_filtered2,
        x='odometer',
        y='price',
        title='How Does Mileage Affect Price Across Fuel Types?',
        labels={'odometer': 'Odometer (Miles)', 'price': 'Price (USD)', 'fuel': 'Fuel Type'},
        color='fuel',
        color_discrete_sequence=px.colors.qualitative.Set1,
        trendline='ols' 
    )

    fig2.for_each_trace(lambda t: t.update(line=dict(color='white')) if 'gas' in t.name else ())
    st.plotly_chart(fig2)

# Summary for "How Does Mileage Affect Price Across Fuel Types?"
mileage_summary = """
This scatterplot shows that as mileage increases, used car prices generally decrease — a trend most evident in gas vehicles, which depreciate faster. 
Diesel vehicles retain value better, likely due to their durability. Hybrid, electric, and other fuel types are rare in the dataset, making their trends harder to interpret. 
Still, the market is likely to shift away from gas and diesel as alternative fuel vehicles become more common.
"""
st.markdown(mileage_summary)

# --- 3. Which Vehicle Types Hold Their Value Better? ---
st.subheader("3. Which Vehicle Types Hold Their Value Better?")

# Calculate vehicle age
df['vehicle_age'] = 2019 - df['model_year']

# Filtering data for relevant vehicles
df_filtered3 = df[
    (df['price'] < 40000) &
    (df['vehicle_age'] < 30) &  # Limit vehicle age to under 30 years
    (df['odometer'] < 250000)  # Limit odometer to reasonable mileage
]

fig3 = px.scatter(
    df_filtered3,
    x='vehicle_age',
    y='price',
    color='type',
    title='Which Vehicle Types Hold Their Value Better?',
    labels={
        'vehicle_age': 'Vehicle Age (Years)',
        'price': 'Price (USD)',
        'type': 'Vehicle Type'
    },
    color_discrete_sequence=px.colors.qualitative.Set2,
    trendline='ols' 
)

st.plotly_chart(fig3)

# Summary for "Which Vehicle Types Hold Their Value Better?"
value_retention_summary = """
This scatterplot shows the varying depreciation rates across different vehicle types. The R² values indicate that offroad (0.6116) and pickup (0.5595) vehicles 
have the strongest relationship between age and price, meaning their value depreciation is more predictable over time. In contrast, convertibles (0.1511) 
and other vehicles (0.1459) have the weakest relationship, suggesting greater price variability not explained by age. SUVs, sedans, and trucks—common vehicle types—
fall in the mid-range, with R² values around 0.33 to 0.38, indicating moderate value retention patterns. Overall, vehicle type plays a significant role in how predictable 
a vehicle depreciates in value over time.
"""
st.markdown(value_retention_summary)

# --- 4. R² Value by Vehicle Type ---
st.subheader("4. R² Value by Vehicle Type")

r2_values = {
    'SUV': 0.3306,
    'pickup': 0.5595,
    'sedan': 0.3791,
    'truck': 0.3754,
    'coupe': 0.3026,
    'van': 0.2287,
    'hatchback': 0.2520,
    'wagon': 0.3751,
    'mini-van': 0.4852,
    'convertible': 0.1511,
    'other': 0.1459,
    'offroad': 0.6116,
    'bus': 0.1994
}

# Bar chart for R² values by vehicle type
vehicle_types = list(r2_values.keys())
r2_vals = list(r2_values.values())

fig_r2 = go.Figure(data=[go.Bar(x=vehicle_types, y=r2_vals)])

fig_r2.update_layout(
    title='R² Value by Vehicle Type',
    xaxis_title='Vehicle Type',
    yaxis_title='R² Value',
    xaxis_tickangle=45 
)

st.plotly_chart(fig_r2)

# --- 5. What Kinds of Cars Dominate Listings? ---
st.subheader("5. What Kinds of Cars Dominate Listings?")

# Filtering the data 
df_filtered4 = df[
    (df['price'] < 40000) &
    (df['odometer'] < 250000)
]

type_counts = df_filtered4['type'].value_counts(normalize=True).reset_index()
type_counts.columns = ['type', 'percent']
type_counts['percent'] *= 100  # Convert to percentage

# Creating a bar chart 
fig4 = px.bar(
    type_counts,
    x='type',
    y='percent',
    title='What Kinds of Cars Dominate Listings?',
    labels={'type': 'Vehicle Type', 'percent': 'Percentage of Listings'},
    color_discrete_sequence=['darkred']
)

fig4.update_layout(
    xaxis_tickangle=45, 
    yaxis_title='Percentage of Listings'
)
fig4.update_traces(
    texttemplate='%{y:.1f}%', 
    textposition='outside'  
)

st.plotly_chart(fig4)

# Summary for "What Kinds of Cars Dominate Listings?"
listing_summary = """
The histogram shows the distribution of vehicle types in the listings. SUVs, Sedans, and Trucks dominate the listings at around 24%. 
Pickups make up about 13%, and Coupes are at 4.5%. Wagons and Mini-vans together account for ≈5%, while the remaining ≈5% includes Bus, 
Off-road, Other, Convertibles, Vans, and Hatchbacks, which together make up 4.3% of all listings with the filters (price < 40000, odometer < 250000).
"""
st.markdown(listing_summary)

# --- Conclusion ---
st.subheader("Conclusion")
conclusion_text = """
In conclusion, the used car market is shaped by a mix of popular, practical vehicles like SUVs and Trucks, which dominate the listings. 
There's also a noticeable trend toward better value retention in certain vehicle types, particularly Off-road vehicles and Pickups. 
As the market evolves, we can expect a growing trend toward fuel-efficient and eco-friendly vehicles, although these types still represent a relatively small fraction of the total listings.
"""

st.markdown(conclusion_text)
