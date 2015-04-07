class Field:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.coords = [[] for i in range(height)]

    def print_field(self):
        for i in range(1, self.width + 1):
            print('  ', end=str(i))
        print()
        for i in range(self.height):
            print(chr(ord('A') + i), end=' ')
            for j in range(self.width):
                print(self.coords[i][j] if self.coords[i][j] is not None
                      else '..', end=' ')
            print()
