# H&M Sustainability Dashboard

Project links:

📊 [**H&M Sustainability Dashboard**](https://frontend-dot-hardy-symbol-376415.oa.r.appspot.com/)

🔗 [**Flask REST API**](https://api-dot-hardy-symbol-376415.oa.r.appspot.com/)

## Screenshots:

Homepage:
<img width="1122" alt="Screen Shot 2023-03-30 at 12 32 23 AM" src="https://user-images.githubusercontent.com/107649745/228956044-25c983ac-a7df-4f6e-939c-0f553c742bcf.png">

Environmental Impact
<img width="1032" alt="Screen Shot 2023-03-30 at 12 32 38 AM" src="https://user-images.githubusercontent.com/107649745/228956221-603fa8b6-975f-4096-8259-030e8840db35.png">

Customer Insights
<img width="1055" alt="Screen Shot 2023-03-30 at 12 32 58 AM" src="https://user-images.githubusercontent.com/107649745/228956296-ef1489eb-2216-4725-8914-e4ca5f42edef.png">

Economic Performance

<img width="779" alt="Screen Shot 2023-03-30 at 12 33 21 AM" src="https://user-images.githubusercontent.com/107649745/228956371-46739c66-4419-4d34-9ad6-4641531d72d8.png">

The app also has a login page were users can authenticate themselves.
<img width="1011" alt="Screen Shot 2023-03-30 at 10 27 48 PM" src="https://user-images.githubusercontent.com/107649745/228956606-c0df3d9e-77f7-4154-8262-02f10a6d6857.png">


## **Overview**

The H&M Sustainability Dashboard is a web application that provides a dashboard of KPIs using a dataset from H&M.

I also created an extra dataset to obtain some additional sustainability metrics, related to CO2 emissions and water consumption of their products.

To provide a general view of the sustainability of H&Ms business, I decided to divide the dashboard into three tabs: Environmental Impact, Customer Insights, and Economic Performance.

The dashboard was created using Streamlit and a Flask API that retrieves data from a Google Cloud SQL database.

## Datasets

The datasets used in this project come from H&M and include three tables: a customers table, a transactions table, and an articles table. These tables are stored in a Google Cloud SQL database and are retrieved by the Flask API.

I also created an extra dataset that has the "CO2 emissions" and "Water Consumption" of each product. The values in this dataset are very bold approximations and were made for experimentation purposes.

As an example, here's a few lines of the json file I created:

```json
{
  "Trousers": {"CO2": 10.2, "Water": 2060},
  "Dress": {"CO2": 16.8, "Water": 3360},
  "Sweater": {"CO2": 7.5, "Water": 1500},
  "T-shirt": {"CO2": 3.6, "Water": 720},
  "Top": {"CO2": 4.3, "Water": 860}
}
```

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

The Streamlit app connects to the Flask API and retrieves data from it. It then displays this data in the form of interactive visualizations, allowing the user to explore the sustainability KPIs related to H&M. The app is divided into three tabs: Environmental Impact, Customer Insights, and Economic Performance.

I also did some minor changes to the CSS of the Streamlit app so that it would addapt to the look and feel I wanted to achieve.

### This are the username and passwords currently allowed to login:

| Username | Password |
| --- | --- |
| felipefischel | Capstone! |
| pepe | Capstone! |
| gustavo | Capstone! |

# Conclusion

The H&M Sustainability Dashboard is a powerful tool for tracking H&M's sustainability performance and identifying areas for improvement. By connecting to a Google Cloud SQL database and transforming data into JSON format, this project demonstrates how to create an API that can be used to power a Streamlit dashboard. With its user-friendly interface and interactive visualizations, this dashboard is a valuable tool for anyone interested in sustainability and data analysis.
