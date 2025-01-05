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

## Excel Integration
This project is designed to work seamlessly with an Excel file containing two sheets (`Sheet1` and `Sheet2`). The workflow is automated using a VBA macro to send data to the API and process the response.

### VBA Macro Functionality:
1. **Collects Data:**
   - Reads data from `Sheet1` (details) and `Sheet2` (materials).
2. **Formats Data into JSON:**
   - Converts the collected data into a JSON structure that matches the API input format.
3. **Sends JSON to the API:**
   - Sends the formatted JSON via an HTTP POST request to `http://127.0.0.1:5000/optimize`.
4. **Processes the API Response:**
   - Parses the JSON response returned by the API.
   - Writes the results to a new sheet called `Results` in the Excel file.

### Example VBA Macro:
Below is an example of the VBA macro used for integration:
```vba
Sub SendDataToPython()
    Dim http As Object
    Dim JSON As String
    Dim Response As String
    Dim details As String
    Dim Materials As String

    ' Collect data from Sheet1 (details)
    details = "["
    Dim LastRowSheet1 As Long
    Dim i As Long
    Dim lengthCol As Long
    Dim widthCol As Long
    Dim quantityCol As Long

    lengthCol = 3 ' Column for "Length, mm" in Sheet1
    widthCol = 4 ' Column for "Width, mm" in Sheet1
    quantityCol = 5 ' Column for "Quantity" in Sheet1

    LastRowSheet1 = ThisWorkbook.Sheets("Sheet1").Cells(Rows.Count, 1).End(xlUp).Row
    For i = 2 To LastRowSheet1
        details = details & "{""material"": """ & ThisWorkbook.Sheets("Sheet1").Cells(i, 2).Value & """, " & _
                            ""length"": " & ThisWorkbook.Sheets("Sheet1").Cells(i, lengthCol).Value & ", " & _
                            ""width"": " & ThisWorkbook.Sheets("Sheet1").Cells(i, widthCol).Value & ", " & _
                            ""quantity"": " & ThisWorkbook.Sheets("Sheet1").Cells(i, quantityCol).Value & "},"
    Next i
    details = Left(details, Len(details) - 1) & "]"

    ' Collect data from Sheet2 (materials)
    Materials = "["
    Dim LastRowSheet2 As Long
    Dim j As Long

    LastRowSheet2 = ThisWorkbook.Sheets("Sheet2").Cells(Rows.Count, 1).End(xlUp).Row
    For j = 2 To LastRowSheet2
        Materials = Materials & "{""material"": """ & ThisWorkbook.Sheets("Sheet2").Cells(j, 1).Value & """, " & _
                                 ""length"": " & ThisWorkbook.Sheets("Sheet2").Cells(j, 2).Value & ", " & _
                                 ""width"": " & ThisWorkbook.Sheets("Sheet2").Cells(j, 3).Value & "},"
    Next j
    Materials = Left(Materials, Len(Materials) - 1) & "]"

    ' Combine details and materials into final JSON
    JSON = "{""Sheet1"": " & details & ", ""Sheet2"": " & Materials & "}"

    ' Display JSON for debugging purposes
    MsgBox "Generated JSON: " & JSON, vbInformation

    ' Create HTTP request to Python API
    Set http = CreateObject("MSXML2.XMLHTTP")
    http.Open "POST", "http://127.0.0.1:5000/optimize", False
    http.setRequestHeader "Content-Type", "application/json"
    http.Send JSON

    ' Handle server response
    Response = http.responseText

    ' Display server response for debugging purposes
    MsgBox "Response from server: " & Response, vbInformation

    ' Write response back to Excel
    Dim ResultsSheet As Worksheet
    On Error Resume Next
    Set ResultsSheet = ThisWorkbook.Sheets("Results")
    If ResultsSheet Is Nothing Then
        Set ResultsSheet = ThisWorkbook.Sheets.Add
        ResultsSheet.Name = "Results"
    Else
        ResultsSheet.Cells.Clear
    End If
    On Error GoTo 0

    ' Parse and write response
    Dim JsonResponse As Object
    Set JsonResponse = JsonConverter.ParseJson(Response)

    Dim row As Long
    row = 1
    ResultsSheet.Cells(row, 1).Value = "Material"
    ResultsSheet.Cells(row, 2).Value = "Sheets Required"
    ResultsSheet.Cells(row, 3).Value = "Details"

    row = 2
    Dim item As Object
    Dim detail As Object
    For Each item In JsonResponse
        ResultsSheet.Cells(row, 1).Value = item("material")
        ResultsSheet.Cells(row, 2).Value = item("sheets_required")
        Dim details As String
        details = ""
        For Each detail In item("details")
            details = details & detail("size") & " x " & detail("count") & "; "
        Next detail
        ResultsSheet.Cells(row, 3).Value = details
        row = row + 1
    Next item

    MsgBox "Results have been written to the 'Results' sheet.", vbInformation
End Sub
```

### Example Workflow:
1. Open the Excel file.
2. Run the macro `SendDataToPython`.
3. JSON data is sent to the API.
4. Results are written back to a new sheet called `Results`.

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
Developed by Andrew Nikitin.
Telegram: [@anikin_dev](https://t.me/anikin_dev)

