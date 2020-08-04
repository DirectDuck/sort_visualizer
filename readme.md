# Sort_visualizer

Sorting_visualizer is a tool that will allow you to easily visualize any sorting algorithms

## Usage

In order to visualize your own sort you need to create a class that inherits from **algs.Sort** and implement **execute(self)** method.

To access array use **self.array**.

Every object in **self.array** is a **Rectangle** class instance. To access associated value use **.height** attribute.

Visual functions:
 - When an element changed its value use **self.redraw()** 
 - When swapping two elements of the array use **self.swap_rects(rect1: Rectangle, rect2: Rectangle)**

(Please note that **swap_rects** function only applies visual part, you still need to *actually swap the values in array*)

In `test.py` you can find example of creating your own algorithm and actually run `python test.py` to see how it works.

To see more examples check `algs.py`
