import tkinter as tk
import random
import copy

class Visualizer:
    def __init__(self, matrices):
        self.root = tk.Tk()
        self.root.title("Matrix Display")
        self.cell_size = 16
        self.update_display(matrices)

    @staticmethod
    def random_color():
        # Generate a random color in hexadecimal format
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def display_matrix(self,matrix, row, col, root, cell_size):
        draw_matrix = [[0 for _ in range(5)] for _ in range(5)]
        draw_matrix[0] = matrix[0]
        for i in range(1, 4):
            draw_matrix[i][-1] = matrix[1][i]
        draw_matrix[4] = matrix[2][::-1]    
        for i in range(3,0,-1):
            draw_matrix[i][0] = matrix[3][i]

        for i in range(1,4):
            for j in range(1,4):
                draw_matrix[i][j] = 1

        rows = len(draw_matrix)
        cols = len(draw_matrix[0])
        color = self.random_color()
        for i in range(rows):
            for j in range(cols):
                if draw_matrix[i][j] == 1:
                    frame = tk.Frame(root, width=cell_size, height=cell_size, bg=color)
                else:
                    frame = tk.Frame(root, width=cell_size, height=cell_size)
                frame.grid(row=row + i, column=col + j)

    @staticmethod
    def clear_window(parent):
        # Destroy all widgets (frames) in the parent widget
        for widget in parent.winfo_children():
            widget.destroy()

    def update_display(self, matrices):
        matrices = copy.deepcopy(matrices)
        self.clear_window(self.root)

        row_position = 0
        col_position = 0
        
        position = [(1, 1), (0, 1), (1, 2), (1, 0), (2, 1), (3, 1)][::-1]
        for matrix in matrices:
            row_position, col_position = position.pop()
            row_position *= len(matrix)+1
            col_position *= len(matrix[0])+1
            self.display_matrix(matrix, row_position, col_position, self.root, self.cell_size)
        matrices.append(matrices.pop(0))

        self.root.update()