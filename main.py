import numpy as np
from helpers import *
import time 

students, studentsHeader = ReadFileArray('student.csv')
requests, requestsHeader = ReadFileArray('requests.csv')

limits, limitsHeader     = ReadFileArray('limits.csv')     # limits i overlaps je kombinirano u dictionaryu
overlaps, overlapsHeader = ReadFileArray('overlaps.csv')   # groupsDict koji sadrži Group objekte

# Remove elements from requests that are in requests but not in students
requests = RemoveDifferentElements(requests, students)

start = time.time()

# TODO Datoteka overlaps može sadržavati i podatke o grupama koje se ne nalaze u  
#      ulaznoj datoteci students-file pa se ti podaci mogu slobodno zanemariti.
#      znaci treba proc kroz overlaps i uzet samo one groupIDeve koji se nalaze u groupID polju u
#      students-file, ovo treba napraviti prije uniqueGroups poziva ili cak unutar njega

# Get all unique groups from overlaps file
uniqueGroups = set()
for i in range(len(overlaps)):
    uniqueGroups.add(overlaps[i][0])
uniqueGroups = list(uniqueGroups)


# Dictionary where key = groupId
#                  value = Group object
groupsDict = {}
for i in range(len(uniqueGroups)):
    overlapsWith = []
    newGroup = Group(uniqueGroups[i])
    for j in range(len(overlaps)):                      # Add all overlaps for groups
        if uniqueGroups[i] == overlaps[j][0]:           # No need for overlaps file from this point
            overlapsWith.append(overlaps[j][1])
    groupsDict[uniqueGroups[i]] = newGroup
    groupsDict[uniqueGroups[i]].overlaps = overlapsWith

for key in groupsDict:
    for j in range(len(limits)):                        # Add all limits for groups
        if limits[j][0] == key:                         # No need for limits file from this point
            groupsDict[key].studentsCount = limits[j][1]
            groupsDict[key].minCount = limits[j][2]
            groupsDict[key].minPref = limits[j][3]
            groupsDict[key].max = limits[j][4]
            groupsDict[key].maxPref = limits[j][5]

print(len(groupsDict))
print(groupsDict['140915'].studentsCount)

end = time.time()
print(end - start)

# AKTIVNOST = PREDMET npr. NASP 
# GRUPA     = UCIONA  npr. B4, B2 
# znaci jedna aktivnost ima vise grupa, student moze biti samo u jednoj grupi 

# TODO for each binary element check if: no group overlap, minmax satisfied and no swap in that activity (?)
# TODO 1) Look if swapping is possible ie check if group overlaps with another (use overlaps field in Group)
# TODO 2) Check if it is possible to add/take away students from this group (use all other fields in Group)
# TODO 3) Some butko shit that I don't understand








