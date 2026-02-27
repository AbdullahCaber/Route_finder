from sys import argv
def cost(inpLine): #function that returns us the a cost dictionary with the given costs in the input
    costValues = inpLine.strip().split()
    return {'Cost1': int(costValues[0]),'Cost2': int(costValues[1]),'Cost3': int(costValues[2])}
def findField(inpLines): #function that returns the field as a list
    fieldList = []
    for line in inpLines:
        fieldList.extend(map(int, line.strip().split()))
    return fieldList
def findNeigh(index, lengthRow, totalCells): #function that finds the neighbors of the given index
    neighbors = []
    row, column = divmod(index, lengthRow)
    directions = [(0, 1), (-1, 0), (1, 0), (0, -1)]
    for x,y in directions:
        newRow = row + x
        newColumn = column + y
        if 0 <= newRow < (totalCells // lengthRow) and 0 <= newColumn < lengthRow:
            neighbors.append(newRow * lengthRow + newColumn)
    return neighbors
def calculateCost(field, lengthRow, costs): #function that calculates the cost of each cell by looking its neighbors
    totalCells = len(field)
    costDict = {}
    for index in range(totalCells):
        if field[index] == 0:
            costDict[index] = None
            continue
        neighbors = findNeigh(index, lengthRow, totalCells)
        nexttoZero = False
        for n in neighbors:
            if field[n] == 0:
                nexttoZero = True
                break
        diagonalZero = False
        diagonals = [index - lengthRow - 1, index - lengthRow + 1, index + lengthRow - 1, index + lengthRow + 1]
        for n in diagonals:
            if 0 <= n < totalCells and field[n] == 0:
                diagonalZero = True
                break
        if nexttoZero:
            costDict[index] = costs['Cost3']
        elif diagonalZero:
            costDict[index] = costs['Cost2']
        else:
            costDict[index] = costs['Cost1']
    return costDict
def findPath(field, lengthRow, costs): #function that returns all the possible paths and their costs
    totalRows = len(field) // lengthRow
    totalCells = len(field)
    paths = []
    database = {}
    def tracePathndCost(index, path, curCost, curMinCost): #function that where the recursion occurs
        if curCost >= curMinCost:                          #finds all the possible paths and their costs
            return curMinCost
        if index % lengthRow == lengthRow - 1:
            paths.append((path.copy(), curCost))
            return min(curCost, curMinCost)
        visitedPath = (index, tuple(path))
        if visitedPath in database and database[visitedPath] <= curCost:
            return curMinCost
        database[visitedPath] = curCost
        for neighbor in findNeigh(index, lengthRow, totalCells):
            if field[neighbor] == 1 and neighbor not in path:
                newCost = curCost + costs.get(neighbor, 0)
                path.append(neighbor)
                curMinCost = tracePathndCost(neighbor, path, newCost, curMinCost)
                path.pop()
        return curMinCost
    curMinCost = float('inf')
    for row in range(totalRows):
        startIndex = row * lengthRow
        if field[startIndex] == 1:
            curMinCost = tracePathndCost(startIndex, [startIndex], costs.get(startIndex, 0), curMinCost)
    return paths
def findCheapestPath(paths): #function that returns the cheapest path
    if not paths:
        return None, None
    cheapestPath = min(paths, key=lambda x: x[1])
    return cheapestPath
def writePath(field, lengthRow, cheapestPath, outFile): #function that writes us the output
    if not cheapestPath or not cheapestPath[0]:
        outFile.write("There is no possible route!")
        return
    path, cost = cheapestPath
    copiedField = field[:]
    for index in path:
        copiedField[index] = 'X'
    outFile.write(f"Cost of the route: {cost}")
    for i in range(0, len(copiedField), lengthRow):
        outFile.write('\n' + ' '.join(map(str, copiedField[i:i + lengthRow])))
def main():
    inpFile = argv[1]
    outFile = argv[2]
    with open(inpFile, 'r') as file:
        lines = file.readlines()
    costs = cost(lines[0])
    field = findField(lines[1:])
    lengthRow = len(lines[1].strip().split())
    calcCosts = calculateCost(field, lengthRow, costs)
    paths = findPath(field, lengthRow, calcCosts)
    cheapestPath = findCheapestPath(paths)
    with open(outFile, 'w') as file:
        writePath(field, lengthRow, cheapestPath, file)
if __name__ == "__main__":
    main()
