# H&M Sustainability Dashboard

This project is a dashboard of KPIs using a dataset from H&M.

The dashboard is divided into three tabs: Environmental Impact, Customer Insights, and Economic Performance, each containing several KPIs related to sustainability.

The dashboard was created using Streamlit, and it connects to a Flask API that retrieves data from a Google Cloud SQL database.

## Installation

To install the required packages, run the following command:

```python
pip install -r requirements.txt
```

The requirements.txt file includes all the necessary packages to run both the Flask API and the Streamlit app.

## Running the Flask API

To run the Flask API, navigate to the api directory and run the following command:

```python
python [app.py](http://app.py/)
```

This will start the Flask API and make it available at [http://localhost:5000](http://localhost:5000/).

## Running the Streamlit App

To run the Streamlit app, navigate to the streamlit-app directory and run the following command:

```python
streamlit run [app.py](http://app.py/)
```

This will start the Streamlit app and make it available at [http://localhost:8501](http://localhost:8501/).

## Database

The database used in this project is a Google Cloud SQL database, which contains three tables from an H&M dataset: a customers table, a transactions table, and an articles table. The Flask API connects to this database and retrieves data from it.

## API Endpoints

The Flask API has several endpoints that retrieve data from the database and transform it into JSON format. The available endpoints are:

- /api/customers: Retrieves data from the customers table.
- /api/transactions: Retrieves data from the transactions table.
- /api/articles: Retrieves data from the articles table.

## Streamlit App

The Streamlit app connects to the Flask API and retrieves data from it. It then displays this data in the form of interactive visualizations, allowing the user to explore the sustainability KPIs related to H&M. The app is divided into three tabs: Environmental Impact, Customer Insights, and Economic Performance.

## Conclusion

The H&M Sustainability Dashboard is a powerful tool for tracking H&M's sustainability performance and identifying areas for improvement. By connecting to a Google Cloud SQL database and transforming data into JSON format, this project demonstrates how to create an API that can be used to power a Streamlit dashboard. With its user-friendly interface and interactive visualizations, this dashboard is a valuable tool for anyone interested in sustainability and data analysis.
