'''
TODO:  

Fall of Junior year (4 sem remaining), and not taking CSE 1341.

Eventually we want a global routine provided by pydpr, 
that allows the user to select which degree we want to create.
This routine should accept 'degreecode' and 'speccode' and then
return the appropriate degree.

If this is done using objects, then each degree object should 
include routines such as


pre_check()
check()


'''

import sys
import numpy as np
import pydpr.pydpr as dpr


spectext = dict({'PM':'Pure', 'ANU':'Applied/Numerical', 'CSE':'Computer Science', 'OR':'Operations Research', 'ENG-EE':'Elec. Eng.', 'ENG-ME':'Mech. Eng.', '':'NONE DECLARED!!!'})

CAL1 = set( ['MATH 1337', 'MATH 1309'] )
CAL2 = set( ['MATH 1338', 'MATH 1340'] )
CORE = set( ['MATH 3302', 'MATH 2339', 'MATH 3304', 'MATH 3353', 'MATH 3313', 'MATH 2343'] )

IPRF = set( ['MATH 3308', 'MATH 3311'] )
ISCP = set( ['MATH 3315', 'CSE 3365', 'MATH 3316'] )

PURE = set( ['MATH 3337', 'MATH 4338', 'MATH 4351', 'MATH 4355', 'MATH 4381', 'MATH 5331', 'MATH 5353', 'MATH 6337'])
APPL = set( ['MATH 3334', 'MATH 3337', 'MATH 4337', 'MATH 4325', 'MATH 4335', 'MATH 5331', 'MATH 5334', 'MATH 5353', 'MATH 6324'])
COMP = set( ['MATH 4315', 'MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 6315', 'MATH 6316', 'CSE 7365'])
ADV  = PURE|APPL|COMP
APNU = APPL|COMP


CSE  = set( ['ASIM 1310', 'CRCP 1310', 'CSE 1341', 'CSE 1342', 'CEE 3310'] )
STAT = set( ['STAT 4340', 'CSE 4340', 'EMIS 3340', 'STAT 5340', 'EE 3360', 'STAT 4341', 'EMIS 7370', 'ECO 5350'] )

PHYS = set( ['PHYS 1303', 'PHYS 1304', 'PHYS 1105', 'PHYS 1106', 'PHYS 1403', 'PHYS 1404',] )
CHEM = set( ['CHEM 1303', 'CHEM 1304', 'CHEM 1113', 'CHEM 1114'] )
BIOL = set( ['BIOL 1301', 'BIOL 1302', 'BIOL 1101', 'BIOL 1102', 'BIOL 1401', 'BIOL 1402'] )
GEOL = set( ['GEOL 1301', 'GEOL 1305', 'GEOL 1307', 'GEOL 1313', 'GEOL 1315', 'GEOL 3340'] ) 
SCI  = PHYS|CHEM|BIOL|GEOL

ENG1 = set(['MATH 3337', 'MATH 4337', 'MATH 4325', 'MATH 4315', 'MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 5331', 'MATH 5334', 'MATH 6315', 'MATH 6316', 'CSE 7365'])

MEG2 = set(['ME 4322', 'ME 4360', 'ME 5302', 'ME 5320', 'ME 5322', 'ME 5336', 'ME 5361', 'ME 5386', 'ME 7302', 'ME 7322',  'ME 7361'])
EEG2 = set(['EE 5330', 'EE 5332', 'EE 5336', 'EE 5360', 'EE 5362', 'EE 5372', 'EE 7330', 'EE 7336', 'EE 7360', 'EE 3322', 'EE 3330', 'EE 3372'])
CEG2 = set(['ME 4322', 'ME 5336', 'MATH 6336', 'CEE 5331', 'CEE 5332', 'CEE 5334', 'CEE 7331', 'CEE 7332', 'CEE 5361', 'CEE 5364', 'CEE 7361', 'CEE 7364', 'ME 4322', 'ME 5322', 'ME 7322'])
ORG2 = set(['EMIS 3360', 'EMIS 5361', 'EMIS 5362', 'EMIS 5369', 'STAT 5344', 'EMIS 5364', 'EMIS 7362'])
CSG2 = set(['CSE 4381'])



