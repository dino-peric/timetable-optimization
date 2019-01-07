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

def Output(filename, studentsHeader, students, studentsDict):
    with open(filename, 'w') as f:
        f.write( studentsHeader[0] + ',' + studentsHeader[1] + ',' + studentsHeader[2] + ',' + studentsHeader[3] + ',' + studentsHeader[4] + '\n')
        for i in range(len(students)):
            #if students[i][3] != studentsDict[students[i][0]].activityGroupPair[students[i][1]]:
                #print (students[i][3], studentsDict[students[i][0]].activityGroupPair[students[i][1]] )
            f.write( students[i][0] + ',' + students[i][1] + ',' + students[i][2] + ',' + students[i][3] + ',' + studentsDict[students[i][0]].activityGroupPair[students[i][1]] + '\n' )

def IsRequestValid(reqStdId, reqActId, reqGrpId, requestsDict, groupsDict, studentsDict):
    # Provjera je li već dan request za taj activity 
    if not requestsDict[ (reqStdId, reqActId) ].granted:
        # Provjera za overlapping
        noOverlaps = True
        for key in studentsDict[ reqStdId ].activityGroupPair:  # groupIDevi u kojima je student valjda
            if key != reqActId: # Ignoriramo aktivnost za koju trenutno gledamo
                if reqGrpId in groupsDict[studentsDict[ reqStdId ].activityGroupPair[key]].overlaps:
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

def GrantRequest(arr, index, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict):
    arr[index] = 1
    # Povecaj broj ljudi u grupi u koju zeli ici
    groupsDict[reqGrpId].currentStudentCount += 1
    # Smanji broj ljudi u grupi iz koje izlazi
    groupsDict[ studentsDict[ reqStdId ].activityGroupPair[ reqActId ] ].currentStudentCount -= 1
    # Promijeni studentov raspored 
    studentsDict[ reqStdId ].activityGroupPair[ reqActId ] = groupsDict[reqGrpId].groupID
    studentsDict[ reqStdId ].numberOfRequestsGranted += 1
    requestsDict[ (reqStdId, reqActId) ].granted = True
    return arr

def RevokeRequest(arr, index, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict, studentsDictOrg): 
    # Micemo request znaci u vectoru mora biti 0
    arr[index] = 0
    # Micemo granted jer sad opet mozemo raditi zamjene za tog studenta za tu aktivnost
    requestsDict[ (reqStdId, reqActId) ].granted = False
    studentsDict[ reqStdId ].numberOfRequestsGranted -= 1
    # Trebamo ga vratiti u staru grupu
    studentsDict[ reqStdId ].activityGroupPair[ reqActId ] = studentsDictOrg[ reqStdId ].activityGroupPair[reqActId]
    # Smanjiti broj ljudi u grupi iz koje izlazi 
    groupsDict[reqGrpId].currentStudentCount -= 1
    # Povecati broj ljudi u orginalnoj grupi jer se u nju vraca, grupu smo zamijenili 2 linije gore
    groupsDict[ studentsDict[ reqStdId ].activityGroupPair[ reqActId ] ].currentStudentCount += 1
    return arr       

