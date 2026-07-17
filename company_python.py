print("Program Started...\n")

import mysql.connector

# ==========================
# Database Connection
# ==========================
try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR-PASSWORD",
        auth_plugin="mysql_native_password",
        use_pure=True
    )

    cursor = con.cursor()
    print("✅ Connected to MySQL\n")

except Exception as e:
    print("Connection Error:", e)
    exit()

# ==========================
# Create Database & Table
# ==========================
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS company_db")
    cursor.execute("USE company_db")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employee(
        Emp_ID VARCHAR(10) PRIMARY KEY,
        Name VARCHAR(50),
        Department VARCHAR(50),
        Salary INT,
        Experience INT,
        Rating DECIMAL(2,1)
    )
    """)

    print("✅ Database & Table Ready\n")

except Exception as e:
    print("Database Error:", e)

# ==========================
# Insert Sample Data
# (Run only once)
# ==========================
def insert_data():

    cursor.execute("DELETE FROM Employee")

    cursor.executemany("""
    INSERT INTO Employee
    (Emp_ID, Name, Department, Salary, Experience, Rating)
    VALUES(%s,%s,%s,%s,%s,%s)
    """,[
        ("101","Amit","Sales",45000,2,4.1),
        ("102","Priya","HR",52000,5,4.8),
        ("103","Rahul","IT",68000,6,4.5),
        ("104","Neha","Finance",59000,4,4.2),
        ("105","Karan","Sales",43000,2,3.9),
        ("106","Sneha","IT",72000,8,4.9),
        ("107","Riya","HR",50000,3,4.3),
        ("108","Arjun","Finance",61000,5,4.6),
        ("109","Vikas","Sales",47000,3,4.0),
        ("110","Anjali","IT",75000,9,5.0)
    ])

    con.commit()
    print("✅ Sample Data Inserted Successfully")

# Uncomment only for first run
# insert_data()

# ==========================
# Show All Employees
# ==========================
def show_employee():

    cursor.execute("SELECT * FROM Employee")

    records = cursor.fetchall()

    if len(records) == 0:
        print("No Employees Found.")
        return

    print("\n===== EMPLOYEE LIST =====")

    for row in records:

        print("-"*40)
        print(f"ID         : {row[0]}")
        print(f"Name       : {row[1]}")
        print(f"Department : {row[2]}")
        print(f"Salary     : ₹{row[3]:,}")
        print(f"Experience : {row[4]} Years")
        print(f"Rating     : {row[5]}")

    print("-"*40)

# ==========================
# Search Employee
# ==========================
def search_employee():

    emp_id = input("Enter Employee ID : ")

    cursor.execute(
        "SELECT * FROM Employee WHERE Emp_ID=%s",
        (emp_id,)
    )

    record = cursor.fetchone()

    if record:

        print("\n===== EMPLOYEE DETAILS =====")
        print(f"ID         : {record[0]}")
        print(f"Name       : {record[1]}")
        print(f"Department : {record[2]}")
        print(f"Salary     : ₹{record[3]:,}")
        print(f"Experience : {record[4]} Years")
        print(f"Rating     : {record[5]}")
        print("="*30)

    else:
        print("❌ Employee Not Found")

# ==========================
# Add Employee
# ==========================
def add_employee():

    emp_id = input("Enter Employee ID : ")

    cursor.execute(
        "SELECT * FROM Employee WHERE Emp_ID=%s",
        (emp_id,)
    )

    if cursor.fetchone():
        print("❌ Employee ID Already Exists")
        return

    name = input("Enter Name : ")
    department = input("Enter Department : ")
    salary = int(input("Enter Salary : "))
    experience = int(input("Enter Experience : "))
    rating = float(input("Enter Rating : "))

    cursor.execute("""
    INSERT INTO Employee
    (Emp_ID,Name,Department,Salary,Experience,Rating)
    VALUES(%s,%s,%s,%s,%s,%s)
    """,
    (emp_id,name,department,salary,experience,rating))

    con.commit()

    print("✅ Employee Added Successfully")

# ==========================
# Update Salary
# ==========================
def update_salary():

    emp_id = input("Enter Employee ID : ")

    cursor.execute(
        "SELECT * FROM Employee WHERE Emp_ID=%s",
        (emp_id,)
    )

    record = cursor.fetchone()

    if record:

        new_salary = int(input("Enter New Salary : "))

        cursor.execute("""
        UPDATE Employee
        SET Salary=%s
        WHERE Emp_ID=%s
        """,
        (new_salary, emp_id))

        con.commit()

        print("✅ Salary Updated Successfully")

    else:
        print("❌ Employee Not Found")


# ==========================
# Delete Employee
# ==========================
def delete_employee():

    emp_id = input("Enter Employee ID : ")

    cursor.execute(
        "SELECT * FROM Employee WHERE Emp_ID=%s",
        (emp_id,)
    )

    record = cursor.fetchone()

    if record:

        cursor.execute(
            "DELETE FROM Employee WHERE Emp_ID=%s",
            (emp_id,)
        )

        con.commit()

        print("✅ Employee Deleted Successfully")

    else:
        print("❌ Employee Not Found")


# ==========================
# Analysis Report
# ==========================
def analysis_report():

    print("\n========== COMPANY REPORT ==========\n")

    # Total Employees
    cursor.execute("SELECT COUNT(*) FROM Employee")
    total = cursor.fetchone()
    print("Total Employees :", total[0])

    # Highest Salary
    cursor.execute("SELECT MAX(Salary) FROM Employee")
    highest = cursor.fetchone()
    print(f"\nHighest Salary : ₹{highest[0]:,}")

    # Lowest Salary
    cursor.execute("SELECT MIN(Salary) FROM Employee")
    lowest = cursor.fetchone()
    print(f"\nLowest Salary : ₹{lowest[0]:,}")

    # Average Salary
    cursor.execute("SELECT AVG(Salary) FROM Employee")
    average = cursor.fetchone()
    print(f"\nAverage Salary : ₹{average[0]:,.0f}")

    # Department with Highest Average Salary
    cursor.execute("""
    SELECT Department
    FROM Employee
    GROUP BY Department
    ORDER BY AVG(Salary) DESC
    LIMIT 1
    """)

    department = cursor.fetchone()

    print("\nDepartment with Highest Average Salary :")
    print(department[0])

    # Top 3 Employees
    cursor.execute("""
    SELECT Name
    FROM Employee
    ORDER BY Salary DESC
    LIMIT 3
    """)

    top = cursor.fetchall()

    print("\nTop 3 Employees")

    for i, row in enumerate(top, start=1):
        print(f"{i}. {row[0]}")

    # Rating > 4.5
    cursor.execute("""
    SELECT Name
    FROM Employee
    WHERE Rating > 4.5
    """)

    records = cursor.fetchall()

    print("\nEmployees Rating > 4.5")

    for row in records:
        print(row[0])

    print("\n====================================")


# ==========================
# Main Menu
# ==========================
while True:

    print("\n========== EMPLOYEE MANAGEMENT ==========")
    print("1. Show All Employees")
    print("2. Search Employee")
    print("3. Add Employee")
    print("4. Update Salary")
    print("5. Delete Employee")
    print("6. Analysis Report")
    print("7. Exit")

    choice = input("\nEnter Your Choice : ").strip()

    if choice == "1":
        show_employee()

    elif choice == "2":
        search_employee()

    elif choice == "3":
        add_employee()

    elif choice == "4":
        update_salary()

    elif choice == "5":
        delete_employee()

    elif choice == "6":
        analysis_report()

    elif choice == "7":
        print("\nThank You For Using Employee Management System.")
        break

    else:
        print("❌ Invalid Choice. Try Again.")


# ==========================
# Close Connection
# ==========================
cursor.close()
con.close()

print("✅ MySQL Connection Closed.")
