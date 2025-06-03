from insights import Getinsights
import streamlit as st
import pymysql
import pandas as pd

class Databasemanager:
    def __init__(self, host, user, password, db):
        # connects to MySQL database

        self.connection = pymysql.connect(
            host=host, user=user, password=password, database=db
        )
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


class Studentfiltering:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_filters(self):
        st.sidebar.title("Filter Candidates")

        language = st.sidebar.multiselect(
            "Candidate should know any of the selected programming languages",
            options=["Python", "SQL", "Java", "C++", "Javascript", "C#"],
            default=["Python"]
        )
        min_problems = st.sidebar.slider("Minimum number of problems solved", 0, 500, 0)
        min_soft_skill_score = st.sidebar.slider("Minimum Soft Skills Score(averaged)", 0, 100, 0)
        min_mock_interview_score = st.sidebar.slider("Minimum mock interview score", 0, 100, 0)
        min_internships = st.sidebar.slider("Minimum number of internships completed", 0, 4, 0)

        return {
            "language": language,
            "min_problems": min_problems,
            "min_soft_skill_score": min_soft_skill_score,
            "min_mock_interview_score": min_mock_interview_score,
            "min_internships": min_internships
        }

    def fetch_filtered_students(self, filters):
        placeholders = ', '.join(['%s'] * len(filters["language"]))
        sql = f"""
        SELECT s.student_id, s.name, s.age, s.email, p.language, p.problems_solved, 
               ss.communication, ss.teamwork, ss.presentation, pl.mock_interview_score, pl.internships_completed
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        JOIN SoftSkills ss ON s.student_id = ss.student_id
        JOIN Placements pl ON s.student_id = pl.student_id
        WHERE p.language IN ({placeholders})
          AND p.problems_solved >= %s
          AND ((ss.communication + ss.teamwork + ss.presentation) / 3) >= %s
          AND pl.mock_interview_score >= %s
          AND pl.internships_completed >= %s
          AND pl.placement_status != 'placed'
        """
        params = (*filters["language"], filters["min_problems"], filters["min_soft_skill_score"],
                  filters["min_mock_interview_score"], filters["min_internships"])
        results = self.db.query(sql, params)
        return results

    def display_students(self, students):
        st.write(f"### Found {len(students)} Eligible Students")
        if students:
            df = pd.DataFrame(students)

            df['avg_soft_skill_score'] = (df['communication'] + df['teamwork'] + df['presentation']) / 3

            df = df[['student_id', 'name', 'age', 'email', 'language', 'problems_solved',
                     'avg_soft_skill_score', 'mock_interview_score', 'internships_completed']]

            st.dataframe(df)

        else:
            st.write("No eligible students found.")

    def run(self):
        st.title("Placement Eligibility Filter")
        filters = self.get_filters()
        students = self.fetch_filtered_students(filters)
        self.display_students(students)


def run_insights(insights):
    st.title("Insights Dashboard")
    insight_options = {
        "What is the average programming performance per batch?": insights.avg_programming_per_batch,
        "Who are the top 5 students by probelms solved and ready for placements? ?": insights.top_5_ready_students,
        "What is the soft skills distribution?": insights.soft_skills_distribution,
        "What is the count of students per placement status?": insights.count_students_per_placement_status,
        "What is the average mock interview score per batch?": insights.avg_mock_interview_score_per_batch,
        "who are the top 5 students by internships done?": insights.top_internships_done,
        "What are the most popular programming languages?": insights.most_popular_programming_languages,
        "Who are the top 5 students by problems ssolved?": insights.top_problems_solved,
        "What is the average soft skills score by language?": insights.avg_soft_skills_score_by_language,
        "How many students are eligible for placement per batch?": insights.students_eligible_for_placement_per_batch,
    }
    choice = st.sidebar.selectbox("Select an Insight to View", list(insight_options.keys()))
    result = insight_options[choice]()
    if result:
        df = pd.DataFrame(result)
        st.dataframe(df)
    else:
        st.write("No data found for this insight.")


if __name__ == "__main__":
    db_manager = Databasemanager(host="localhost", user="root", password="timewaste", db="placement_db")

    app = Studentfiltering(db_manager)
    insights = Getinsights(db_manager)

    page = st.sidebar.radio("Choose a page", ["Candidate Filtering", "Insights Dashboard"])

    if page == "Candidate Filtering":
        app.run()
    else:
        run_insights(insights)

    db_manager.close()




