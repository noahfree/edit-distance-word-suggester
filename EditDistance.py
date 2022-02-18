
# SIZE constant changes how many suggested words appear in the output
SIZE = 10

# Word class is used to hold a word and that word's edit distance info
class Word:
    def __init__(self, word, distance, edits, adds, deletes):
        self.word = word
        self.distance = distance
        self.edits = edits
        self.adds = adds
        self.deletes = deletes

# Function FindEditDistance() takes two strings and calculates the edit distance between the two words using the dynamic edit distance algorithm
def FindEditDistance(word_1, word_2):
    # variables columns & rows are set to the dimensions of the matrix used to find the edit distance
    columns = len(str(word_2)) + 1
    rows = len(str(word_1)) + 1

    # set variables edits, adds, and deletes to 0 to be incremented
    edits = adds = deletes = 0

    # create a matrix to hold the edit distance for every combination of the two inputs
    matrix = [[ -1 for i in range(columns)] for j in range(rows)]

    # initialize the first row & column of the matrix to the index of that row/column
    matrix[0][0] = 0
    for i in range(1, max(columns, rows)):
        if i < columns:
            matrix[0][i] = i;
        if i < rows:
            matrix[i][0] = i;

    # nested loops iterate through the matrix once for every element in the matrix
    for i in range(1, rows):
        for j in range(1, columns):
            # if the current letters are the same, then set this element in the matrix equal to the edit distance of both string without the current letters,
            # which is found in the diagonal entry, matrix[i-1][j-1]
            if word_2[j-1] == word_1[i-1]:
                matrix[i][j] = matrix[i-1][j-1]
            # else, set it to the minimum + 1 of the 3 surrounding entries, meaning that an edit, addition, or deletion is necessary
            else:
                matrix[i][j] = min(matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1])+1

    # create variables current, i, and j to iterate back through the matrix in order to find the specific number of edits, adds, and deletes
    current = -1
    i = rows - 1
    j = columns - 1
    while i > 0 or j > 0:
            # if i or j is equal to zero, then the remaining function are adds or deletes
            if i == 0:
                j -= 1
                adds += 1
                continue
            elif j == 0:
                i -= 1
                deletes += 1
                continue
            
            # set current equal to the current element in the matrix
            current = matrix[i][j]
            # if current is equal to the element above it +1, then an addition was needed
            if current == matrix[i][j-1]+1:
                j -= 1
                adds += 1
                continue
            # if current is equal to the element to its left +1, then a deletion was needed
            elif current == matrix[i-1][j]+1:
                i -= 1
                deletes += 1
                continue
            # if current is equal to the element diagonal to it +1, then an edit was needed
            elif current == matrix[i-1][j-1]+1:
                i -= 1
                j -= 1
                edits += 1
                continue
            # if current is equal to the element diagonal to it, then the letters were equal, so no operation was needed
            elif current == matrix[i-1][j-1]:
                i -= 1
                j -= 1
                continue
            
    # a Word object is going to be returned with the given word & its edit distance info
    return Word(word_2, matrix[rows - 1][columns - 1], edits, adds, deletes)

# Function AddWord() adds a given Word object into the words list based on its distance attribute
def AddWord(words, word):
    # words is iterated through until the next word's distance is greater than the inputted word, or the loop reaches the end of the list
    for i in range(-1, len(words)):
        if i == (len(words) - 1) or words[i+1].distance >= word.distance:
            # once the word is inserted, the function returns 
            words.insert(i+1, word)
            return

# Function GetInput() gets user input for the string that the user wants to use
def GetInput():
    string = input("\nPlease enter a string: ")
    # since the user input is going to be compared to words, the input must only contain alpha characters
    while not string.isalpha():
        print("\nA valid string contains only alpha characters.")
        string = input("\nPlease enter a string: ")
    # the string is converted to lowercase 
    return string.lower()

# Function GetWords() reads the words from the text files into a list of strings that is returned
def GetWords():
    # the first file is opened for reading
    file = open("sgb-words.txt", "r")
    # the data is read and splitted by newline characters
    wordList = file.read().split("\n")
    # wordList.pop() removes a "" element from the end of the list
    wordList.pop()
    # the file is closed
    file.close()

    # the second file is opened for reading
    file = open("1000-most-common-words.txt", "r")
    # again, the data is read and splitted by newline characters
    extension = file.read().split("\n")
    # while loop iterates through the 2nd list and removes any 5 letter words, in order to not have duplicates
    i = 0
    while i < len(extension):
        if len(extension[i]) == 5:
            extension.pop(i)
            i -= 1
        i += 1
    # the "" element at the end of the list is removed, and the file is then closed
    extension.pop()
    file.close()

    # the two lists are joined together and returned
    return wordList + extension

# Function IterateWords() iterates through the inputted list and calls FindEditDistance() for every word in the list and the inputted string
def IterateWords(wordList, string):
    # output is a list of Word objects with the lowest edit distances
    output = []
    # for loop iterates once for every word in wordList
    for i in range(len(wordList)):
        # FindEditDistance() returnes a Word object contain the word's edit distance from the inputted string
        word = FindEditDistance(str(string), str(wordList[i]))
        # if the length of output is less than the SIZE constant, add the word to output no matter what
        if len(output) < SIZE:
            AddWord(output, word)
        # else, if the word's edit distance is less than the edit distance of the last word in the list, remove that word & add the word to the output
        elif (word.distance < output[len(output)-1].distance):
            output.pop()
            AddWord(output, word)
    # return the output list
    return output

# Function GenerateOutput() prints the output data to the console
def GenerateOutput(output, string):
    # editStr, addStr, and delStr are utilized in order to print the correct singular/plural form of edit, add, and delete
    editStr = "edit,"
    addStr = "add,"
    delStr = "delete"

    print("\nSuggested words (word => edit distance):")
    # for every value from 0 to the SIZE constant
    for i in range(SIZE):
        # 3 if statement ensure there is an 's' on edit/add/delete if the edits/adds/deletes is not equal to 1
        if output[i].edits != 1:
            editStr = "edits,"
        if output[i].adds != 1:
            addStr = "adds,"
        if output[i].deletes != 1:
            delStr += "s"
        # the output for the current word is printed to the console
        print("   %2d) %-6s  => %2d  (%d %-6s %d %-5s %d %s)" % (i+1, output[i].word, output[i].distance, output[i].edits, editStr, output[i].adds, addStr, output[i].deletes, delStr))
        # the 3 string variables are reset
        editStr = "edit,"
        addStr = "add,"
        delStr = "delete"
    # the user's inputted string is printed at the end
    print("\nInput: " + string)
    
# Function Main() is the main part of the function, which calls the above functions
def Main():
    # wordList is created by calling GetWords()
    wordList = GetWords()
    # string is created by calling GetInput() to get input from the user
    string = GetInput()
    # output is created by calling IterateWords()
    output = IterateWords(wordList, string)
    # GenerateOutput() prints the resulting data to the user
    GenerateOutput(output, string)

    # toggle is used to run the program again if the user chooses
    toggle = input("\nWould you like to run the program again? (y/n)\n")
    while toggle != 'y' and toggle != 'Y' and toggle != 'n' and toggle != 'N':
        toggle = input("\n\nWould you like to run the program again? (y/n)\n")

    # if the user inputes 'y' or 'Y', the Main() runs again
    if toggle == 'y' or toggle == 'Y':
        Main()

Main()
