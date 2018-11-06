import sys
import string
from os.path import basename

# for reading XLSX files
from openpyxl import load_workbook

# for e-mailing
from smtplib import SMTP_SSL, SMTPException
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

# for degree status
import pydpr.pydpr as dpr 
from pydpr.degrees.Math import create_degree, autodetect_eng_specialization


termtext = "Spring 2018"
ycbmlink = "http://smu-snorris.ycb.me"


# files with student and course histories
studentfile  = './records/current-mathmajors.xlsx'
coursesfile  = './records/current-coursehistories.xlsx'
done_email   = './documents/advising-email-template-complete.txt'
active_email = './documents/advising-email-template-inprogress.txt'
catalogfile  = './documents/2016-math-catalog.pdf'
advicefile   = './documents/general-advice.pdf'
changesfile  = './documents/2017-math-curricular-changes.pdf'
declaredfaq  = './documents/FAQ-majors.pdf'

done_attach = []
active_attach = [declaredfaq]


# get the e-mail template
with open(done_email, 'r') as myfile:
  emailstring = myfile.read()
done_template = string.Template(emailstring)

# get the e-mail template
with open(active_email, 'r') as myfile:
  emailstring = myfile.read()
active_template = string.Template(emailstring)


# Log in to mail server
success = 0
try:
  print("Logging in: ")
  smtp = SMTP_SSL('smtp.smu.edu:465')
  smtp.login('01370901', 'password')
  success = 1
  print("success!")
except SMTPException:
  print("Error: unable to login.")
  exit()
  quit()


# open up the database file, and iterate through students
majors = set(['MATH-BA', 'MATH-BS'])
wb = load_workbook(studentfile, read_only=True)
ws = wb[wb.get_sheet_names()[0]]
IDS = []
for row in ws:
  ID = str(row[0].value)
  major = str(row[22].value)
  print(ID)
  if major in majors:  IDS.append(ID)



for studentID in IDS:

  # load student information
  try:
    student = dpr.load_student_from_query(studentfile, studentID)
  except dpr.MissingStudentError as mse:
    print("StudentID %s not found in course file %s." % (studentID, studentfile))
    print("This shouldn't happen.  Something is very wrong.")
    quit()
    exit()


  # load course information
  try:
    courses = dpr.load_courses_from_query(coursesfile, studentID)
    autodetect_eng_specialization(student, courses)
  except dpr.MissingCoursesError as mce:
    print("StudentID %s not found in course file %s." % (studentID, coursesfile))
    print("Skipping this student.")
    continue


  # create degree plan and check requirements
  try:
    degree = create_degree(student.degreecode, student.speccode)
    degree.check(courses)

    # create a PDF report of the student's progress
    pdfreport = "math-dpr-%s.pdf"%(studentID)
    dpr.pdf_report(student, courses, degree, pdfreport)
  except Exception as ee:
    print("This shouldn't happen.  Something is very wrong.")
    quit()
    exit()


  # has the student graduated or not?
  myemail = None
  myattach = [pdfreport]
  if degree.complete == True:
    myemail = done_template
    myattach.extend(done_attach)
  else:
    myemail = active_template
    myattach.extend(active_attach)




  # set up message
  me = 'snorris@smu.edu'
  you = str(student.email)

  # create the body of the email
  values = dict()
  values['ID']    = student.ID
  values['fname'] = student.fname
  values['lname'] = student.lname
  values['email'] = student.email
  values['term']  = termtext
  values['link']  = ycbmlink
  body = myemail.substitute(values)

  # set up message
  msg = MIMEMultipart()
  msg['From'] = me
  msg['To'] = you
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = "Math Advising (%s): %s Course Selection" % (student.ID, termtext)
  msg.attach(MIMEText(body))

  # add attachments
  allattach = [pdfreport]
  allattach.extend(myattach)
  print(allattach)
  for f in allattach:
    with open(f, "rb") as fil:
      msg.attach(MIMEApplication(
        fil.read(),
        Content_Disposition='attachment; filename="%s"' % basename(f),
        Name=basename(f)
      ))

  # send message
  if(len(sys.argv) > 1 and sys.argv[1] == '--run'):
    try:
      smtp.sendmail(me, [you], msg.as_string())
      print("Successfully sent email to %s" % (student.email))
    except SMTPException:
      print("Error: unable to send email to %s" % (student.email))
  else:
    print(body)






