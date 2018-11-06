import sys
from openpyxl import load_workbook
import pydpr.pydpr as dpr
from pydpr.degrees.Math import create_degree, autodetect_eng_specialization

# basic setup info
studentfile = './records/current-mathmajors.xlsx'
coursesfile = './records/current-coursehistories.xlsx'

# identify the student
fragment = sys.argv[1]
studentID = dpr.find_student(studentfile, fragment)


# load student information, and identify precise degree type
student = dpr.load_student_from_query(studentfile, studentID)
courses = dpr.load_courses_from_query(coursesfile, studentID)
autodetect_eng_specialization(student, courses)

# create degree plan and check requirements
degree = create_degree(student.degreecode, student.speccode)
degree.check(courses)

# print report
report = dpr.terminal_report(student, courses, degree)
print(report)

# plot semester GPA
dpr.plot_gpa_progression(courses)





