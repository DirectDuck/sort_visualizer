
# Sort_visualizer
[![Downloads](https://pepy.tech/badge/sort-visualizer)](https://pepy.tech/project/sort-visualizer)

Sort_visualizer is a tool that will allow you to easily visualize any sorting algorithms

## Install

    pip install sort-visualizer

## Usage

### Short guide

 1. Install package
 2. Create `.py` and import package with `from sort_visualizer import gui, algs`
 3. Create your own sort (Or use ones you need from [algs.py](https://github.com/DirectDuck/sort_visualizer/blob/master/sort_visualizer/algs.py))
 4. Initialize gui object with `gui.GUI()` 
 5. Add sorting algorithms to gui via `test_gui.add_sort(NAME, SORT_CLASS)`
 > To add from `algs.py` simply use `test_gui.add_sort('Bubble', algs.BubbleSort)`, for example
6. Run gui with `test_gui.run()`

### How to write your own sort

In order to visualize your own sort you need to create a class that inherits from **algs.Sort** and implement **execute(self)** method.

To access array use **self.array**.

Every object in **self.array** is a **Rectangle** class instance. To access associated value use **.height** attribute.

Visual functions:
 - When an element changed its value use **self.redraw()** 
 - When swapping two elements of the array use **self.swap_rects(rect1: Rectangle, rect2: Rectangle)**

(Please note that **swap_rects** function only applies visual part, you still need to *actually swap the values in array*)

In [test.py](https://github.com/DirectDuck/sort_visualizer/blob/master/test.py) you can find example of creating your own algorithm and actually run python test.py` to see how it works.

To see more examples check [sort_visualizer/algs.py](https://github.com/DirectDuck/sort_visualizer/blob/master/sort_visualizer/algs.py)
