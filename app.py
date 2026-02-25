from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " " or board[0][i] == board[1][i] == board[2][i] != " ":
            return board[i][0] if board[i][0] != " " else board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " " or board[0][2] == board[1][1] == board[2][0] != " ":
        return board[1][1]
    return None

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def minimax(board, depth, is_maximizing, ai_symbol, human_symbol):
    winner = check_winner(board)
    if winner == ai_symbol:
        return 10 - depth
    elif winner == human_symbol:
        return depth - 10
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = ai_symbol
                    score = minimax(board, depth + 1, False, ai_symbol, human_symbol)
                    board[i][j] = " " 
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = human_symbol
                    score = minimax(board, depth + 1, True, ai_symbol, human_symbol)
                    board[i][j] = " " 
                    best_score = min(score, best_score)
        return best_score

def computer_move(board, ai_symbol):
    human_symbol = "X" if ai_symbol == "O" else "O"
    best_score = -float('inf')
    best_move = None
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = ai_symbol
                score = minimax(board, 0, False, ai_symbol, human_symbol)
                board[i][j] = " " 
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
                    
    return best_move

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_move', methods=['POST'])
def get_move():
    data = request.json
    board = data.get('board')
    ai_symbol = data.get('ai_symbol', 'O')
    
    best_move = computer_move(board, ai_symbol)
    
    if best_move:
        return jsonify({"row": best_move[0], "col": best_move[1]})
    else:
        return jsonify({"error": "No moves available"}), 400

if __name__ == '__main__':
    app.run(debug=True)
