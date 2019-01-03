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
#      a mozda i ne moramo uopce ne znam utjece li na performans, ovaj TODO je za kasnije

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

print(studentsDict['15317'].activityGroupPair)

# Get all unique groups from overlaps file
uniqueGroups = set()
for i in range(len(overlaps)):
    uniqueGroups.add(overlaps[i][0])
uniqueGroups = list(uniqueGroups)

groupsDict = {} # Dictionary where key = groupId, value = Group object
for i in range(len(uniqueGroups)):
    overlapsWith = []
    newGroup = Group(uniqueGroups[i])
    for j in range(len(overlaps)):                      # Add all overlaps for groups
        if uniqueGroups[i] == overlaps[j][0]:           # No need for overlaps file from this point
            overlapsWith.append(overlaps[j][1])
    groupsDict[uniqueGroups[i]] = newGroup
    groupsDict[uniqueGroups[i]].overlaps = overlapsWith
    for k in range(len(limits)):                        # Add all limits for groups
        if limits[k][0] == uniqueGroups[i]:                         # No need for limits file from this point
            groupsDict[uniqueGroups[i]].initStudentsCount = limits[k][1]
            groupsDict[uniqueGroups[i]].minCount = limits[k][2]
            groupsDict[uniqueGroups[i]].minPref = limits[k][3]
            groupsDict[uniqueGroups[i]].max = limits[k][4]
            groupsDict[uniqueGroups[i]].maxPref = limits[k][5]

print(len(groupsDict))
print(groupsDict['140915'].initStudentsCount)

# AKTIVNOST = PREDMET npr. NASP 
# GRUPA     = UCIONA  npr. B4, B2 
# znaci jedna aktivnost ima vise grupa, student moze biti samo u jednoj grupi 

# TODO for each binary element check if: no group overlap, minmax satisfied and no swap in that activity (?)
# TODO 1) Look if swapping is possible ie check if group overlaps with another (use overlaps field in Group)
# TODO 2) Check if it is possible to add/take away students from this group (use all other fields in Group)
# TODO 3) Some butko shit that I don't understand

# Main loop
while True:

    end = time.time()
    if end - start > int(timeout):
        break

print(end - start)




