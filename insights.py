class Getinsights:
    def __init__(self, db_manager):
        self.db = db_manager

    def avg_programming_per_batch(self):
        # to get average number of problems solved by students grouped by their course batch
        sql = """
        SELECT s.course_batch, AVG(p.problems_solved) AS avg_problems_solved
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        GROUP BY s.course_batch
        ORDER BY s.course_batch
        """
        return self.db.query(sql)
    
    def top_5_ready_students(self):
        # to get top 5 students who are ready for placement, ordered by problems solved
        sql = """
        SELECT s.student_id, s.name, p.language, p.problems_solved, pl.placement_status
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        JOIN Placements pl ON s.student_id = pl.student_id
        WHERE pl.placement_status = 'ready'
        ORDER BY p.problems_solved DESC
        LIMIT 5
        """
        return self.db.query(sql)

    
    def soft_skills_distribution(self):
        # Distribution of students by average soft skill scores in ranges
        sql = """
        SELECT 
            CASE 
                WHEN avg_score BETWEEN 90 AND 100 THEN '90-100'
                WHEN avg_score BETWEEN 80 AND 89 THEN '80-89'
                WHEN avg_score BETWEEN 70 AND 79 THEN '70-79'
                WHEN avg_score BETWEEN 60 AND 69 THEN '60-69'
                WHEN avg_score BETWEEN 50 AND 59 THEN '50-59'
                WHEN avg_score BETWEEN 40 AND 49 THEN '40-49'
                ELSE 'Below 40'
            END AS score_range,
            COUNT(*) AS student_count
        FROM (
            SELECT student_id, (communication + teamwork + presentation)/3 AS avg_score
            FROM SoftSkills
        ) AS sub
        GROUP BY score_range
        ORDER BY score_range DESC
        """
        return self.db.query(sql)

    def count_students_per_placement_status(self):
        # Count how many students fall under each placement status category
        sql = """
        SELECT placement_status, COUNT(*) AS student_count
        FROM Placements
        GROUP BY placement_status
        """
        return self.db.query(sql)

    def avg_mock_interview_score_per_batch(self):
        # Average mock interview scores of students grouped by their course batch
        sql = """
        SELECT s.course_batch, AVG(pl.mock_interview_score) AS avg_mock_interview_score
        FROM Students s
        JOIN Placements pl ON s.student_id = pl.student_id
        GROUP BY s.course_batch
        ORDER BY s.course_batch
        """
        return self.db.query(sql)

    def top_internships_done(self):
        # Top 5 students (ready for placement) with the most internships completed  
        sql = """
        SELECT s.student_id, s.name, pl.internships_completed, pl.placement_status
        FROM Students s
        JOIN Placements pl ON s.student_id = pl.student_id
        WHERE pl.placement_status='ready'
        ORDER BY pl.internships_completed DESC
        LIMIT 5
        """
        return self.db.query(sql)

    def most_popular_programming_languages(self):
        # programming languages ranked by number of students that know them
        sql = """
        SELECT language, COUNT(DISTINCT student_id) AS student_count
        FROM Programming
        GROUP BY language
        ORDER BY student_count DESC
        """
        return self.db.query(sql)

    def top_problems_solved(self):
        # Top 5 students by total problems solved in programming
        sql = """
        SELECT s.student_id, s.name, p.problems_solved
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        ORDER BY p.problems_solved DESC
        LIMIT 5
        """
        return self.db.query(sql)

    def avg_soft_skills_score_by_language(self):
        # Average soft skills score by programming language proficiency
        sql = """
        SELECT p.language, AVG((ss.communication + ss.teamwork + ss.presentation)/3) AS avg_soft_skill_score
        FROM Programming p
        JOIN SoftSkills ss ON p.student_id = ss.student_id
        GROUP BY p.language
        ORDER BY avg_soft_skill_score DESC
        """
        return self.db.query(sql)

    def students_eligible_for_placement_per_batch(self):
        # Count of students ready for placement grouped by course batch
        sql = """
        SELECT s.course_batch, COUNT(*) AS eligible_students_count
        FROM Students s
        JOIN Placements pl ON s.student_id = pl.student_id
        WHERE pl.placement_status = 'ready'
        GROUP BY s.course_batch
        ORDER BY s.course_batch
        """
        return self.db.query(sql)
