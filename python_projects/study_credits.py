from functools import reduce

# Creates a class for each course attempt with its name, grade, and number of credits
class CourseAttempt:
    # Method to initialize object
    def __init__(self, course_name: str, grade: int, credits: int):
        self.course_name = course_name
        self.grade = grade
        self.credits = credits
    
    # Returns a string representation of the course attempt in the desired format
    def __str__(self):
        return f"{self.course_name} ({self.credits} cr) grade {self.grade}"

# A helper function that returns an updated sum of credits
def sums_credits(credits_sum, attempt) -> int:
    return credits_sum + attempt.credits 

# Course sum regardless if passed or failed 
def sum_of_all_credits(attempts:list) -> int:
    return reduce(sums_credits, attempts, 0) 

# Calculates the sum of credits for all the passed attempts
def sum_of_passed_credits(attempts:list) -> int:
    passed_credits = filter(lambda passed: passed.grade > 0, attempts)
    return reduce(sums_credits, passed_credits, 0)
 
 # Calculates the average grade of passed courses from a list of attempts
def average_grade(attempts:list) -> float:
    passed_courses = [course for course in attempts if course.grade > 0]
    if not passed_courses: # Function returns 0.0 if there are no passed courses
        return 0.0
    passed_grades = [courses.grade for courses in passed_courses]
    return sum(passed_grades) / len(passed_courses)
 
if __name__ == "__main__":
    # Testing the code by creating new instances for each student
    student_1 = CourseAttempt("Introduction to Programming", 5, 5)
    student_2 = CourseAttempt("Advanced Course in Programming", 0, 4)
    student_3 = CourseAttempt("Data Structures and Algorithms", 3, 10)
    print(f"{student_1}\n{student_2}\n{student_3}")
    print(f"Average grade: {average_grade([student_1, student_2, student_3])}")
