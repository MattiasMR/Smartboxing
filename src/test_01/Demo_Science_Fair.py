from openai import OpenAI
from funciones import pedir_dato_campo, generar_csv, generar_df
import variables

client = OpenAI(api_key=variables.key())
boxes = variables.boxes()
medicos = variables.medicos()

def crear_prompt():
    prompt = f"""
    Eres un asistente experto en generar y actualizar tablas de asignación de médicos a boxes de hospital.
    Debes producir siempre una tabla completa y sin errores.
    Sigue estrictamente estas reglas:
    1. Cada box tiene un campo "especialidades": solo asigna médicos cuya especialidad coincida exactamente.
    2. No asignes médicos a boxes deshabilitados ("habilitado": False).
    3. Cada médico solo puede ocupar un box a la vez.
    4. Respeta la disponibilidad horaria de cada médico ("desde", "hasta").
    5. El rango operativo de cada box es desde 08:00 hasta 22:00.
    6. No pueden solaparse los horarios de los médicos en un mismo box.
    7. Siempre genera la tabla completa, incluyendo las asignaciones previas y actualizando con los nuevos médicos.
    8. Mantén un balance equitativo de especialidades, evitando concentraciones en un mismo box.
    
    
    **Formato de entrada**:
    Boxes: {boxes}
    Médicos: {medicos}
    
    **Verificación de solapamientos**:
    ANTES de asignar un médico a un box, revisa los horarios en los que está ocupado el box y asegurate de que la nueva asignación no calce con alguna existente.
    Asegurate de incorporar la mayor cantidad de medicos posibles.

    **Formato de salida solo con los valores separados por comas**:
    **Orden de los valores Box,Doctor,Especialidad,Fecha,Desde,Hasta**
    ... (todas las filas de la asignación separadas por comas) ...

    **Por favor, no incluyas ningún texto adicional ni explicaciones.**

    """
    return prompt

def obtener_respuesta():
    prompt = crear_prompt()
    resp = client.chat.completions.create(
    model="gpt-4.1-2025-04-14",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2,
    max_tokens=10000
    )
    return resp.choices[0].message.content

# Función para interactuar con el usuario
def interactuar(agenda_actual=None):
    print("¡Bienvenido al chatbot de agendamiento de hospital!")
    while True:
        print("\n¿Qué te gustaría hacer?")
        print("1. Consultar la agenda actual")
        print("2. Agregar un nuevo médico")
        print("3. Salir")
        opcion = input("Ingresa el número de la opción: ")

        if opcion == "1":
            if agenda_actual is None:
                print("Generando plantilla inicial, por favor espere unos segundos...")
                agenda_actual = obtener_respuesta()
            tabla = agenda_actual.split("\n")  # Asumiendo que la tabla está en formato de texto
            generar_csv(tabla)
            df = generar_df()

            print("\nAgenda actual:\n")
            print(df.to_string(index=False))
        elif opcion == "2":
            if agenda_actual is None:
                print("Primero debes generar una plantilla inicial antes de agregar un nuevo médico.")
                continue
            print("\nPor favor, proporciona los datos del nuevo médico.")
            nombre = pedir_dato_campo("Nombre", "Nombre del médico: ")
            especialidad = pedir_dato_campo("Especialidad", "Especialidad: ")
            horario_inicio = pedir_dato_campo("Horario de inicio", "Horario de inicio (ej. 07:00): ")
            horario_fin = pedir_dato_campo("Horario de fin", "Horario de fin (ej. 13:00): ")

            # Mostrar los datos ingresados
            print(f"\nDatos del nuevo médico:")
            print(f"Nombre: {nombre}")
            print(f"Especialidad: {especialidad}")
            print(f"Horario: {horario_inicio} - {horario_fin}")

            # Preguntar al usuario si los datos son correctos o desea modificar alguno
            confirmacion = input("\n¿Está todo correcto? (Sí/No): ").strip().lower()
            
            if confirmacion == "sí" or confirmacion == "si":
                # Si el usuario confirma, agregar el nuevo médico a la lista
                nuevo_medico = {"nombre": nombre, "especialidad": especialidad, "desde": horario_inicio, "hasta": horario_fin}
                medicos.append(nuevo_medico)

                # Regenerar la agenda actualizada
                print("Generando la agenda actualizada, por favor espere...")
                agenda_actual = obtener_respuesta()
                print(f"\nEl nuevo Dr/a. {nombre} ha sido agregado con éxito.")
            else:
                print("No se han realizado cambios. Puedes intentar nuevamente.")
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, por favor intenta nuevamente.")

# Ejecutar el chatbot
interactuar()