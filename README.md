# E-Commerce Data Management System

## Description
Backend system to manage and analyze product and sales data using Python, MySQL, and Flask. Integrated with Power BI for visual insights.

## Features
- Add and manage products
- Record sales and track inventory
- Automated data pipeline for inventory updates
- Power BI dashboard for revenue and sales trends

## Tech Stack
- Python, Flask
- MySQL
- Pandas
- Power BI

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `db_config.py` with your MySQL credentials
4. Run Flask app: `python app.py`

## API Endpoints
- `/add_product` [POST] – Add new product
- `/get_products` [GET] – Get all products
- `/add_sale` [POST] – Record a sale
- `/get_sales_summary` [GET] – Get sales summary
