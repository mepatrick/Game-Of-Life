from tkinter import *
from random import *
from time import sleep
from math import *
import copy

root = Tk()
canvas_width = 400
canvas_height = 400
rect_size = 20
canvas = Canvas(width=canvas_width,height=canvas_height,bg='white')
canvas.grid()

class Cell():

    def __init__(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.alive = choice([True,False])
        self.cell = None

    def __str__(self):
        return "x: %s, y: %s, state: %s" % (self.pos_x,self.pos_y,self.alive)

    def drawCell(self):
        if self.cell != None:
            canvas.delete(self.cell)
        if self.alive:
            self.cell = canvas.create_rectangle(self.pos_x,self.pos_y,
                                    self.pos_x+rect_size,self.pos_y+rect_size,
                                    fill='black')
        else:
            self.cell = canvas.create_rectangle(self.pos_x,self.pos_y,
                                    self.pos_x+rect_size,self.pos_y+rect_size,
                                    fill='white')

    def changeState(self):
        self.alive = not self.alive

    def highlight(self):
        canvas.itemconfig(self.cell,fill='black')


class Board():

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.new_board = []
        self.board = []
        for i in range(self.width):
            l = []
            for j in range(self.height):
               l.append(Cell(i*rect_size,j*rect_size))
            self.board.append(l)

    def drawBoard(self):
        for row in self.board:
            for cell in row:
                cell.drawCell()

    def updateBoard(self):
        for row in self.new_board:
            for cell in row:
                cell.drawCell()

    def switchBoards(self):
        self.board = self.new_board
        self.new_board = []

    def cellAtMouseLocation(self,x,y):
        if x > self.width-1 or x < 0:
            return "No Cell"
        if y > self.height-1 or y < 0:
            return "No Cell"
        cell = self.board[x][y]
        return self.board[x][y]

    def four_neighbors(self,position):
        x,y = position
        N = [(x+1,y),(x+1,y+1),(x+1,y-1),(x-1,y),(x,y+1),(x,y-1),(x-1,y-1),(x-1,y+1)]
        return [self.board[a][b] for a,b in N if 0<=a<self.width and 0<=b<self.height]

    def generateNewBoard(self):
        for row in self.board:
            l = []
            for cell in row:
                copy_cell = copy.deepcopy(cell)
                l.append(copy_cell)
            self.new_board.append(l)

    def changeCellStates(self):
        for i,row in enumerate(self.board):
            for j,cell in enumerate(row):
                cellNeighbors = self.four_neighbors((int(cell.pos_x/rect_size),int(cell.pos_y/rect_size)))
                numOfAliveNeighbors = 0
                for neighbor in cellNeighbors:
                    if neighbor.alive:
                        numOfAliveNeighbors += 1
                if cell.alive and numOfAliveNeighbors < 2:
                    self.new_board[i][j].changeState()
                    
                if cell.alive and numOfAliveNeighbors > 3:
                    self.new_board[i][j].changeState()
                    
                if numOfAliveNeighbors == 3 and not cell.alive:
                    self.new_board[i][j].changeState()
                    
                
                
            

board = Board(20,20)

def click(e):
    x,y = floor(e.x/rect_size),floor(e.y/rect_size)
    cell = board.cellAtMouseLocation(x,y)
    if isinstance(cell,Cell):
        cell.changeState()
        cell.drawCell()

def run(e):
    board.generateNewBoard()
    board.changeCellStates()
    board.updateBoard()
    board.switchBoards()


#hold r to run, click to activate new cells
def main():
    board.drawBoard()
    root.bind('<Button-1>',click)
    root.bind('r',run)
    root.mainloop()
    

if __name__ == "__main__":
    main()
