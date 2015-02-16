# datatable.py is a data table displayer/editor built using the curses library
# main idea is to display the square data table stored in an input file and
# allow the user to edit it's contents, changing entries and adding/deleting
# rows/columns, and then save it back to the original file

# usage: python datatable.py filename

# bottom line of the screen is a prompter where the user can type commands
# user commands supported by the displayer/editor
# 'c': change and entry
# 'a': add a new row/column
# 'd': delete a row/column
# 'u': undo last change
# 's': save file


import curses, sys, traceback

# global variables
class gb:
    scrn = None                 # point to curses window object
    fptr = open(sys.argv[1], "r+")    # handle for file
    numOfFields = -1            # number of fields per line
    colWidth = []               # width of each column based on largest entry
    table = []                  # initial table as presented in file
    row = None                  # current row position of curser
    col = None                  # current col position of curser
    history = []                # stack used for undo, all elements are instances of Change


class Change:
    def __init__(self, changeParameter='', oldContent=[], newContent=[], location=[], isRow = True):
        
        #input validated
        if (changeParameter != '') and \
            ((changeParameter == 'c' and oldContent != [] and location != []) or \
            (changeParameter == 'a'  and location   != []) or \
            (changeParameter == 'd'  and oldContent != [] and location != [])):

            self.type       = changeParameter   # type of change
            self.isRow      = isRow             # flag whether added/deleted entity is a row
            self.location   = location          # location of change, for c format is [r,c]
            self.oldContent = oldContent        # old content
            self.newContent = newContent        # (opt) new content
            self.undone     = False             # flag that indicates whether the undo method has been invoked successfully

        else:
            print "Change:__init__ could not instantiate Change object, due to an invalid combination of input parameters"

    #method undoes the change stored by this instance
    def undo(self):
        if self.type == 'c' and not self.undone:
            #insert code for handling single entry reversal here
            self.undone = True
            #change te relevant field
            argumentString = ""
            for el in self.location: argumentString += str(el) + " "
            argumentString += str(self.oldContent)
            changeField(argumentString, False)

        elif self.type == 'a' and not self.undone:
            #revert adding a column/row
            self.undone = True
            #delete column or row
            if self.isRow:
                #delete row
                deleteRowCol('row', self.location[0], False)
            else:
                #delete col
                deleteRowCol('column', self.location[0], False)

        elif self.type == 'd' and not self.undone:
            #revert deleting row/column
            self.undone = True

            #create argument strings
            line = ""
            for el in self.oldContent: line += str(el) + " " # adds one space too much

            if self.isRow:
                #add a row
                addRowCol('row', str(self.location[0]), line, False)
            else:
                #add a col
                addRowCol('column', str(self.location[0]), line, False)
        elif not self.undone:
            #error handling
            print "Change:undo input parameter not recognised"
            sys.exit()

#------------------------------------------------
# file processing
#------------------------------------------------
def processFile():
    # start processing file line by line
    for line in gb.fptr.readlines():
        fields = line.split()
        # add each parsed row to global variable table
        gb.table.append(fields)
        # find out the number of fields per row
        if gb.numOfFields == -1:
            gb.numOfFields = len(fields)
            gb.colWidth = [0] * gb.numOfFields
        # error checking
        if len(fields) != gb.numOfFields:
            print 'Error: not the same number of fields'
            sys.exit(1)
        # figure out the width of each column
        for i in range(gb.numOfFields):
            if len(fields[i]) > gb.colWidth[i]:
                gb.colWidth[i] = len(fields[i])

def saveToFile():
    # delete contents of the file
    gb.fptr.seek(0)
    gb.fptr.truncate()
    gb.fptr.close()

    #open file in "append"-mode and write new contents
    write_ptr = open(sys.argv[1], "a")
    for row in gb.table:
        line = " ".join(row)
        write_ptr.write(line + "\n")

    #open file with original file handle
    gb.fptr = open(sys.argv[1], "r+")


#------------------------------------------------
# start display, and revert to original display type
#------------------------------------------------
def displayTable():
    # for each row of the file
    for row in gb.table:
        for i in range(gb.numOfFields):
            # adjust each field based on maximum column width
            field = row[i].rjust(gb.colWidth[i])
            # write it on the screen
            gb.scrn.addstr(gb.row, gb.col, field)
            # adjust the curser postion 
            gb.col = gb.col + gb.colWidth[i] + 1
            # + 1 in above line because of space between fields
        # after each line is processed written column back to 0
        # and increase row by one
        gb.col = 0
        gb.row += 1

