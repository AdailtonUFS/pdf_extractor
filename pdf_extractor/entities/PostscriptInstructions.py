from reportlab.lib.colors import Color


class PostscriptInstructions:
    def __init__(self, canvas):
        self.canvas = canvas

    def parser_line(self, postscript_line_code):
        if 'rg' in postscript_line_code:
            r, g, b, *_ = postscript_line_code.split(" ")
            color = Color(float(r), float(g), float(b))
            self.canvas.setFillColor(color)

        if 're' in postscript_line_code:
            x_coord, y_coord, width, height, *_ = postscript_line_code.split(" ")
            x_coord = float(x_coord)
            y_coord = float(y_coord)
            width = float(width)
            height = float(height)

            self.canvas.rect(x_coord, y_coord, width, height, fill=True, stroke=False)
