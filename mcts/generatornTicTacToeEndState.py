
def generatorTictacToeEndState(boardSize=3):
    # Each row state for end
    rows = []
    for r in range(boardSize):
        row = ()
        for c in range(boardSize):
            row = row + (r*boardSize+c,)
        rows.append(row)

    # Each column state for end
    for c in range(boardSize):
        col = ()
        for r in range(boardSize):
            col = col + (r*boardSize+c,)
        rows.append(col)


    # Two diagonal states for end
    col = ()
    for c in range(boardSize):
        col = col+((boardSize+1)*c,)
    rows.append(col)

    col = ()
    for c in range(boardSize):
        col = col + ((boardSize-1)*(c+1),)
    rows.append(col)

    return rows

if __name__ == "__main__":    
    print(generatorTictacToeEndState(5))