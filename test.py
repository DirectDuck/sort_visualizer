import gui
import algs

gui = gui.GUI()
gui.add_sort('Bubble', algs.BubbleSort)
gui.add_sort('Merge', algs.MergeSort)
gui.add_sort('Radix', algs.RadixSort)
gui.add_sort('Gnome', algs.GnomeSort)
gui.add_sort('Quick', algs.QuickSort)
gui.run()