def restorescreen():
    # restore original settings    
    curses.nocbreak()
    curses.echo()
    curses.endwin()

#------------------------------------------------
# data manipulation methods
#------------------------------------------------
def addRowCol(type, num, line, notUndo = True):
    #adds a row or column; takes in strings of add type, index, and line of values
    #converts index string to int and splits line input into list of values

    index = int(num)
    values = line.split()
	
    if type == 'row':
        #if not undoing, creates change instance for adding row, pushes to history stack
        if notUndo:
            added = Change('a', [], [], [index], True)
            gb.history.insert(0, added)
        #add row to table
        gb.table.insert(index, values)

        #update max widths of columns
        for i in range(gb.numOfFields):
            if len(values[i]) > gb.colWidth[i]:
                gb.colWidth[i] = len(values[i])
                #If the max column width has changed, redraw that column
                redrawCol(i)
        #Update the rows    
        redrawRow(index)

    elif type == 'column':
        #if not undoing, creates change instance for adding column, pushes to history stack
        if notUndo:
            added = Change('a', [], [], [index], False)
            gb.history.insert(0, added)
        #go through every row and insert values[i] into table[i][index]
        maxWidth = 0
        for i in range(len(gb.table)):
            gb.table[i].insert(index, values[i])
            if len(values[i]) > maxWidth:
                maxWidth = len(values[i])
        #update number of columns in table, insert new column's max width
        gb.numOfFields += 1
        gb.colWidth.insert(index, maxWidth)
        redrawCol(index)


    else:
        print 'Error: invalid input'
		
def deleteRowCol(type, num, notUndo = True):
    #deletes a row or column; takes in strings of delete type, index 
    #convert index string to int
    index = int(num)

    if type == 'row':
        #Creates instance of change for 'd' row
        #gb.row = index - 1
        if notUndo:
            deleted = Change('d', gb.table[index], [], [index], True)   
            gb.history.insert(0, deleted)
        del gb.table[index]
        gb.scrn.move(index,0)
        gb.scrn.deleteln()

        #check if the maxes of any columns have been changed
        for col in range(gb.numOfFields):
            max = 0
            for i in range(len(gb.table)):
                if len(gb.table[i][col]) == gb.colWidth[col]:
                    max = gb.colWidth[col]
                    break
                elif len(gb.table[i][col]) > max:
                    max = len(gb.table[i][col])
            

            if max != gb.colWidth[col]:
                gb.colWidth[col] = max
                redrawCol(col)


    elif type == 'column':
        #creates instance of change for 'd' column
        #creates a list of the deleted column while simultaneously
		#popping values from rows
        lastIndex = False
        if index == gb.numOfFields - 1:
            lastIndex = True
        if notUndo:
            column = []
            for i in range(len(gb.table)):
                column.append(gb.table[i].pop(index))
            deleted = Change('d', column, [], [index], False)
            gb.history.insert(0, deleted)
        else:
            for i in range(len(gb.table)):
                del gb.table[i][index]
        #Remove deleted column's max width, decrease table's number of columns
        gb.numOfFields -= 1
        del gb.colWidth[index]

        #move cursor position to the right column in each row
        moveBy = 0
        for i in range(gb.numOfFields):
            moveBy += gb.colWidth[i] + 1

        #if deleting last column you just want to clear that column, if it's one of the other columns call redraw    
        if lastIndex:
            for i in range(len(gb.table)):
                gb.scrn.move(i, moveBy)
                gb.scrn.clrtoeol()           
        else:
            redrawCol(index)   
        
    else:
        print 'Error: invalid input'

def changeField(line, notUndo = True):
    #changes a specified field; takes in input string and converts to values	
    inputs = line.split()
    row = int(inputs[0])
    col = int(inputs[1])
    value = inputs[2]
	
    #Creates instance of change for 'c'
    if notUndo:
        edit = Change('c', gb.table[row][col], [], [row, col]) 
        gb.history.insert(0, edit)
    editValue(row, col, value)
    
    #if the length of the inserted value is larger than the max, resize column
    if len(value) > gb.colWidth[col]:
        gb.colWidth[col] = len(value)
        redrawCol(col)
    #else check to see if the widest element was changed; if so, reduce column size
    else:
        max = 0
        for i in range(len(gb.table)):
            if len(gb.table[i][col]) == gb.colWidth[col]:
                max = len(gb.colWidth[col])
                break
            elif len(gb.table[i][col]) > max:
                max = len(gb.table[i][col])
        

        if max != gb.colWidth[col]:
            gb.colWidth[col] = max
            redrawCol(col)
        else:
            redrawField(col, row)

	
