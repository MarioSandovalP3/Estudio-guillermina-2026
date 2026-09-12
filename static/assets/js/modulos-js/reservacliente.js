console.log('Abrio rrservas de clientes.js');



document.addEventListener('DOMContentLoaded', function () {

    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {

        initialView: window.innerWidth < 768 ? 'timeGridDay' : 'dayGridMonth',
        locale: 'es',
        selectable: true,
        editable: false,
        themeSystem: 'bootstrap5',

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: window.innerWidth < 768 ? 'timeGridDay,timeGridWeek' : 'dayGridMonth,timeGridWeek,timeGridDay'
        },

        buttonText: {
            today: 'Hoy',
            month: 'Mes',
            week: 'Semana',
            day: 'Día'
        },

        eventTimeFormat: {
            hour: 'numeric',
            minute: '2-digit',
            meridiem: 'short'
        },

        slotLabelFormat: {
            hour: 'numeric',
            minute: '2-digit',
            meridiem: 'short'
        },

        dateClick: function (info) {
            const fechaSeleccionada = new Date(info.dateStr + "T00:00:00");
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);

            if (fechaSeleccionada.getTime() < hoy.getTime()) {
                Swal.fire('Fecha inválida', '❌ No se puede seleccionar una fecha anterior a hoy.', 'error');
                return;
            }

            document.getElementById('formReserva').reset();
            document.getElementById('fecha_reserva').value = info.dateStr;
            new bootstrap.Modal(document.getElementById('modalReserva')).show();
        },

        eventClick: function (info) {
            mostrarDetalles(info.event);
        },

        // ✅ AQUÍ VA BIEN COLOCADO
        eventDidMount: function (info) {

            const status = info.event.extendedProps.status;

            if (status == 0) {
                info.el.style.backgroundColor = '#dc3545';
                info.el.style.borderColor = '#dc3545';
                info.el.style.opacity = '0.7';
                info.el.style.textDecoration = 'line-through';
            }

            if (status == 1) {
                info.el.style.backgroundColor = '#38f827';
                info.el.style.borderColor = '#000000';
            }

            info.el.style.fontWeight = 'bold';
        }

    });

    calendar.render();



    // ================== CARGAR RESERVAS ==================
    function cargarReservas() {
        $.ajax({
            url: '/admin?ruta=misreservas&cargar_reservas=1',
            type: 'GET',
            dataType: 'json',
            success: function (reservas) {



                // 🔥 AQUÍ VA EL CAMBIO
                calendar.getEventSources().forEach(s => s.remove());
                calendar.addEventSource(reservas);

            },
            error: function (xhr) {
                console.error("ERROR:", xhr.responseText);
            }
        });
    }
    cargarReservas();



    // ================== REGISTRAR RESERVA ==================
    $('#formReserva').on('submit', function (e) {
        e.preventDefault();

        const reserva = {
            cedula: $('#cedula').val(),
            nombre_usuario: $('#nombre_usuario').val(),
            fecha_reserva: $('#fecha_reserva').val(),
            hora_reserva: $('#hora_reserva').val(),
            servicio: []
        };

        // ================== SERVICIOS ==================
        $('#formReserva input[name="servicio[]"]:checked').each(function () {
            reserva.servicio.push($(this).val());
        });

        if (reserva.servicio.length === 0) {
            Swal.fire('Error', 'Debe seleccionar al menos un servicio.', 'error');
            return;
        }

        // ================== ESPECIALISTA ==================
        let estilista = $('#estilista').val();
        let manicurista = $('#manicurista').val();


        estilista = estilista ? estilista : null;
        manicurista = manicurista ? manicurista : null;

        // Validación: ninguno seleccionado
        if (!estilista && !manicurista) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Debe seleccionar un estilista o un manicurista.'
            });
            return;
        }


        if (estilista && manicurista) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Solo puede seleccionar un especialista.'
            });
            return;
        }

        // ================== AJAX ==================
        $.ajax({
            type: 'POST',
            url: '/admin?ruta=reservacliente',
            data: $(this).serialize(),
            dataType: 'json',
            success: function (resp) {

                if (resp.success) {

                    bootstrap.Modal.getInstance(
                        document.getElementById('modalReserva')
                    ).hide();

                    Swal.fire({
                        icon: 'success',
                        title: 'Reserva registrada',
                        timer: 1500,
                        showConfirmButton: false
                    });

                    cargarReservas();
                    $('#formReserva')[0].reset();

                } else {
                    Swal.fire('Error', resp.message, 'error');
                }
            },
            error: function (xhr) {
                console.error("ERROR AJAX:", xhr.responseText);
            }
        });
    });


    // ================== ACTUALIZAR RESUMEN DE SERVICIOS ==================
    function actualizarResumenServicios() {

        let html = '';
        let total = 0;

        let seleccionados = $('#formReserva input[name="servicio[]"]:checked');

        seleccionados.each(function () {

            let label = $(this).closest('.form-check').find('label').text();
            let precio = parseFloat(label.split('$')[1]);

            html += `
            <tr>
                <td><i class="bi bi-check-circle text-success"></i> ${label.split('-')[0]}</td>
                <td>$${precio.toFixed(2)}</td>
            </tr>
        `;

            total += precio;
        });

        if (seleccionados.length === 0) {

            html = `
            <tr>
                <td colspan="2" class="text-muted py-3">
                    No hay servicios seleccionados
                </td>
            </tr>
        `;
        } else {

            html += `
            <tr class="table-light fw-bold">
                <td>Total</td>
                <td>$${total.toFixed(2)}</td>
            </tr>
        `;
        }

        $('#tablaServicios').html(html);
    }


    // ================== EVENTO CHECKBOX ==================
    $('#formReserva input[name="servicio[]"]').on('change', function () {
        actualizarResumenServicios();
    });


    // ================== LIMPIAR AL CERRAR MODAL ==================
    $('#modalReserva').on('hidden.bs.modal', function () {

        // reset formulario
        $('#formReserva')[0].reset();

        // reset tabla
        $('#tablaServicios').html(`
        <tr>
            <td colspan="2" class="text-muted py-3">
                No hay servicios seleccionados
            </td>
        </tr>
    `);
    });

    // evento
    $('#formReserva input[name="servicio[]"]').on('change', actualizarResumenServicios);
    //validar hora ocupada con fecha
    $('#hora_reserva').on('input change', function () {
        const hora = $(this).val().trim();
        const fecha = $('#fecha_reserva').val();
        const parsleyHora = $('#hora_reserva').parsley();

        if (!hora || !fecha) return;

        $.ajax({
            type: 'POST',
            url: '/admin?ruta=reservacliente',
            data: {
                buscar_horas: true,
                fecha_reserva: fecha
            },
            dataType: 'json',
            success: function (res) {
                if (res.success) {
                    const horaOcupada = res.ocupadas.includes(hora); // compara hora exacta en esa fecha

                    if (horaOcupada) {
                        const errorExists = parsleyHora.getErrorsMessages().includes('❌ Esta hora no está disponible.');
                        if (!errorExists) {
                            window.ParsleyUI.removeError(parsleyHora, 'hora_ocupada');
                            window.ParsleyUI.addError(parsleyHora, 'hora_ocupada', '❌ Esta hora no está disponible.');
                        }
                    } else {
                        window.ParsleyUI.removeError(parsleyHora, 'hora_ocupada');
                    }
                }
            },
            error: function (xhr) {
                console.error('Error verificando horas ocupadas:', xhr.responseText);
            }
        });
    });

    $(document).ready(function () {
        // ✅ Validador Parsley corregido (permite hoy)
        window.Parsley.addValidator('fechafutura', {
            validateString: function (value) {
                const fecha = new Date(value + "T00:00:00");
                const hoy = new Date();
                hoy.setHours(0, 0, 0, 0);
                return fecha.getTime() >= hoy.getTime();
            },
            messages: {
                es: '❌ No se permite seleccionar una fecha anterior a hoy.'
            }
        });

        // Inicializar Parsley en el formulario
        $('#formReserva').parsley();

        // Aplicar mensaje obligatorio a los campos requeridos
        $('#hora_reserva').each(function () {
            $(this).attr('data-parsley-required', 'true')
                .attr('data-parsley-error-message', '❌ Este campo es obligatorio.');
        });

        // ✅ Limitar el campo de fecha directamente desde HTML
        const inputFecha = document.getElementById('fecha_reserva');
        if (inputFecha) {
            const hoy = new Date();
            const yyyy = hoy.getFullYear();
            const mm = String(hoy.getMonth() + 1).padStart(2, '0');
            const dd = String(hoy.getDate()).padStart(2, '0');
            inputFecha.min = `${yyyy}-${mm}-${dd}`;
        }


    });

    const modalReserva = document.getElementById('modalReserva');
    const formReserva = document.getElementById('formReserva');

    // Al cerrar el modal (por botón, "X", o click fuera)
    modalReserva.addEventListener('hidden.bs.modal', function () {

        // 🔹 1. Si Parsley está cargado, limpiar su estado completamente
        if ($(formReserva).parsley) {
            $(formReserva).parsley().reset();
        }

        // 🔹 2. Resetear todos los campos del formulario
        formReserva.reset();

        // 🔹 3. Eliminar manualmente cualquier lista de errores residual
        formReserva.querySelectorAll('.parsley-errors-list').forEach(errorList => {
            errorList.remove();
        });

        // 🔹 4. Quitar clases de validación (rojo, verde, etc.)
        formReserva.querySelectorAll('.is-valid, .is-invalid, .parsley-success, .parsley-error')
            .forEach(el => el.classList.remove('is-valid', 'is-invalid', 'parsley-success', 'parsley-error'));

        // 🔹 5. Ocultar tooltips abiertos (si los hay)
        const tooltipList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipList.map(function (tooltipEl) {
            const tooltip = bootstrap.Tooltip.getInstance(tooltipEl);
            if (tooltip) tooltip.hide();
        });

    });


    $(document).ready(function () {
        let mostrarErroresReserva = false;
        let temporizadorReserva;
        $("#modalReserva").on("shown.bs.modal", function () {
            mostrarErroresReserva = false;
            clearTimeout(temporizadorReserva);
            $("#error-hora").hide();
            $("#error-servicios").hide();
            $("#error-especialista").hide();
            temporizadorReserva = setTimeout(function () {
                mostrarErroresReserva = true;
                validarCamposReserva();
            }, 3000);
        });
        function validarCamposReserva() {
            if (!mostrarErroresReserva) return;
            if ($("#hora_reserva").val().trim() === "") {
                $("#error-hora").fadeIn(200);
            } else {
                $("#error-hora").fadeOut(200);
            }
            if ($('input[name="servicio[]"]:checked').length === 0) {
                $("#error-servicios").fadeIn(200);
            } else {
                $("#error-servicios").fadeOut(200);
            }
            if ($("#estilista").val() === null && $("#manicurista").val() === null) {
                $("#error-especialista").fadeIn(200);
            } else {
                $("#error-especialista").fadeOut(200);
            }
        }

        $('input[name="servicio[]"]').on("change", function () {
            if ($('input[name="servicio[]"]:checked').length > 0) {
                $("#error-servicios").fadeOut(200);
            } else if (mostrarErroresReserva) {
                $("#error-servicios").fadeIn(200);
            }
        });
        $("#estilista,#manicurista").on("change", function () {
            if ($("#estilista").val() !== null || $("#manicurista").val() !== null) {
                $("#error-especialista").fadeOut(200);
            } else if (mostrarErroresReserva) {
                $("#error-especialista").fadeIn(200);
            }
        });
        $("#modalReserva").on("hidden.bs.modal", function () {
            clearTimeout(temporizadorReserva);
            mostrarErroresReserva = false;
            $("#error-hora").hide();
            $("#error-servicios").hide();
            $("#error-especialista").hide();
        });
    });


    // ================== VALIDACIÓN DE HORA EN TIEMPO REAL ==================

    const inputHora = document.getElementById("hora_reserva");
    const errorHora = document.getElementById("error-hora");

    if (inputHora && errorHora) {

        function validarHoraTiempoReal() {

            const valor = inputHora.value.trim();

            // CAMPO VACÍO
            if (valor === "") {
                errorHora.style.display = "none";
                inputHora.setCustomValidity("");
                return;
            }

            const formato = /^(0[1-9]|1[0-2]):([0-5][0-9]) (AM|PM)$/i;


            if (!formato.test(valor)) {

                errorHora.innerHTML =
                    '<i class="bi bi-exclamation-circle-fill me-1"></i>' +
                    'Formato inválido. Use 08:00 AM o 10:00 PM';

                errorHora.style.display = "block";

                inputHora.setCustomValidity("Formato inválido");

                return;
            }
            const partes = valor.split(" ");

            const horaMinutos = partes[0];
            const periodo = partes[1].toUpperCase();

            let partesHora = horaMinutos.split(":");

            let horas = parseInt(partesHora[0]);
            let minutos = parseInt(partesHora[1]);

            // PM
            if (periodo === "PM" && horas !== 12) {
                horas += 12;
            }

            // 12 AM = 00:00
            if (periodo === "AM" && horas === 12) {
                horas = 0;
            }

            const minutosTotales = (horas * 60) + minutos;

            if (minutosTotales < 360 || minutosTotales > 1200) {

                errorHora.innerHTML =
                    '<i class="bi bi-exclamation-circle-fill me-1"></i>' +
                    'La hora debe estar entre 06:00 AM y 08:00 PM';

                errorHora.style.display = "block";

                inputHora.setCustomValidity("Hora fuera del límite");

                return;
            }
            errorHora.style.display = "none";

            inputHora.setCustomValidity("");
        }


        inputHora.addEventListener("input", function () {

            this.value = this.value
                .replace(/[^0-9: aApPmM]/g, "")
                .substring(0, 8);

            validarHoraTiempoReal();
        });
    }
});
