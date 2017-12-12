# Visualization of sorting algorithms
# Created by Tyler Doyle in Python 3.6 with pygame

import random
import pygame

numEntries = 512  # Number of entries in the array (0 -> numEntries)
factor = 1       # Amount of pixels per block
current = ""

# Set these to True if you want to see a visualization of the algorithm
# The program will run in the order seen here
showSelection = False
showInsertion = False
showMerge = False
showBubble = False
showQuick = False
showHeap = False
showShell = False
showCocktail = False
showGnome = False
showBitonic = True  # Note: numEntries must be a power of 2
showRadix = True


# Screen size is dependent on the number of entries and the block size
DISPLAY_WIDTH = numEntries * factor
DISPLAY_HEIGHT = numEntries * factor

# Initialize pygame
pygame.init()
pygame.font.init()
# Create display
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
# Initialize font
fontSize = 30
font = pygame.font.SysFont("Arial", fontSize)

# Run the program
def run ():

    # Create a random array
    a = createArray()

    # Display the sorting algorithms specified above using a copy of the random
    # array
    global current
    if (showSelection):
        current = "Selection Sort"
        selectionSort(a.copy())
    if (showInsertion):
        current = "Insertion Sort"
        insertionSort(a.copy())
    if (showMerge):
        current = "Merge Sort"
        mergeSort(a.copy(), 0, numEntries)   
    if (showBubble):
        current = "Bubble Sort"
        bubbleSort(a.copy())
    if (showQuick):
        current = "Quick Sort"
        quickSort(a.copy(), 0 , numEntries - 1)
    if (showHeap):
        current = "Heap Sort"
        heapSort(a.copy(), numEntries - 1)
    if (showShell):
        current = "Shell Sort"
        shellSort(a.copy())
    if (showCocktail):
        current = "Cocktail Shaker Sort"
        cocktailShakerSort(a.copy())
    if (showGnome):
        current = "Gnome Sort"
        gnomeSort(a.copy())
    if (showBitonic):
        current = "Bitonic Sort"
        bitonicSort(a.copy(), True, 0, len(a))
    if (showRadix):
        current = "Radix Sort"
        radixSort(a.copy())

    # Allows the user to close the screen once the algorithms have finished
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                       
    pygame.quit()

# Draw the current state of the array     
def draw (a):
    # Make the background black
    display.fill((0,0,0))
    # Display current algorithm
    label = font.render(current, True, (255,255,255))
    display.blit(label, (0, DISPLAY_HEIGHT - fontSize))
    # Draw the current state
    for i in range(0,len(a)):
        width = factor                  # Width is the size of the factor (block size)
        height = (a[i] + 1) * factor    # Height is the value at the state (+1 so 0 is shown)
                                        # multiplied by the factor
                                        
        # Draw a white rectangle from the top left of the screen
        pygame.draw.rect(display, (255,255,255), (i * factor, 0, width, height))
    
    # Display the next state
    pygame.display.flip()

# Creates a random array of size numEntries 
def createArray():
    a = []
    for i in range(0, numEntries):
        a.append(i)
    random.shuffle(a)
    return a

# Used for testing to determine if a sorting algorithm works
def checkSort(a):
    if len(a) > 1:
        for i in range(1, len(a)):
            if a[i - 1] > a[i]:
                return False
    return True

# Selection Sort (O(n^2))
# Recommended numEntries: 500   Recommended factor: 2
def selectionSort(a):
    # Find the next smallest element and place it at the start of the unsorted
    # portion of the list
    for i in range(0, len(a)):
        minElement = i
        for j in range(i, len(a)):
            if (a[minElement] > a[j]):
                minElement = j
        swap(a, i, minElement)
        draw(a)

# Insertion sort (O(n^2))
# Recommended numEntries: 250   Recommended factor: 3
def insertionSort(a):
    # For every element in the array, iterate backwards until the element is
    # in the corrent spot
    for i in range(1, len(a)):
        j = i
        while j > 0 and a[j-1] > a[i]: 
            j -= 1
        shift(a, j, i)
        draw(a)
    return a

# Merge Sort (O(nlogn))
# Recommended numEntries: 500   Recommended factor: 1
# a: array, s: start, e: end
def mergeSort(a, s, e):
    # Sub-divides the array into left and right recursively merges
    if (e - s >= 1):
        m = int((s + e - 1) / 2) # the midpoint
        mergeSort(a, s, m)       # merge sort the left side
        mergeSort(a, m+1, e)     # merge sort the right side
        merge(a, s, m, e)        # merge the two sides together

# Merges the left and right sides around a midpoint
# a: array, s: start, e: end, m: middle
def merge(a, s, m, e):
    leftI = s
    rightI = m + 1
    # If the left element is the smallest, leave it. If the right element is
    # smallest, shift it down into the next position
    for i in range(0, e - s + 1):
        if not (leftI == rightI or rightI > e or rightI == len(a)):
            if (a[leftI] > a[rightI]):
                shift(a, leftI, rightI)
                rightI += 1
            leftI += 1
        draw(a)

# Shifts an element down array by moving all pervious elements up a position
# a: array, s: start, vslInd: index of the value to be shifted
def shift(a, s, valInd):
    val = a[valInd]
    for i in range(valInd, s, -1):
        a[i] = a[i-1]
    a[s] = val

# Bubble Sort (O(n^2))
# Recommended numEntries: 1000  Recommended factor: 1
def bubbleSort(a):
    # Swaps pairs of elements if they are out of order until the array is sorted
    currentEnd = len(a)
    while currentEnd > 0:
        for j in range(1, currentEnd):
            if (a[j-1] > a[j]):
                swap(a, j, j-1)
        currentEnd -= 1
        draw(a)

