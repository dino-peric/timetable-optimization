import numpy as np
from helpers import *
import argparse, sys
import time 
from collections import deque

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-timeout', help='How long the program will run for')
parser.add_argument('-award-activity', help='Array of awards')
parser.add_argument('-award-student', help='Award for doing all swaps of a student')
parser.add_argument('-minmax-penalty', help='Amount of points deducted for being outside pref values')
parser.add_argument('-students-file', help='Students file')
parser.add_argument('-requests-file', help='Requests file')
parser.add_argument('-overlaps-file', help='Overlaps file')
parser.add_argument('-limits-file', help='Limits file')

args = parser.parse_args()

timeout        = args.timeout                   # Time for which the program will run
award_activity = args.award_activity.split(',') # Array of awards
award_student  = int(args.award_student)        # Award for doing all swaps of a single student
minmax_penalty = int(args.minmax_penalty)       # Penalty for each student in each group that has a number of students not between minpref and maxpref
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

# TODO Datoteka overlaps može sadržavati i podatke o grupama koje se ne nalaze u  
#      ulaznoj datoteci students-file pa se ti podaci mogu slobodno zanemariti.
#      znaci treba proc kroz overlaps i uzet samo one groupIDeve koji se nalaze u groupID polju u
#      students-file, ovo treba napraviti prije uniqueGroups poziva ili cak unutar njega, 
#      a mozda i ne moramo uopce ne znam utjece li na performans, ovaj TODO je za kasnije nakon implementacije algoritma, ili mozda nikada :^)

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
            activsGroups[students[j][1]] = students[j][3]                    # Get all activity -> group pairs of a student and put it in activsGroups dict
            weight = students[j][2]
    newStudent.activityGroupPair = activsGroups
    newStudent.weight = int(weight)      
    studentsDict[uniqueStudents[i]] = newStudent

studentsDictOrg = studentsDict.copy()
studentsDictFinal = studentsDict.copy()

groupsDict = {}                                                              # Dictionary where key = groupId, value = Group object
for i in range(len(limits)):
    groupsDict[limits[i][0]] = Group(limits[i][0])
    groupsDict[limits[i][0]].initStudentsCount = int(limits[i][1])
    groupsDict[limits[i][0]].currentStudentCount = int(limits[i][1])            
    groupsDict[limits[i][0]].minCount = int(limits[i][2])
    groupsDict[limits[i][0]].minPref = int(limits[i][3])
    groupsDict[limits[i][0]].max = int(limits[i][4])
    groupsDict[limits[i][0]].maxPref = int(limits[i][5])

for key in groupsDict:
    overlapsWith = []
    for j in range(len(overlaps)):                                           # Add all overlaps for groups
        if key == overlaps[j][0]:                                            # No need for overlaps file from this point
            overlapsWith.append(overlaps[j][1])
    groupsDict[key].overlaps = overlapsWith


reqFromOneStudent = set()                                                    # Get all requests grouped by students
for i in range(len(requests)):
    reqFromOneStudent.add((requests[i][0], requests[i][1]))
reqFromOneStudent = list(reqFromOneStudent)


requestsDict = {}                                                            # Dictionary where key = (studentId, activityId), value = Request object
for i in range(len(reqFromOneStudent)):
    newRequest = Request( reqFromOneStudent[i] )
    requestedGroups = []
    for j in range(len(requests)):
        if requests[j][0] == reqFromOneStudent[i][0] and requests[j][1] == reqFromOneStudent[i][1]:
            requestedGroups.append(requests[j][2])
    newRequest.requestedGroups = requestedGroups      
    requestsDict[ ( reqFromOneStudent[i][0], reqFromOneStudent[i][1] )] = newRequest

# Number of requests for each student, but counting only requests for different activities ==> FOR SCORE C
for keyStd in studentsDict:
    for keyReq in requestsDict:
        if keyStd in keyReq:
            studentsDict[keyStd].numberOfRequests += 1

studentsDictOrg = studentsDict.copy()
bestStudentsDict = studentsDict.copy()

# Initial solution
vector = [0] * len(requests)
indices = random.sample(range(0, len(vector)), int(len(vector)/2))
for i in indices: 
    reqStdId = requests[i][0] # studentId in request
    reqActId = requests[i][1] # activityId in request
    reqGrpId = requests[i][2] # groupId in request
    if IsRequestValid(reqStdId, reqActId, reqGrpId, requestsDict, groupsDict, studentsDict):
        # Moze se napravit zamjena -> napravimo ju
        vector[i] = 1
        GrantRequest(vector, i, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict)
        #vector = RevokeRequest(vector, i, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict, studentsDictOrg)

overallBestScore = Score(vector, studentsDict, groupsDict, requests, limits, award_activity, award_student, minmax_penalty)
overallBestSolution = vector[:]


bestNeighbour = vector[:]
counter = 0

queue = deque()
queue.clear()
start = time.time()
iterations = 0
# Main loop
while True:
    #bestNeighbour, overallBestScore, bestStudentsDict, queue = GenerateNeighbours(bestNeighbour, overallBestScore, bestStudentsDict, requests, requestsDict, groupsDict, studentsDict, studentsDictOrg, limits, award_activity, award_student, minmax_penalty,queue) 
    neighbours, scores = GenNeighboursAndScores(bestNeighbour, requests, requestsDict, groupsDict, studentsDict, studentsDictOrg, limits, award_activity, award_student, minmax_penalty, queue)
    bestNeighbour, overallBestScore, bestStudentsDict, queue = GetBestNeighbour(neighbours, scores, overallBestScore, bestStudentsDict, requests, requestsDict, groupsDict, studentsDict, studentsDictOrg, queue)
    
    # Timeout check
    end = time.time()
    if end - start > int(timeout):
        break
    iterations += 1

print(overallBestScore, iterations)

# output to file
Output('results/student' + str(int(end - start)) + '.csv', studentsHeader, students, bestStudentsDict)
#Output('student.csv', studentsHeader, students, bestStudentsDict)

print(end - start)

'''
with open("results/sample4results.txt", 'a') as f:
    f.write("\nSample 4\n")
    f.write("Award activity: " + str(award_activity) + "\n")
    f.write("Award student: " + str(award_student) + "\n")
    f.write("Minmax penalty: " + str(minmax_penalty) + "\n")
    f.write("Iterations: " + str(iterations) + "\n")
    f.write("Time elapsed: " + str(end - start) + "\n")
    f.write("Best score: " + str(overallBestScore) + "\n")
    f.write("Number of requests given: " + str(bestNeighbour.count(1)) + "\n")
    f.write("\n")
'''
