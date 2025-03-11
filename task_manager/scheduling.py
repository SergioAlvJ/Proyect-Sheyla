import matplotlib.pyplot as plt
import numpy as np

# Definir las tareas con nombre, tiempo de procesamiento y fecha límite
tasks = [
    {"name": "A", "processing_time": 2, "deadline": 3},
    {"name": "B", "processing_time": 1, "deadline": 2},
    {"name": "C", "processing_time": 1, "deadline": 2},
    {"name": "D", "processing_time": 1, "deadline": 3},
]

# Ordenar tareas por fecha límite (heurística EDF)
tasks.sort(key=lambda x: x["deadline"])

# Variables para la programación de tareas
schedule = []
time = 0
missed_tasks = []

# Ejecutar el algoritmo de planificación EDF
for task in tasks:
    if time + task["processing_time"] <= task["deadline"]:  
        schedule.append((task["name"], time, time + task["processing_time"]))
        time += task["processing_time"]
    else:
        missed_tasks.append(task["name"])  # Tareas que no cumplen el plazo

# Graficar la planificación
fig, ax = plt.subplots(figsize=(8, 4))

# Dibujar tareas en la línea de tiempo
for task_name, start, end in schedule:
    ax.broken_barh([(start, end - start)], (10, 5), facecolors='lightblue', edgecolor="black")
    ax.text((start + end) / 2, 12, task_name, ha='center', va='center', fontsize=12, color='black')

# Configurar gráfico
ax.set_xlim(0, time + 2)
ax.set_ylim(8, 18)
ax.set_xlabel("Time")
ax.set_yticks([])
ax.set_title("Earliest Deadline First (EDF) Scheduling")

# Mostrar tareas no programadas
if missed_tasks:
    ax.text(time + 1, 12, f"Missed: {', '.join(missed_tasks)}", fontsize=10, color='red')

plt.show()
