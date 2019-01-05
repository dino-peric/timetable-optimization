import os
import random 

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


def Score(students , requests , vec):
    #Rješenja koja nisu prihvatljiva imaju ukupnu ocjenu 0. 
    score = 0
    scoreA = scoreB = scoreC = scoreD = scoreE = 0
    scoraA = 0
    #TODO
    
    for a in range(0,len(vec)):
        if vec[a]==1:
            stID = requests[a][0]
            acID = requests[a][1]
            for i in range (0,len(students)):
                if (students[i][0] == stID and students[i][1] == acID):
                	scoreA += int(students[i][2])
    print("Score A " , scoreA)
    
    return score

#class Activity: 
#    def __init__(self, activityID):
#        self.activityID = activityID
#        self.groups = []

class Student:
    def __init__(self, studentID):
        self.studentID = studentID
        # Dictionary where key = activityID, value = groupID of that student
        # This is basically the timetable of the student 
        self.activityGroupPair = {}

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