def create_degree(degcode, speccode):


  # create a generic degree instance
  degree = dpr.Degree()


  # add major-specific warnings
  degree.add_major_warning_check(credits_per_semester)
  degree.add_major_warning_check(incomplete_foundation)
  if speccode == 'PM':
    degree.add_major_warning_check(pure_missing_3311)
  if speccode in ['CSE', 'OR']:
    degree.add_major_warning_check(comp_missing_1341)
    degree.add_major_warning_check(comp_missing_3315)
  if speccode in ['ANU', 'ENG-ME', 'ENG-EE', 'ENG-CEE']:
    degree.add_major_warning_check(anum_missing_1341)



  # If it is a minor, adjust and return
  if (0):
  #if degcode == 'MN':
    degree.name = "Minor in Mathematics"
    degree.required_credits = 18

    minfund = dpr.Group("Calculus Sequence")
    minfund.add_requirement("Calculus I", CAL1, 1)
    minfund.add_requirement("Calculus II", CAL2, 1)
    minfund.add_requirement("Calculus III", ['MATH 2339'], 1)
    degree.add_group(minfund)

    minelec = dpr.Group("Three Advanced Electives")
    minelec.add_requirement("Elective", MID|ADV, 3)
    degree.add_group(minelec)
    return degree


  # Fundamentals for major
  fund = dpr.Group("Math Foundation")
  fund.add_requirement("Calculus I",     ['MATH 1337', 'MATH 1309'], 1)
  fund.add_requirement("Calculus II",    ['MATH 1338', 'MATH 1340'], 1)
  fund.add_requirement("Calculus III",   ['MATH 3302', 'MATH 2339'], 1)
  fund.add_requirement("Linear Algebra", ['MATH 3304', 'MATH 3353'], 1)
  fund.add_requirement("Intro to ODEs",  ['MATH 3313', 'MATH 2343'], 1)
  degree.add_group(fund)

  # Supplemental Courses
  supp = dpr.Group("Supplemental Courses")
  supp.add_requirement("Sci/Eng Statistics", STAT, 1, greedy=True)
  supp.add_requirement("Intro. Programming", CSE, minhours=3, greedy=True)


  # check for BA/BS and specialization
  specstring = speccode
  if speccode in [None, 'UNS', 'ENG']:
    specstring = 'UNKNOWN -- SEE ME ASAP.'
    speccode = 'ANU'

  if degcode == 'BA':
    degree.name = 'B.A. Mathematics:  Spec. %s ' % (specstring)

  if degcode == 'BS':
    degree.name = 'B.S. Mathematics:  Spec. %s ' % (specstring)
    supp.add_requirement("Science", SCI, minhours=6, greedy=True) 

  degree.add_group(supp)




  spec = dpr.Group("Specialization Electives")
  ENG4P = set([])

  if speccode == 'PM':
    spec.add_requirement("Intro. Proof", IPRF, 1)
    spec.add_requirement("Pure Math", PURE, minhours=9)

  if speccode == 'ANU' or speccode == None or speccode == 'UNS':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("App/Num. Math", APNU, 3)

  if speccode == 'ENG-ME':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Two Math 4000+", ENG1, 2)
    spec.add_requirement("Two ME", MEG2, 2, greedy=True)
    ENG4P = MEG2
    
  if speccode == 'ENG-CEE':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Two Math 4000+", ENG1, 2)
    spec.add_requirement("Two CEE", CEG2, 2, greedy=True)
    ENG4P = CEG2

  if speccode == 'ENG-EE':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Two Math 4000+", ENG1, 2)
    spec.add_requirement("Two EE", EEG2, 2, greedy=True)
    ENG4P = EEG2

  if speccode == 'CSE':
    spec.add_requirement("Int. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Two Math 4000+",  APNU, 2) 
    spec.add_requirement("CSE 4381", CSG2, 1)
    ENG4P = CSG2

  if speccode == 'OR':
    spec.add_requirement("Int. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Adv. Sci. Comp.", COMP, 1 )
    spec.add_requirement("Two EMIS", ORG2, 2, greedy=True)
    ENG4P = ORG2

  spec.add_verification( "ver: One 4000+ (MATH)", ADV, 1)
  spec.add_verification( "ver: Two 4000+ (any)", ADV|ENG4P, 2)
  degree.add_group(spec)


  # one advanced elective
  if speccode in set(['PM', 'ANU', 'CSE', 'OR']):
    elec = dpr.Group("Additional Elective(s)")
    elec.add_requirement("Extra Math 3000+", IPRF|ISCP|ADV, mincourses=1, greedy=True)
    degree.add_group(elec)

  #return
  return degree






# ---------------------------------------------------------
#    Degree-specific pre- and post-check routines
# ---------------------------------------------------------


def detect_eng_specialization(student, courselist):

  if student.speccode == 'ENG':
    depts = [a.dept for a in courselist if a.dept in ['ME', 'EE', 'CEE']]
    if len(depts) == 0: return

    maxdep = max(set(depts), key=depts.count)
    if maxdep == 'ME':  student.speccode = 'ENG-ME'
    if maxdep == 'EE':  student.speccode = 'ENG-EE'
    if maxdep == 'CEE':  student.speccode = 'ENG-CEE'



