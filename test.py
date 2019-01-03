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