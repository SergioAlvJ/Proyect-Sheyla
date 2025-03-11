document.addEventListener('DOMContentLoaded', () => {
    const daysContainer = document.querySelector('.days-container');
    const currentWeekDisplay = document.getElementById('current-week');
    const prevWeekButton = document.getElementById('prev-week');
    const nextWeekButton = document.getElementById('next-week');
    const taskInput = document.getElementById('task-input');
    const taskDescription = document.getElementById('task-description');
    const taskDay = document.getElementById('task-day');
    const taskTime = document.getElementById('task-time');
    const addTaskButton = document.getElementById('add-task');
    const modal = document.getElementById('task-modal');
    const closeModal = document.querySelector('.close-modal');
    const modalTaskTitle = document.getElementById('modal-task-title');
    const modalTaskDescription = document.getElementById('modal-task-description');
    const modalTaskTime = document.getElementById('modal-task-time');

    let currentDate = dayjs(); // Fecha actual usando Day.js

    // Horas del día
    const hours = Array.from({ length: 11 }, (_, i) => `${i + 8}:00`);

    // Generar opciones de horas en el formulario
    hours.forEach(hour => {
        const option = document.createElement('option');
        option.value = hour;
        option.textContent = hour;
        taskTime.appendChild(option);
    });

    // Función para renderizar el horario
    function renderSchedule() {
        daysContainer.innerHTML = ''; // Limpiar el horario
        const startOfWeek = currentDate.startOf('week'); // Inicio de la semana

        // Mostrar la semana actual
        currentWeekDisplay.textContent = `Semana del ${startOfWeek.format('DD/MM/YYYY')}`;

        // Generar los días de la semana
        for (let i = 0; i < 7; i++) {
            const day = startOfWeek.add(i, 'day');
            const dayElement = document.createElement('div');
            dayElement.classList.add('day');
            dayElement.innerHTML = `<div class="day-header">${day.format('dddd, DD/MM')}</div>`;

            // Generar slots de tiempo para cada día
            hours.forEach(hour => {
                const taskSlot = document.createElement('div');
                taskSlot.classList.add('task-slot');
                taskSlot.dataset.day = day.format('YYYY-MM-DD');
                taskSlot.dataset.time = hour;
                dayElement.appendChild(taskSlot);
            });

            daysContainer.appendChild(dayElement);
        }

        // Cargar tareas desde localStorage
        loadTasks();
    }

    // Cargar tareas en el horario
    function loadTasks() {
        const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
        tasks.forEach(task => {
            const taskSlot = document.querySelector(`.task-slot[data-day="${task.day}"][data-time="${task.time}"]`);
            if (taskSlot) {
                const taskElement = document.createElement('div');
                taskElement.classList.add('task');
                taskElement.textContent = task.text;
                taskElement.addEventListener('click', () => showTaskDetails(task));
                taskSlot.appendChild(taskElement);
            }
        });
    }

    // Mostrar detalles de la tarea en el modal
    function showTaskDetails(task) {
        modalTaskTitle.textContent = task.text;
        modalTaskDescription.textContent = task.description || "Sin descripción";
        modalTaskTime.textContent = `${task.day} a las ${task.time}`;
        modal.style.display = 'flex';
    }

    // Cerrar el modal
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Añadir tarea
    addTaskButton.addEventListener('click', () => {
        const taskText = taskInput.value.trim();
        const taskDesc = taskDescription.value.trim();
        const selectedDay = currentDate.startOf('week').add(taskDay.value, 'day').format('YYYY-MM-DD');
        const selectedTime = taskTime.value;

        if (taskText && selectedDay && selectedTime) {
            const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
            tasks.push({ day: selectedDay, time: selectedTime, text: taskText, description: taskDesc });
            localStorage.setItem('tasks', JSON.stringify(tasks));
            taskInput.value = '';
            taskDescription.value = '';
            renderSchedule();
        }
    });

    // Navegación entre semanas
    prevWeekButton.addEventListener('click', () => {
        currentDate = currentDate.subtract(1, 'week');
        renderSchedule();
    });

    nextWeekButton.addEventListener('click', () => {
        currentDate = currentDate.add(1, 'week');
        renderSchedule();
    });

    // Renderizar el horario al cargar la página
    renderSchedule();
});