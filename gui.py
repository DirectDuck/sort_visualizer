import PySimpleGUI as sg
from sorter import Sorter
import algs

class GUI:

    def __init__(self):
        self.width = 850
        self.height = 400
        self.algorithms = {}
        self.graph = sg.Graph((self.width, self.height),
                        (0, 0),
                        (self.width, self.height),
                        background_color='#fff', float_values=True)
        
        self.sorter = Sorter(self.graph)

        self.layout = [
            [sg.Button('Start')],

            [sg.Slider(range=(10, 200), orientation='horizontal', key='slider',
                       change_submits=True, disable_number_display=True),
             sg.Text('Array access: 0    ', key='text')],

            [self.graph],
        ]
        self.started = False
        self.slider_value = 0


    def draw_screen(self):
        self.sorter.graph.Erase()

        self.sorter.bar_width = int(self.sorter.graph.Size[0] / (self.slider_value * 2))
        free_space = self.sorter.graph.Size[0] - (self.sorter.bar_width + 1) * self.slider_value
        self.sorter.startx = int(free_space / 2)

        self.sorter._draw_rects(self.slider_value)

    def add_sort(self, name: str, algh: algs.Sort):
        self.layout[0].append(sg.Button(name))
        self.algorithms[name] = algh

    def run(self):
        window = sg.Window('Sorting Visualizer', self.layout, finalize=True)
        self.sorter.set_window(window)

        while True:
            event, values = window.read()

            if event in (None, 'Cancel'):
                break

            self.sorter.timeout = int(values['slider']) * 3 - 25

            if event == 'Start' or self.slider_value != int(values['slider']):
                self.started = True
                self.sorter.array_access = 0
                self.sorter.window.FindElement('text').Update('Array access: 0')
                self.slider_value = int(values['slider'])
                self.draw_screen()

            if self.started:
                for name, algh in self.algorithms.items():
                    if event == name:
                        self.sorter.algorithm = algh(self.sorter)
                        self.sorter.execute()
                        self.started = False
                        break


if __name__ == '__main__':
    gui = GUI()
    gui.add_sort('Bubble', algs.BubbleSort)
    gui.add_sort('Merge', algs.MergeSort)
    gui.add_sort('Radix', algs.RadixSort)
    gui.add_sort('Gnome', algs.GnomeSort)
    gui.add_sort('Quick', algs.QuickSort)
    gui.run()