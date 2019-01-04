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

def GenerateNeighbours(vec):
    indices = random.sample(range(0, len(vec)), int(len(vec)/3))

    neighbours = []
    for i in indices:

        neighbour = []
        for j in range(0,len(vec)):
            neighbour.append(vec[j])

        if (neighbour[i] == 0):
            neighbour[i] = 1
        else:
            neighbour[i] = 0
        neighbours.append(neighbour)
        
    return neighbours

def Score(students,vec):
    #Rješenja koja nisu prihvatljiva imaju ukupnu ocjenu 0. 
    score = 0
    scoreA = scoreB = scoreC = scoreD = scoreE = 0
    #TODO
    #for a in range(0,len(students)):
    #    if students[a][2]==vec[a]:
    #        scoreA += students[a][2]
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
        self.minCount = 0  
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