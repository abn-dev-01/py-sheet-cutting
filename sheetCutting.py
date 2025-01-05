import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

# Загрузка данных из файлов Excel
file_details = "details.xlsx"  # файл с данными о деталях
file_materials = "materials.xlsx"  # файл с данными о материалах

details = pd.read_excel(file_details)
materials = pd.read_excel(file_materials)

# Оптимизация для каждого материала
results = []
for material_name, material_data in materials.groupby("Наименование материала"):
    # Фильтрация деталей для текущего материала
    material_details = details[details["Наименование материала"] == material_name]

    # Параметры исходной заготовки
    sheet_length = material_data["Длина, мм"].values[0]
    sheet_width = material_data["Ширина, мм"].values[0]

    # Создание задачи линейного программирования
    prob = LpProblem(f"OptimalCutting_{material_name}", LpMinimize)

    # Создание переменных для количества исходных заготовок
    num_sheets = LpVariable("NumSheets", lowBound=0, cat="Integer")

    # Создание переменных для каждого типа детали
    detail_vars = []
    for _, detail in material_details.iterrows():
        length, width, quantity = detail["Длина, мм"], detail["Ширина, мм"], detail["Количество, шт."]
        var = LpVariable(f"Detail_{length}x{width}", lowBound=0, cat="Integer")
        detail_vars.append((var, length, width, quantity))

    # Целевая функция: минимизация количества исходных заготовок
    prob += num_sheets

    # Ограничения: каждая деталь должна быть изготовлена в нужном количестве
    for var, length, width, quantity in detail_vars:
        prob += var * length * width <= num_sheets * sheet_length * sheet_width
        prob += var >= quantity

    # Решение задачи
    prob.solve()

    # Сохранение результатов
    result = {
        "Материал": material_name,
        "Количество исходных заготовок": value(num_sheets),
        "Детали": []
    }

    for var, length, width, quantity in detail_vars:
        result["Детали"].append({
            "Размеры": f"{length}x{width}",
            "Количество": value(var)
        })

    results.append(result)

# Вывод результатов
for result in results:
    print(f"Материал: {result['Материал']}")
    print(f"Количество исходных заготовок: {result['Количество исходных заготовок']}")
    print("Детали:")
    for detail in result["Детали"]:
        print(f"  Размеры: {detail['Размеры']}, Количество: {detail['Количество']}")
    print()
