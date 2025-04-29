from openai import OpenAI
from funciones import pedir_dato_campo, generar_csv, generar_df
import variables

client = OpenAI(api_key=variables.key())
boxes = variables.boxes()
medicos = variables.medicos()

def prompt_base():
    return """
Eres un asistente experto en generar y actualizar tablas de asignación de médicos a boxes de hospital.
Debes producir siempre una tabla completa y sin errores.
Sigue estrictamente estas reglas:
1. Cada box tiene un campo "especialidades": solo asigna médicos cuya especialidad coincida exactamente.
2. No asignes médicos a boxes deshabilitados ("habilitado": False).
3. Cada médico solo puede ocupar un box a la vez.
4. Respeta la disponibilidad horaria de cada médico ("desde", "hasta").
5. El rango operativo de cada box es desde 08:00 hasta 22:00.
6. El rango operativo de cada medico es DISTINTO que el rango operativo de cada box.
7. No pueden solaparse los horarios de los médicos en un mismo box.
8. Siempre genera la tabla completa, incluyendo las asignaciones previas y actualizando con los nuevos médicos.
9. Mantén un balance equitativo de especialidades, evitando concentraciones en un mismo box.
**Salida**: Valores separados por comas: Box,Doctor,Especialidad,Fecha,Desde,Hasta. Sin texto adicional.
"""

def generar_agenda_inicial():
    prompt = prompt_base() + f"\n\nBoxes: {boxes}\nMédicos: {medicos}" + "\n**Verificación de solapamientos**: ANTES de asignar un médico a un box revisa los horarios en los que está ocupado el box y asegurate de que la nueva asignación no calce con alguna existente."
    resp = client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[{"role":"user","content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content

def actualizar_agenda(agenda_actual, nuevo_medico):
    # Instrucción para añadir solo el nuevo médico
    prompt = prompt_base() + (
        f"\n\nAquí está la plantilla actual:\n{agenda_actual}\n\n"
        f"Añade únicamente al final la(s) fila(s) correspondiente(s) a este nuevo médico:\n"
        f"{nuevo_medico}\n\n"
    )
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content": prompt}],
        temperature=0.2
    )
    # Concatena la respuesta con la agenda anterior
    return agenda_actual.strip() + "\n" + resp.choices[0].message.content.strip()

def preguntar_agenda(agenda_actual, pregunta):
    prompt = (
        f"Tengo esta agenda actualmente:\n{agenda_actual}\n\n"
        f"Responde a la siguiente consulta considerando toda la información, lo más importante es la agenda que tengo actualmente (solo texto):\n{pregunta}"
    )
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role":"user","content": prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content

def interactuar():
    agenda_actual = None
    print("¡Bienvenido al chatbot de agendamiento de hospital!")
    while True:
        print("\n¿Qué te gustaría hacer?")
        print("1. Consultar la agenda actual")
        print("2. Agregar un nuevo médico")
        print("3. Preguntar sobre la plantilla actual")
        print("4. Salir")
        opcion = input("Ingresa el número de la opción: ").strip()

        if opcion == "1":
            if agenda_actual is None:
                print("Generando plantilla inicial, por favor espere...")
                agenda_actual = generar_agenda_inicial()
            generar_csv(agenda_actual.split("\n"))
            df = generar_df()
            print("\nAgenda actual:\n")
            print(df.to_string(index=False))

        elif opcion == "2":
            if agenda_actual is None:
                print("Primero debes generar la plantilla inicial.")
                continue
            nombre = pedir_dato_campo("Nombre", "Nombre del médico: ")
            especialidad = pedir_dato_campo("Especialidad", "Especialidad: ")
            inicio = pedir_dato_campo("Desde", "Horario de inicio (HH:MM): ")
            fin = pedir_dato_campo("Hasta", "Horario de fin (HH:MM): ")
            nuevo = {"nombre": nombre, "especialidad": especialidad, "desde": inicio, "hasta": fin}
            print(f"\nAgregando Dr/a. {nombre}...")
            medicos.append(nuevo)
            agenda_actual = actualizar_agenda(agenda_actual, nuevo)
            print(f"Dr/a. {nombre} agregado. Plantilla actualizada.")

        elif opcion == "3":
            if agenda_actual is None:
                print("Aún no hay plantilla generada.")
                continue
            pregunta = input("¿Qué quieres saber de la plantilla? ")
            respuesta = preguntar_agenda(agenda_actual, pregunta)
            print(f"\n{respuesta}")

        elif opcion == "4":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida, intenta de nuevo.")
    

interactuar()
