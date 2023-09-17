import copy
import pprint
import visualizer
pp = pprint.PrettyPrinter(indent=4)

# Set debug to True to have a visualizer displaying the algorithm execution
debug = False

""" 
Assembled cube format:
              _____________ 
             |    0        |
             |3   <f:1>   3|
             |    2        |
_____________|_____________|_____________
|    0       |    0        |     0       |
|3   <f:3>  1|3   <f:0>   1|3    <f:2>  1|
|    2       |    2        |     2       |
|____________|_____________|_____________|
             |    0        |
             |3   <f:4>   1|
             |    2        |
             |_____________|
             |    0        |
             |3   <f:5>   1|
             |    2        |
             |_____________|
"""

class Cube:
    def __init__(self,piece) -> None:
        # initalize empty cube then add first piece in
        self.matrix = [[[0] * 5 for _ in range(4)] for _ in range(6)]
        self.matrix[0] = copy.deepcopy(piece.matrix)
        self.face_to_add = 1

    # Load every possible cubes by adding piece to current cube
    def possible_next_cubes(self,piece):
        cubes_result = []

        # Define targeted piece side
        if self.face_to_add == 1:
            target = {2:self.matrix[0][0]}
        elif self.face_to_add == 2:
            target = {0:self.matrix[1][1],
                       3:self.matrix[0][1]}
        elif self.face_to_add == 3:
            target = {1:self.matrix[0][3],
                       0:self.matrix[1][3]}
        elif self.face_to_add == 4:
            target = {0:self.matrix[0][2],
                       1:self.matrix[2][2],
                       3:self.matrix[3][2]}
        elif self.face_to_add == 5:
            target = {0:self.matrix[4][2],
                       1:self.matrix[2][1],
                       2:self.matrix[1][0],
                       3:self.matrix[3][3]}     

        #print("face to add:",self.face_to_add)
        #print("target:",target)       

        # Check if piece match targeted piece side by rotating it in every directions possibles
        for i in range(8):
            valid_piece = True
            for key in target:
                #pp.pprint(piece.matrix[key])
                if self.collision_detector(piece.matrix[key],target[key][::-1]):
                    valid_piece = False
                    break
            if valid_piece:
                cube_copy = copy.deepcopy(self)
                cube_copy.fill(piece,self.face_to_add)
                cubes_result.append(cube_copy)
            piece.rotate()
            if i == 3:
                piece.reverse()
        #pp.pprint([c.matrix for c in cubes_result])
        return cubes_result
    
    @staticmethod
    def collision_detector(a,b):
        if (a[0] & b[0]) or (a[-1] & b[-1]):
            return True
        for i in range(1,4):
            if a[i] == b[i]:
                return True
        return False
    
    # Fill current cube with piece
    def fill(self,piece,face):                 
        def slot_pieces(self,face1,side1,face2,side2):
            angle_left = self.matrix[face1][side1][0] | self.matrix[face2][side2][-1]
            angle_right = self.matrix[face1][side1][-1] | self.matrix[face2][side2][0]

            self.matrix[face1][side1] = [angle_left] + [1]*3 + [angle_right]
            self.matrix[face1][(side1-1)%4][-1] = angle_left
            self.matrix[face1][(side1+1)%4][0] = angle_right
            
            self.matrix[face2][side2] = [angle_right] + [1]*3 + [angle_left]
            self.matrix[face2][(side2-1)%4][-1] = angle_right
            self.matrix[face2][(side2+1)%4][0] = angle_left

        self.matrix[face] = copy.deepcopy(piece.matrix)      
        match face:
            case 1:
                slot_pieces(self,0,0,1,2)         
            case 2:
                slot_pieces(self,0,1,2,3)   
                slot_pieces(self,1,1,2,0)    
            case 3:
                slot_pieces(self,0,3,3,1)    
                slot_pieces(self,1,3,3,0)    
            case 4: 
                slot_pieces(self,0,2,4,0)   
                slot_pieces(self,3,2,4,3)   
                slot_pieces(self,2,2,4,1)  
            case 5:
                slot_pieces(self,5,0,4,2)  
                slot_pieces(self,5,1,2,1)  
                slot_pieces(self,5,2,1,0)  
                slot_pieces(self,5,3,3,3)  
                
        self.face_to_add = face+1                   

class Piece:
    def __init__(self, edge_matrix) -> None:
        self.matrix = edge_matrix
    def rotate(self):
        self.matrix = [self.matrix[(i-1)%4] for i in range(4)]
    
    def reverse(self):
        self.matrix[0] = self.matrix[0][::-1]
        self.matrix[2] = self.matrix[2][::-1]
        self.matrix[1],self.matrix[3] = self.matrix[3][::-1],self.matrix[1][::-1]

def make_cube(pieces_list, cube=None, visu=None):
    if cube is None:
        # Cube initialisation
        cube = Cube(pieces_list.pop(0))     

    if debug:
        if visu is None:
            visu = visualizer.Visualizer(cube.matrix)
        visu.update_display(cube.matrix)

    if pieces_list == []:
        return True
    
    for i,piece in enumerate(pieces_list):
        cube_next_list = cube.possible_next_cubes(piece)
        if cube_next_list == []:
            continue
        pieces_list_copy = copy.deepcopy(pieces_list)
        pieces_list_copy.pop(i)
        for cube_next in cube_next_list:
            if make_cube(pieces_list_copy, cube_next, visu):
                return True        
    return False
    

pieces_list = [[[1,1,0,1,1],
                [1,0,1,0,0],
                [0,1,0,1,0],
                [0,0,1,0,1]],

               [[0,0,1,0,1],
                [1,1,0,1,1],
                [1,1,0,1,0],
                [0,0,1,0,0]],

                [[1,1,0,1,0],
                 [0,1,0,1,0],
                 [0,1,0,1,0],
                 [0,0,1,0,1]],

                [[1,0,1,0,0],
                 [0,1,0,1,1],
                 [1,0,1,0,0],
                 [0,1,0,1,1]],

                [[1,1,0,1,0],
                 [0,0,1,0,0],
                 [0,0,1,0,0],
                 [0,0,1,0,1]],

                [[0,1,0,1,0],
                 [0,0,1,0,0],
                 [0,1,0,1,0],
                 [0,0,1,0,0]]]

print("Could we create a cube with these pieces ?")
if make_cube([Piece(p) for p in pieces_list]):
    print("Yes")
else:
    print("No")