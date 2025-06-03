Placement Eligibility Data Science Project

Project Overview:
This project involves creating an application to analyse and gain insights on student placement eligibility using Python, MySQL, and Streamlit library. Fake data is generated and stored in a MySQL database, and queries are executed to extract insights on student performance, skills, and placement readiness.

Features:
- Generate data for students, programming skills, soft skills, and placements using Faker library.
- Store and manage data in MySQL database.
- Execute queries to get insights such as:
  - Average programming problems solved per batch
  - Top students based on problems solved and internships done
  - Distribution of soft skills scores
  - Count of students by placement status
  - Average mock interview scores per batch
  - Most popular programming languages among students
  - Students eligible for placement per batch
-Streamlit app with filters to get data insights.

Project Structure:
- data_generation.py: Generates and inserts synthetic data into MySQL database using OOP.
- insights.py: Contains the `Getinsights` class with methods that run SQL queries to get insights.
- app.py: Streamlit app that connects to the database and display results.

Tool Used:
- VS Code: Used for writing and running Python code (.py files).
- MySQL Workbench: Used to view or manage the MySQL database 
- Streamlit: Used to build the interactive web application.

Usage:
- Install Required Libraries.
- Open MySQL Workbench.
- Set Up MySQL Database
- Update the login credentials in your .py files to match your setup.
- Run data_generation.py to create the tables with fake data.
- Open the folder in VS Code. Review and modify credentials in .py files if needed.
- Enter this in the VS Code terminal: streamlit run app.py
- This will open a browser window with the application interface. 
- Use filters on the sidebar to customize the data insights  
- View summary tables student performance and placement readiness

