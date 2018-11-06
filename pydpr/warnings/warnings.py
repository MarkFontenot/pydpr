import copy
import time
import os.path
import numpy as np



class Warning:

  def __init__(self, checker=None, wdata=None, reporter=None):

    self.checker  = checker
    self.wdata    = wdata
    self.reporter = reporter
    self.level    = 0





# check last semester GPA

class LastSemesterGPA:

  def __init__(self, threshhold=2.0, level=2):

    # required of all warnings
    self.triggered  = False
    self.level      = level

    # specific to this warning
    self.threshhold = 2.0
    self.actual     = None


  def checker(self, student, courselist, degree):

    this_term = dpr.current_term()
    last_term = dpr.current_term() - 5
    last_year = dpr.current_term() - 10

    # get last semester's courses
    courses_ls = [cc for cc in courselist if cc.term == last_term and cc.grade in dpr.GPAgrades]

    # calculate last semester's GPA
    gpoints = np.array([dpr.GPAlookup[cc.grade] for cc in courses_ls]) 
    credits = np.array([cc.credits for cc in courses_ls])
    last_credits = sum(credits)
    last_GPA = np.dot(gpoints, credits) / sum(credits)

    self.actual = last_GPA
    if self.actual < self.threshhold:
      self.triggered = True

  def reporter(self):

    report = "Last semester GPA = %2.2f < %2.2f." % (self.actual, self.threshhold)
    return report







# check fails in last two semesters

class LastYearFails:

  def __init__(self, threshhold=0, level=2):

    # required of all warnings
    self.triggered  = False
    self.level      = level

    # specific to this warning
    self.threshhold = threshhold
    self.actual     = None


  def checker(self, student, courselist, degree):

    this_term = dpr.current_term()
    last_term = dpr.current_term() - 5
    last_year = dpr.current_term() - 10

    # count failed courses last year
    failset = set(['F', 'D-', 'D', 'D+'])
    courses_ly = [cc for cc in courselist if int(cc.term) >= last_year and cc.grade in dpr.GPAgrades]
    self.actual = len([cc for cc in courses_ly if cc.grade in failset])

    if (self.actual > self.threshhold):
      self.triggered = True


  def reporter(self):

    report = "Last semester fails = %d > %d." % (self.actual, self.threshhold)
    return report





# check degree GPA

class DegreeGPA:

  def __init__(self, threshhold=2.5, level=2):

    # required of all warnings
    self.triggered  = False
    self.level      = level

    # specific to this warning
    self.threshhold = threshhold
    self.actual     = None

  def checker(self, student, courselist, degree):

    # get all degree courses
    degcourses = []
    for grp in degree.grplist:
      for cc in grp.satcourses:
        degcourses.append(cc)

    # calculate degree GPA
    degcourseset = set([cc.code for cc in degcourses])
    alldegcourses = [cc for cc in coursehistory if cc.code in degcourseset and cc.grade in dpr.GPAgrades]
    gpoints = np.array([GPAlookup[cc.grade] for cc in alldegcourses]) 
    credits = np.array([cc.credits for cc in alldegcourses])
    self.actual = np.dot(gpoints, credits) / sum(credits)

    if (self.actual < self.threshhold):
      self.triggered = True


  def reporter(self):
    report = "Cumulative degree GPA = %2.2f < %2.2f." % (self.actual, self.threshhold)
    return report

    

# assess remaining credits per semester

class CreditsPerSemester:

  def __init__(self, threshholds=[3.0, 6.0, 9.0]):

    # required of all warnings
    self.triggered  = False
    self.level      = 0

    # specific to this warning
    self.threshholds = threshholds
    self.actual      = None


  def checker(self, student, courselist, degree):

    this_term = dpr.current_term()

    # get all degree courses
    degcourses = []
    for grp in degree.grplist:
      for cc in grp.satcourses:
        degcourses.append(cc)

   # assess remaining credits and semesters
    degree_rem_semesters = (int(student.gterm) - current_term())*2/10
    degree_rem_credits = degree.required_credits - sum([ cc.credits for cc in degcourses ])
    if degree_rem_semesters < 1: 
      self.actual = np.inf if self.degree_rem_credits > 0 else 0
    else:
      self.actual = float(self.degree_rem_credits) / float(self.degree_rem_semesters)

    
    for th in threshholds:
      if (self.actual > th):
        level += 1

    if level > 0:
      triggered = True


  def reporter(self):

    report = "Needed degree credits / semester = %2.2f" % (self.actual)
    return report



