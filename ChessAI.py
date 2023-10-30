import chess
import chess.svg
import  math


#Using sunfish piece values and pst
piece_values = {"P": 100, "N": 280, "B": 320, "R": 479, "Q": 929, "K": 60000}
pst = {
    'P': (   0,   0,   0,   0,   0,   0,   0,   0,
            78,  83,  86,  73, 102,  82,  85,  90,
             7,  29,  21,  44,  40,  31,  44,   7,
           -17,  16,  -2,  15,  14,   0,  15, -13,
           -26,   3,  10,   9,   6,   1,   0, -23,
           -22,   9,   5, -11, -10,  -2,   3, -19,
           -31,   8,  -7, -37, -36, -14,   3, -31,
             0,   0,   0,   0,   0,   0,   0,   0),
    'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
            -3,  -6, 100, -36,   4,  62,  -4, -14,
            10,  67,   1,  74,  73,  27,  62,  -2,
            24,  24,  45,  37,  33,  41,  25,  17,
            -1,   5,  31,  21,  22,  35,   2,   0,
           -18,  10,  13,  22,  18,  15,  11, -14,
           -23, -15,   2,   0,   2,   0, -23, -20,
           -74, -23, -26, -24, -19, -35, -22, -69),
    'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
           -11,  20,  35, -42, -39,  31,   2, -22,
            -9,  39, -32,  41,  52, -10,  28, -14,
            25,  17,  20,  34,  26,  25,  15,  10,
            13,  10,  17,  23,  17,  16,   0,   7,
            14,  25,  24,  15,   8,  25,  20,  15,
            19,  20,  11,   6,   7,   6,  20,  16,
            -7,   2, -15, -12, -14, -15, -10, -10),
    'R': (  35,  29,  33,   4,  37,  33,  56,  50,
            55,  29,  56,  67,  55,  62,  34,  60,
            19,  35,  28,  33,  45,  27,  25,  15,
             0,   5,  16,  13,  18,  -4,  -9,  -6,
           -28, -35, -16, -21, -13, -29, -46, -30,
           -42, -28, -42, -25, -25, -35, -26, -46,
           -53, -38, -31, -26, -29, -43, -44, -53,
           -30, -24, -18,   5,  -2, -18, -31, -32),
    'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
            14,  32,  60, -10,  20,  76,  57,  24,
            -2,  43,  32,  60,  72,  63,  43,   2,
             1, -16,  22,  17,  25,  20, -13,  -6,
           -14, -15,  -2,  -5,  -1, -10, -20, -22,
           -30,  -6, -13, -11, -16, -11, -16, -27,
           -36, -18,   0, -19, -15, -15, -21, -38,
           -39, -30, -31, -13, -31, -36, -34, -42),
    'K': (   4,  54,  47, -99, -99,  60,  83, -62,
           -32,  10,  55,  56,  56,  55,  10,   3,
           -62,  12, -57,  44, -67,  28,  37, -31,
           -55,  50,  11,  -4, -19,  13,   0, -49,
           -55, -43, -52, -28, -51, -47,  -8, -50,
           -47, -42, -43, -79, -64, -32, -29, -32,
            -4,   3, -14, -50, -57, -18,  13,   4,
            17,  30,  -3, -14,   6,  -1,  40,  18),
}


CENTER_SQUARES = [chess.D4, chess.E4, chess.D5, chess.E5]

def evaluate_position(board):
    if not board.is_valid():
        raise ValueError("Invalid board")
    
    # Check the game outcome
    result = board.result()
    if result == "1-0":
        return float('inf')  # White has won
    elif result == "0-1":
        return float('-inf')  # Black has won
    elif board.is_stalemate():
        return 0  # Stalemate

    score = 0
    
    can_castle = bool(board.castling_rights)
    if can_castle:
        castle = 50
    else: 
        castle = -50
    
    # Deduct points for undeveloped knights and bishops
    undeveloped_pieces = [
        (chess.B1, chess.KNIGHT, chess.WHITE),
        (chess.G1, chess.KNIGHT, chess.WHITE),
        (chess.C1, chess.BISHOP, chess.WHITE),
        (chess.F1, chess.BISHOP, chess.WHITE),
        (chess.B8, chess.KNIGHT, chess.BLACK),
        (chess.G8, chess.KNIGHT, chess.BLACK),
        (chess.C8, chess.BISHOP, chess.BLACK),
        (chess.F8, chess.BISHOP, chess.BLACK)
]

    
    for square, piece_type, color in undeveloped_pieces:
        piece = board.piece_at(square)
        if piece and piece.piece_type == piece_type and piece.color == color:
            score -= 10 if color == chess.WHITE else 10

    # Iterate through each square on the board
    for square in chess.SQUARES:
        # Get the piece at the current square
        piece = board.piece_at(square)
        if piece is None:
            continue
        
        # Bonus for controlling the center
        if square in CENTER_SQUARES:
            if piece.color == chess.WHITE:
                score += 10
            else:
                score -= 10
        
        # Get the piece type and color
        piece_type = piece.piece_type
        color = piece.color
        
        # Convert the piece_type to uppercase string representation
        piece_str = chess.piece_name(piece_type).upper()[0]
        
        # Get the piece value and piece-square table value
        piece_value = piece_values[piece_str]
        pst_value = pst[piece_str][square]
        
        # If the piece is white, add the values to the score, otherwise subtract them
        if color:
            score += (piece_value + pst_value + castle)
        else:
            score -= (piece_value + pst_value + castle)
    
    return score