def GenerateNeighbours(vec, requests, requestsDict, groupsDict, studentsDict, studentsDictOrg, limits, award_activity, award_student, minmax_penalty):
    indices = random.sample(range(0, len(vec)), int(len(vec)))
    neighbours = []
    bestScore = -10000
    for i in indices:
        reqStdId = requests[i][0] # studentId in request
        reqActId = requests[i][1] # activityId in request
        reqGrpId = requests[i][2] # groupId in request
        neighbour = vec[:]
        if (neighbour[i] == 0):  # Zelimo flipat taj bit pa idemo vidit jel moze taj request proć         
            if IsRequestValid(reqStdId, reqActId, reqGrpId, requestsDict, groupsDict, studentsDict): # Request može proć
                #print("give me my nigga")
                #neighbour = GrantRequest(neighbour, i, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict)
                neighbours.append((neighbour, i))
        else: # neighbour[i] = 1 zelimo oduzet taj request
            #print("take my nigga away")
            #neighbour = RevokeRequest(neighbour, i, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict, studentsDictOrg)
            neighbours.append((neighbour, i))
    
    scores = []
    for neighbour in neighbours: 
        currentScore = Score( neighbour[0][:], studentsDict, groupsDict, requests, limits, award_activity, award_student, minmax_penalty )
        if currentScore >= bestScore:
            scores.append( currentScore )

    if len(scores) > 0:
        print(max(scores))
    bestScore = max(scores)
    bestNeigbourIndex = scores.index( bestScore )
    bestNeighbour = neighbours[ bestNeigbourIndex ][0][:]

    if (bestNeighbour[i] == 0):  # Zelimo flipat taj bit pa idemo vidit jel moze taj request proć         
        if IsRequestValid(reqStdId, reqActId, reqGrpId, requestsDict, groupsDict, studentsDict): # Request može proć
        #print("give me my nigga")
            bestNeighbour = GrantRequest(bestNeighbour, i, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict)
    else: # neighbour[i] = 1 zelimo oduzet taj request
        #print("take my nigga away")
        bestNeighbour = RevokeRequest(bestNeighbour, i, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict, studentsDictOrg)

    return bestNeighbour



def Score(vec, studentsDict, groupsDict, requests, limits, award_activity, award_student, minmax_penalty):
    score = 0
    scoreA = scoreB = scoreC = scoreD = scoreE = 0  
    for i in range(len(vec)):
        if vec[i] == 1: # Only granted requests 
            # Score A
            scoreA += studentsDict[requests[i][0]].weight
            # Score B
            if studentsDict[ requests[i][0] ].numberOfRequestsGranted - 1 >= len(award_activity):
                scoreB += int(award_activity[-1])
            elif studentsDict[ requests[i][0] ].numberOfRequestsGranted - 1 > 0:
                scoreB += int(award_activity[ studentsDict[ requests[i][0] ].numberOfRequestsGranted - 1 ])      
            # Score C
            if studentsDict[ requests[i][0] ].numberOfRequestsGranted == studentsDict[ requests[i][0] ].numberOfRequests:
               scoreC += 1  
            '''
            # Score D OVAJ DIO SE VALJDA NE MOZE OVDJE NEGO SE TREBA ZA SVE GRUPE IZRAČUNATI :'(
            if groupsDict[ requests[i][2] ].currentStudentCount < groupsDict[ requests[i][2] ].minPref:
                scoreD += (groupsDict[ requests[i][2] ].minPref - groupsDict[ requests[i][2] ].currentStudentCount) * minmax_penalty
            # Score E
            if groupsDict[ requests[i][2] ].currentStudentCount > groupsDict[ requests[i][2] ].maxPref:
                scoreE += (groupsDict[ requests[i][2] ].currentStudentCount - groupsDict[ requests[i][2] ].maxPref) * minmax_penalty
            '''
            
    for key in groupsDict: # Loop through all groups :'(
        # Score D
        if groupsDict[key].currentStudentCount < groupsDict[key].minPref:
            scoreD += (groupsDict[key].minPref - groupsDict[key].currentStudentCount) * minmax_penalty
        # Score E
        if groupsDict[key].currentStudentCount > groupsDict[key].maxPref:
            scoreE += (groupsDict[key].currentStudentCount - groupsDict[key].maxPref) * minmax_penalty
    
    score = scoreA + scoreB + scoreC - scoreD - scoreE
    return score

def ReturnBestNeighbour(vec, requests, requestsDict, groupsDict, studentsDict, studentsDictOrg, limits, award_activity, award_student, minmax_penalty):
    neighbours = GenerateNeighbours(vec, requests, requestsDict, groupsDict, studentsDict, studentsDictOrg)



class Student:
    def __init__(self, studentID):
        self.studentID = studentID
        self.weight = 0
        # Dictionary where key = activityID, value = groupID of that student
        # This is basically the timetable of the student 
        self.activityGroupPair = {}
        self.numberOfRequests = 0 # Total number of requests
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


