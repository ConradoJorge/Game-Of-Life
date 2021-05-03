#Game of Life application which in it's current implementation only supports Windows OS

import random
import os
import time
import msvcrt

MAX_ROW = 40
MAX_COL = 80


#displayMenu function displays the menu which appears at the top of the screen
# and instructs the user on the actions available to them.
def displayMenu():
    print("[P]lay - Press 'P' to play.")
    print("[Q]uit - Press 'Q' to exit.")
    print()
    print("[C]lear - Press 'C' to clear.                   [1] - Press '1' to load the 'Heart' pattern.")
    print("[S]ave - Press 'S' to save.                     [2] - Press '2' to load the 'Diamond' pattern.")
    print("[L]oad - Press 'L' to save.                     [3] - Press '3' to load the 'Smiley' pattern.")
    print("[M]anual - Press 'M' to create a pattern.       [U] - Press 'U' to load the 'U' pattern.")
    print()

#setZeroList resets all values in the array to equal 0.
def setZeroList(zeroList):
    for height in range(MAX_ROW):
        for width in range(MAX_COL):
            zeroList[height][width] = "O"

#creates a U shaped pattern which has no reliance on a .txt file to load the pattern.
def setInitialPatternList(Pattern):
    setZeroList(Pattern)
    rowPattern = random.randint(0,MAX_ROW-6)
    columnPattern = random.randint(0,MAX_COL-7)
    for rows in range (6):
        for columns in range(7):
            if (columns == 0 or columns == 6) or (rows == 5 and (columns > 0 and columns < 6)):
                Pattern[rowPattern + rows][columnPattern + columns] = "*"

#copys the values of one list to another.
def copyList(temp, current):
        for row in range(MAX_ROW):
            for col in range(MAX_COL):
                current[row][col] = temp[row][col]

#prints the array passed in via argument to the display.
def displayList(list):
    for row in range(MAX_ROW):
        for col in range(MAX_COL):
            if (col == (MAX_COL - 1)):
                print(list[row][col], end = "\n")
            else:
                print(list[row][col], end = "")

#submenu which appears above the game while it runs instructing the user to halt
def displaySubMenu():
    print("[H]alt - Press 'H' to halt.")

#determines which cells live and die by checking the cells around each item
def setNextGenList(temp, current):
    copyList(current, temp)
    modifiers = [-1, 0, 1]
    for height in range(MAX_ROW):
        for width in range(MAX_COL):
            count = 0
            for row in modifiers:
                for col in modifiers:
                    if row == 0 and col == 0:
                        continue
                    if (height+row < 0) or (height + row >= MAX_ROW) or (width+col < 0) or (width + col >= MAX_COL):
                        continue
                    if (current[height+row][width+col] == "*"):
                        count += 1
            if current[height][width] == "O":
                if count == 3:
                    temp[height][width] = "*"
            else:
                if count < 2:
                    temp[height][width] = "O"
                elif count > 3:
                    temp[height][width] = "O"

#Allows loading from preset files
def LoadPattern(FilePattern, ArrayPattern):
    rowPattern = random.randint(0,MAX_ROW-7)
    columnPattern = random.randint(0,MAX_COL-7)
    setZeroList(ArrayPattern)
    if (FilePattern == 1):
        pattern = open("pattern1.txt", "r")
    if (FilePattern == 2):
        pattern = open("pattern2.txt", "r")
    if (FilePattern == 3):
        pattern = open("pattern3.txt", "r")
    for line in pattern:
        line = line.rstrip()
        coordinates = line.split()
        ArrayPattern[rowPattern + int(coordinates[0])][columnPattern + int(coordinates[1])] = "*"

#Allows the user to save a file to a user-specified file name
def SaveArray(ArrayPattern):
    print("Please enter the file name you with to save it as (file extention:.txt:)")
    usersave = input(">")
    userfile = open(usersave, 'w')

    for row in range(MAX_ROW):
        for col in range(MAX_COL):
            if ArrayPattern[row][col] == "*":
                concatr = str(row) + ' ' + str(col) + '\n'
                userfile.write(concatr)
    userfile.close()

#Allows the user to load a saved file by entering the file name
def LoadArray(ArrayPattern):
    print("Please enter the file name you wish to load (file extention:.txt):")
    userload = input(">")
    try:
        userfile = open(userload)
    except:
        print("File not found!")
        input("Press enter to continue...")
        return

    for line in userfile:
        line = line.rstrip()
        coordinates = line.split()
        ArrayPattern[int(coordinates[0])][int(coordinates[1])] = "*"

#allows the user to manually enter in the coordinates of cells they'd like to insert a live cell.
def Manual(ArrayPattern):
    os.system("cls")
    print ("Enter the row and column numbers.")
    print ("Row should be between 0 and", MAX_ROW-1, ". Column should be betweeen 0 and", MAX_COL-1)
    print ("Repeat until you are done with your input. When done, enter -99 and press return.")
    print ()

    count = 1

    while (True):
        print("Row    #", count, end = '>>')
        number = input()
        row = int(number)
        if ((row >= MAX_ROW or row < 0) and row != -99):
            print("Please enter a number between 0 to", MAX_ROW-1)
            continue
        elif(row == -99):
            break
        else:
            while (True):
                print("Column #", count, end =  ">>")
                number = input()
                col = int(number)
                if (col >= MAX_COL or col < 0):
                    print("Please enter a number between 0 to", MAX_COL-1)
                    continue
                else:
                    ArrayPattern[row][col] = "*"
                    count = count + 1
                    break


currentGen = []
tempGen = []

for row in range(MAX_ROW):
    currentGen.append([0] * MAX_COL)
for row in range(MAX_ROW):
    tempGen.append([0] * MAX_COL)

kbchar = ""
commandlist = ["p", "q", "u", "1", "2", "3", "c", "s", "l", "m"]
while(True):
    os.system("cls")
    displayMenu()
    displayList(currentGen)

    while(True):
        if msvcrt.kbhit():
            kbchar = msvcrt.getch().decode()
            if (kbchar.lower() in commandlist):
                break
    if kbchar.lower() == "q":
        break
    if kbchar.lower() == "c":
        setZeroList(tempGen)
        setZeroList(currentGen)
        continue
    if kbchar.lower() == "s":
        SaveArray(currentGen)
        continue
    if kbchar.lower() == "l":
        LoadArray(currentGen)
        continue
    if kbchar.lower() == "m":
        Manual(currentGen)
        continue
    if kbchar == "1" or kbchar == "2" or kbchar == "3":
        LoadPattern(int(kbchar), currentGen)
        continue
    if kbchar.lower() == "u":
        setInitialPatternList(currentGen)
        continue

    while(True):
        os.system("cls")
        displaySubMenu()
        setNextGenList(tempGen, currentGen)
        copyList(tempGen, currentGen)
        displayList(currentGen)
        time.sleep(.8)
        if msvcrt.kbhit():
            kbchar = msvcrt.getch().decode()
            if kbchar.lower() == "h":
                break
        else:
            continue
