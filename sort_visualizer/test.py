from sort_visualizer import gui, algs
'''
In order to visualize your own sort you 
need to create a class that inherits from 
algs.Sort and implement execute(self) method.

To access array use self.array.

Every object in self.array is a Rectangle class
instance. To access associated value use .height attribute.

Visual functions:
When an element changed its value use self.redraw()
When swapping two elements of the array use 
self.swap_rects(rect1: Rectangle, rect2: Rectangle)
(Please note that swap_rects function only applies visual
part, you still need to actually swap the values in array)

To see more examples check algs.py
'''


class TestBubbleSort(algs.Sort):

    def execute(self):
        for i in range(len(self.array) - 1):
            for j in range(len(self.array) - i - 1):
                if self.array[j].height > self.array[j + 1].height:
                    self.swap_rects(self.array[j], self.array[j + 1])
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]


if __name__ == '__main__':
    test_gui = gui.GUI()

    test_gui.add_sort('Bubble', algs.BubbleSort)
    test_gui.add_sort('Merge', algs.MergeSort)
    test_gui.add_sort('Radix', algs.RadixSort)
    test_gui.add_sort('Gnome', algs.GnomeSort)
    test_gui.add_sort('Quick', algs.QuickSort)
    test_gui.add_sort('Test', TestBubbleSort)

    test_gui.run()