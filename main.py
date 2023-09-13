# Send list of possible cubes with piece to put in current cube
def put_piece_in_cube(piece,cube):
    current_face_index = None
    for i,f in enumerate(cube):
        is_empty = True
        for l in f:
            if 1 in l:
                is_empty = False
                break
        if is_empty:
            current_face_index = i
            break

    cubes_result = []

    # In case of inital face we just put it in the cube
    if current_face_index == 0:
        cube[0] = piece
        return [cube]
    
    #In case of putting another face
    elif current_face_index == 1:
        target = [int(not i) for i in cube[0][0]]
        for i,s in enumerate(piece):
            if s == target:
                cube_copy = cube.copy()
                cube_copy[0][0] = [1]*5
                cube_copy[1] = [piece[(j+i)%4] for j in range(4)]
                cube_copy[1][0] = [1]*5
                cubes_result.append(cube_copy)
            if [s[4-i] for i in range(4)] == target:
                cube_copy = cube.copy()
                cube_copy[0][0] = [1]*5
                cube_copy[1] = [piece[(j+i)%4] for j in range(4)]
                cube_copy[1][0] = [1]*5
                cubes_result.append(cube_copy)

# DFS back-tracking algorithm with brute force
def make_cube(pieces_list,cube=None):
    if cube is None:
        cube = [[[0] * 5 for _ in range(4)] for _ in range(6)]
        
    # Check if cube is complete, if it is the case return True else continue
    break_check_loop = False
    for face in cube:
        for line in face:
            if 0 in line:
                break_check_loop = True
                break
        if break_check_loop:
            break
    # If there is no 0 in the cube, the cube is complete and return True
    if not break_check_loop:
        return True
    
    # We try for each piece to have every combinations possibles
    for piece in pieces_list:
        # List of every cubes possibles for every rotation possibles
        cube_next_list = put_piece_in_cube(piece,cube)
        if cube_next_list is None:
            continue

        for cube_next in cube_next_list:
            pieces_list_copy = pieces_list.copy()
            pieces_list_copy.remove(piece)
            if make_cube(pieces_list_copy, cube_next):
                return True
    
    # If no possible combinations has been found, the cube is not possible for current configuration
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

make_cube(pieces_list)