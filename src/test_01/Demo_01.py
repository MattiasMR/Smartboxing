from openai import OpenAI
client = OpenAI(
  api_key="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"
)

nuevos_boxes = [
    {"id": 1, "especialidades": ["Ginecología", "Obstetricia"], "capacidad": 1, "habilitado": True},
    {"id": 2, "especialidades": ["Medicina General"], "capacidad": 1, "habilitado": True},
    {"id": 3, "especialidades": ["Pediatría"], "capacidad": 1, "habilitado": True},
    {"id": 4, "especialidades": ["Otorrino"], "capacidad": 1, "habilitado": True},
    {"id": 5, "especialidades": ["Cardiología"], "capacidad": 1, "habilitado": True},
    {"id": 6, "especialidades": ["Dermatología"], "capacidad": 1, "habilitado": True},
    {"id": 7, "especialidades": ["Neurología"], "capacidad": 1, "habilitado": True},
    {"id": 8, "especialidades": ["Psiquiatría"], "capacidad": 1, "habilitado": True},
    {"id": 9, "especialidades": ["Traumatología"], "capacidad": 1, "habilitado": True},
    {"id": 10, "especialidades": ["Endocrinología"], "capacidad": 1, "habilitado": False}
]

nuevos_medicos = [
    {"nombre": "Dr. Alvarez", "especialidad": "Ginecología", "desde": "07:00", "hasta": "13:00"},
    {"nombre": "Dr. Bustamante", "especialidad": "Medicina General", "desde": "07:00", "hasta": "13:00"},
    {"nombre": "Dr. Cortes", "especialidad": "Pediatría", "desde": "07:00", "hasta": "13:00"},
    {"nombre": "Dr. Díaz", "especialidad": "Otorrino", "desde": "07:00", "hasta": "13:00"},
    {"nombre": "Dr. Espinoza", "especialidad": "Cardiología", "desde": "07:00", "hasta": "13:00"},
    {"nombre": "Dr. Fernández", "especialidad": "Dermatología", "desde": "08:00", "hasta": "14:00"},
    {"nombre": "Dr. García", "especialidad": "Neurología", "desde": "08:00", "hasta": "14:00"},
    {"nombre": "Dr. Herrera", "especialidad": "Psiquiatría", "desde": "08:00", "hasta": "14:00"},
    {"nombre": "Dr. Ibarra", "especialidad": "Traumatología", "desde": "08:00", "hasta": "14:00"},
    {"nombre": "Dr. Jiménez", "especialidad": "Endocrinología", "desde": "08:00", "hasta": "14:00"}
    # Aquí puedes seguir agregando los demás médicos
]

# Prompt actualizado para la generación de la tabla
prompt = f"""
Eres un asistente que asigna médicos a boxes con estas reglas:
1. Cada box tiene un campo "especialidades": solo puede asignarse un médico cuya especialidad coincida.
2. Si un box está inhabixlitado ("habilitado": false), no debe asignarse.
3. Un médico no puede estar en más de un box al mismo tiempo.
4. Busca un balance equitativo de especialidades en todos los boxes, evitando concentraciones.
5. Respeta la disponibilidad horaria de cada médico ("desde", "hasta").
6. Un box tiene un rango horario de 08:00 a 22:00, tratar de ocupar todo el rango horario.
7. Tu objetivo es asignar médicos a boxes de manera eficiente y clara. 

Boxes: {nuevos_boxes}
Médicos: {nuevos_medicos}

Genera una tabla con el siguiente formato:

| Doctor         | Box | Especialidad       | Fecha      | Horario     | Nota                                   |
|----------------|-----|--------------------|------------|-------------|--------------------|

Y luego entrega notas sobre la asignación, como por ejemplo:
**Notas:**
- El Dr. Jiménez (Endocrinología) no fue asignado ya que su box está deshabilitado.
- Todos los médicos han sido asignados a boxes que coinciden con su especialidad y están habilitados.
- Se ha buscado un balance equitativo de especialidades en los boxes.
"""

# Llamada al API de OpenAI
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
    max_tokens=500
)

# Mostrar el resultado
print(resp.choices[0].message.content)
