# 📚 Library Management System

An interactive and user-friendly Library Management System built using **Streamlit** and **MySQL**, designed for seamless administration of students, books, and borrowing activities. This system provides features for managing book inventory, student registration, borrowing/returning books, and insightful data visualization.

---

## 🔧 Features

- ✅ **Admin Login System**
- 🧑‍🎓 Student Registration and Management
- 📖 Add, View, and Search Books
- 📕 Borrow and Return Book Functionality
- 📈 Visualizations of Borrowing Trends
- 📂 Export Borrow History as CSV
- 🔐 Secure, validated form inputs
- 📊 Plotly Charts Integration

---

## 📌 Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/)
- **Backend Database:** [MySQL](https://www.mysql.com/)
- **Data Handling:** Pandas
- **Visualization:** Plotly Express
- **Backend Connection:** mysql-connector-python

---

## 🚀 Setup Instructions
 1. Clone the Repository

   git clone https://github.com/rimagoit/Library_database.git
-cd Library_database

2. Install Required Packages -
 pip install streamlit pandas mysql-connector-python plotly

3. Start MySQL Server and Create Database
CREATE DATABASE library;
-Create necessary tables like `students`, `books`, `borrow_records`, and `admins`
You can use the provided schema.sql (if available) to create tables.

4. Run the Application -
 streamlit run app.py

## 🚀 Live Demo

👉 [Click here to view the live app on Streamlit](https://rimagoit-library-database-app-csmq8l.streamlit.app/)
  ⚠️ Note: The Streamlit-hosted version does not support MySQL connections (e.g., localhost:3306) as it doesn't allow backend servers. As a 
  result, features like login or database access won't work online.

