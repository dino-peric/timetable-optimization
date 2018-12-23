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