from reportlab.lib.colors import Color

class PostscriptInstructions:
    def __init__(self, canvas, x_coordinate_min, x_coordinate_max, y_coordinate_min, y_coordinate_max):
        self.canvas = canvas
        self.current_x = 0
        self.current_y = 0
        self.x_coordinate_min = x_coordinate_min
        self.x_coordinate_max = x_coordinate_max
        self.y_coordinate_min = y_coordinate_min
        self.y_coordinate_max = y_coordinate_max

    def parser_line(self, postscript_line_code):
        if 'rg' in postscript_line_code:
            self._handle_color(postscript_line_code)
        elif 'm' in postscript_line_code:
            self._handle_moveto(postscript_line_code)
        elif 'l' in postscript_line_code:
            self._handle_lineto(postscript_line_code)
        elif 're' in postscript_line_code:
            self._handle_rectangle(postscript_line_code)

    def _handle_color(self, line):
        r, g, b, *_ = line.split(" ")
        color = Color(float(r), float(g), float(b))
        self.canvas.setFillColor(color)

    def _handle_moveto(self, line):
        x, y, *_ = line.split(" ")
        self.current_x = float(x)
        self.current_y = float(y)

    def _handle_lineto(self, line):
        x, y, *_ = line.split(" ")
        x = float(x)
        y = float(y)
        if (self.x_coordinate_min < x < self.x_coordinate_max) and (
                self.y_coordinate_min < y < self.y_coordinate_max):
            self.canvas.line(self.current_x, self.current_y, x, y)
            self.current_x = x
            self.current_y = y

    def _handle_rectangle(self, line):
        x_coord, y_coord, width, height, *_ = line.split(" ")
        x_coord = float(x_coord)
        y_coord = float(y_coord)
        width = float(width)
        height = float(height)
        if (self.x_coordinate_min < x_coord < self.x_coordinate_max) and (
                self.y_coordinate_min < y_coord < self.y_coordinate_max):
            self.canvas.rect(x_coord, y_coord, width, height, fill=True, stroke=False)
