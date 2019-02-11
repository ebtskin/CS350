
import array
# print(request.content)

arr = array.array('i', [2, 3, 9, 4, 33, 22, 12, 43, 1])


def swap(arr, low, high):
    temp = arr[low]
    arr[low] = arr[high]
    arr[high] = temp


def bubble_sort(arr):
    size = len(arr)
    for i in range(0, size):
        flag = 0
        for j in range(0, size - i - 1):
            if arr[j] > arr[j+1]:
                swap(arr, j, j+1)
                flag = 1
        if flag == 0:
            return 1


def display(arr):
    for i in range(0, len(arr)):
        print("%d" % arr[i], end=" ")


bubble_sort(arr)
display(arr)