def editValue(r,c,val):
    #helper function to change the value of a field
    gb.table[r][c] = val

#------------------------------------------------
# redraw methods
# (invoked by the data manipulation methods)
#------------------------------------------------
def redrawRow(x):
    gb.row = x # move cursor to relevant row
    for row in gb.table[x:]:
        gb.col = 0
        for i in range(gb.numOfFields):
            # adjust each field based on maximum column width
            field = row[i].rjust(gb.colWidth[i])
            # write it on the screen
            gb.scrn.addstr(gb.row, gb.col, field)
            # adjust the curser postion 
            gb.col = gb.col + gb.colWidth[i] + 1
            # + 1 in above line because of space between fields
        # after each line is processed written column back to 0
        # and increase row by one
        gb.row += 1


def redrawCol(x):
    #x is the col to start drawing from, so get the col width for preceeding columns + 1 and then incerement gb.col to that

    # for each row of the file
    gb.row = 0
    moveBy = 0
    for i in range(x):
            moveBy += gb.colWidth[i] + 1
    for row in gb.table:
        gb.col = moveBy
        #gb.col = moveBy # cursor to relevant column in each row
        for i in range(x,gb.numOfFields): # for all columns in that row
            #if i < x: continue #fast forward the iterator to the first relevant column
            # adjust each field based on maximum column width
            field = row[i].rjust(int(gb.colWidth[i]))
            # write it on the screen
            gb.scrn.addstr(gb.row, gb.col, field)
            gb.scrn.clrtoeol()
            # adjust the curser postion 
            gb.col = gb.col + int(gb.colWidth[i]) + 1
            # + 1 in above line because of space between fields
        
        # and increase row by one
        gb.row += 1


def redrawField(x,y):
    #redraw only the coordinates of the field
    #move cursor to coordinates, draw, refresh
    gb.row = y
    gb.col = 0
    for i in range(x): gb.col += gb.colWidth[i] + 1

    field = gb.table[y][x].rjust(gb.colWidth[x])
    
    gb.scrn.addstr(gb.row, gb.col, field.rstrip())


def main():
    processFile()
    
    # window setup
    gb.scrn = curses.initscr()
    curses.noecho()
    curses.cbreak()
    gb.scrn.clear()
    
	#Gets the height and width of the window
    dimensions = gb.scrn.getmaxyx()
	
    # display the table in file properly
    gb.row = 0
    gb.col = 0
    displayTable()
    gb.scrn.refresh()

    # quit?
    while True:
        c = gb.scrn.getch()
        c = chr(c)
        if c == 'q':
            break
        elif c == 'c':
            curses.nocbreak()
            curses.echo()
            gb.scrn.addstr(curses.LINES-1, 0, 'Enter row, column, value separated by spaces: ')
            userInput = gb.scrn.getstr()
            curses.noecho()
            curses.cbreak()
            gb.scrn.clrtoeol()
            changeField(userInput)
        elif c == 'a':
            curses.nocbreak()
            curses.echo()
            gb.scrn.addstr(curses.LINES-1, 0, 'Type either row or column: ')
            userInput1 = gb.scrn.getstr()
            gb.scrn.clrtoeol()
            gb.scrn.addstr(curses.LINES-1, 0, 'Enter number indicating where to insert: ')
            userInput2 = gb.scrn.getstr()
            gb.scrn.clrtoeol()
            gb.scrn.addstr(curses.LINES-1, 0, 'Enter values separated by spaces: ')
            userInput3 = gb.scrn.getstr()
            curses.noecho()
            curses.cbreak()
            gb.scrn.clrtoeol()
            addRowCol(userInput1, userInput2, userInput3)
        elif c == 'd':
            curses.nocbreak()
            curses.echo()
            gb.scrn.addstr(curses.LINES-1, 0, 'Type either row or column: ')
            userInput1 = gb.scrn.getstr()
            gb.scrn.clrtoeol()
            gb.scrn.addstr(curses.LINES-1, 0, 'Enter number indicating where to delete: ')
            userInput2 = gb.scrn.getstr()
            curses.noecho()
            curses.cbreak()
            gb.scrn.clrtoeol()
            deleteRowCol(userInput1, userInput2)
        elif c == 'u':
            if len(gb.history) > 0:
                change_obj = gb.history[0]
                change_obj.undo()
                gb.history.pop(0)
        elif c=='s':
            saveToFile()
    restorescreen()
    

if __name__ == '__main__':
    try:
        main()
    except:
        restorescreen()
        traceback.print_exc()
