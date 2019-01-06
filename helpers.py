import os
import random 
from collections import Counter

# Returns file as array, returns file without header + header
def ReadFileArray(filename):
    with open(filename, 'r') as f:
        lines = f.read().splitlines()
    arr = []
    for line in lines:
         arr.append( line.split(',') )
    header = arr[0]
    arr.pop(0)
    return arr, header

# Remove elements from a that are in a but not in b
def RemoveDifferentElements(a, b):
    indices = []
    # Get indices of elements in a that are not in b
    for i in range(len(a)):
        toRemove = True
        for j in range(len(b)):
            if a[i][0] == b[j][0] and a[i][1] == b[j][1]:
                toRemove = False
        if toRemove:
            indices.append([a[i][0], a[i][1]])

    # Remove elements from a
    for i in range(len(indices)):
        for j in range(len(a)):
            if a[j][0] == indices[i][0] and a[j][1] == indices[i][1]:
                a.pop(j)
                break
    return a


def Score(studentsDict , requests , vec, award_activity,award_student):
    #Rješenja koja nisu prihvatljiva imaju ukupnu ocjenu 0. 
    score = 0
    scoreA = scoreB = scoreC = scoreD = scoreE = 0
    scoraA = 0
    #TODO
    __DEBUG__ = 0
    
    #Score A
    for a in range(0,len(vec)):
        if vec[a]==1:
            stID = requests[a][0]
            acID = requests[a][1]
            #for i in range (0,len(students)):
                #if (students[i][0] == stID and students[i][1] == acID):
            scoreA += studentsDict[stID].weight
    if __DEBUG__:
        print("Score A " , scoreA)

    #Score B
    ### DINO SCORE B ###
    for i in range(len(vec)):
        if vec[i] == 1:
            if studentsDict[ requests[i][0] ].numberOfRequestsGranted - 1 > len(award_activity):
                scoreB += int(award_activity[-1])
            else:
                scoreB += int(award_activity[studentsDict[ requests[i][0] ].numberOfRequestsGranted])
    ### DINO SCORE B ###

    swapMade = []
    swapMadePerStudent = []
    for b in range(0,len(vec)):
        if vec[b] == 1:
            swapMade.append(requests[b][0])

    temp = list(set(swapMade))
    for i in range(0,len(temp)):
        numPerSt = swapMade.count(temp[i])
        if numPerSt-1 > len(award_activity):
            scoreB += int(award_activity[-1])
        else:
            scoreB += int(award_activity[numPerSt-1])

    if __DEBUG__:
        print("Score B " , scoreB)

    #Score C
    numberOfRequestsForStudentDone = []
    numberOfRequestsForStudentGiven = []
    allRequests = []
    allRequestsAc = []
    resultList = []
    numberOfRequestsForStudentDoneInActivity = []
    numberOfRequestsForStudentGivenInActivity = []

    #Svi zahtijevi
    for c in range(0,len(requests)):
        allRequests.append(requests[c][0])
        allRequestsAc.append(requests[c][1])
    
    #Liste napravljenih zahtijeva i svih zahtijeva od svakog studenta kojem je napravljena barem jedna zamjena
    #print(swapMade)
    #print(allRequests)
    for c in range(0,len(temp)):
        #for i in range(0,len())
        numberOfRequestsForStudentDone.append(swapMade.count(temp[c]))
        numberOfRequestsForStudentGiven.append(allRequests.count(temp[c]))
    
    for i in range (0,len(temp)):
        tmp = []
        for c in range(0,len(requests)):
            if temp[i] == requests[c][0]:
                tmp.append(requests[c][1])
        numberOfRequestsForStudentGivenInActivity.append(len(list(set(tmp))))
    numberOfRequestsForStudentDoneInActivity = numberOfRequestsForStudentDone

    #Provjera rezultata
    if __DEBUG__:
        print(numberOfRequestsForStudentDone)
        print(numberOfRequestsForStudentGiven)
        print(numberOfRequestsForStudentDoneInActivity)
        print(numberOfRequestsForStudentGivenInActivity)
    for c in range(0,len(temp)):
        if numberOfRequestsForStudentDoneInActivity[c] == numberOfRequestsForStudentGivenInActivity[c]:
            scoreC += 1
    
    scoreC = scoreC * int(award_student)
    #for c in range(0,len(temp)):
    #    resultList.append(numberOfRequestsForStudentDone[c] - numberOfRequestsForStudentGiven[c])
    #Provjera broja aktivnosti
    if __DEBUG__:
        print(scoreC)
    


    score = scoreA + scoreB + scoreC + scoreD + scoreE
    return score

#class Activity: 
#    def __init__(self, activityID):
#        self.activityID = activityID
#        self.groups = []

class Student:
    #def __init__(self, studentID):
    def __init__(self, studentID):
        self.studentID = studentID
        self.weight = 0
        # Dictionary where key = activityID, value = groupID of that student
        # This is basically the timetable of the student 
        self.activityGroupPair = {}
        self.numberOfRequests = 0
        self.numberOfRequestsGranted = 0

class Group:
    def __init__(self, groupID):
        self.groupID = groupID
        # Should contain all groups that this group overlaps with
        self.overlaps = []
        self.initStudentsCount = 0
        self.currentStudentCount = 0
        self.min = 0  
        self.minPref = 0 
        self.max = 0 
        self.maxPref = 0

# TODO figure this out 
class Request:
    def __init__(self, requestID):
        self.requestID = requestID
        self.requestedGroups = []
        self.reqGroupId = 0
        self.granted = False
