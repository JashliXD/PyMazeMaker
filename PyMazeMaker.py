import pygame as py

py.init()

WIDTH = 600

win = py.display.set_mode((WIDTH,WIDTH))
py.display.set_caption("Boxes")


WHITE = (255,255,255)
GREY = (100,100,100)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

PlayerPosition = (0,0)

class Spot:
	def __init__(self,row,col,WIDTH,total_rows):
		self.row = row
		self.col = col
		self.x = row * WIDTH
		self.y = col * WIDTH
		self.color = WHITE
		self.WIDTH = WIDTH
		self.total_rows = total_rows
		self.adjacent = {"upper": [None,None], "lower": [None,None], "left": [None,None], "right": [None,None]}

	def get_pos(self):
		return self.row, self.col

	def block(self):
		return self.color == BLACK

	def open(self):
		return self.color == WHITE

	def reset(self):
		self.color = WHITE

	def make_block(self):
		self.color = BLACK

	def make_player(self):
		self.color = GREEN

	def make_flag(self):
		self.color = BLUE

	def draw(self, win):
		py.draw.rect(win, self.color, (self.x,self.y,self.WIDTH,self.WIDTH))

	def update(self,grid):

		#BLOCKED

		if self.row != self.total_rows-1:
			if grid[self.row+1][self.col].block():
				self.adjacent["right"] = [self.row+1,self.col]

		if grid[self.row-1][self.col].block():
			self.adjacent["left"]=[self.row-1,self.col]
		if self.col != self.total_rows-1:
			if grid[self.row][self.col+1].block():
				self.adjacent["lower"]=[self.row,self.col+1]
		if grid[self.row][self.col-1].block():
			self.adjacent["upper"]=[self.row,self.col-1]

		#OPENED
		if self.row != self.total_rows-1:
			if grid[self.row+1][self.col].open():
				self.adjacent["right"] = [None,None]

		if self.row != self.total_rows-1:
			if grid[self.row-1][self.col].open():
				self.adjacent["left"]=[None,None]
		if self.col != self.total_rows-1:
			if grid[self.row][self.col+1].open():
				self.adjacent["lower"]=[None,None]
		if grid[self.row][self.col-1].open():
			self.adjacent["upper"]=[None,None]

def generatebox (rows ,width):
	grid = []
	gap =  width // rows
	for x in range(rows):
		grid.append([])
		for y in range(rows):
			spot = Spot(x,y,gap,rows)
			grid[x].append(spot)

	return grid

def drawBox(win,rows,width):
	gap = width // rows
	for x in range(rows):
		py.draw.line(win, GREY, (0, x * gap), (width, x * gap))
		for y in range(rows):
			py.draw.line(win, GREY, (y * gap, 0), (y * gap, width))

def draw(win,grid,rows,width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	drawBox(win, rows,width)
	py.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

run = True

ROWS = 20 # 20 normal in this project
grids = generatebox(ROWS,WIDTH)

PlayerSpot = None
FinishFlag = None

pressed = False


while run:
	draw(win,grids,ROWS,WIDTH)

	for event in py.event.get():
		if event.type == py.QUIT:
			run = False
		if py.mouse.get_pressed()[0]:
			pos = py.mouse.get_pos()
			row,col = get_clicked_pos(pos,ROWS,WIDTH)
			spot = grids[row][col]
			if not PlayerSpot and spot != FinishFlag:
				PlayerSpot = spot
				PlayerSpot.make_player()
			if not FinishFlag and spot != PlayerSpot:
				FinishFlag = spot
				FinishFlag.make_flag()
			elif spot != PlayerSpot and spot != FinishFlag:
				spot.make_block()
		if py.mouse.get_pressed()[2]:
			pos = py.mouse.get_pos()
			row,col = get_clicked_pos(pos,ROWS,WIDTH)
			spot = grids[row][col]
			spot.reset()
			if spot == PlayerSpot:
				PlayerSpot = None
			if spot == FinishFlag:
				FinishFlag = None
		if py.mouse.get_pressed()[1]:
			print("EEE")
		if event.type == py.KEYDOWN: # PRESSED
			if event.key == py.K_w and not pressed:
				pressed = True
				if (PlayerSpot != None):
					if PlayerSpot.col == 0:
						PlayerSpot.reset()
						col = 0
						row = PlayerSpot.row
						spot = grids[row][col]
						PlayerSpot = spot
					else:
						if PlayerSpot.adjacent["upper"][1] == PlayerSpot.col - 1:
							PlayerSpot.reset()
							col = PlayerSpot.col
							row = PlayerSpot.row
							spot = grids[row][col]
							PlayerSpot = spot
						else:
							PlayerSpot.reset()
							col = PlayerSpot.col - 1
							row = PlayerSpot.row
							spot = grids[row][col]
							PlayerSpot = spot
			if event.key == py.K_s and not pressed:
				pressed = True
				if (PlayerSpot != None):
					if PlayerSpot.col == 19:
						row = PlayerSpot.row
						col = 19
						spot = grids[row][col]
						PlayerSpot = spot
					else:
						if PlayerSpot.adjacent["lower"][1] == PlayerSpot.col + 1:
							PlayerSpot.reset()
							col = PlayerSpot.col
							row = PlayerSpot.row
							spot = grids[row][col]
							PlayerSpot = spot
						else:
							PlayerSpot.reset()
							col = PlayerSpot.col + 1
							row = PlayerSpot.row
							spot = grids[row][col]
							PlayerSpot = spot
			if event.key == py.K_a and not pressed:
				pressed = True
				if PlayerSpot != None:
					if PlayerSpot.row == 0:
						PlayerSpot.reset()
						col = PlayerSpot.col
						row = 0

						spot = grids[row][col]
						PlayerSpot = spot
					else:	
						if PlayerSpot.adjacent["left"][0] == PlayerSpot.row - 1:
							PlayerSpot.reset()
							col = PlayerSpot.col
							row = PlayerSpot.row
							spot = grids[row][col]
							PlayerSpot = spot
						else:
							PlayerSpot.reset()
							col = PlayerSpot.col
							row = PlayerSpot.row - 1
							spot = grids[row][col]
							PlayerSpot = spot
			if event.key == py.K_d and not pressed:
				pressed = True
				if (PlayerSpot != None):
					if PlayerSpot.row == 19:
						PlayerSpot.reset()
						row = 19
						col = PlayerSpot.col

						spot = grids[row][col]
						PlayerSpot = spot
						PlayerSpot.update(grids)
					else:
						if PlayerSpot.adjacent["right"][0] == PlayerSpot.row + 1:
							PlayerSpot.reset()
							col = PlayerSpot.col
							row = PlayerSpot.row
							spot = grids[row][col]
							PlayerSpot = spot
						else:
							PlayerSpot.reset()
							col = PlayerSpot.col
							row = PlayerSpot.row + 1
							spot = grids[row][col]
							PlayerSpot = spot
		if event.type == py.KEYUP:
			if event.key == py.K_w or event.key == py.K_a or event.key == py.K_s or event.key == py.K_d:
				pressed = False


	if PlayerSpot != None:
		if FinishFlag != None:
			if PlayerSpot == FinishFlag:
				PlayerSpot = None
				FinishFlag = None
				grids = generatebox(ROWS, WIDTH)
	if PlayerSpot != None:
		PlayerSpot.update(grids)
		PlayerSpot.make_player()