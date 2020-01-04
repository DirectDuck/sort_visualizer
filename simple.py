import PySimpleGUI as sg
import random
import time


class Rectangle:

    def __init__(self, rect_id, y1):
        self.rect_id = rect_id
        self.y1 = y1

    def highlight(self, color):
        graph.TKCanvas.itemconfig(self.rect_id, fill=color)
        window.Refresh()


class Sorter:

    def __init__(self, window, graph):
        self.window = window
        self.graph = graph

        self.timeout = 0.1

        self.bar_width = 0
        self.startx = 0

        self.array = None
        self.r_values = None
        self.array_access = 0

    def draw_rects(self, slider_value):
        x1 = self.startx
        x2 = x1 + self.bar_width
        k = 0
        self.array = []
        self.r_values = []
        for i in range(slider_value):
            self.r_values.append(random.randint(1, HEIGHT))

        while True:
            rectangle_id = self.graph.DrawRectangle(
                (x1, float(self.r_values[k])), (x2, 0.0), fill_color='Black')
            self.array.append(Rectangle(rectangle_id, float(self.r_values[k])))
            k += 1
            x1 = x2 + 1
            x2 = x1 + self.bar_width
            if k >= len(self.r_values):
                break

    def redraw(self):
        self.array_access += 1
        self.window.FindElement('text').Update(f'Array access: {self.array_access}')
        self.graph.Erase()
        for i, elem in enumerate(self.array):
            x1 = self.startx + (i) * (self.bar_width + 1)
            elem.rect_id = self.graph.DrawRectangle(
                (x1, elem.y1), (x1 + self.bar_width, 0.0), fill_color='Black')
        window.Refresh()
        time.sleep(1 / self.timeout)

    def color_all_green(self):
        for elem in self.array:
            self.graph.TKCanvas.itemconfig(elem.rect_id, fill="Green")
            window.Refresh()
            time.sleep(1/self.timeout)

    def swap_rects(self, rect1, rect2):
        self.array_access += 1
        self.window.FindElement('text').Update(f'Array access: {self.array_access}')


        self.graph.TKCanvas.itemconfig(rect1.rect_id, fill="Green")
        self.graph.TKCanvas.itemconfig(rect2.rect_id, fill="Green")

        self.window.Refresh()
        time.sleep(1 / self.timeout)

        rect1_upper_left_x = self.graph.GetBoundingBox(rect1.rect_id)[0][0]
        rect2_upper_left_x = self.graph.GetBoundingBox(rect2.rect_id)[0][0]

        delta1 = rect2_upper_left_x - rect1_upper_left_x
        delta2 = rect1_upper_left_x - rect2_upper_left_x

        self.graph.MoveFigure(rect1.rect_id, delta1, 0)
        self.graph.MoveFigure(rect2.rect_id, delta2, 0)

        self.window.Refresh()
        time.sleep(1 / self.timeout)

        self.graph.TKCanvas.itemconfig(rect1.rect_id, fill="Black")
        self.graph.TKCanvas.itemconfig(rect2.rect_id, fill="Black")

        self.window.Refresh()

    def bubble(self):
        for i in range(len(self.array) - 1):
            for j in range(len(self.array) - i - 1):
                if self.array[j].y1 > self.array[j + 1].y1:
                    self.swap_rects(self.array[j], self.array[j + 1])
                    self.array[j], self.array[j +1] = self.array[j + 1], self.array[j]
            self.window.Refresh()

    def partition(self, start, end):
        pivot = self.array[start].y1
        low = start + 1
        high = end

        while True:
            while low <= high and self.array[high].y1 >= pivot:
                high = high - 1

            while low <= high and self.array[low].y1 <= pivot:
                low = low + 1

            if low <= high:
                self.swap_rects(self.array[low], self.array[high])
                self.array[low], self.array[high] = self.array[high], self.array[low]
            else:
                break

        self.swap_rects(self.array[start], self.array[high])
        self.array[start], self.array[high] = self.array[high], self.array[start]

        return high

    def quick_sort(self, start, end):
        if start >= end:
            return

        p = self.partition(start, end)
        self.quick_sort(start, p - 1)
        self.quick_sort(p + 1, end)

    def mergeSort(self, arr, startindex):
        if len(arr) > 1:
            mid = len(arr) // 2
            lefthalf = arr[:mid]
            righthalf = arr[mid:]

            self.mergeSort(lefthalf, int(startindex))
            self.mergeSort(righthalf, int(startindex + len(arr) / 2))

            i = 0
            j = 0
            k = startindex
            k_or = 0

            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i].y1 <= righthalf[j].y1:
                    self.array[k].highlight('Green')
                    lefthalf[i].highlight('Green')
                    temp = self.array[k]
                    time.sleep(1 / self.timeout)
                    self.array[k] = lefthalf[i]
                    arr[k_or] = lefthalf[i]
                    self.redraw()

                    i = i + 1
                else:
                    self.array[k].highlight('Green')
                    righthalf[j].highlight('Green')
                    temp = self.array[k]
                    time.sleep(1 / self.timeout)
                    self.array[k] = righthalf[j]
                    arr[k_or] = righthalf[j]
                    self.redraw()
                    j = j + 1
                k = k + 1
                k_or += 1

            while i < len(lefthalf):
                self.array[k].highlight('Green')
                lefthalf[i].highlight('Green')
                temp = self.array[k]
                time.sleep(1 / self.timeout)
                self.array[k] = lefthalf[i]
                arr[k_or] = lefthalf[i]
                self.redraw()
                i = i + 1
                k = k + 1
                k_or += 1

            while j < len(righthalf):
                self.array[k].highlight('Green')
                righthalf[j].highlight('Green')
                temp = self.array[k]
                time.sleep(1 / self.timeout)
                self.array[k] = righthalf[j]
                arr[k_or] = righthalf[j]
                self.redraw()
                j = j + 1
                k = k + 1
                k_or += 1

    def gnome(self):
        i, size = 1, len(self.array)
        while i < size:
            if self.array[i - 1].y1 <= self.array[i].y1:
                i += 1
            else:
                self.array[i - 1], self.array[i] = self.array[i], self.array[i - 1]
                self.swap_rects(self.array[i - 1], self.array[i])
                if i > 1:
                    i -= 1


