# contact-management-python
Contact Management System using Python

## Contact Management System 📇
A Python application integrated with MySQL to manage and persist contact data.
## 🚀 Features

* Add & View: Store and list contacts directly from a SQL database.
* Update: Modify existing contact details (name, phone, or email) easily.
* Search & Delete: Find or remove entries with real-time database syncing.

## 🛠️ Tech Stack

* Language: Python 3.x
* Database: MySQL (Managed via MySQL Workbench)
* Library: mysql-connector-python

## ⚙️ Database Setup
Before running the app, you need to set up your database in MySQL Workbench:

   1. Create a database: CREATE DATABASE contact_db;
   2. Create a table:
   
   CREATE TABLE contacts (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       phone VARCHAR(15),
       email VARCHAR(255)
   );
   
   3. Update the connection details (host, user, password) in your Python script.

## 🖥️ How to Run

   1. Install the MySQL connector:
   
   pip install mysql-connector-python
   
   2. Run the script:
   
   python main.py


