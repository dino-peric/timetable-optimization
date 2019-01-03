import os

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
        self.studentID = 0 
        self.reqGroupId = 0
        self.granted = False