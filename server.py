from flask import Flask, request, jsonify
from sheetCutting import optimize_cutting
import os

app = Flask(__name__)

@app.route('/optimize', methods=['POST'])
def optimize():
    # Получение пути к загруженному файлу Excel
    file_data = request.files['file']
    file_path = os.path.join("uploads", file_data.filename)
    file_data.save(file_path)

    # Выполнение оптимизации
    try:
        results = optimize_cutting(file_path)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(port=5000)
