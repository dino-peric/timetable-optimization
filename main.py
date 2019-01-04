import numpy as np
from helpers import *
import argparse, sys
import time 

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-timeout', help='How long the program will run for')
parser.add_argument('-award_activity', help='Array of awards')
parser.add_argument('-award_student', help='Award for doing all swaps of a student')
parser.add_argument('-minmax_penalty', help='Amount of points deducted for being outside pref values')
parser.add_argument('-students_file', help='Students file')
parser.add_argument('-requests_file', help='Requests file')
parser.add_argument('-overlaps_file', help='Overlaps file')
parser.add_argument('-limits_file', help='Limits file')

args = parser.parse_args()

timeout        = args.timeout                   # Time for which the program will run
award_activity = args.award_activity.split(',') # Array of awards
award_student  = args.award_student             # Award for doing all swaps of a single student
minmax_penalty = args.minmax_penalty            # Penalty for each student in each group that has a number of students not between minpref and maxpref
students_file  = args.students_file             # Should be like: student_id, activity_id, swap_weight, group_id, new_group_id
requests_file  = args.requests_file             # Should be like: student_id, activity_id, req_group_id
overlaps_file  = args.overlaps_file             # Should be like: group1_id, group2_id
limits_file    = args.limits_file               # Should be like: group_id, students_cnt, min, min_preferred, max, max_preferred

students, studentsHeader = ReadFileArray(students_file)
requests, requestsHeader = ReadFileArray(requests_file)

limits, limitsHeader     = ReadFileArray(limits_file)     
overlaps, overlapsHeader = ReadFileArray(overlaps_file)   

# Remove elements from requests that are in requests but not in students
requests = RemoveDifferentElements(requests, students)

start = time.time()

# TODO Datoteka overlaps može sadržavati i podatke o grupama koje se ne nalaze u  
#      ulaznoj datoteci students-file pa se ti podaci mogu slobodno zanemariti.
#      znaci treba proc kroz overlaps i uzet samo one groupIDeve koji se nalaze u groupID polju u
#      students-file, ovo treba napraviti prije uniqueGroups poziva ili cak unutar njega, 
#      a mozda i ne moramo uopce ne znam utjece li na performans, ovaj TODO je za kasnije nakon implementacije algoritma

# Get all unique students
uniqueStudents = set()
for i in range(len(students)):
    uniqueStudents.add(students[i][0])
uniqueStudents = list(uniqueStudents)

studentsDict = {} # Dictionary where key = studentID, value = Student object
for i in range(len(uniqueStudents)):
    activsGroups = {}
    newStudent = Student(uniqueStudents[i])
    for j in range(len(students)):
        if students[j][0] == uniqueStudents[i]:
            #activsGroups.append( (students[j][1], students[j][3]) )
            # Get all activity -> group pairs of a student and put it in activsGroups dict
            activsGroups[students[j][1]] = students[j][3]
    newStudent.activityGroupPair = activsGroups      
    studentsDict[uniqueStudents[i]] = newStudent

studentsDictOrg = studentsDict
#print(studentsDict['15317'].activityGroupPair)

# Get all unique groups from overlaps file
uniqueGroups = set()
for i in range(len(overlaps)):
    uniqueGroups.add(overlaps[i][0])
uniqueGroups = list(uniqueGroups)

groupsDict = {} # Dictionary where key = groupId, value = Group object, combines LIMITS and OVERLAPS files
for i in range(len(uniqueGroups)):
    overlapsWith = []
    newGroup = Group(uniqueGroups[i])
    for j in range(len(overlaps)):                      # Add all overlaps for groups
        if uniqueGroups[i] == overlaps[j][0]:           # No need for overlaps file from this point
            overlapsWith.append(overlaps[j][1])
    groupsDict[uniqueGroups[i]] = newGroup
    groupsDict[uniqueGroups[i]].overlaps = overlapsWith
    for k in range(len(limits)):                        # Add all limits for groups
        if limits[k][0] == uniqueGroups[i]:             # No need for limits file from this point
            groupsDict[uniqueGroups[i]].initStudentsCount = limits[k][1]
            groupsDict[uniqueGroups[i]].currentStudentCount = limits[k][1]            
            groupsDict[uniqueGroups[i]].minCount = limits[k][2]
            groupsDict[uniqueGroups[i]].minPref = limits[k][3]
            groupsDict[uniqueGroups[i]].max = limits[k][4]
            groupsDict[uniqueGroups[i]].maxPref = limits[k][5]

#print(len(groupsDict))
#print(groupsDict['140915'].initStudentsCount)

# TODO 0) How to transform requests file into a class so it's easier to manipulate within main loop, maybe not needed(?)
# Get all requests grouped by students
reqFromOneStudent = set()
for i in range(len(requests)):
    reqFromOneStudent.add((requests[i][0], requests[i][1]))
reqFromOneStudent = list(reqFromOneStudent)

