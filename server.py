from flask import Flask, request, jsonify
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, value

app = Flask(__name__)

def optimize_cutting(data):
    sheet1 = pd.DataFrame(data["Sheet1"])  # Details data
    sheet2 = pd.DataFrame(data["Sheet2"])  # Materials data

    # Optimization for each material
    results = []
    for material_name, material_data in sheet2.groupby("material"):
        # Filter details for the current material
        material_details = sheet1[sheet1["material"] == material_name]

        # Parameters of the raw sheet
        sheet_length = material_data["length"].values[0]
        sheet_width = material_data["width"].values[0]

        # Create the linear programming problem
        prob = LpProblem(f"OptimalCutting_{material_name}", LpMinimize)

        # Create a variable for the number of sheets
        num_sheets = LpVariable("NumSheets", lowBound=0, cat="Integer")

        # Create variables for each type of detail
        detail_vars = []
        for _, detail in material_details.iterrows():
            length, width, quantity = detail["length"], detail["width"], detail["quantity"]
            var = LpVariable(f"Detail_{length}x{width}", lowBound=0, cat="Integer")
            detail_vars.append((var, length, width, quantity))

        # Objective function: minimize the number of sheets
        prob += num_sheets

        # Constraints: each detail must be produced in the required quantity
        for var, length, width, quantity in detail_vars:
            prob += var * length * width <= num_sheets * sheet_length * sheet_width
            prob += var >= quantity

        # Solve the problem
        prob.solve()

        # Store the results
        result = {
            "material": material_name,
            "sheets_required": value(num_sheets),
            "details": []
        }

        for var, length, width, quantity in detail_vars:
            result["details"].append({
                "size": f"{length}x{width}",
                "count": value(var)
            })

        results.append(result)

    return results

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        data = request.get_json()
        results = optimize_cutting(data)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
