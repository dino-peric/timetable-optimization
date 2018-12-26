import numpy as np
from helpers import *
import time 

students, studentsHeader = ReadFileArray('student.csv')
requests, requestsHeader = ReadFileArray('requests.csv')

limits, limitsHeader = ReadFileArray('limits.csv')
overlaps, overlapsHeader = ReadFileArray('overlaps.csv')

# Remove elements from requests that are in requests but not in students
requests = RemoveDifferentElements(requests, students)

start = time.time()
groupsDict = {}

# Get all unique groups in a list
uniqueGroups = set()
for i in range(len(overlaps)):
    #overlapsWith = []
    #if(overlaps[i][0] not in uniqueGroups):
    #    for j in range(len(overlaps)):
    #        if overlaps[i][0] == overlaps[j][0]:
    #            overlapsWith.append(overlaps[j][1])
    #        groupsDict[overlaps[i][0]] = overlapsWith  
    uniqueGroups.add(overlaps[i][0])
uniqueGroups = list(uniqueGroups)

print(len(uniqueGroups))

# Dictionary where key = groupId 
#                  value = array of groupIds that this one overlaps with
for i in range(len(uniqueGroups)):
    overlapsWith = []
    for j in range(len(overlaps)):
        if uniqueGroups[i] == overlaps[j][0]:
            overlapsWith.append(overlaps[j][1])
    groupsDict[uniqueGroups[i]] = overlapsWith

#print(len(groupsDict))
#print(groupsDict['140915'])

end = time.time()
print(end - start)

# for each binary element check if: no group overlap, minmax satisfied and no swap in that activity (?)
# 1) Look if swapping is possible ie check if group overlaps with another
# 2) Check if it is possible to add/take away students from this group 
# 3) Some butko shit that I don't understand








