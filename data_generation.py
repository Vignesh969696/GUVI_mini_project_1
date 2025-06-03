import pymysql
from faker import Faker
import random

fake = Faker()

# Handling Database connection
class Databasemanager:
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, data=None):
        self.cursor.execute(query,data if data else ())
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


# Student Table created(if it doesnt exist)
class Studentdatagenerator:
    def __init__(self, db_manager):
        self.db = db_manager

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Students (
            student_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100),
            age INT,
            gender VARCHAR(10),
            email VARCHAR(100),
            phone BIGINT,
            enrollment_year INT,
            course_batch VARCHAR(50),
            city VARCHAR(50),
            graduation_year INT
        );
        """
        self.db.execute(query)

    def insert_fake_data(self,num_records=500):
        for _ in range(num_records):
            name = fake.name()
            age = random.randint(18,26)
            gender = random.choice(['Male','Female','Other'])
            email = fake.email()
            phone = int(fake.msisdn()[0:10])
            enrollment_year = random.choice([2019,2020,2021,2022])
            course_batch = f"Batch-{random.randint(1,5)}"
            city = fake.city()
            graduation_year = enrollment_year + 4

            query = """
            INSERT INTO Students 
            (name,age,gender,email,phone,enrollment_year,course_batch,city,graduation_year)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values = (name,age,gender,email,phone,enrollment_year, course_batch,city,graduation_year)
            self.db.execute(query,values)

# fake data for programming table
class Programdatagenerator:
    def __init__(self,db_manager):
        self.db = db_manager
# creates programming table if it doesn't exist, with foreign key to Students
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Programming (
            programming_id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT,
            language VARCHAR(50),
            problems_solved INT,
            assessments_completed INT,
            mini_projects INT,
            certifications_earned INT,
            latest_project_score INT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        );
        """
        self.db.execute(query)
# Inserts programming data for students in the students table
    def insert_fake_data(self):
        self.db.execute("SELECT student_id FROM Students")
        student_ids = [row[0] for row in self.db.cursor.fetchall()]
        languages = ['Python','SQL','Java','C++','Javascript','C#']

        for sid in student_ids:
            query = """
            INSERT INTO Programming
            (student_id,language,problems_solved,assessments_completed,mini_projects,certifications_earned,latest_project_score)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
            values = (
                sid,
                random.choice(languages),
                random.randint(10,500),
                random.randint(1,10),
                random.randint(0,5),
                random.randint(0,5),
                random.randint(35,100)
            )
            self.db.execute(query,values)

# fake data for soft skills table
class Softskilldatagenerator:
    def __init__(self,db_manager):
        self.db = db_manager
    # Creates soft skills table with various skill scores and foreign key to Students
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS SoftSkills (
            soft_skill_id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT,
            communication INT,
            teamwork INT,
            presentation INT,
            leadership INT,
            critical_thinking INT,
            interpersonal_skills INT,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        );
        """
        self.db.execute(query)
    # will insert random soft skills scores for students

    def insert_fake_data(self):
        self.db.execute("SELECT student_id FROM Students")
        student_ids = [row[0] for row in self.db.cursor.fetchall()]

        for sid in student_ids:
            query = """
            INSERT INTO SoftSkills
            (student_id,communication,teamwork,presentation,leadership,critical_thinking,interpersonal_skills)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """
            values = (
                sid,
                random.randint(35,100),
                random.randint(35,100),
                random.randint(35,100),
                random.randint(35,100),
                random.randint(35,100),
                random.randint(35,100)
            )
            self.db.execute(query,values)

# generates fake data for placements Table
class Placementdatagenerator:
    def __init__(self,db_manager):
        self.db = db_manager
    # creates placements table with placement info and foreign key to Students
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Placements (
            placement_id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT,
            mock_interview_score INT,
            internships_completed INT,
            placement_status VARCHAR(50),
            company_name VARCHAR(100),
            placement_package_usd FLOAT,
            interview_rounds_cleared INT,
            placement_date DATE,
            FOREIGN KEY (student_id) REFERENCES Students(student_id)
        );
        """
        self.db.execute(query)

    # inserts placement details with  constraints based on placement status
    def insert_fake_data(self):
        self.db.execute("SELECT student_id FROM Students")
        student_ids = [row[0] for row in self.db.cursor.fetchall()]
        statuses = ['Ready','Not Ready','Placed']
        companies = ['TCS','Google','Microsoft','L&T','Amazon']
        
        for sid in student_ids:
            status = random.choice(statuses)
            
            if status == 'Placed':
                company = random.choice(companies)
                package = random.randint(50000, 120000)
                rounds = random.randint(2,5)
                date = fake.date_between(start_date='-1y', end_date='today')
            else:
                company = 'None'
                package = 0.0
                rounds = random.randint(0,2)
                date = None
            
            query = """
            INSERT INTO Placements
            (student_id, mock_interview_score, internships_completed, placement_status, company_name, 
            placement_package_usd, interview_rounds_cleared, placement_date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values = (
                sid,
                random.randint(35,100),
                random.randint(0,4),
                status,
                company,
                package,
                rounds,
                date
            )
            self.db.execute(query,values)

# Clears all tables, in case of errors
def reset_database(db):
    tables = ['Placements','SoftSkills','Programming','Students']
    db.execute("SET FOREIGN_KEY_CHECKS=0;")
    for table in tables:
        db.execute(f"TRUNCATE TABLE {table};")
    db.execute("SET FOREIGN_KEY_CHECKS=1;")

if __name__ == "__main__":
    db = Databasemanager(host="localhost",user="root",password="timewaste",db="placement_db")

    # In case some issues with the iDs(it starts from 7000), resets tables

    reset_database(db)

    # Generate and insert fake data into all tables

    student_generator = Studentdatagenerator(db)
    student_generator.insert_fake_data()

    programming_generator = Programdatagenerator(db)
    programming_generator.insert_fake_data()

    softskills_generator = Softskilldatagenerator(db)
    softskills_generator.insert_fake_data()

    placement_generator = Placementdatagenerator(db)
    placement_generator.insert_fake_data()

    db.close()
    print("Data has been inserted")