WIDTH = 850
HEIGHT = 400

graph = sg.Graph((WIDTH, HEIGHT), (0, 0), (WIDTH, HEIGHT),
                 background_color='#ffffff', float_values=True)

layout = [
    [sg.Button('Start'),
     sg.Button('Merge'),
     sg.Button('Quicksort'),
     sg.Button('Bubble'),
     sg.Button('Gnome')],

    [sg.Slider(range=(10, 400), orientation='horizontal', key='slider',
               change_submits=True, disable_number_display=True),
    sg.Text('Array access: 0       ', key='text')],
    [graph],
]


def draw_screen(sorter, slider_value):
    sorter.graph.Erase()

    sorter.bar_width = int(WIDTH / (slider_value * 2))
    freespace = WIDTH - (sorter.bar_width + 1) * slider_value
    sorter.startx = int(freespace / 2)

    sorter.draw_rects(slider_value)


window = sg.Window('Window Title', layout, finalize=True)

sorter = Sorter(window, graph)

started = False

slider_value = 0

while True:
    event, values = window.read()

    if event in (None, 'Cancel'):
        break

    sorter.timeout = int(values['slider'])*3 - 25

    if event == 'Start' or slider_value != int(values['slider']):
        sorter.array_access = 0
        sorter.window.FindElement('text').Update('Array access: 0')
        started = True
        slider_value = int(values['slider'])
        draw_screen(sorter, slider_value)

    if event == 'Merge' and started:
        sorter.mergeSort(sorter.array, 0)
        sorter.color_all_green()
        started = False

    if event == 'Bubble' and started:
        sorter.bubble()
        sorter.color_all_green()
        started = False

    if event == 'Quicksort' and started:
        sorter.quick_sort(0, len(sorter.array) - 1)
        sorter.color_all_green()
        started = False

    if event == 'Gnome' and started:
        sorter.gnome()
        sorter.color_all_green()
        started = False
