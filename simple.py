import PySimpleGUI as sg
import random
import time


class Rectangle:

    def __init__(self, rect_id, height):
        self.rect_id = rect_id
        self.height = height

    def highlight(self, graph, color1, color2=None):
        if color2 is None:
            color2 = color1
        graph.TKCanvas.itemconfig(self.rect_id, fill=color1, outline=color2)
        window.Refresh()

    def __gt__(self, other):
        return self.height > other.height


class Sorter:

    BLUE = '#64778d'
    BLUE_OUTLINE = '#5c6d81'
    MAGENTA = '#a26ba2'
    MAGENTA_OUTLINE = '#8d5d8d'
    GREEN = '#6ba970'
    GREEN_OUTLINE = '#5e9362'

    def __init__(self, window, graph):
        self.window = window
        self.graph = graph

        self.timeout = 0.1

        self.bar_width = 0
        self.startx = 0

        self.array_of_rects = None
        self.values = None
        self.array_access = 0

    def draw_rects(self, slider_value):
        x1 = self.startx
        x2 = x1 + self.bar_width
        k = 0
        self.array_of_rects = []
        self.values = []
        for _ in range(slider_value):
            number = random.randint(1, self.graph.Size[1])
            self.values.append(number)
            rectangle_id = self.graph.DrawRectangle(
                (x1, number),
                (x2, 0.0),
                fill_color=Sorter.BLUE,
                line_color=Sorter.BLUE_OUTLINE)
            self.array_of_rects.append(Rectangle(rectangle_id, number))
            x1 = x2 + 1
            x2 = x1 + self.bar_width

    def redraw(self):
        self.array_access += 1
        self.window.FindElement('text').Update(
            f'Array access: {self.array_access}')
        self.graph.Erase()

        for i, elem in enumerate(self.array_of_rects):
            x1 = self.startx + (i) * (self.bar_width + 1)
            if elem.height == self.values[i]:
                elem.rect_id = self.graph.DrawRectangle(
                    (x1, elem.height),
                    (x1 + self.bar_width, 0.0),
                    fill_color=Sorter.BLUE,
                    line_color=Sorter.BLUE_OUTLINE)
            else:
                self.values[i] = elem.height
                elem.rect_id = self.graph.DrawRectangle(
                    (x1, elem.height),
                    (x1 + self.bar_width, 0.0),
                    fill_color=Sorter.MAGENTA,
                    line_color=Sorter.MAGENTA_OUTLINE)

        window.Refresh()
        time.sleep(1 / self.timeout)

    def color_all_green(self):
        for elem in self.array_of_rects:
            elem.highlight(self.graph, Sorter.BLUE, Sorter.BLUE_OUTLINE)

        for elem in self.array_of_rects:
            elem.highlight(self.graph, Sorter.GREEN, Sorter.GREEN_OUTLINE)
            time.sleep(1 / self.timeout)

    def swap_rects(self, rect1, rect2):
        self.array_access += 1
        self.window.FindElement('text').Update(
            f'Array access: {self.array_access}')

        rect1.highlight(self.graph, Sorter.MAGENTA, Sorter.MAGENTA_OUTLINE)
        rect2.highlight(self.graph, Sorter.MAGENTA, Sorter.MAGENTA_OUTLINE)
        time.sleep(1 / self.timeout)

        rect1_upper_left_x = self.graph.GetBoundingBox(rect1.rect_id)[0][0]
        rect2_upper_left_x = self.graph.GetBoundingBox(rect2.rect_id)[0][0]

        delta1 = rect2_upper_left_x - rect1_upper_left_x
        delta2 = rect1_upper_left_x - rect2_upper_left_x

        self.graph.MoveFigure(rect1.rect_id, delta1, 0)
        self.graph.MoveFigure(rect2.rect_id, delta2, 0)

        self.window.Refresh()
        time.sleep(1 / self.timeout)

        rect1.highlight(self.graph, Sorter.BLUE, Sorter.BLUE_OUTLINE)
        rect2.highlight(self.graph, Sorter.BLUE, Sorter.BLUE_OUTLINE)

    def bubble(self):
        for i in range(len(self.array_of_rects) - 1):
            for j in range(len(self.array_of_rects) - i - 1):
                if self.array_of_rects[j].height > self.array_of_rects[j + 1].height:
                    self.swap_rects(
                        self.array_of_rects[j], self.array_of_rects[j + 1])
                    self.array_of_rects[j], self.array_of_rects[j +
                                                                1] = self.array_of_rects[j + 1], self.array_of_rects[j]
            self.window.Refresh()

    def partition(self, start, end):
        pivot = self.array_of_rects[start].height
        low = start + 1
        high = end

        while True:
            while low <= high and self.array_of_rects[high].height >= pivot:
                high = high - 1

            while low <= high and self.array_of_rects[low].height <= pivot:
                low = low + 1

            if low <= high:
                self.swap_rects(
                    self.array_of_rects[low], self.array_of_rects[high])
                self.array_of_rects[low], self.array_of_rects[high] = self.array_of_rects[high], self.array_of_rects[low]
            else:
                break

        self.swap_rects(self.array_of_rects[start], self.array_of_rects[high])
        self.array_of_rects[start], self.array_of_rects[high] = self.array_of_rects[high], self.array_of_rects[start]

        return high

    def quick_sort(self, start, end):
        if start >= end:
            return

        p = self.partition(start, end)
        self.quick_sort(start, p - 1)
        self.quick_sort(p + 1, end)

    def merge_sort(self, arr, startindex):
        if len(arr) > 1:
            mid = len(arr) // 2
            lefthalf = arr[:mid]
            righthalf = arr[mid:]

            self.merge_sort(lefthalf, int(startindex))
            self.merge_sort(righthalf, int(startindex + len(arr) / 2))

            i = 0
            j = 0
            k = startindex
            k_or = 0

            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i].height <= righthalf[j].height:
                    self.array_of_rects[k] = lefthalf[i]
                    arr[k_or] = lefthalf[i]
                    i += 1

                    self.redraw()
                else:
                    self.array_of_rects[k] = righthalf[j]
                    arr[k_or] = righthalf[j]
                    j += 1

                    self.redraw()
                k += 1
                k_or += 1

            while i < len(lefthalf):
                self.array_of_rects[k] = lefthalf[i]
                arr[k_or] = lefthalf[i]
                i += 1
                k += 1
                k_or += 1

                self.redraw()

            while j < len(righthalf):
                self.array_of_rects[k] = righthalf[j]
                arr[k_or] = righthalf[j]
                j += 1
                k += 1
                k_or += 1

                self.redraw()

    def gnome(self):
        i, size = 1, len(self.array_of_rects)
        while i < size:
            if self.array_of_rects[i - 1].height <= self.array_of_rects[i].height:
                i += 1
            else:
                self.swap_rects(
                    self.array_of_rects[i - 1], self.array_of_rects[i])
                self.array_of_rects[i -
                                    1], self.array_of_rects[i] = self.array_of_rects[i], self.array_of_rects[i - 1]
                if i > 1:
                    i -= 1

    def counting_sort(self, exp1):
        n = len(self.array_of_rects)
        output = [0] * (n)
        count = [0] * (10)

        for i in range(0, n):
            index = int(self.array_of_rects[i].height / exp1)
            count[(index) % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = int(self.array_of_rects[i].height / exp1)
            output[count[(index) % 10] - 1] = self.array_of_rects[i]
            count[(index) % 10] -= 1
            i -= 1

        i = 0
        for i in range(0, len(self.array_of_rects)):
            self.array_of_rects[i] = output[i]
            self.redraw()

    def radix(self):
        max1 = max(self.array_of_rects).height
        exp = 1
        while self.array_of_rects != sorted(self.array_of_rects):
            self.counting_sort(exp)
            exp *= 10


WIDTH = 850
HEIGHT = 400

graph = sg.Graph((WIDTH, HEIGHT),
                 (0, 0),
                 (WIDTH, HEIGHT),
                 background_color='#fff', float_values=True)

layout = [
    [sg.Button('Start'),
     sg.Button('Merge'),
     sg.Button('Quicksort'),
     sg.Button('Bubble'),
     sg.Button('Gnome'),
     sg.Button('Radix')],

    [sg.Slider(range=(10, 200), orientation='horizontal', key='slider',
               change_submits=True, disable_number_display=True),
     sg.Text('Array access: 0    ', key='text')],

    [graph],
]


def draw_screen(sorter, slider_value):
    sorter.graph.Erase()

    sorter.bar_width = int(sorter.graph.Size[0] / (slider_value * 2))
    free_space = sorter.graph.Size[0] - (sorter.bar_width + 1) * slider_value
    sorter.startx = int(free_space / 2)

    sorter.draw_rects(slider_value)


window = sg.Window('Sorting Visualizer', layout, finalize=True)

sorter = Sorter(window, graph)

started = False
slider_value = 0

while True:
    event, values = window.read()

    if event in (None, 'Cancel'):
        break

    sorter.timeout = int(values['slider']) * 3 - 25

    if event == 'Start' or slider_value != int(values['slider']):
        started = True
        sorter.array_access = 0
        sorter.window.FindElement('text').Update('Array access: 0')
        slider_value = int(values['slider'])
        draw_screen(sorter, slider_value)

    if started:
        if event == 'Merge':
            sorter.merge_sort(sorter.array_of_rects, 0)
            sorter.color_all_green()
            started = False

        if event == 'Bubble':
            sorter.bubble()
            sorter.color_all_green()
            started = False

        if event == 'Quicksort':
            sorter.quick_sort(0, len(sorter.array_of_rects) - 1)
            sorter.color_all_green()
            started = False

        if event == 'Gnome':
            sorter.gnome()
            sorter.color_all_green()
            started = False

        if event == 'Radix':
            sorter.radix()
            sorter.color_all_green()
            started = False
