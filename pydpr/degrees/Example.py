import sys
import pydpr.pydpr as dpr

'''
IDEAL STRUCTURE
----------------

A degree could consist of
-- a list of groups
-- a list of redflag condition callbacks
-- a list of precheck callbacks

When creating a degree, 


TODO:  

Need specific departmental warnings in the following cases:

Spring of Sophomore year (5 sem remaining), and not taking 3308.
Fall of Junior year (4 sem remaining), and not taking CSE 1341.
Spring of Junior year (3 sem remaining), and not taking 3337.
Spring of Junior year (3 sem remaining), and not taking 3315.

Eventually we want a global routine provided by pydpr, 
that allows the user to select which degree we want to create.
This routine should accept 'degreecode' and 'speccode' and then
return the appropriate degree.

If this is done using objects, then each degree object should 
include routines such as


pre_check()
check()






'''









spectext = dict({'PM':'Pure', 'ANU':'Applied/Numerical', 'CSE':'Computer Science', 'OR':'Operations Research', 'ENG-EE':'Elec. Eng.', 'ENG-ME':'Mech. Eng.', '':'NONE DECLARED!!!'})

CSE    = set( ['CSE 1341', 'CSE 1342', 'CEE 3310'] )
STAT   = set( ['STAT 4340', 'CSE 4340', 'EMIS 3340', 'STAT 5340', 'EE 3360', 'STAT 4341', 'EMIS 7370'] )
PHYS   = set( ['PHYS 1403', 'PHYS 1404', 'PHYS 1301', 'PHYS 1303', 'PHYS 1304'] )
CHEM   = set( ['CHEM 1303', 'CHEM 1304'] )
BIOL   = set( ['BIOL 1401', 'BIOL 1402', 'BIOL 1301', 'BIOL 1302'] )
GEOL   = set( ['GEOL 1301', 'GEOL 1305', 'GEOL 1307', 'GEOL 1313', 'GEOL 1315'] ) 
SCI    = PHYS|CHEM|BIOL|GEOL

CAL1   = set( ['MATH 1337', 'MATH 1309'] )
CAL2   = set( ['MATH 1338', 'MATH 1340'] )

CORE   = set( ['MATH 1338', 'MATH 2339', 'MATH 2343'] )
MID    = set( ['MATH 3308', 'MATH 3315', 'MATH 3334', 'MATH 3337', 'MATH 3353'] )
PURE   = set( ['MATH 4338', 'MATH 4351', 'MATH 4355', 'MATH 4381', 'MATH 5331', 'MATH 5353'])
APPL   = set( ['MATH 4335', 'MATH 5334', 'MATH 6324'] )
COMP   = set( ['MATH 4370', 'MATH 5315', 'MATH 5316', 'CSE 7365'] )
GRAD   = set( ['MATH 6315', 'MATH 6316', 'MATH 6324', 'MATH 6350', 'MATH 6333'] )
ADV    = PURE|APPL|COMP|GRAD

ISCP = set( ['MATH 3315', 'CSE 3365', 'MATH 3316'] )
PM5  = set( ['MATH 3308', 'MATH 3337', 'MATH 3353', 'MATH 4338', 'MATH 4351', 'MATH 4355', 'MATH 4381', 'MATH 5331', 'MATH 5353'])
ANU4 = set( ['EMIS 3360', 'MATH 3334', 'MATH 3337', 'MATH 3353', 'MATH 4335', 'MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 5331', 'MATH 5334', 'MATH 5353'])




