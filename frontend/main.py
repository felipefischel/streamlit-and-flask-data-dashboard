import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, engine, text
import matplotlib.pyplot as plt
import requests
from streamlit_option_menu import option_menu
import datetime
import altair as alt
from statistics import mean
import streamlit_authenticator as stauth
import authenticator
import yaml
from yaml.loader import SafeLoader
import os
import json


# ----------------- CHANGING SOME OF THE STYLING  -------------------------

st.write('<style>.css-12oz5g7 { max-width: 1000px; }</style>', unsafe_allow_html=True)
# Changing the style of "column elements"
st.write("""
    <style>
        .css-keje6w{
            border-radius: 5px;
            box-shadow: 2px 2px 14px rgba(0,0,0,0.1);
            padding: 15px;
        }
    </style>
        """, unsafe_allow_html=True)

# ----------------- LOGIN & AUTHORIZATION  --------------------------------

# Get the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Build the path to your credentials.yaml file
credentials_path = os.path.join(current_directory, 'config.yaml')

with open(credentials_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
elif authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')

    # I create a function that loads the data from the api with the authorization header included.
    # and then converts the json into a pandas dataframe
    @st.experimental_memo
    def load_data_from_api(endpoint):
        try:
            # url = "http://127.0.0.1:5005/api/" + endpoint // when running the local api
            url = "https://api-dot-hardy-symbol-376415.oa.r.appspot.com/api/"  + endpoint
            headers = {"Authorization": "Bearer wPE&QADG@869k5"}
            response = requests.get(url, headers=headers)
            response_json = response.json()
            data = pd.json_normalize(response_json, "result")
            return data
        except Exception as e:
            st.error(e)

    # -------------- OPTION MENU -----------------------------------------------

    st.title("H&M Sustainability Dashboard")

    # Topbar navigation menu
    selected = option_menu(
        menu_title = None,
        options = ["Home", "Environmental Impact", "Customer Insights", "Economic Performance"],
        icons = ["house", "tree-fill", "people-fill", "bag-check-fill"],
        default_index = 0,
        orientation = "horizontal"
    )

    # -------------- HOME PAGE ---------------------------------------------------
    if selected == "Home":

        st.write("""
        👋🏻 Welcome to H&M's Sustainability Dashboard. This app is designed to provide a comprehensive view of H&M's sustainability performance, enabling them to track their progress and make informed decisions.

        The Sustainability Dashboard is divided into three categories: Environmental Impact, Customer Insights, and Economic Performance.
        """)
        st.subheader("Environmental Impact 🍃")
        st.write("""
        The Environmental Impact tab tracks H&M's impact on the environment, including metrics such as CO2 emissions and water consumption for their top products sold, as well as the total emissions and consumption for all products over a 2-year period. With this information, H&M can make data-driven decisions to reduce their environmental footprint.
        """)
        st.subheader("Customer Insights 👨‍👩‍👧‍👦")
        st.write("""
        The Customer Insights tab provides an overview of H&M's customer demographics and behavior, including the number of customers by age group, the total amount spent per age group, and the average amount spent per age group. The tab also includes the percentage spent by customers in each age group, giving H&M insight into which groups are most engaged with their brand.
        """)
        st.subheader("Economic Performance 📊")
        st.write("""
        The Economic Performance tab tracks H&M's financial performance, including metrics such as daily revenue, average daily price of products sold, and total revenue per month by sales channel. By monitoring these KPIs, H&M can ensure that their sustainability initiatives align with their financial goals.
        """)

    # -------------- Environmental Impact ---------------------------------------
    if selected == "Environmental Impact":
        st.write("""
        This tab provides insight into H&M's environmental impact, including metrics such as CO2 emissions and water consumption for their top products sold, as well as the total emissions and consumption for all products over a 2-year period.

        By monitoring these metrics, H&M can make data-driven decisions to reduce their environmental footprint and work towards a more sustainable future.

        ** I calculated the CO2 emissions and Water Consumption values by creating a json file with average values for each product. The values are very bold averages and should not be taken as accurate metrics.
        """)

        # ----------------------------- Filters -----------------------------
        # Add side bar for filters
        st.sidebar.write("## Top products:")

        # ------------------------- Retrieving data from API endpoint -------------------------
        # Top articles sold
        sales_count = load_data_from_api("articles/sold/count")

        # ------------------- Retrieving sustainability data from json file ------------------

        # I created a json file and filled it with data for each product type. The json is a dictionary of dictionaries.
        # Each product type is one key and inside it theres another dictionary with the "CO2 emissions" and "Water Consumption" keys.
        # The values are very bold averages and were made for experimentation purposes.

        # Get the current working directory
        sust_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the JSON file using os.path
        json_path = os.path.join(sust_directory, 'sustainability.json')

        # Load the JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Convert the JSON to a DataFrame
        sustainability_df = pd.DataFrame.from_dict(data, orient='index')
        sustainability_df.columns = ['CO2', 'Water']

        # Reset the index
        sustainability_df = sustainability_df.reset_index()
        sustainability_df.rename(columns={'index': 'product_type_name'}, inplace=True)

        # ----------------------- Merging dataframes --------------------------------------------

        # merge the two dataframes based on product_type_name column
        merged_df = sales_count.merge(sustainability_df, on='product_type_name')

        # create new columns by multiplying corresponding columns
        merged_df['total_CO2_emissions'] = merged_df['CO2'] * merged_df['count_products']
        merged_df['total_water_consumption'] = merged_df['Water'] * merged_df['count_products']

        # select only the columns we're interested in for the new dataframe
        total_co2_and_water = merged_df[['product_type_name', 'total_CO2_emissions', 'total_water_consumption']]

        # ---------------------------------- Adding filters -------------------------------------
        top_filter_article = st.sidebar.slider(
        'Select how many of the most sold products you want to see',
        1, len(sales_count), (1, 10))

        # ---------------------------------- Plotting the data ----------------------------------

        # ---------------------------------------------------------------------------------------

        kpi1, kpi2 = st.columns(2)

        # Total CO2 emissions in time all time frame.
        total_co2 = sum(total_co2_and_water['total_CO2_emissions'])

        # Total water consumption in time frame
        total_water = sum(total_co2_and_water['total_water_consumption'])


        kpi1.metric(
            label = "Total CO2 emissions for the 2 year period (in kgs)",
            value = round(total_co2,2),
        )

        kpi2.metric(
            label = "Total water consumption for the 2 year period (in litres)",
            value = round(total_water,2),
        )

        # ----------------------------------------------------------------------------------------
        # AVERAGE CO2 EMISSIONS BY EACH PRODUCT TYPE

        # Chart to display the emissions per product
        co2_emissions_filtered = sustainability_df.iloc[top_filter_article[0]-1:top_filter_article[1]+1]

        # Create chart using altair
        chart_co2_emissions_per_product = alt.Chart(co2_emissions_filtered, title='CO2 emissions by Product').mark_bar(color='#5a6872').encode(
            x=alt.X('CO2:Q', axis=alt.Axis(title='CO2 emissions per item (kg CO2)')),
            y=alt.Y('product_type_name:N', sort='-x', axis=alt.Axis(title='Product')),
            tooltip=['product_type_name', 'CO2']
        )

        # ---------------------------------------------------------------------------------------------
        # AVERAGE WATER CONSUMPTION BY EACH PRODUCT TYPE

        # Chart to display the water consumption per product
        water_filtered = sustainability_df.iloc[top_filter_article[0]-1:top_filter_article[1]+1]

        # Create chart using altair
        chart_water_per_product = alt.Chart(water_filtered, title='Water Consumption by Product').mark_bar(color='#00BFFF').encode(
            x=alt.X('Water:Q', axis=alt.Axis(title='Water consumption per item (Litres)')),
            y=alt.Y('product_type_name:N', sort='-x', axis=alt.Axis(title='Product')),
            tooltip=['product_type_name', 'Water']
        )

        # -------------------------------------------------------------------------------------------------
        # TOTAL CO2 EMISSIONS OF PRODUCTS

        # Chart to display the water consumption per product
        total_co2_filtered = total_co2_and_water.iloc[top_filter_article[0]-1:top_filter_article[1]+1]

        # Create chart using altair
        chart_total_co2_per_product = alt.Chart(total_co2_filtered, title='Total CO2 emissions by Product').mark_bar(color='#5a6872').encode(
            x=alt.X('total_CO2_emissions:Q', axis=alt.Axis(title='Total CO2 emissions of items sold (kg CO2)')),
            y=alt.Y('product_type_name:N', sort='-x', axis=alt.Axis(title='Product')),
            tooltip=['product_type_name', 'total_CO2_emissions']
        )
        # -------------------------------------------------------------------------------------------------
        # TOTAL WATER CONSUMPTION BY PRODUCT

        # Chart to display the water consumption per product
        total_water_filtered = total_co2_and_water.iloc[top_filter_article[0]-1:top_filter_article[1]+1]

        # Create chart using altair
        chart_total_water_per_product = alt.Chart(total_water_filtered, title='Total Water Consumption by Product').mark_bar(color='#00BFFF').encode(
            x=alt.X('total_water_consumption:Q', axis=alt.Axis(title='Total water consumption of items sold (Litres)')),
            y=alt.Y('product_type_name:N', sort='-x', axis=alt.Axis(title='Product')),
            tooltip=['product_type_name', 'total_water_consumption']
        )
        # -------------------------------------------------------------------------------------------------
        # Display charts in 2 columns
        col1, col2 = st.columns(2)
        with col1:
            st.altair_chart(chart_co2_emissions_per_product, use_container_width=True)
        with col2:
            st.altair_chart(chart_water_per_product, use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            st.altair_chart(chart_total_co2_per_product, use_container_width=True)
        with col4:
            st.altair_chart(chart_total_water_per_product, use_container_width=True)

        # ----------------------------------------------------------------------------------------------------

    # ------------- Customer Insights -------------------------------------------
    if selected == "Customer Insights":
        st.write("""
        This tab provides insight into H&M's customer demographics, including the number of customers by age group, the total amount spent per age group, and the average amount spent per age group. The tab also includes the percentage spent by customers in each age group, giving H&M insight into which groups are most engaged with their brand.

        By monitoring these metrics, H&M can better understand their customers and tailor their initiatives to meet their needs and preferences.
        """)

        # ----------------------------- Customers filters sidebar -----------------------------
        # Add side bar for filters
        st.sidebar.write("## Age range")

        # Age range filter
        age_filtered_lst = st.sidebar.slider(
            'Select a range of ages:',
            15, 100, (15, 70))

        age_lb = age_filtered_lst[0]
        age_ub = age_filtered_lst[1]

        # ------------------------- Retrieving data from API endpoint -------------------------

        customers_data_age = load_data_from_api("customers/ages")
        customers_data_spent_age = load_data_from_api("customers/ages/spent")

        # ---------------------------------- Merging the data ----------------------------------
        # Merging both dataframes retrieved to get the mean spent by age.
        customers_ages_merged = pd.merge(customers_data_age, customers_data_spent_age, on='age')
        customers_ages_merged['avg_spent'] = customers_ages_merged['spent'] / customers_ages_merged['number_customers']

        # ---------------------------------- Plotting the data ----------------------------------

        # ---------------------------------------------------------------------------------------
        # NUMBER OF CUSTOMERS BY AGES
        customers_ages_filtered = customers_data_age[(customers_data_age['age'] >= age_lb) & (customers_data_age['age'] <= age_ub)]

        chart_customers_ages = alt.Chart(customers_ages_filtered, title='Number of customers by ages').mark_bar(color='#2f7bf5').encode(
            x=alt.X('age', axis=alt.Axis(title='Age')),
            y=alt.Y('number_customers', axis=alt.Axis(title='Number of customers'))
            )
        # ---------------------------------------------------------------------------------------
        # TOTAL AMOUNT SPENT BY CUSTOMER PER AGE

        customers_ages_spent_filtered = customers_data_spent_age[(customers_data_spent_age['age'] >= age_lb) & (customers_data_spent_age['age'] <= age_ub)]

        chart_customers_spent_ages = alt.Chart(customers_ages_spent_filtered, title='Total amount spent by customers per age').mark_bar(color='#2f7bf5').encode(
            x=alt.X('age', axis=alt.Axis(title='Age')),
            y=alt.Y('spent', axis=alt.Axis(title='Amount spent'))
            )

        # ---------------------------------------------------------------------------------------
        # AVERAGE AMOUNT SPENT BY CUSTOMER PER AGE

        customers_ages_spent_avg_filtered = customers_ages_merged[(customers_ages_merged['age'] >= age_lb) & (customers_ages_merged['age'] <= age_ub)]

        chart_customers_spent_avg_ages = alt.Chart(customers_ages_spent_avg_filtered, title='Average amount spent by customers per age').mark_bar(color='#2f7bf5').encode(
            x=alt.X('age', axis=alt.Axis(title='Age')),
            y=alt.Y('avg_spent', axis=alt.Axis(title='Average amount spent'))
            )
        # ------------------------------------------------------------------------------------------
        # PERCENTAGE SPENT BY CUSTOMER PER AGE GROUP

        # create a bar chart of age groups and amount spent
        bins_df = customers_data_spent_age.loc[:, ['age', 'spent']]

        bins_df['age_groups'] = pd.cut(bins_df['age'], bins=[15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, float('Inf')], labels=['16-20', '20-25', '25-30', '30-35', '35-40','40-45','45-50','50-55', '55-60','60-65', '65-70', '70+'])
        grouped_df = bins_df.groupby('age_groups').agg({'spent': 'sum'}).reset_index()
        grouped_df['percent_spent'] = grouped_df['spent'] / grouped_df['spent'].sum() * 100

        chart_bins = alt.Chart(grouped_df, title='Percentage spent by customers per age group').mark_bar(color='#2f7bf5').encode(
            x=alt.X('age_groups', axis=alt.Axis(title='Age group', labelAngle=0)),
            y=alt.Y('percent_spent', axis=alt.Axis(title='% of total spent'))
            )

        # ---------------------------------------------------------------------------------------------------
        # Display charts in 2 columns
        col1, col2 = st.columns(2)
        with col1:
            st.altair_chart(chart_customers_ages, use_container_width=True)
        with col2:
            st.altair_chart(chart_customers_spent_ages, use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            st.altair_chart(chart_customers_spent_avg_ages, use_container_width=True)
        with col4:
            st.altair_chart(chart_bins, use_container_width=True)

    # ------------- Economic Performance ----------------------------------------
    if selected == "Economic Performance":
        st.write("""
        This tab provides insight into H&M's financial peformance, including metrics such as daily revenue, average daily price of products sold, and total revenue per month by sales channel.

        By monitoring these metrics, H&M can ensure that their sustainability initiatives align with their financial goals and identify opportunities to optimize their operations.

        ** I calculate the Operating Costs and Operating Profits by using a 7.7 Operating Margin as per H&M's 2021 anual financial report.
        """)

        # --------------------------- Creating filters ---------------------------
        st.sidebar.write("## Filter by dates and number of products")

        # Create date filter
        start_date = st.sidebar.date_input("Start date", value=datetime.date(2018, 9, 20))
        end_date = st.sidebar.date_input("End date", value=datetime.date(2020, 9, 22))

        # ------------------------- Retrieving data from API endpoint -------------------------

        # Top articles
        sales_count = load_data_from_api("articles/sold/count")
        sales_sum = load_data_from_api("articles/sold/revenue")

        # Sum of price per day and channel id avg request and load data
        transactions_sum_day = load_data_from_api(f"transactions/revenue/{start_date}/{end_date}")

        # Change the column t_dat to be of type datetime
        transactions_sum_day["t_dat"] = pd.to_datetime(transactions_sum_day["t_dat"])

        # Average price per day request and load data
        transactions_avg_day = load_data_from_api(f"transactions/avg_price/{start_date}/{end_date}")

        # Change the column t_dat to be of type datetime
        transactions_avg_day["t_dat"] = pd.to_datetime(transactions_avg_day["t_dat"])

        # ----------------- Create products filter --------------------------------------
        top_filter_article = st.sidebar.slider(
        'Select how many of the most sold products you want to see',
        1, len(sales_count), (1, 10))

        # ------------------------- Adding KPIs -------------------------
        kpi1, kpi2 = st.columns(2)

        # Total revenue in time frame selected.
        total_revenue = sum(transactions_sum_day['price'])

        # Average price in time frame selected.
        total_avg_price = mean(transactions_avg_day['price'])

        kpi1.metric(
            label = "Total revenue in selected time frame",
            value = round(total_revenue,2),
        )

        kpi2.metric(
            label = "Average price of sales in selected time frame",
            value = round(total_avg_price,4),
        )

        # Operating margin from H&M 2021 Financial Report (given in percentage)
        operating_margin = 7.7

        # Calculate the operating costs and profits
        operating_costs = total_revenue * (1 - operating_margin / 100)
        operating_profit = total_revenue * (operating_margin / 100)

        kpi3, kpi4 = st.columns(2)

        kpi3.metric(
            label="Operating costs in selected time frame",
            value=round(operating_costs, 2),
        )

        kpi4.metric(
            label="Operating profits in selected time frame",
            value=round(operating_profit, 2),
        )

        # ------------------------- Plotting the data -------------------------

        # ----------------------------------------------------------------------
        # DAILY REVENUE

        chart_sum_price_day = alt.Chart(transactions_sum_day, title='Daily revenue').mark_bar(color='#32bf6f').encode(
            x=alt.X('t_dat', axis=alt.Axis(title='Day')),
            y=alt.Y('price', axis=alt.Axis(title='Revenue'))
            )
        # -------------------------------------------------------------------------
        # TOTAL MONTHLY REVENUE, BY SALES CHANNEL

        df_monthly = transactions_sum_day.groupby(pd.Grouper(key='t_dat', freq='M')).agg(
            {'price': 'sum', 'percentage_online': 'mean', 'percentage_offline': 'mean'})

        # reset index to get a column for the month
        df_monthly = df_monthly.reset_index()

        # rename the t_dat column to month
        df_monthly = df_monthly.rename(columns={'t_dat': 'month'})

        # Online and offline revenue for each month
        df_monthly['revenue_online'] = df_monthly['price'] * df_monthly['percentage_online']
        df_monthly['revenue_offline'] = df_monthly['price'] * df_monthly['percentage_offline']

        # Melt the dataframe to have a 'revenue_type' column and a 'revenue' column
        df_melted = pd.melt(df_monthly, id_vars=['month'], value_vars=['revenue_online', 'revenue_offline'],
                            var_name='revenue_type', value_name='revenue')

        chart_sum_month = alt.Chart(df_melted, title='Total revenue per month, by sales channel').mark_bar().encode(
            x=alt.X('month', axis=alt.Axis(title='Month')),
            y=alt.Y('revenue', axis=alt.Axis(title='Revenue')),
            color=alt.Color('revenue_type', scale=alt.Scale(domain=['revenue_online', 'revenue_offline'],
                                                            range=['#32bf6f', '#5a6872'])),
            # Set the legend orientation to "bottom"
            tooltip=['revenue_type', 'revenue'],
            # Set the tooltip to show the revenue type and revenue value
            ).properties(
                width=800, height=400  # Set the chart dimensions
            ).configure_legend(
                orient='bottom'  # Move the legend to the bottom
            )

        # ---------------------------------------------------------------------------------------
        # TOP ARTICLES BY SALES

        # Chart to display the top articles by number of sales
        top_articles_sold_filtered = sales_count.iloc[top_filter_article[0]-1:top_filter_article[1]+1]

        # Create chart using altair
        chart_top_articles_sold = alt.Chart(top_articles_sold_filtered, title='Total sales for top products').mark_bar(color='#32bf6f').encode(
            x=alt.X('count_products:Q', axis=alt.Axis(title='Number of products sold')),
            y=alt.Y('product_type_name:N', sort='-x', axis=alt.Axis(title='Type of product')),
            tooltip=['product_type_name', 'count_products']
        )

        # ---------------------------------------------------------------------------------------
        # TOP ARTICLES BY REVENUE

        # Chart to display the top articles revenue
        top_articles_rev_filtered = sales_sum.iloc[top_filter_article[0]-1:top_filter_article[1]+1]

        # Create chart using altair
        chart_top_articles_rev = alt.Chart(top_articles_rev_filtered, title='Total revenue for top products').mark_bar(color='#32bf6f').encode(
            x=alt.X('revenue:Q', axis=alt.Axis(title='Revenue generated')),
            y=alt.Y('product_type_name:N', sort='-x', axis=alt.Axis(title='Type of product')),
            tooltip=['product_type_name', 'revenue']
        )

        # -------------------------------------------------------------------------------------------------
        # Display charts in 2 columns
        col1, col2 = st.columns(2)
        with col1:
            st.altair_chart(chart_sum_month, use_container_width=True)
        with col2:
            st.altair_chart(chart_sum_price_day, use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            st.altair_chart(chart_top_articles_rev, use_container_width=True)
        with col4:
            st.altair_chart(chart_top_articles_sold, use_container_width=True)

        # ----------------------------------------------------------------------------------------------------
