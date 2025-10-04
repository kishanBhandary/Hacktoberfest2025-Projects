# Interview Preparation Problems
# This file contains various Python programming problems commonly asked in interviews,
# along with their solutions, explanations, and example outputs.

# 1. Reverse a String
# Problem: Write a function to reverse a given string.
# Explanation: Using Python's slicing feature with [::-1] to reverse the string.
def reverse_string(s):
    return s[::-1]

# 2. Factorial of a Number
# Problem: Calculate the factorial of a non-negative integer n.
# Explanation: Recursive function that multiplies n by factorial of (n-1), with base case 0! = 1! = 1.
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# 3. Check if a Number is Prime
# Problem: Determine if a number is prime (greater than 1 with no divisors other than 1 and itself).
# Explanation: Check divisibility from 2 to sqrt(num). If any divisor found, not prime.
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# 4. Fibonacci Sequence
# Problem: Generate the first n numbers in the Fibonacci sequence.
# Explanation: Start with [0, 1], then append sum of last two for each subsequent number.
def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    seq = [0, 1]
    for i in range(2, n):
        seq.append(seq[i-1] + seq[i-2])
    return seq

# 5. Check if a String is a Palindrome
# Problem: Check if a string reads the same forwards and backwards.
# Explanation: Compare the string with its reverse, ignoring case.
def is_palindrome(s):
    s = s.lower().replace(" ", "")  # Ignore case and spaces
    return s == s[::-1]

# 6. Check if Two Strings are Anagrams
# Problem: Determine if two strings are anagrams (contain same characters with same frequencies).
# Explanation: Sort both strings and compare, or use character count dictionaries.
def are_anagrams(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

# 7. Find the Maximum Element in a List
# Problem: Find the largest number in a list.
# Explanation: Use Python's built-in max() function or iterate to find max.
def find_max(lst):
    if not lst:
        return None
    max_val = lst[0]
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val

# 8. Bubble Sort
# Problem: Sort a list using bubble sort algorithm.
# Explanation: Repeatedly swap adjacent elements if they are in wrong order.
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 9. Binary Search
# Problem: Search for an element in a sorted list using binary search.
# Explanation: Divide the search space in half each time, compare with middle element.
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# 10. Merge Two Sorted Lists
# Problem: Merge two sorted lists into one sorted list.
# Explanation: Use two pointers to compare elements and build the merged list.
def merge_sorted_lists(list1, list2):
    merged = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1
    merged.extend(list1[i:])
    merged.extend(list2[j:])
    return merged

# 11. Remove Duplicates from a List
# Problem: Remove duplicate elements from a list while preserving order.
# Explanation: Use a set to track seen elements, or list comprehension with condition.
def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# 12. Count Vowels in a String
# Problem: Count the number of vowels (a, e, i, o, u) in a string.
# Explanation: Iterate through the string and check if each character is a vowel.
def count_vowels(s):
    vowels = "aeiouAEIOU"
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

# 13. Find the Second Largest Element in a List
# Problem: Find the second largest number in a list.
# Explanation: Sort the list and return the second last element, or use two variables to track max and second max.
def second_largest(lst):
    if len(lst) < 2:
        return None
    max1 = max2 = float('-inf')
    for num in lst:
        if num > max1:
            max2 = max1
            max1 = num
        elif num > max2 and num != max1:
            max2 = num
    return max2 if max2 != float('-inf') else None

# 14. Check if a List is Sorted
# Problem: Determine if a list is sorted in ascending order.
# Explanation: Check if each element is less than or equal to the next.
def is_sorted(lst):
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1]:
            return False
    return True

# 15. Calculate the Power of a Number
# Problem: Compute base raised to the power of exponent.
# Explanation: Use recursion or Python's ** operator.
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

# Example function calls with outputs
print("1. Reverse 'hello':", reverse_string("hello"))
print("2. Factorial of 5:", factorial(5))
print("3. Is 7 prime?", is_prime(7))
print("4. Fibonacci sequence of 10:", fibonacci(10))
print("5. Is 'racecar' a palindrome?", is_palindrome("racecar"))
print("6. Are 'listen' and 'silent' anagrams?", are_anagrams("listen", "silent"))
print("7. Max in [3, 1, 4, 1, 5]:", find_max([3, 1, 4, 1, 5]))
print("8. Bubble sort [64, 34, 25, 12, 22, 11, 90]:", bubble_sort([64, 34, 25, 12, 22, 11, 90]))
print("9. Binary search for 4 in [1, 2, 3, 4, 5]:", binary_search([1, 2, 3, 4, 5], 4))
print("10. Merge [1, 3, 5] and [2, 4, 6]:", merge_sorted_lists([1, 3, 5], [2, 4, 6]))
print("11. Remove duplicates from [1, 2, 2, 3, 3, 3]:", remove_duplicates([1, 2, 2, 3, 3, 3]))
print("12. Vowels in 'Hello World':", count_vowels("Hello World"))
print("13. Second largest in [1, 2, 3, 4, 5]:", second_largest([1, 2, 3, 4, 5]))
print("14. Is [1, 2, 3, 4] sorted?", is_sorted([1, 2, 3, 4]))
print("15. 2^3:", power(2, 3))