def incomplete_foundation(student, coursehistory, degree):

  # get necessary information
  now = dpr.current_term()
  grad = int(student.gterm)
  termsleft = (grad-now)/5
  fcomp = degree.grplist[0].satisfied

  # return appropriate warning
  if termsleft < 2 and not fcomp:
    return dpr.DPRWarning(3, "Foundation incomplete with <= 2 semesters remaining.")
  if termsleft < 4 and not fcomp:
    return dpr.DPRWarning(2, "Foundation incomplete with <= 4 semesters remaining.")
  if termsleft < 6 and not fcomp:
    return dpr.DPRWarning(1, "Aim to complete foundation by the end of sophomore year.")
  return None



def pure_missing_3311(student, coursehistory, degree):

  # get necessary information
  ccodes = [c.code for c in coursehistory]
  uterms = dpr.unplanned_terms(student, coursehistory)
  unready = ('MATH 3311' not in ccodes and 'MATH 3308' not in ccodes)

  # return appropriate warning
  if unready and uterms < 3:
    return dpr.DPRWarning(3, "missing MATH 3311: Pure specializaion no longer possible.")
  if unready and uterms < 4:
    return dpr.DPRWarning(2, "you must change your schedule to be enrolled in MATH 3311.")
  if unready and uterms < 5:
    return dpr.DPRWarning(1, "make sure to take MATH 3311 as early as possible.")

  return None


def comp_missing_1341(student, coursehistory, degree):

  # get necessary information
  ccodes = [c.code for c in coursehistory]
  uterms = dpr.unplanned_terms(student, coursehistory)
  unready = ('CSE 1341' not in ccodes and 'ASIM 1310' not in ccodes and 'CRCP' not in ccodes)

  # return appropriate warning
  if unready and uterms < 3:
    return dpr.DPRWarning(3, "missing CSE 1341: CSE/EMIS specializaion no longer possible.")
  if unready and uterms < 4:
    return dpr.DPRWarning(2, "you need to change your schedule to be enrolled in CSE 1341.")
  if unready and uterms < 5:
    return dpr.DPRWarning(1, "it is best to take CSE 1341 by the end of Sophomore year.")

  return None



def anum_missing_1341(student, coursehistory, degree):

  # get necessary information
  ccodes = [c.code for c in coursehistory]
  uterms = dpr.unplanned_terms(student, coursehistory)
  unready = ('CSE 1341' not in ccodes and 'ASIM 1310' not in ccodes and 'CRCP' not in ccodes)

  # return appropriate warning
  if unready and uterms < 2:
    return dpr.DPRWarning(4, "missing CSE 1341: will not be able to graduate on time.")
  if unready and uterms < 3:
    return dpr.DPRWarning(3, "you won't graduate unless you add CSE 1341 to your schedule.")
  if unready and uterms < 4:
    return dpr.DPRWarning(2, "CSE 1341 not taken by the end of Junior year: inadvisable.")
  if unready and uterms < 5:
    return dpr.DPRWarning(1, "make sure to take CSE 1341 by the end of Junior year.")

  return None


def comp_missing_3315(student, coursehistory, degree):

  # get necessary information
  ccodes = [c.code for c in coursehistory]
  uterms = dpr.unplanned_terms(student, coursehistory)
  unready = ('MATH 3315' not in ccodes and 'MATH 3316' not in ccodes and 'CSE 3365' not in ccodes)

  # return appropriate warning
  if unready and uterms < 2:
    return dpr.DPRWarning(3, "missing MATH 3315: CSE/EMIS specializaion no longer possible.")
  if unready and uterms < 3:
    return dpr.DPRWarning(2, "you need to change your schedule to be enrolled in MATH 3315.")
  if unready and uterms < 4:
    return dpr.DPRWarning(1, "make sure to take MATH 3315 by Junior year at the latest.")

  return None




def credits_per_semester(student, coursehistory, degree, threshhold=6.0):

    # assess remaining credits and semesters
    rem_semesters = (int(student.gterm) - dpr.current_term())*2/10
    rem_credits = degree.hours_rem
    if rem_semesters < 1: 
      cps = np.inf if rem_credits > 0 else 0
    else:
      cps = float(rem_credits) / float(rem_semesters)

    # return the appropriate response
    warning = None
    if cps == np.inf:
      return dpr.DPRWarning(4, "graduation not possible by intended date")
    if cps > 11.9:
      return dpr.DPRWarning(3, "courses per semester >= 4")
    if cps > 8.9:
      return dpr.DPRWarning(2, "courses per semester >= 3")
    if cps > 5.9:
      return dpr.DPRWarning(1, "courses per semester >= 2")

    return None


