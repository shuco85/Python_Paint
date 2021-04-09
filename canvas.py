from tkinter import ttk
import tkinter as tk

ROI_POINT_RADIUS = 5


class MyCanvas(tk.Canvas):
    def __init__(self, container):
        self.canvas_width = 600
        self.canvas_height = 400

        self.roi_points = {}
        self.current_point = None
        self.current_drawing_roi = []
        self.dragging = False

        super().__init__(container,
                         width=self.canvas_width,
                         height=self.canvas_height,
                         bg='black')

        self.bind('<B1-Motion>', self.move)
        self.bind('<ButtonPress-1>', self._create_circle_by_event)
        self.bind('<ButtonRelease-1>', self.stop_move)
        self.bind('<Double-Button-1>', self._end_roi_by_event)
        self.bind('<Button-1>', self._create_circle_by_event)
        self.bind('<Button-2>', self._delete_circle_by_event)
        self.bind("<Motion>", self.check_hand)  # binding to motion

    def move(self, event):
        if self.current_point is not None:
            self.dragging = True
            self.change_circle_position(self.current_point, event.x, event.y)
            self.roi_points[self.current_point] = (event.x, event.y)
            self._print_roi_from_points()

            if self.current_point == 9999999:
                self.roi_points[list(self.roi_points.keys())[0]] = self.roi_points[self.current_point]
            elif self.current_point == list(self.roi_points.keys())[0]:
                self.roi_points[9999999] = self.roi_points[self.current_point]

    def stop_move(self, event):
        if self.dragging:
            self.roi_points[self.current_point] = (event.x, event.y)
            self.dragging = False

    def _create_circle_by_event(self, event):
        if self.current_point is None:
            index = self.create_circle(event.x, event.y, ROI_POINT_RADIUS, fill='grey')
            self.roi_points[index] = (event.x, event.y)
            self._print_roi_from_points()

    def _print_roi_from_points(self):
        keys_list = list(self.roi_points.keys())
        for line in self.current_drawing_roi:
            self.delete(line)
        self.current_drawing_roi = []
        for index in range(len(keys_list) - 1):
            line = self.create_line(*self.roi_points[keys_list[index]],
                                    *self.roi_points[keys_list[index + 1]],
                                    fill='yellow')
            self.current_drawing_roi.append(line)

        print(self.current_drawing_roi)

    def _delete_circle_by_event(self, event):
        if self.current_point is not None:
            self.delete(self.current_point)
            self.roi_points.pop(self.current_point, None)
            self._print_roi_from_points()

    def _end_roi_by_event(self, event):
        if len(self.roi_points) >= 3:
            self.roi_points[9999999] = self.roi_points[list(self.roi_points.keys())[0]]
            self._print_roi_from_points()

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def change_circle_position(self, index, x, y):
        return self.coords(index,
                           x - ROI_POINT_RADIUS,
                           y - ROI_POINT_RADIUS,
                           x + ROI_POINT_RADIUS,
                           y + ROI_POINT_RADIUS)

    def check_hand(self, event):
        for index, roi_point in self.roi_points.items():
            if (
                    roi_point[0] - ROI_POINT_RADIUS < event.x < roi_point[0] + ROI_POINT_RADIUS and
                    roi_point[1] - ROI_POINT_RADIUS < event.y < roi_point[1] + ROI_POINT_RADIUS):
                self.config(cursor="cross")
                self.current_point = index
                return

        self.config(cursor="")
        self.current_point = None
