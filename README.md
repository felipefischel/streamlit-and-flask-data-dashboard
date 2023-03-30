# H&M Sustainability Dashboard

<aside>
📊 [H&M Dashboard](https://frontend-dot-hardy-symbol-376415.oa.r.appspot.com/)

</aside>

<aside>
🔗 [Flask REST API](https://api-dot-hardy-symbol-376415.oa.r.appspot.com/)

</aside>

## **Overview**

The H&M Sustainability Dashboard is a web application that provides a dashboard of KPIs using a dataset from H&M.

I also created an extra dataset to obtain some additional sustainability metrics, related to CO2 emissions and water consumption of their products.

To provide a general view of the sustainability of H&Ms business, I decided to divide the dashboard into three tabs: Environmental Impact, Customer Insights, and Economic Performance.

The dashboard was created using Streamlit and a Flask API that retrieves data from a Google Cloud SQL database.

## Datasets

The datasets used in this project come from H&M and include three tables: a customers table, a transactions table, and an articles table. These tables are stored in a Google Cloud SQL database and are retrieved by the Flask API.

I also created an extra dataset that has the "CO2 emissions" and "Water Consumption" of each product. The values in this dataset are very bold approximations and were made for experimentation purposes.

Given that the three main dataframes from the H&M database contain a large number of entries, loading this data directly in the application would result in large loading times, negatively affecting the user experience. To overcome this issue, I created new dataframes by groping and merging multiple dataframes. By doing so, I created smaller, more manageable dataframes that can be loaded with ease, ensuring a seamless and enjoyable user experience.

## Flask API

The Flask API has several endpoints that retrieve data from the database and transform it into JSON format.

In order to have access to the data, I implement a token-based authentication system. The user must provide a valid token in the header when making a get request to the API. Without a valid token, the user cannot access the data.

I created an `execute_query` function to check that checks that the Authorization token is in the request header. It also handles errors and returns the corresponding error code.

```python
def execute_query(query):
    try:
        if "Authorization" not in request.headers:
            return make_response(jsonify({"error": "unauthorized"}), 401)
        else:
            header = request.headers["Authorization"]
            token = header.split()[1]

            if token not in auth_db:
                return make_response(jsonify({"error": "unauthorized"}), 401)

        conn = connect()
        result = conn.execute(query).fetchall()
        disconnect(conn)
        return make_response(jsonify({'result': [dict(row) for row in result]}), 200)

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 500)
```

The APIs are structured into three parts: Customers, Articles, and Transactions, each containing different endpoints to retrieve corresponding data. The endpoints are as follows:

### Customers:

- /customers/ages: This endpoint returns a table that groups customers by age, showing the number of customers in each age group.
- /customers/ages/spent: This endpoint returns a table that groups customers by age, showing the total amount spent by customers in each age group. It is obtained through a merge with the transactions table.

### Articles:

- /articles/sold/count: This endpoint returns the data from the product_name_sales_count table, which groups products by name and shows the number of sales for each product.
- /articles/sold/revenue: This endpoint returns the data from the product_name_sales_sum table, which groups products by name and shows the total revenue generated by each product through a merge with the transactions table.
- /articles/top/products: This endpoint returns the data from the product_count table, which groups products by type and shows the number of products in each type.

### Transactions:

- /transactions/revenue/:start_date/:end_date: This endpoint returns the sum of transactions by day (revenue) between the start_date and end_date. It groups transactions by date and sums the price for each day.
- /transactions/avg_price/:start_date/:end_date: This endpoint returns the average of transactions by day (revenue) between the start_date and end_date. It groups transactions by date and calculates the average price for each day.

## Streamlit App

The Streamlit app connects to the Flask API and retrieves data from it. It then displays this data in the form of interactive visualizations, allowing the user to explore the sustainability KPIs related to H&M. The app is divided into three tabs: Environmental Impact, Customer Insights, and Economic Performance. Here are screenshot of each tab:

![Homepage](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/86bb185f-a1fe-4a97-aedf-ed5541dd8725/Screen_Shot_2023-03-30_at_12.32.23_AM.png)

Homepage

![Environmental Impact](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/977b13ad-3b31-4d12-abef-509dd15a3565/Screen_Shot_2023-03-30_at_12.32.38_AM.png)

Environmental Impact

![Customer Insights](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c5910237-f165-4828-a023-f247ea2b0fd5/Screen_Shot_2023-03-30_at_12.32.58_AM.png)

Customer Insights

![Economic Performance](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3a2f60e4-a91a-4eef-bba5-2b8fcf8e250c/Screen_Shot_2023-03-30_at_12.33.21_AM.png)

Economic Performance

The app also has a login page were users can authenticate themselves.

![Login page](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f7545040-135c-4cff-8ff7-144de2869bc9/Screen_Shot_2023-03-30_at_10.10.36_PM.png)

Login page

This are the username and passwords currently allowed:

| Username | Password |
| --- | --- |
| felipefischel | Capstone! |
| pepe | Capstone! |
| gustavo | Capstone! |

# Conclusion

The H&M Sustainability Dashboard is a powerful tool for tracking H&M's sustainability performance and identifying areas for improvement. By connecting to a Google Cloud SQL database and transforming data into JSON format, this project demonstrates how to create an API that can be used to power a Streamlit dashboard. With its user-friendly interface and interactive visualizations, this dashboard is a valuable tool for anyone interested in sustainability and data analysis.
