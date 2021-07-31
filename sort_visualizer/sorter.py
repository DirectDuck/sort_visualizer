import random
import time
import PySimpleGUI as sg


class Rectangle:

    def __init__(self, rect_id: int, height: int):
        self.rect_id = rect_id
        self.height = height

    def highlight(self, graph: sg.Graph, color1: str, color2: str=None):
        if color2 is None:
            color2 = color1
        
        graph.TKCanvas.itemconfig(self.rect_id, fill=color1, outline=color2)

    def __gt__(self, other):
        return self.height > other.height


class Sorter:

    BLUE = '#64778d'
    BLUE_OUTLINE = '#5c6d81'
    MAGENTA = '#a26ba2'
    MAGENTA_OUTLINE = '#8d5d8d'
    GREEN = '#6ba970'
    GREEN_OUTLINE = '#5e9362'

    RECTANGLE_SPACING = 1

    def __init__(self, graph: sg.Graph):
        self._window = None
        self.graph = graph

        self.timeout = 0

        self.bar_width = 0
        self.start_x = 0

        self.array_of_rects = None
        self.values = None
        self.array_access = 0

        self._algorithm = None

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window: sg.Window):
        self._window = window

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algh):
        self._algorithm = algh

        self._algorithm.array = self.array_of_rects
        self._algorithm.swap_rects = self.swap_rects
        self._algorithm.redraw = self.redraw

    def _increment_array_access(self):
        self.array_access += 1
        self.window.FindElement('text').Update(
            f'Array access: {self.array_access}')

    def _reset_array_access(self):
        self.array_access = 0
        self.window.FindElement('text').Update(
            f'Array access: {self.array_access}')

    def _calculate_and_set_timeout(self, value: int, speed_modifier: float):
        self.timeout = (value * 3 - 25) * speed_modifier

    def _calculate_and_set_bar_width(self, value: int):
        self.bar_width = int(self.graph.Size[0] / (value * 2))

    def _calculate_and_set_start_x(self, value: int):
        free_space = self.graph.Size[0] - (self.bar_width + 1) * value
        self.start_x = int(free_space / 2)

    def execute(self):
        self._algorithm.execute()
        self._reset_all_rects_color()
        self._color_all_rects_green()

    def _draw_rects(self, slider_value: int):
        x1 = self.start_x
        x2 = x1 + self.bar_width

        self.array_of_rects = []
        self.values = []

        for _ in range(slider_value):
            height = random.randint(1, self.graph.Size[1])
            self.values.append(height)

            rectangle_id = self.graph.DrawRectangle(
                (x1, height),
                (x2, 0.0),
                fill_color=Sorter.BLUE,
                line_color=Sorter.BLUE_OUTLINE)
            self.array_of_rects.append(Rectangle(rectangle_id, height))
            
            x1 = x2 + self.RECTANGLE_SPACING
            x2 = x1 + self.bar_width

    def redraw(self):
        self._increment_array_access()

        self.graph.Erase()
        for i, elem in enumerate(self.array_of_rects):
            x1 = self.start_x + (i) * (self.bar_width + 1)
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

        self.window.Refresh()
        time.sleep(1 / self.timeout)

    def _reset_all_rects_color(self):
        for elem in self.array_of_rects:
            elem.highlight(self.graph, Sorter.BLUE, Sorter.BLUE_OUTLINE)
            self.window.Refresh()

    def _color_all_rects_green(self):
        for elem in self.array_of_rects:
            elem.highlight(self.graph, Sorter.GREEN, Sorter.GREEN_OUTLINE)
            self.window.Refresh()
            time.sleep(1 / self.timeout)

    def swap_rects(self, rect1: Rectangle, rect2: Rectangle):
        self._increment_array_access()

        rect1.highlight(self.graph, Sorter.MAGENTA, Sorter.MAGENTA_OUTLINE)
        rect2.highlight(self.graph, Sorter.MAGENTA, Sorter.MAGENTA_OUTLINE)
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

        rect1.highlight(self.graph, Sorter.BLUE, Sorter.BLUE_OUTLINE)
        rect2.highlight(self.graph, Sorter.BLUE, Sorter.BLUE_OUTLINE)
        self.window.Refresh()
