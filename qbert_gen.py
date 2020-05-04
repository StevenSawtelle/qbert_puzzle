def cmpr_lt(a,b):
  return ord(a) <= ord(b) if a and b else True

class Cube:
  def __init__(self, order):
    self.order = order
    self.touches = []
    self.left = None
    self.right = None
    self.top = None

  def validate(self):
    poss = cmpr_lt(self.left, self.right) and cmpr_lt(self.right, self.top) and cmpr_lt(self.left, self.top)
    # if not poss:
    #   print("not poss, left: " + (self.get_left() if self.get_left() else '') + " right: " + (self.get_right() if self.get_right() else '') + " top: " + (self.get_top() if self.get_top() else ''))
    return poss

  
  def get_order(self):
    return self.order
  def get_left(self):
    return self.left
  def get_top(self):
    return self.top
  def get_right(self):
    return self.right
  def get_touches(self):
    return self.touches

  def set_left(self, left):
    self.left = left
  def set_right(self, right):
    self.right = right
  def set_top(self, top):
    self.top = top
  def add_touches(self, ar):
    if(ar==self):
      self.touches.append(None)
      return
    self.touches.append(ar)

def print_grid(grid):
  for cube in grid:
    print ("cube " + cube.get_order())
    print("left: " + cube.get_left() if cube.get_left() else '')
    print("right: " + cube.get_right() if cube.get_right() else '')
    print("top: " + cube.get_top() if cube.get_top() else '')

def print_cubes(cubes):
  for cube in cubes:
    print(cube.order + " with neighbors:")
    for n in cube.get_touches():
      if n:
        print(n.order)
      else:
        print(n)

def map_cubes(cubes,i,others):
  for j in others:
    cubes[i].add_touches(cubes[j])
  
def init_grid():
  cubes = []
  for i in range(97,113):
    cubes.append(Cube(chr(i)))
  
  map_cubes(cubes, 0, [0,0,1,2])
  map_cubes(cubes, 1, [1,0,3,4])
  map_cubes(cubes, 2, [0,2,4,5])
  map_cubes(cubes, 3, [3,1,6,7])
  map_cubes(cubes, 4, [1,2,7,8])
  map_cubes(cubes, 5, [2,5,8,9])
  map_cubes(cubes, 6, [6,3,6,10])
  map_cubes(cubes, 7, [3,4,10,11])
  map_cubes(cubes, 8, [4,5,11,12])
  map_cubes(cubes, 9, [5,9,12,9])
  map_cubes(cubes, 10, [6,7,10,13])
  map_cubes(cubes, 11, [7,8,13,14])
  map_cubes(cubes, 12, [8,9,14,12])
  map_cubes(cubes, 13, [10,11,13,15])
  map_cubes(cubes, 14, [11,12,15,14])
  map_cubes(cubes, 15, [13,14,15,15])
  return cubes

def get_grid(cur_cube, visited, cur_idx, cur_path, goal_clue, goal_path, grid):
  # print_grid(grid)
  cur_path += cur_cube.get_order()
  # if(len(cur_path) > 13):
  #   print(cur_path)
  cur_cube.set_top(goal_path[cur_idx])
  if not cur_cube.validate():
    cur_cube.set_top(None)
    return (False, '')
  if len(cur_path) == len(goal_path):
    print("FOUND: ")
    print(cur_path)
    return (True, cur_path)
  visited[cur_cube.get_order()] = True
  # print(visited)
  for i in range(4):

    if i == 0 and cur_cube.get_touches()[i] and cur_cube.get_touches()[i].get_order() not in visited:
      # up left
      next_cube = cur_cube.get_touches()[i]
      next_cube.set_right(goal_clue[cur_idx])
      next_idx = cur_idx + 1
      temp,temp_path = get_grid(next_cube, dict(visited), next_idx, cur_path, goal_clue, goal_path, grid)
      if temp:
        return (temp, temp_path)
      next_cube.set_right(None)
    elif i == 1 and cur_cube.get_touches()[i] and cur_cube.get_touches()[i].get_order() not in visited:
      # up right
      next_cube = cur_cube.get_touches()[i]
      next_cube.set_left(goal_clue[cur_idx])
      next_idx = cur_idx + 1
      temp,temp_path = get_grid(next_cube, dict(visited), next_idx, cur_path, goal_clue, goal_path, grid)
      if temp:
        return (temp, temp_path)
      next_cube.set_left(None)
    elif i == 2 and cur_cube.get_touches()[i] and cur_cube.get_touches()[i].get_order() not in visited:
      # down left
      next_cube = cur_cube.get_touches()[i]
      cur_cube.set_left(goal_clue[cur_idx])
      if not cur_cube.validate():
        cur_cube.set_left(None)
        continue
      next_idx = cur_idx + 1
      temp,temp_path = get_grid(next_cube, dict(visited), next_idx, cur_path, goal_clue, goal_path, grid)
      if temp:
        return (temp, temp_path)
      cur_cube.set_left(None)
    elif i == 3 and cur_cube.get_touches()[i] and cur_cube.get_touches()[i].get_order() not in visited:
      # down right
      next_cube = cur_cube.get_touches()[i]
      cur_cube.set_right(goal_clue[cur_idx])
      if not cur_cube.validate():
        cur_cube.set_right(None)
        continue
      next_idx = cur_idx + 1
      temp,temp_path = get_grid(next_cube, dict(visited), next_idx, cur_path, goal_clue, goal_path, grid)
      if temp:
        return (temp, temp_path)
      cur_cube.set_right(None)
  # print("nothing found from here")
  cur_cube.set_top(None)
  del visited[cur_cube.get_order()]
  return (False, '')

