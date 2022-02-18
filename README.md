# edit-distance word suggester
For this assignment, I implemented the Dynamic Edit Distance algorithm to find the edit distance of two strings. However, in order to create a useful application of this algorithm, I created a program which essentially provides word suggestions to the user's inputted string based on the calculated edit distance between the user's inputted string and each of the words in the files "sgb-words.txt", which contains all 5-letter words, and "1000-most-common-words.txt", which contains the 1000 most common words. One interpretation of this application/program is a spellcheck bot, although given that the number of words it compares is only ~6000, that function is slightly limited.

The program is a simple Python3 program than can be run with the command "python3 EditDistance.py", without the use of a virtual environment since the program does not have any dependencies.

When run, the program first prompts the user with "Please enter a string:". Keep in mind that since the list of words the inputted string will be compared to only contains alpha characters, I made it so that the inputted string must not contain any numbers of special characters. An invalid string will receive the message "A valid string contains only alpha characters." and another prompt to enter a string.

Once a valid string is inputted, the program finds the edit distance for the inputted string and every word in the two word files. As this iteration is happening, the 10 words with the smallest edit distance are stored in a list, and that list, along with each word's edit distance from the input (and the number of edits, adds, and deletes) is outputted to the user once the algorithm is finished. Finally, the user is asked if they would like to run the program again.

## Dynamic Edit-Distance Algorithm description & analysis
This algorithm creates a matrix that is used to find the edit distance for every single combination of substrings for each of the two inputs. By doing this, the algorithm can dynamically find the edit distance for the complete strings by avoiding the recomputation of the same subproblems. To demonstrate this approach to finding edit distance, let's show a simple example: cat vs. create

>         c r e a t e 
>       0 1 2 3 4 5 6 
>     c 1 0 1 2 3 4 5 
>     a 2 1 1 2 2 3 4 
>     t 3 2 2 2 3 2 3 

Each value in the matrix represents the edit distance for the substrings from index 0 to indexes m & n. For example, substrings "ca" and "cre" corresponds to a value of 2, which is accurate since it would take 2 edits/adds/deletes to change "ca" to "cre" or vice versa. This is true for any entry in the matrix, including the final entry 3 which represents the edit distance for the full strings "cat" and "create".

To create this matrix, you first initialize a table like this:

>         c r e a t e
>       0 1 2 3 4 5 6
>     c 1            
>     a 2            
>     t 3            
  
Then, you iterate through the strings and compare the current character in string 1 to each character in string 2. If the characters match, the value diagonal to the current element is set to the current element, since no operations need to be done. Otherwise, the minimum of the left entry, diagonal entry, and above entry plus one is set to the current element, since one of the three operations needs to be done to convert this substring to that substring:

>     if word_2[j-1] == word_1[i-1]:
>          matrix[i][j] = matrix[i-1][j-1]
>     else:
>          matrix[i][j] = min(matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1]) + 1
          
This is indeed easier to see in a video, so here is a YouTube video showing an example of the matrix that is created by this algorithm: https://youtu.be/We3YDTzNXEk

Once this matrix is created, the last element is equal to the edit distance between the two strings. However, what is we want to see the specific number of edits, adds, and deletes? To find this, we are able to traverse the created matrix backwards from the ending element to the beginning element. If the current element is one greater than the element to its left, an add was needed. If the current element is one greater than the element above it, then a delete was needed. If the current element is one greater than its diagonal, then an edit was needed. And lastly, if the current element is equal to its diagonal, then no operation was needed. Through this process, we can go from indexes m,n to 0,0 and calculate how many edits, adds, and deletes were needed. This is done in my program, and the result is outputted to the user.

Lastly, the efficiency of this algorithm is O(m x n) with m and n being the lengths of the inputted words. This is not the most efficient approach to solving the edit distance problem, but it is indeed much faster than the naive resursive solution since it solves the problem dynamically and it able to avoid solving the same subproblems multiple times. Additionally, given this application, the algorithm still runs quite fast even for relatively long inputs.
