from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

def row_reduction(matrix, rows, cols):
    matrix = np.array(matrix, dtype=float)
    steps = []
    
    def add_step(operation, matrix):
        steps.append({"operation": operation, "matrix": matrix.tolist()})

    add_step("ماتریس اولیه", matrix)
    
    lead = 0
    row_count = rows
    col_count = cols

    for r in range(row_count):
        if lead >= col_count:
            break
        i = r
        while matrix[i, lead] == 0:
            i += 1
            if i == row_count:
                i = r
                lead += 1
                if col_count == lead:
                    break
        if i < row_count:
            if i != r:
                matrix[[i, r]] = matrix[[r, i]]
                add_step(f"تعویض سطر {r + 1} با سطر {i + 1}", matrix)
            
            if matrix[r, lead] != 0:
                matrix[r] = matrix[r] / matrix[r, lead]
                add_step(f"تقسیم سطر {r + 1} بر {matrix[r, lead]:.2f} برای نرمال‌سازی", matrix)
            
            for i in range(row_count):
                if i != r:
                    factor = matrix[i, lead]
                    matrix[i] -= factor * matrix[r]
                    if factor != 0:
                        add_step(f"کسر {factor:.2f} برابر سطر {r + 1} از سطر {i + 1}", matrix)
            
            lead += 1
    
    return steps, matrix.tolist()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/row_reduction', methods=['POST'])
def perform_row_reduction():
    data = request.get_json()
    matrix = data['matrix']
    rows = data['rows']
    cols = data['cols']
    steps, result = row_reduction(matrix, rows, cols)
    return jsonify({"steps": steps, "result": result})

if __name__ == '__main__':
    app.run(debug=True)