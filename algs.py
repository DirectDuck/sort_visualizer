from abc import ABC, abstractmethod
from sorter import Sorter

class Sort(ABC):

    @abstractmethod
    def __init__(self, sorter: Sorter):
        pass

    @abstractmethod
    def execute(self):
        pass

class BubbleSort(Sort):

    def __init__(self, sorter: Sorter):
        self.sorter = sorter
        self.array = self.sorter.array_of_rects

    def execute(self):
        self._bubble()

    def _bubble(self):
        for i in range(len(self.array) - 1):
            for j in range(len(self.array) - i - 1):
                if self.array[j].height > self.array[j + 1].height:
                    self.sorter.swap_rects(self.array[j], self.array[j + 1])
                    self.array[j], self.array[j +
                                              1] = self.array[j + 1], self.array[j]
            self.sorter.window.Refresh()


class QuickSort(Sort):

    def __init__(self, sorter: Sorter):
        self.sorter = sorter
        self.array = self.sorter.array_of_rects

    def execute(self):
        self._quick_sort(0, len(self.array) - 1)

    def _partition(self, start, end):
        pivot = self.array[start].height
        low = start + 1
        high = end

        while True:
            while low <= high and self.array[high].height >= pivot:
                high = high - 1

            while low <= high and self.array[low].height <= pivot:
                low = low + 1

            if low <= high:
                self.sorter.swap_rects(self.array[low], self.array[high])
                self.array[low], self.array[high] = self.array[high], self.array[low]
            else:
                break

        self.sorter.swap_rects(self.array[start], self.array[high])
        self.array[start], self.array[high] = self.array[high], self.array[start]

        return high

    def _quick_sort(self, start, end):
        if start >= end:
            return

        p = self._partition(start, end)
        self._quick_sort(start, p - 1)
        self._quick_sort(p + 1, end)


class MergeSort(Sort):

    def __init__(self, sorter: Sorter):
        self.sorter = sorter
        self.array = self.sorter.array_of_rects

    def execute(self):
        self._merge_sort(self.array, 0)

    def _merge_sort(self, arr: list, startindex: int):
        if len(arr) > 1:
            mid = len(arr) // 2
            lefthalf = arr[:mid]
            righthalf = arr[mid:]

            self._merge_sort(lefthalf, int(startindex))
            self._merge_sort(righthalf, int(startindex + len(arr) / 2))

            i = 0
            j = 0
            k = startindex
            k_or = 0

            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i].height <= righthalf[j].height:
                    self.array[k] = lefthalf[i]
                    arr[k_or] = lefthalf[i]
                    i += 1

                    self.sorter.redraw()
                else:
                    self.array[k] = righthalf[j]
                    arr[k_or] = righthalf[j]
                    j += 1

                    self.sorter.redraw()
                k += 1
                k_or += 1

            while i < len(lefthalf):
                self.array[k] = lefthalf[i]
                arr[k_or] = lefthalf[i]
                i += 1
                k += 1
                k_or += 1

                self.sorter.redraw()

            while j < len(righthalf):
                self.array[k] = righthalf[j]
                arr[k_or] = righthalf[j]
                j += 1
                k += 1
                k_or += 1

                self.sorter.redraw()


class GnomeSort(Sort):

    def __init__(self, sorter: Sorter):
        self.sorter = sorter
        self.array = self.sorter.array_of_rects

    def execute(self):
        self._gnome()

    def _gnome(self):
        i, size = 1, len(self.array)
        while i < size:
            if self.array[i - 1].height <= self.array[i].height:
                i += 1
            else:
                self.sorter.swap_rects(self.array[i - 1], self.array[i])
                self.array[i - 1], self.array[i] = self.array[i], self.array[i - 1]
                if i > 1:
                    i -= 1


class RadixSort(Sort):

    def __init__(self, sorter: Sorter):
        self.sorter = sorter
        self.array = self.sorter.array_of_rects

    def execute(self):
        self._radix()

    def _counting_sort(self, exp1: int):
        n = len(self.array)
        output = [0] * (n)
        count = [0] * (10)

        for i in range(0, n):
            index = int(self.array[i].height / exp1)
            count[(index) % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = int(self.array[i].height / exp1)
            output[count[(index) % 10] - 1] = self.array[i]
            count[(index) % 10] -= 1
            i -= 1

        i = 0
        for i in range(0, len(self.array)):
            self.array[i] = output[i]
            self.sorter.redraw()

    def _radix(self):
        max1 = max(self.array).height
        exp = 1
        while self.array != sorted(self.array):
            self._counting_sort(exp)
            exp *= 10
