# Optimal Sheet Cutting API

This project implements an API for solving the **optimal sheet cutting problem** using linear programming. The application takes input in JSON format, performs calculations to determine the optimal cutting of materials, and returns the results.

## Features
- Minimizes the number of sheets required for cutting.
- Supports multiple materials and details.
- Accepts data from Excel files in JSON format.
- Uses the **PuLP** library for linear programming.

## Requirements

### Python Libraries:
- Flask
- pandas
- PuLP

Install the required libraries with:
```bash
pip install flask pandas pulp
```

### Excel File Structure
The input JSON is expected to have data from two Excel sheets:

#### Sheet1 (Details):
| material | length | width | quantity |
|----------|--------|-------|----------|
| m1       | 200    | 100   | 5        |
| m2       | 300    | 150   | 10       |

#### Sheet2 (Materials):
| material | length | width |
|----------|--------|-------|
| m1       | 5000   | 2700  |
| m2       | 3000   | 2100  |

## API Endpoints

### `/optimize` (POST)
#### Description:
Accepts JSON input with details and materials data, performs the cutting optimization, and returns the results.

#### Input Format:
```json
{
  "Sheet1": [
    {"material": "m1", "length": 200, "width": 100, "quantity": 5},
    {"material": "m2", "length": 300, "width": 150, "quantity": 10}
  ],
  "Sheet2": [
    {"material": "m1", "length": 5000, "width": 2700},
    {"material": "m2", "length": 3000, "width": 2100}
  ]
}
```

#### Response Format:
```json
[
  {
    "material": "m1",
    "sheets_required": 2,
    "details": [
      {"size": "200x100", "count": 5}
    ]
  },
  {
    "material": "m2",
    "sheets_required": 1,
    "details": [
      {"size": "300x150", "count": 10}
    ]
  }
]
```

### Running the API
1. Clone the repository.
2. Run the server:
   ```bash
   python server.py
   ```
3. Access the API at `http://127.0.0.1:5000/optimize`.

### Testing the API
You can test the API using tools like:
- **Postman**:
  - Set the request type to `POST`.
  - Use `http://127.0.0.1:5000/optimize` as the URL.
  - Add the input JSON in the body (raw, application/json).

- **cURL**:
  ```bash
  curl -X POST http://127.0.0.1:5000/optimize -H "Content-Type: application/json" -d '{
    "Sheet1": [
      {"material": "m1", "length": 200, "width": 100, "quantity": 5},
      {"material": "m2", "length": 300, "width": 150, "quantity": 10}
    ],
    "Sheet2": [
      {"material": "m1", "length": 5000, "width": 2700},
      {"material": "m2", "length": 3000, "width": 2100}
    ]
  }'
  ```

## Code Overview
### Main File: `server.py`
- **Flask** serves as the API framework.
- **optimize_cutting**: Core function for performing optimization.
- Handles exceptions and returns error messages if the input is invalid.

### Optimization Logic
- Uses **PuLP** for linear programming.
- Defines constraints to ensure all details are cut as per requirements.
- Minimizes the number of sheets required.

## Example Workflow
1. Prepare input data in Excel.
2. Convert the Excel data into JSON format.
3. Send the JSON to the API.
4. Receive the optimized results and use them as needed.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Author
Developed by [Your Name].