# def evaluate_position(board):
#     if not board.is_valid():
#         raise ValueError("Invalid board")
    
#     # Check the game outcome
#     result = board.result()
#     if result == "1-0":
#         return float('inf')  # White has won
#     elif result == "0-1":
#         return float('-inf')  # Black has won
#     elif board.is_stalemate():
#         return 0  # Stalemate

#     score = 0
    
#     can_castle = bool(board.castling_rights)
#     if can_castle:
#         castle = 50
#     else: 
#         castle = -50
#     # Iterate through each square on the board
#     for square in chess.SQUARES:
#         # Get the piece at the current square
#         piece = board.piece_at(square)
#         if piece is None:
#             continue
        
#         # Get the piece type and color
#         piece_type = piece.piece_type
#         color = piece.color
        
#         # Convert the piece_type to uppercase string representation
#         piece_str = chess.piece_name(piece_type).upper()[0]
        
#         # Get the piece value and piece-square table value
#         piece_value = piece_values[piece_str]
#         pst_value = pst[piece_str][square]
        
#         # If the piece is white, add the values to the score, otherwise subtract them
#         if color:
#             score += (piece_value + pst_value + castle)
#         else:
#             score -= (piece_value + pst_value + castle)
    
#     return score


def minimax(board, depth:int, maximize:bool, alpha=-math.inf, beta=math.inf):
    if depth == 0 or board.is_game_over():
        return evaluate_position(board), None
    
    legal_moves = board.legal_moves
    best_move = None
    
    if maximize:
        maximum = -math.inf
        for move in legal_moves:
            board.push(move)
            evaluation, _ = minimax(board, depth-1, not maximize, alpha, beta)
            board.pop()
            if evaluation > maximum:
                maximum = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maximum, best_move
    else:
        minimum = math.inf
        for move in legal_moves:
            board.push(move)
            evaluation, _ = minimax(board, depth-1, not maximize, alpha, beta)
            board.pop()
            if evaluation < minimum:
                minimum = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minimum, best_move


def get_player_move(board):
    while True:
        ply_move = input("Enter your move using standard algebraic chess notation\n")
        try:
            ply_move_san = board.parse_san(ply_move)
            if ply_move_san in board.legal_moves:
                return ply_move_san  # Return the valid move
            else:
                print('That is not a legal move')
        except ValueError:
            print('That is not a valid move')

def main():
    board = chess.Board()
    color = input('Enter "w" to play as white or "b" to play as black\n').lower()
    maximizing = True
    if color == "w":
        while not board.is_game_over():
            print(board)
            ply_move_san = get_player_move(board)  # Call the function to get a valid player move
            board.push(ply_move_san)
    else:
        while not board.is_game_over():
            eval, cpu_move = minimax(board, 3, maximizing)
            board.push(cpu_move)
            print(f"The CPU played {cpu_move}")
            print(board)
            ply_move_san = get_player_move(board)  # Call the function to get a valid player move
            board.push(ply_move_san)
            print(bool(board.castling_rights))

if __name__ == "__main__":
    main()





# Joshs game
# board.push_san('e3')
# board.push_san('e5')
# board.push_san('Ke2')
# board.push_san('Ngf6')
# board.push_san('Kf3')
# board.push_san('d6')
# board.push_san('Qe1')
# board.push_san('Bg4')
# board.push_san('Kg3')
# board.push_san('Qd7')
# board.push_san('f3')
# board.push_san('Be6')
# board.push_san('Kf2')
# board.push_san('Nc6')
# board.push_san('Bb5')
# board.push_san('Be7')
# board.push_san('Bxc6')
# board.push_san('Qxc6')
# board.push_san('c3')
# board.push_san('O-O')
# board.push_san('Kf1')
# board.push_san('e4')
# board.push_san('f4')
# board.push_san('Bc4')
# board.push_san('Kf2')
# board.push_san('Nd7')
# board.push_san('f5')
# board.push_san('Ne5')
# board.push_san('Kg3')
# board.push_san('d5')
# board.push_san('d4')
# board.push_san('exd3')
# board.push_san('Bd2')
# board.push_san('Bd6')
# board.push_san('Qf2')
# board.push_san('h5')
# board.push_san('Qe1')
# board.push_san('Ng4')
# board.push_san('Kf3')
# board.push_san('d4')
# board.push_san('e4')
# board.push_san('Bxh2')
# board.push_san('Nh3')
# board.push_san('Bd6')
# board.push_san('cxd4')
# board.push_san('Rfe8')
# board.push_san('d5')
# board.push_san('Bxd5')
# board.push_san('Bf4')
# board.push_san('Bxe4')
# board.push_san('Qxe4')
# board.push_san('Qxe4')
# board.push_san('Kg3')
# board.push_san('Qe3')
# board.push_san('Kh4')
# board.push_san('Bxf4')
# board.push_san('Nxf4')
# board.push_san('Qxf4')
# board.push_san('g3')
# board.push_san('Qxf5')
# board.push_san('Rg1')
# board.push_san('Qf2')
# board.push_san('Kxh5')
# board.push_san('Qxg1')
# board.push_san('Kxg4')
# board.push_san('d2')
# board.push_san('Nxd2')
# board.push_san('Qxa1')
# board.push_san('b4')
# board.push_san('Re6')
# board.push_san('Kh3')
# board.push_san('Qh1')
# board.push_san('Kg4')
# board.push_san('Rg6')
# board.push_san('Kf4')
# board.push_san('Qf1')




# eval, move = minimax(board, 4, True)
# print(eval, move)
# board.push(move)
# print(board)






