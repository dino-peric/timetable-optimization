import random 


scores = [1, 2, 3, 5, 4]
bestNeighbourIndex = scores.index( max(scores) )
print(bestNeighbourIndex)

# '''int(len(vec)/3)'''
neighbours = []
for i in range(10):
    reqStdId = requests[i][0] # studentId in request
    reqActId = requests[i][1] # activityId in request
    reqGrpId = requests[i][2] # groupId in request
    neighbour = vec[:]
    if (neighbour[i] == 0):  # Zelimo flipat taj bit pa idemo vidit jel moze taj request proć         
        if IsRequestValid(reqStdId, reqActId, reqGrpId, requestsDict, groupsDict, studentsDict): # Request može proć
            #print("give me my nigga")
            neighbour = GrantRequest(neighbour, i, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict)
            neighbours.append(neighbour)
    else: # neighbour[i] = 1 zelimo oduzet taj request
        #print("take my nigga away")
        neighbour = RevokeRequest(neighbour, i, reqStdId, reqGrpId, reqActId, requestsDict, groupsDict, studentsDict, studentsDictOrg)
        neighbours.append(neighbour)

print(neighbours)



'''
import argparse, sys

parser = argparse.ArgumentParser()

parser.add_argument('--timeout', help='How long the program will run for')
parser.add_argument('--award_activity', help='Array of awards')
parser.add_argument('--award_student', help='Award for doing all swaps of a student')
parser.add_argument('--minmax_penalty', help='Amount of points deducted for being outside pref values')
parser.add_argument('--students_file', help='Students file')
parser.add_argument('--requests_file', help='Requests file')
parser.add_argument('--overlaps_file', help='Overlaps file')
parser.add_argument('--limits_file', help='Limits file')
args = parser.parse_args()

print (args.timeout)
print (args.award_activity)
print (args.award_student)
print (args.minmax_penalty)
print (args.students_file)
print (args.requests_file)
print (args.overlaps_file)
print (args.limits_file)
'''

'''
for key in groupsDict:
    for j in range(len(limits)):                        # Add all limits for groups
        if limits[j][0] == key:                         # No need for limits file from this point
            groupsDict[key].initStudentsCount = limits[j][1]
            groupsDict[key].minCount = limits[j][2]
            groupsDict[key].minPref = limits[j][3]
            groupsDict[key].max = limits[j][4]
            groupsDict[key].maxPref = limits[j][5]
'''



'''
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
                vector[i] = 0 # Request se ne moze napravit, tako da neka bude 0
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
    '''