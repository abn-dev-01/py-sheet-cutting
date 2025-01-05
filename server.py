from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/cutting', methods=['POST'])
def cutting():
    # Получаем данные от клиента
    data = request.get_json()
    details = pd.DataFrame(data['details'])
    materials = pd.DataFrame(data['materials'])
    
    # Здесь должна быть ваша логика раскроя (пример выше)
    results = [{"material": "Example", "sheets_required": 3, "details_cut": [{"size": "100x200", "count": 5}]}]

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000)
