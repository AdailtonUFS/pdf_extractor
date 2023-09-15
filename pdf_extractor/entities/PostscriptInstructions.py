from reportlab.lib.colors import Color
from reportlab.lib import colors


class PostscriptInstructions:
    def __init__(self, canvas, x_coordinate_min, x_coordinate_max, y_coordinate_min, y_coordinate_max):
        self.path_points = []
        self.canvas = canvas
        self.current_x = 0
        self.current_y = 0
        self.x_scale = 1
        self.y_scale = 1
        self.x_coordinate_min = float(x_coordinate_min)
        self.x_coordinate_max = float(x_coordinate_max)
        self.y_coordinate_min = float(y_coordinate_min)
        self.y_coordinate_max = float(y_coordinate_max)

    def parser_line(self, postscript_line_code):
        instruction = postscript_line_code.split(" ")
        instruction_name = instruction[-1]

        match instruction_name:
            case 'rg':
                self._handle_fill_color(postscript_line_code)
            case 'RG':
                self._handle_stroke_color(postscript_line_code)
            case 'm':
                self._handle_moveto(postscript_line_code)
            case 'l':
                self._handle_lineto(postscript_line_code)
            case 're':
                self._handle_rectangle(postscript_line_code)
            case 'c':
                self._handle_curveto(postscript_line_code)
            case 'w':
                self._handle_setlinewidth(postscript_line_code)
            case 'd':
                self._handle_define_pattern(postscript_line_code)
            case 'cm':
                self._handle_scale(postscript_line_code)
            # case 'f*':  # Handle 'f*'
            #     self._handle_eofill()
            # case 'S':  # Handle 'S'
            #     pass
            # case 'h':  # Handle 'h'
            #     pass
            # case 'q':  # Handle 'q'
            #     pass
            case _:
                pass
                # print(postscript_line_code)

    def _handle_fill_color(self, line):
        r, g, b, *_ = line.split(" ")
        color = Color(float(r), float(g), float(b))
        self.canvas.setFillColor(color)

    def _handle_stroke_color(self, line):
        r, g, b, *_ = line.split(" ")
        color = Color(float(r), float(g), float(b))
        self.canvas.setStrokeColor(color)

    def _handle_moveto(self, line):
        x, y, *_ = line.split(" ")
        x = float(x)
        y = float(y)
        if not (self.x_coordinate_min < x < self.x_coordinate_max) and not (
                self.y_coordinate_min < y < self.y_coordinate_max):
            return

        self.current_x = x * self.x_scale
        self.current_y = y * self.y_scale

        self.path_points.append((self.current_x, self.current_y))

    def _handle_lineto(self, line):
        x, y, *_ = line.split(" ")
        x = float(x) * self.x_scale
        y = float(y) * self.y_scale
        if not (self.x_coordinate_min < x < self.x_coordinate_max) and not (
                self.y_coordinate_min < y < self.y_coordinate_max):
            return

        self.canvas.line(self.current_x, self.current_y, x, y)
        self.current_x = x
        self.current_y = y

    def _handle_rectangle(self, line):
        x_coord, y_coord, width, height, *_ = line.split(" ")
        x_coord = float(x_coord) * self.x_scale
        y_coord = float(y_coord) * self.y_scale
        if not (self.x_coordinate_min < x_coord < self.x_coordinate_max) and not (
                self.y_coordinate_min < y_coord < self.y_coordinate_max):
            return

        width = float(width)
        height = float(height)

        self.canvas.rect(x_coord, y_coord, width, height, fill=True, stroke=False)

    def _handle_curveto(self, line):
        x1, y1, x2, y2, x3, y3, *_ = line.split(" ")
        x1 = float(x1) * self.x_scale
        y1 = float(y1) * self.y_scale
        x2 = float(x2) * self.x_scale
        y2 = float(y2) * self.y_scale
        x3 = float(x3) * self.x_scale
        y3 = float(y3) * self.y_scale

        if (self.x_coordinate_min <= x1 <= self.x_coordinate_max and
                self.y_coordinate_min <= y1 <= self.y_coordinate_max and
                self.x_coordinate_min <= x3 <= self.x_coordinate_max and
                self.y_coordinate_min <= y3 <= self.y_coordinate_max):
            x4 = 2 * x2 - x3
            y4 = 2 * y2 - y3

            self.canvas.bezier(x1, y1, x2, y2, x3, y3, x4, y4)
            self.current_x = x3
            self.current_y = y3

    def _handle_setlinewidth(self, line):
        linewidth, *_ = line.split(" ")
        linewidth = float(linewidth)
        self.canvas.setLineWidth(linewidth)

    def _handle_define_pattern(self, line):
        pattern_values = line.strip("[]").split()[:-2]
        pattern = [float(value) for value in pattern_values]
        self.canvas.setStrokeColor(colors.green)
        self.canvas.setLineWidth(1)
        self.canvas.setDash(pattern)

    def _handle_scale(self, line):
        x, _, _, y, _, _, *_ = line.split(" ")
        x = float(x)
        y = float(y)
        self.x_scale = x
        self.y_scale = y

    def _handle_eofill(self):
        path = self.canvas.beginPath()

        for i in range(len(self.path_points)):
            x, y = self.path_points[i]
            x = x * self.x_scale
            y = y * self.y_scale
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)

        path.close()
        self.canvas.saveState()
        self.canvas.clipPath(path, stroke=0, fill=1)
        self.canvas.rect(
            self.x_coordinate_min, self.y_coordinate_min,
            self.x_coordinate_max - self.x_coordinate_min, self.y_coordinate_max - self.y_coordinate_min,
            fill=1, stroke=0
        )
        self.canvas.restoreState()