grid = init_grid()
# print_cubes(grid)
#neighbors will be upper left, upper right, lower left, lower right
good_clues = {}
for i in range(0,16):
  goal_clues = ["GREENFOEOFQBERT", "QBERTSPURPLEFOE", "TOLEAPLIKEAFROG", "TOJUMPLIKEAFROG", "TOLEAPLIKEATOAD", "TOJUMPLIKEATOAD", "BOUNDSLIKEAFROG", "BOUNDSLIKEATOAD", "HOMEOFCAGEDBOAS", "TOLEAPASIFAFROG", "TOLEAPASIFATOAD", "TOMOVEASIFATOAD", "LEAPLIKEBUNNIES", "LEAPLIKEARABBIT", "LEAPLIKERABBITS", "MOVELIKERABBITS", "MOVELIKEBUNNIES", "MOVELIKEARABBIT", "JUMPOFAKANGAROO","MOVEOFAKANGAROO","LEAPOFAKANGAROO","JUMPASAKANGAROO", "MOVEASAKANGAROO", "LEAPASAKANGAROO", "BOUNCELIKEAHARE", "TOLEAPLIKEAHARE", "TOMOVELIKEAHARE", "TOJUMPLIKEAHARE", "ABUNNYSMANEUVER", "QBERTSPURPLEFOE", "QBERTSVIOLETFOE", "MYGREENFLAMEFOE", "GREENFLAMINGFOE"]
  goal_paths = ["PYTHONVIPERKRAIT", "PYTHONKRAITVIPER", "VIPERPYTHONKRAIT", "VIPERKRAITPYTHON", "VIPERASPRATKRAIT", "VIPERRATASPKRAIT", "VIPERPYTHONCOBRA", "VIPERCOBRAPYTHON", "COBRAPYTHONVIPER", "COBRAVIPERPYTHON", "PYTHONVIPERCOBRA", "PYTHONCOBRAVIPER", "VIPERPYTHONCORAL", "VIPERCORALPYTHON", "CORALPYTHONVIPER", "CORALVIPERPYTHON", "PYTHONVIPERCORAL", "PYTHONCORALVIPER", "VIPERPYTHONGRASS", "VIPERGRASSPYTHON", "GRASSPYTHONVIPER", "GRASSVIPERPYTHON", "PYTHONVIPERGRASS", "PYTHONGRASSVIPER"]
  # goal_clues = ["LEAPLIKEARABBIT"]
  # goal_paths = ["GRASSVIPERPYTHON"]
  for clue in goal_clues:
    for path in goal_paths:
      if(len(path) != len(clue) + 1):
        print("wrong lengths: " + path + " " + str(len(path)) + ' and ' + clue + str(len(clue)))
        break
      poss, fin_path = get_grid(grid[i], {}, 0, "", clue, path, grid)
      if poss and clue=="LEAPOFAKANGAROO":
        good_clues[clue] = True
        print("found for " + clue + " and " + path)
        print(fin_path)
        # print_grid(grid)


print(good_clues)
