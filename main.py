import numpy as np
from helpers import *

students, studentsHeader = ReadFileArray('student.csv')
requests, requestsHeader = ReadFileArray('requests.csv')
limits, limitsHeader = ReadFileArray('limits.csv')
overlaps, overlapsHeader = ReadFileArray('overlaps.csv')

# Remove elements from requests that are in requests but not in students
requests = RemoveDifferentElements(requests, students)