'''
Halfway solution to a clean implementation of degree red flags.  All red flags are hard-coded into this object.
'''

class ProgressReport:

  def __init__(self, student, coursehistory, degree):

    self.last_GPA = None
    self.last_credits = None
    self.last_year_fails = None
    self.degree_GPA = None
    self.degree_rem_credits = None
    self.degree_rem_semesters = None
    self.degree_credits_per_semester = None

    this_term = dpr.current_term()
    last_term = dpr.current_term() - 5
    last_year = dpr.current_term() - 10

    # count failed courses last year
    failset = set(['F', 'D-', 'D', 'D+'])
    courses_ly = [cc for cc in courselist if int(cc.term) >= last_year and cc.grade in dpr.GPAgrades]
    self.last_year_fails = len([cc for cc in courses_ly if cc.grade in failset])

    # get all degree courses
    degcourses = []
    for grp in degree.grplist:
      for cc in grp.satcourses:
        degcourses.append(cc)

    # calculate degree GPA
    degcourseset = set([cc.code for cc in degcourses])
    alldegcourses = [cc for cc in coursehistory if cc.code in degcourseset and cc.grade in GPAgrades]
    gpoints = np.array([GPAlookup[cc.grade] for cc in alldegcourses]) 
    credits = np.array([cc.credits for cc in alldegcourses])
    self.degree_GPA = np.dot(gpoints, credits) / sum(credits)
  

    # assess remaining credits and semesters
    self.degree_rem_semesters = (int(student.gterm) - current_term())*2/10
    self.degree_rem_credits = degree.required_credits - sum([ cc.credits for cc in degcourses ])
    if self.degree_rem_semesters < 1: 
      self.degree_credits_per_semester = np.inf if self.degree_rem_credits > 0 else 0
    else:
      self.degree_credits_per_semester = float(self.degree_rem_credits) / float(self.degree_rem_semesters)


    # here add a set of progress report





    # Assessment of Degree progress
    credits_per_sem = pr.degree_credits_per_semester
    credit_rating = ""
    if   credits_per_sem == 0.0:  credit_rating = Fore.CYAN    + 'COMPLETE!!'  + Style.RESET_ALL
    elif credits_per_sem <= 3.0:  credit_rating = Fore.GREEN   + 'excellent!'  + Style.RESET_ALL
    elif credits_per_sem <= 4.5:  credit_rating = Fore.YELLOW  + 'acceptable.' + Style.RESET_ALL
    elif credits_per_sem <= 6.0:  credit_rating = Fore.YELLOW  + 'caution ...' + Style.RESET_ALL
    elif credits_per_sem <= 7.5:  credit_rating = Fore.RED     + 'concern!'    + Style.RESET_ALL
    else:                         credit_rating = Fore.MAGENTA + 'CRITICAL!!'  + Style.RESET_ALL
    credit_report = "needs %d credits over %d semesters: %s" % (pr.degree_rem_credits, pr.degree_rem_semesters, credit_rating)



    # Warnings
    if pr.last_credits < 12:
      report += Fore.RED+"Warning:"+Style.RESET_ALL+" last sem. credits = %d \n" % (pr.last_credits)
    if pr.last_GPA < 2.5:
      report += Fore.RED+"Warning:"+Style.RESET_ALL+" last semester GPA = %2.2f \n" % (pr.last_GPA)
    if pr.last_year_fails > 0:
      report += Fore.RED+"Warning:"+Style.RESET_ALL+" fails in last year = %d \n" % (pr.last_year_fails)
    if pr.degree_GPA < 2.5:
      report += Fore.RED+"Warning:"+Style.RESET_ALL+" cumulative degree GPA = %2.2f \n" % (pr.degree_GPA)
    if pr.degree_credits_per_semester > 6:
      report += Fore.RED+"Warning:"+Style.RESET_ALL+" needed degree credits / semester = %2.2f \n" % (pr.degree_credits_per_semester)

