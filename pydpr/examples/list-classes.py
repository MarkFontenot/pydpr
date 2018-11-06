import sys
import pydpr.pydpr as dpr

# basic setup info
studentfile = './records/current-mathmajors.xlsx'
coursesfile = './records/current-coursehistories.xlsx'

# identify the student
fragment = sys.argv[1]
studentID = dpr.find_student(studentfile, fragment)

# is there a filter?
dfilter   = False
if len(sys.argv) > 2:
  dfilter = True
  dept = sys.argv[2]

courselist = dpr.load_courses_from_query(coursesfile, studentID)
courselist.sort(key=lambda course: course.term)
for cc in courselist:
  if cc.credits == 0: 
    continue
  if dfilter == True and cc.dept != dept:
    continue

  print("{0:4} {1:4} --> {2:16} --> {3:4} {4:4}".format(cc.dept, cc.number, dpr.termcode_to_text(cc.term), cc.credits, cc.grade))

print('\n')