# Swaps two array elements
def swap(a, i1, i2):
    temp = a[i1]
    a[i1] = a[i2]
    a[i2] = temp
    
# Quick Sort (O(n^2))
# Recommended numEntries: 750  Recommended factor: 1
# a: array, s: start, e: end
def quickSort(a, s, e):
    # Pick a random pivot point and shift elements until all smaller elements
    # are on the left and all larger elements are on the right then iteratively
    # use quick sort until the array is sorted
    if (e - s > 0):
        pivot = random.randint(s, e)
        l = s           # Left pointer
        r = e           # Right pointer
        while (l <= r):
            if (a[l] > a[pivot]):
                if (a[r] <= a[pivot]):
                    if (a[r] == a[pivot]):
                        pivot = l
                    swap(a, l, r)
                    draw(a)
                else:
                    r -= 1
            else:
                l += 1
                if (a[r] > a[pivot]):
                    r -= 1
        swap(a, pivot, r)   # Swap the pivot with the right index
        draw(a)
        quickSort(a, s, r - 1)
        quickSort(a, r + 1, e)

# Heap Sort (O(nlogn))
# Recommended numEntries: 500  Recommended factor: 2
def heapSort(a, e):
    # Creates a max heap then moves the largest element to the end of the array
    # and fixes the heap until the whole array is sorted
    createMaxHeap(a, e) 
    while (e > 0):
        swap(a, 0, e)
        draw(a)
        e -= 1
        maintainMaxHeap(a, 0, e)

# Creates a max heap from a random array by creating a max heap iteratively
# from the leaves to the root
def createMaxHeap(a, e):
    for i in range(int(len(a)/2) - 1, -1, -1):
        maintainMaxHeap(a, i, e)

# Fixes a max heap once the max element has been moved to the end
# a: array, i: index, e: end
def maintainMaxHeap(a, i, e):
    left = (2 * (i + 1)) - 1
    right = (2 * (i + 1))
    largest = i
    if (left < e + 1 and a[left] > a[largest]):
        largest = left
    if (right < e + 1 and a[right] > a[largest]):
        largest = right
    if (largest != i):
        swap(a, largest, i)
        draw(a)
        maintainMaxHeap(a, largest, e)

# Shell Sort (O(n^2))
# Recommended numEntries: 400  Recommended factor: 2
def shellSort(a):
    # Runs insertion sort at various gap sizes
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]
    for gap in gaps:
        for i in range(gap, len(a)):
            cur = a[i]
            j = i
            while j >= gap and a[j - gap] > cur:
                a[j] = a[j - gap]
                j -= gap
                draw(a)
            a[j] = cur
            draw(a)

# Cocktail Shaker Sort (O(n^2))
# Recommended numEntries: 150  Recommended factor: 6
def cocktailShakerSort(a):
    # Bubble sort up and down the array
    leftInd = 0
    rightInd = len(a) - 1
    while leftInd <= rightInd:
        newRightInd = leftInd
        newLeftInd = rightInd
        for i in range(leftInd, rightInd):
            if (a[i] > a[i+1]):
                swap(a, i, i+1)
                newRightInd = i
                draw(a)
        rightInd = newRightInd
        for j in range(rightInd, leftInd - 1, -1):
            if (a[j] > a[j+1]):
                swap(a, j, j+1)
                newLeftInd = j
                draw(a)
        leftInd = newLeftInd

# Gnome Sort (O(n^2))
# Recommended numEntries: 250   Recommended factor: 3
def gnomeSort(a):
    # Very similar to insertion sort but uses a series of swaps 
    start = 0
    while start < len(a):
        if (start == 0 or a[start] >= a[start - 1]):
            start += 1
        else:
            swap(a, start, start - 1)
            draw(a)
            start = start - 1

# Bitonic Sort (O(log^2 n))
# Recommended numEntries: 512   Recommended factor: 1
# Note: numEntries must be a power of 2
# a: array, up: if true, ascending otherwise descending, s: start, e: end
def bitonicSort(a, up, s, e):
    # Iteratively sorts the left and right sides and merges them
    if e - s > 1:
        mid = (s + e) // 2
        bitonicSort(a, True, s, (s + e) // 2)
        bitonicSort(a, False, (s + e) // 2, e)
        bitonicMerge(a, up, s, e)

def bitonicMerge(a, up, s, e):
    # Iteratively compares and merges left and right sides
    if e - s > 1:
        bitonicCompare(a, up, s, e)
        bitonicMerge(a, up, s, (s + e) // 2)
        bitonicMerge(a, up, (s + e) // 2, e)

def bitonicCompare(a, up, s, e):
    # Compares elements mid apart and swaps them if they are in the wrong order
    dist = (s + e) // 2
    mid = (e - s) // 2
    for i in range(s, dist):
        if (a[i] > a[i + mid]) == up:
            swap(a, i, i + mid)
            draw(a)

# Radix Sort (O(wn))
# Recommended numEntries: 750   Recommended factor: 1
# Note: This implementation is not optimized to allow for displaying easily
def radixSort(a, base=10):
    # Sorts by the digit of numbers until it reaches the largest digit base
    # possible
    maxVal = numEntries - 1
    i = 0
    while base ** i <= maxVal:
        radixBuckets(a, base, i)
        i += 1

def radixBuckets(a, base, i):
    numSorted = 0
    while numSorted < len(a):
        digit = (a[-1] // (base ** i)) % base
        cur = 0
        while (a[cur] // (base ** i)) % base < digit and cur < numSorted:
            cur += 1
        shift(a, cur, len(a) - 1)
        draw(a)
        numSorted += 1

run()
