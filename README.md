# Salesphere

Salesphere is a Django-based Store Management and Billing System designed for small and medium-sized businesses. It helps store owners manage products, customers, inventory, invoices, payments, and business operations from a centralized dashboard.

---

## Features

### Store Management
- Store registration during signup
- Business category selection
- GST information management
- Store profile management

### User Authentication
- User Registration
- Secure Login
- Logout Functionality
- Session-based Authentication
- Protected Dashboard Access

### Product Management
- Add Products
- Update Product Details
- Delete Products
- Product Categories
- Product Branding
- GST Tax Configuration
- Stock Management
- Unit Management (PCS, KG, Litre, Box, Pack)

### Inventory Management
- Opening Stock Tracking
- Current Stock Tracking
- Minimum Stock Alerts
- Stock Updates
- Inventory Monitoring

### Customer Management
- Add Customers
- Store Customer Contact Information
- Customer Address Management
- GSTIN & PAN Tracking
- Credit Limit Management
- Payment Term Management

### Billing System
- Create Invoices
- Auto Invoice Number Generation
- Financial Year Based Invoice Series
- Draft Invoice Support
- Finalized Invoice Support
- Customer-wise Billing

### Invoice Calculations
- Automatic Subtotal Calculation
- GST Tax Calculation
- Grand Total Calculation
- Quantity Tracking
- Line Item Management

### Payment Management
- Cash Payments
- UPI Payments
- Bank Transfer Payments
- Credit Payments

### Payment Tracking
- Paid Invoices
- Pending Invoices
- Partial Payments
- Overdue Invoices
- Payment Status Monitoring

### Dashboard Analytics
- Total Products
- Total Customers
- Total Bills
- Monthly Revenue
- Weekly Sales Data
- Top Selling Products

---

## Technology Stack

### Backend
- Python
- Django

### Database
- SQLite (Development)

### Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

### Authentication
- Django Authentication System

---

## Database Models

### Store
Stores business information including:

- Store Name
- GST Number
- Address
- Category
- Mobile Number

### Product

Stores inventory details:

- Product Name
- Product Code
- Category
- Brand
- Purchase Price
- Selling Price
- GST Rate
- Stock Information
- Unit Type

### Customer

Stores customer information:

- Name
- Contact Details
- Address
- GSTIN
- PAN Number
- Credit Limit
- Payment Terms

### Bill

Stores invoice information:

- Invoice Number
- Customer
- Invoice Date
- Due Date
- Payment Status
- Payment Method

### Bill Item

Stores invoice line items:

- Product
- Quantity
- Unit Price
- GST
- Total Amount

---

## Dashboard Metrics

Salesphere provides:

- Product Count
- Customer Count
- Invoice Count
- Monthly Revenue
- Weekly Sales Trend
- Top Selling Products

---

## Business Categories Supported

- Grocery / Supermarket
- Electronics & Appliances
- Clothing & Fashion
- Pharmacy / Medical
- Restaurant / Food
- Hardware / Tools
- Books / Stationery
- Other Businesses

---

## Payment Status Logic

Invoices are automatically categorized as:

- Draft
- Pending
- Partial
- Paid
- Overdue

---

## GST Support

Supported GST Rates:

- 0%
- 5%
- 12%
- 18%
- 28%

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/salesphere.git
```

### Move Into Project

```bash
cd salesphere
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

## 📸 Screenshots

### Login Page

![Login Page](screenshots/login-page.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Product Management

![Product Management](screenshots/products.png)

### Customer Management

![Customer Management](screenshots/customers.png)

### Create Invoice

![Create Invoice](screenshots/create-invoice.png)

### Inventory Management

![Inventory Management](screenshots/inventory.png)

### Payments

![Payments](screenshots/payments.png)


---

## Future Improvements

- Barcode Scanning
- Multi-Store Support
- Sales Reports
- PDF Invoice Generation
- Email Invoice Delivery
- Customer Purchase History
- Purchase Management
- Supplier Management
- AI-Powered Business Insights
- GST Return Reports

---

## Project Highlights

- Django Authentication
- Inventory Tracking
- Automated Invoice Generation
- GST Calculation
- Payment Management
- Revenue Analytics
- Customer Management
- Store Management

---

## Author

Arunesh Natarajan

Python Developer | Django Developer

---

## License

This project is licensed under the MIT License.