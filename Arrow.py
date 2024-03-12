class Arrow:
    def __init__(self, arrow_type, arrow_x, arrow_y, length, width, color):
        self.arrow_type = arrow_type
        self.length = length
        self.width = width
        self.arrow_x = arrow_x
        self.arrow_y = arrow_y
        self.color = color
        self.points = []
        if arrow_type == "up":
            self.points.append(self.create_up(arrow_x, arrow_y))
        if arrow_type == "down":
            self.points.append(self.create_down(arrow_x, arrow_y))
        if arrow_type == "left":
            self.points.append(self.create_left(arrow_x, arrow_y))
        if arrow_type == "right":
            self.points.append(self.create_right(arrow_x, arrow_y))
        if arrow_type == "blank":
            self.points.append(self.create_blank(arrow_x, arrow_y))
        if arrow_type == "updown":
            self.points.append(self.create_up(arrow_x, arrow_y))
            self.points.append(self.create_down(arrow_x, arrow_y))
        if arrow_type == "leftright":
            self.points.append(self.create_left(arrow_x, arrow_y))
            self.points.append(self.create_right(arrow_x, arrow_y))

    def create_up(self, arrow_x, arrow_y):
        points = [
            (arrow_x // 2 - self.width // 2 + 200, arrow_y // 2 + self.length - self.width + 20),
            (arrow_x // 2 - self.width // 2 + 200, arrow_y // 2 + 20),
            (arrow_x // 2 - self.width + 200, arrow_y // 2 + 20),
            (arrow_x // 2 + 200, arrow_y // 2 - self.width + 20),
            (arrow_x // 2 + self.width + 200, arrow_y // 2 + 20),
            (arrow_x // 2 + self.width // 2 + 200, arrow_y // 2 + 20),
            (arrow_x // 2 + self.width // 2 + 200, arrow_y // 2 + self.length - self.width + 20)
        ]
        return points

    def create_down(self, arrow_x, arrow_y):
        points = [
            (arrow_x - self.width // 2 + 115, arrow_y // 2 - self.length + self.width + 20),
            (arrow_x // 2 - self.width // 2 + 120, arrow_y // 2 + 20),
            (arrow_x // 2 - self.width + 120, arrow_y // 2 + 20),
            (arrow_x // 2 + 120, arrow_y // 2 + self.width + 20),
            (arrow_x // 2 + self.width + 120, arrow_y // 2 + 20),
            (arrow_x // 2 + self.width // 2 + 120, arrow_y // 2 + 20),
            (arrow_x // 2 + self.width // 2 + 120, arrow_y // 2 - self.length + self.width + 20),
        ]
        return points

    def create_left(self, arrow_x, arrow_y):
        points = [
            (arrow_x // 2 + self.length - self.width + 40, arrow_y // 2 - self.width // 2),
            (arrow_x // 2 + 40, arrow_y // 2 - self.width // 2),
            (arrow_x // 2 + 40, arrow_y // 2 - self.width),
            (arrow_x // 2 - self.length + 70, arrow_y // 2),
            (arrow_x // 2 + 40, arrow_y // 2 + self.width),
            (arrow_x // 2 + 40, arrow_y // 2 + self.width // 2),
            (arrow_x // 2 + self.length - self.width + 40, arrow_y // 2 + self.width // 2)
        ]
        return points

    def create_right(self, arrow_x, arrow_y):
        points = [
            (arrow_x // 2 - self.length + self.width + 280, arrow_y // 2 - self.width // 2),
            (arrow_x // 2 + 280, arrow_y // 2 - self.width // 2),
            (arrow_x // 2 + 280, arrow_y // 2 - self.width),
            (arrow_x // 2 + self.length + 250, arrow_y // 2),
            (arrow_x // 2 + 280, arrow_y // 2 + self.width),
            (arrow_x // 2 + 280, arrow_y // 2 + self.width // 2),
            (arrow_x // 2 - self.length + self.width + 280, arrow_y // 2 + self.width // 2),
        ]
        return points

    def create_blank(self, arrow_x, arrow_y):

        points = [
            (arrow_x //2 + 380, arrow_y // 2- self.width), (arrow_x // 2+ 380, arrow_y //2), (arrow_x // 2+ 380 + self.length, arrow_y //2),
            (arrow_x //2 + 380 + self.length, arrow_y //2 - self.width),
        ]
        return points

    def update(self):
        self.points = []
        self.arrow_y += 3
        if self.arrow_type == "blank":
            self.points.append(self.create_blank(self.arrow_x, self.arrow_y))
        if self.arrow_type == "up":
            self.points.append(self.create_up(self.arrow_x, self.arrow_y))
        if self.arrow_type == "down":
            self.points.append(self.create_down(self.arrow_x, self.arrow_y))
        if self.arrow_type == "left":
            self.points.append(self.create_left(self.arrow_x, self.arrow_y))
        if self.arrow_type == "right":
            self.points.append(self.create_right(self.arrow_x, self.arrow_y))
        if self.arrow_type == "updown":
            self.points.append(self.create_up(self.arrow_x, self.arrow_y))
            self.points.append(self.create_down(self.arrow_x, self.arrow_y))
        if self.arrow_type == "leftright":
            self.points.append(self.create_left(self.arrow_x, self.arrow_y))
            self.points.append(self.create_right(self.arrow_x, self.arrow_y))
        return self.points

    def update_color(self, color):
        self.color = color
