import csv
import pandas as pd
def pedir_dato_campo(nombre_campo, mensaje):
    valor = input(mensaje)
    while not valor.strip():  # Verifica si el valor es vacío o solo contiene espacios
        print(f"El campo '{nombre_campo}' no puede estar vacío.")
        valor = input(mensaje)
    return valor

def generar_df():
    # Intentamos leer con BOM UTF-8; si falla, con Latin-1
    try:
        df = pd.read_csv('agenda_hospitalaria.csv', encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv('agenda_hospitalaria.csv', encoding='latin1')

    # Asegurarnos de que Box sea texto, extraer sólo dígitos y convertir a entero
    df['Box'] = df['Box'].astype(str) \
                       .str.extract(r'(\d+)', expand=False) \
                       .astype(int)

    # Ordenar y resetear índice
    df = df.sort_values(by='Box').reset_index(drop=True)
    return df


def generar_csv(tabla):
    # Si tabla es lista de cadenas, conviértela en lista de listas
    if tabla and isinstance(tabla[0], str):
        lines = [
            line.strip()
            for line in tabla
            if line.strip() and not line.strip().startswith("```")
        ]
        tabla = [line.split(",") for line in lines]

    # Abrimos con encoding utf-8-sig para incluir BOM y que Excel muestre bien las tildes
    with open("agenda_hospitalaria.csv", "w", encoding="utf-8-sig", newline="") as csvfile:
        fieldnames = ['Box', 'Doctor', 'Especialidad', 'Fecha', 'Desde', 'Hasta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in tabla[1:]:
            if len(row) >= 6:
                fila_dict = {
                    'Box':           row[0].strip(),
                    'Doctor':        row[1].strip(),
                    'Especialidad':  row[2].strip(),
                    'Fecha':         row[3].strip(),
                    'Desde':         row[4].strip(),
                    'Hasta':         row[5].strip()
                }
                writer.writerow(fila_dict)