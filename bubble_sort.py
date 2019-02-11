import sys
import array
import random

from timeit import default_timer as timer


class BubbleSort:

    def __init__(self):
        self.myarray = []
        self.total_cells_in_array = random.randint(1, 10000)
        self.min_element = 1
        self.max_element = 10000

    def gen_rand(self):
        for i in range(self.total_cells_in_array):
            self.myarray.append(random.randint(self.min_element, self.max_element))

    def print_array(self):
        for i in range(len(self.myarray)):
            print(self.myarray[i], end=' ')
            print('\n')

    def swap(self, low, high):
        temp = self.myarray[low]
        self.myarray[low] = self.myarray[high]
        self.myarray[high] = temp

    def bubble_sort(self):
        size = len(self.myarray)
        for i in range(0, size):
            flag = 0
            for j in range(0, size - i - 1):
                if self.myarray[j] > self.myarray[j+1]:
                    temp = self.myarray[j]
                    self.myarray[j] = self.myarray[j+1]
                    self.myarray[j+1] = temp
                    flag = 1
            if flag == 0:
                return 1

    def display(self):
        for i in range(0, len(self.myarray)):
            print("%d" % self.myarray[i], end=" ")


if __name__ == '__main__':
    my_sort = BubbleSort()
    my_sort.gen_rand()
    start = timer()
    my_sort.bubble_sort()
    end = timer()
    my_sort.display()
    print("\n\nThe time it took to sort this array of length", my_sort.total_cells_in_array, "was", end-start)