requestsDict = {} # Dictionary where key = (studentId, activityId), value = [requested groups ids]
for i in range(len(reqFromOneStudent)):
    newRequest = Request( reqFromOneStudent[i] )
    requestedGroups = []
    for j in range(len(requests)):
        if requests[j][0] == reqFromOneStudent[i][0] and requests[j][1] == reqFromOneStudent[i][1]:
            requestedGroups.append(requests[j][2])
            #if (len(requestedGroups) >= 2):
                #print(requests[j][0], requests[j][1], requestedGroups)
            #activsGroups.append( (students[j][1], students[j][3]) )
    newRequest.requestedGroups = requestedGroups      
    requestsDict[ ( reqFromOneStudent[i][0], reqFromOneStudent[i][1] )] = newRequest


print(requestsDict[('16003', '2897934')].requestedGroups)

# AKTIVNOST = PREDMET npr. NASP 
# GRUPA     = UCIONA  npr. B4, B2 
# znaci jedna aktivnost ima vise grupa, student moze biti samo u jednoj grupi, 
# ALI za jednu aktivnost moze traziti da ga prebacimo u jednu od vise grupa


### MAIN LOOP ###

# TODO 3) Calculate goal function for each neighbour: 
#      3.1) for each binary element (IF WE RANDOMLY ASSIGNED 1 DURING NEIGHBOURHOOD GENERATION)
#         check if: no group overlap, minmax satisfied and no swap already for that activity for that student(?)
#      3.2) Check if swapping is possible ie check if group overlaps with another (use overlaps field in Group)
#      3.3) Check if it is possible to add/take away students from this group (use all other fields in Group)
#      3.4) Some butko shit that I don't understand (this is maybe the (?) in TODO 3.1))
#      3.5) If any of 3.1 - 3.4 is not possible goal function = -1 (this neighbour is not possible so we ignore it)
# TODO 4) Select best neighbour based on best goal function and start loop again
### END MAIN LOOP ###

# TODO 1) make binary vector of len(requests) that represents granting or denying of requests, if vec[i] = 0 then 
# request[i] was not granted, if 1 it was granted   
#      1.1) Assign random values and check them
vector = [0] * len(requests)

# Main loop
while True:
    # TODO 2) Generate neighbourhood -> pick which way to generate neighbourhood



    for i in range(len(vector)):
        reqStdId = requests[i][0] # studentId in request
        reqActId = requests[i][1] # activityId in request
        reqGrpId = requests[i][2] # groupId in request
        if vector[i] == 1:  # Ako je 1 idemo provjerit jel se moze taj request dat
            if IsRequestValid(reqStdId, reqActId, reqGrpId):
                # Moze se napravit zamjena -> napravimo ju
                groupsDict[reqGrpId].currentStudentCount += 1 # Povecaj broj ljudi u grupi u koju zeli ici
                # Smanji broj ljudi u grupi iz koje izlazi
                groupsDict[ studentsDict[ reqStdId ].activityGroupPair[ reqActId ] ].currentStudentCount -= 1
                # Promijeni studentov raspored 
                studentsDict[ reqStdId ].activityGroupPair[ reqActId ] = groupsDict[reqGrpId]
                requestsDict[ (reqStdId, reqActId) ].granted = True
        else: 
            # Ako je vector[i] == 0 onda moramo napravit suprotno
            # Request nije više granted
            requestsDict[ (reqStdId, reqActId) ].granted = False
            # Trebamo ga vratiti u staru grupu
            studentsDict[ reqStdId ].activityGroupPair[ reqActId ] = studentsDictOrg[ reqStdId ].activityGroupPair[reqActId]
            # Smanjiti broj ljudi u grupi iz koje izlazi 
            groupsDict[reqGrpId].currentStudentCount -= 1
            # Povecati broj ljudi u orginalnoj grupi jer se u nju vraca
            groupsDict[ studentsDict[ reqStdId ].activityGroupPair[ reqActId ] ].currentStudentCount += 1


    # Timeout check
    end = time.time()
    if end - start > int(timeout):
        break

print(end - start)

def IsRequestValid(vector, i, reqStdId, reqActId, reqGrpId):
    # Provjera je li već dan request za taj activity 
    if not requestsDict[ (reqStdId, reqActId) ].granted:
        # Provjera za overlapping
        noOverlaps = True
        for key in studentsDict[ reqStdId ].activityGroupPair:  # groupIDevi u kojima je student valjda
            if key != reqActId: # Ignoriramo aktivnost za koju trenutno gledamo
                if reqGrpId in groupsDict[key].overlaps:
                    noOverlaps = False
                    break
        if noOverlaps:
            # Provjera za broj studenata
            # nađemo studenta sa id-jem i onda sa activity id-jem nađemo grupu u kojoj se on trenutno nalazi
            currGroup = groupsDict[ studentsDict[ reqStdId ].activityGroupPair[ reqActId ] ]
            requestedGroup = groupsDict[reqGrpId]
            if requestedGroup.currentStudentCount + 1 <= requestedGroup.max and currGroup.currentStudentCount - 1 >= currGroup.min:
                return True
    return False

