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
    html_content = """
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>محاسبه فرم پلکانی ماتریس</title>
        <link href="https://v1.fontapi.ir/css/Vazir" rel="stylesheet">
        <style>
            body {
                font-family: 'Vazir', Arial, sans-serif;
                direction: rtl;
                text-align: center;
                margin: 0;
                background-color: #f4f6f9;
                color: #333;
            }
            .header {
                background-color: #2c3e50;
                color: white;
                padding: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                margin-bottom: 30px;
            }
            .header h1 {
                margin: 0;
                font-size: 2em;
            }
            .header p {
                margin: 5px 0;
                font-size: 1.2em;
            }
            h2 {
                color: #2c3e50;
                margin: 20px 0;
            }
            .matrix-container {
                margin: 20px auto;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                max-width: 600px;
                direction: ltr; /* ترتیب چپ به راست برای ماتریس */
            }
            .matrix-input {
                display: inline-block;
                margin: 10px;
            }
            .matrix-input input {
                width: 60px;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                font-size: 1em;
            }
            .result {
                margin: 30px auto;
                max-width: 800px;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                direction: ltr; /* ترتیب چپ به راست برای نتایج */
            }
            .result p {
                direction: rtl; /* متن توضیحات همچنان راست به چپ */
            }
            button {
                padding: 12px 24px;
                margin: 10px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1em;
                transition: background-color 0.3s, transform 0.2s;
            }
            button:hover {
                background-color: #2980b9;
                transform: translateY(-2px);
            }
            table {
                border-collapse: collapse;
                margin: 20px auto;
                direction: ltr; /* اطمینان از چپ به راست بودن جدول */
            }
            td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: center;
                background-color: #f9f9f9;
            }
            input[type="number"] {
                -moz-appearance: textfield;
            }
            input[type="number"]::-webkit-outer-spin-button,
            input[type="number"]::-webkit-inner-spin-button {
                -webkit-appearance: none;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>محاسبه فرم پلکانی ماتریس</h1>
            <p>دانشجو: امیرحسین قربانی</p>
            <p>استاد: دکتر حسینی</p>
        </div>

        <h2>ابعاد ماتریس را وارد کنید</h2>
        <div class="matrix-container" style="direction: rtl;"> <!-- برچسب‌ها راست به چپ -->
            <label>تعداد سطرها:</label>
            <input type="number" id="rows" min="1">
            <label>تعداد ستون‌ها:</label>
            <input type="number" id="cols" min="1">
            <button onclick="createMatrix()">ساخت ماتریس</button>
        </div>

        <h2>درایه‌های ماتریس را وارد کنید</h2>
        <div id="matrixInput" class="matrix-container"></div>
        <button onclick="calculateRowReduction()" style="display: none;" id="calculateBtn">محاسبه فرم پلکانی</button>

        <h2>ماتریس پلکانی نهایی</h2>
        <div id="result" class="result"></div>

        <script>
            function createMatrix() {
                const rows = parseInt(document.getElementById('rows').value);
                const cols = parseInt(document.getElementById('cols').value);
                if (!rows || !cols) {
                    alert('لطفاً تعداد سطرها و ستون‌ها را وارد کنید.');
                    return;
                }

                let html = '<table>';
                for (let i = 0; i < rows; i++) {
                    html += '<tr>';
                    for (let j = 0; j < cols; j++) {
                        html += `<td><input type="number" id="cell-${i}-${j}" class="matrix-input" value="0"></td>`;
                    }
                    html += '</tr>';
                }
                html += '</table>';
                document.getElementById('matrixInput').innerHTML = html;
                document.getElementById('calculateBtn').style.display = 'block';
            }

            async function calculateRowReduction() {
                const rows = parseInt(document.getElementById('rows').value);
                const cols = parseInt(document.getElementById('cols').value);
                const matrix = [];

                for (let i = 0; i < rows; i++) {
                    const row = [];
                    for (let j = 0; j < cols; j++) {
                        const value = parseFloat(document.getElementById(`cell-${i}-${j}`).value);
                        row.push(isNaN(value) ? 0 : value);
                    }
                    matrix.push(row);
                }

                const response = await fetch('/row_reduction', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ matrix, rows, cols })
                });
                const data = await response.json();

                let resultHtml = '<h3>مراحل حل:</h3>';
                data.steps.forEach(step => {
                    resultHtml += `<p>${step.operation}</p>`;
                    resultHtml += '<table>';
                    step.matrix.forEach(row => {
                        resultHtml += '<tr>';
                        row.forEach(cell => {
                            resultHtml += `<td>${cell.toFixed(2)}</td>`;
                        });
                        resultHtml += '</tr>';
                    });
                    resultHtml += '</table>';
                });

                resultHtml += '<h3>ماتریس نهایی:</h3><table>';
                data.result.forEach(row => {
                    resultHtml += '<tr>';
                    row.forEach(cell => {
                        resultHtml += `<td>${cell.toFixed(2)}</td>`;
                    });
                    resultHtml += '</tr>';
                });
                resultHtml += '</table>';

                document.getElementById('result').innerHTML = resultHtml;
            }
        </script>
    </body>
    </html>
    """
    return html_content

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