def create_degree(degcode, speccode):

  degree = dpr.Degree()

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
  fund = dpr.Group("Fundamentals")
  fund.add_requirement("Calculus I", CAL1, 1)
  fund.add_requirement("Calculus II", CAL2, 1)
  fund.add_requirement("Calculus III", ['MATH 2339'], 1)
  fund.add_requirement("Intro. Diff. Eq.", ['MATH 2343'], 1)
  degree.add_group(fund)

  # Supplemental Courses
  supp = dpr.Group("Supplemental Courses")
  supp.add_requirement("Intro. Statistics", STAT, 1)
  supp.add_requirement("Intro. Programming", CSE, 1)

  if degcode == 'BA':
    degree.name = 'B.A. Mathematics:  Spec. %s ' % ('UNDECLARED (FIX THIS!!!)' if (speccode == None or speccode == 'UNS') else speccode)
    degree.required_credits = 36

  if degcode == 'BS':
    degree.name = 'B.S. Mathematics:  Spec. %s ' % ('UNDECLARED -- USING ANU (FIX!!!)' if (speccode == None or speccode == 'UNS') else speccode)
    degree.required_credits = 42
    supp.add_requirement("Science", SCI, 2) 

  degree.add_group(supp)




  spec = dpr.Group("Advanced Electives")
  ENG4P = set([])

  if speccode == 'PM':
    spec.add_requirement("Pure Math", PM5, 5)

  if speccode == 'ANU' or speccode == None or speccode == 'UNS':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("App/Num. Math", ANU4, 4)

  if speccode == 'CSE':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("CSE 4381", ['CSE 4381'], 1)
    spec.add_requirement("Math", ['MATH 3353', 'MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 6315', 'MATH 6316'], 3) 

  if speccode == 'OR':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("EMIS 3360", ['EMIS 3360'], 1)
    spec.add_requirement("Two Math", ['MATH 3353', 'MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 5353', 'MATH 6315', 'MATH 6316', 'CSE 7365'], 2 )
    spec.add_requirement("Extra EMIS", ['EMIS 5361', 'EMIS 5362', 'EMIS 5369', 'STAT 5344', 'EMIS 5364', 'EMIS 7362'], 1)
    ENG4P = set(['EMIS 5361', 'EMIS 5362', 'EMIS 5369', 'STAT 5344', 'EMIS 5364', 'EMIS 7362'])

  if speccode == 'ENG-EE':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Math 3337", ['MATH 3337'], 1 )
    spec.add_requirement("One MATH 5000+ (or 4370)", ['MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 5331', 'MATH 5334', 'MATH 6315', 'MATH 6316', 'CSE 7365'], 1)
    #spec.add_requirement("One EE 4000+", ['EE 5330', 'EE 5332', 'EE 5336', 'EE 5360', 'EE 5362', 'EE 5372'], 1 )
    spec.add_requirement("Two EE", ['EE 3322', 'EE 3330', 'EE 3372', 'EE 5330', 'EE 5332', 'EE 5336', 'EE 5360', 'EE 5362', 'EE 5372', 'EE 7330', 'EE 7336', 'EE 7360'], 2 )
    ENG4P = set(['EE 5330', 'EE 5332', 'EE 5336', 'EE 5360', 'EE 5362', 'EE 5372', 'EE 7330', 'EE 7336', 'EE 7360'])

  if speccode == 'ENG-ME':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Math 3337", ['MATH 3337'], 1 )
    spec.add_requirement("E. Math 5000+  (or 4370)", ['MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 5331', 'MATH 5334', 'MATH 6315', 'MATH 6316', 'CSE 7365'], 1)
    spec.add_requirement("Two ME", ['ME 4360', 'ME 5302', 'ME 5320', 'ME 5322', 'ME 7322', 'ME 5336', 'ME 5361', 'ME 5386', 'ME 7322',  'ME 7361'], 2 )
    ENG4P = set(['ME 4360', 'ME 5302', 'ME 5320', 'ME 5322', 'ME 5336', 'ME 5361', 'ME 5386', 'ME 7322',  'ME 7361'])

  if speccode == 'ENG-CIV':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Math 3337", ['MATH 3337'], 1 )
    spec.add_requirement("E. Math 5000+  (or 4370)", ['MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 5331', 'MATH 5334', 'MATH 6315', 'MATH 6316', 'CSE 7365'], 1)
    spec.add_requirement("Two CIV", ['CEE 5361', 'CEE 5364', 'ME 5322', 'ME 7322', 'CEE 7361', 'CEE 7364'], 2 )
    ENG4P = set(['CEE 5361', 'CEE 5364', 'ME 5322', 'ME 7322', 'CEE 7361', 'CEE 7364'])

  if speccode == 'ENG-ENV':
    spec.add_requirement("Intro. Sci. Comp.", ISCP, 1) 
    spec.add_requirement("Math 3337", ['MATH 3337'], 1 )
    spec.add_requirement("E. Math 5000+  (or 4370)", ['MATH 4370', 'MATH 5315', 'MATH 5316', 'MATH 5331', 'MATH 5334', 'MATH 6315', 'MATH 6316', 'CSE 7365'], 1)
    spec.add_requirement("Two ENV", ['ME 5336', 'MATH 6336', 'CEE 5331', 'CEE 5332', 'CEE 5334'], 2 )
    ENG4P = set(['ME 5336', 'MATH 6336', 'CEE 5331', 'CEE 5332', 'CEE 5334'])


  #adv.add_subreq( dpr.Requirement("Four from MATH", MATH3|MATH4P, 4))
  spec.add_verification( "ver: Two 4000+ (any)", ADV|ENG4P, 2)
  spec.add_verification( "ver: One 4000+ (MATH)", ADV, 1)
  degree.add_group(spec)


  # one advanced elective
  elec = dpr.Group("One 3000+ elective")
  elec.add_requirement("Elective", MID|ADV|GRAD, 1)
  degree.add_group(elec)

  #return
  return degree






def autodetect_eng_specialization(student, courselist):

  if student.speccode == 'ENG':
    depts = [a.dept for a in courselist if a.dept in ['ME', 'EE', 'CEE']]
    maxdep = max(set(depts), key=depts.count)
    if maxdep == 'ME':  student.speccode = 'ENG-ME'
    if maxdep == 'EE':  student.speccode = 'ENG-EE'
    if maxdep == 'CEE':
      codes = [a.code for a in courselist]
      if 'CEE 2340' in codes:  student.speccode = 'ENG-CIV'
      if 'CEE 2421' in codes:  student.speccode = 'ENG-ENV'








