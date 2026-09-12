console.log('Abrió reservas.js');

$(document).ready(function () {

    // ===============================
    // 🟢 MODAL EDITAR RESERVA
    // ===============================
    const editModalReserva = document.getElementById('editModalReserva');

    if (editModalReserva) {
        editModalReserva.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cod_servicio = button.getAttribute('data-cod_servicio');
            const cedula_cliente = button.getAttribute('data-cedula_cliente');
            const nombre_cliente = button.getAttribute('data-nombre_cliente');
            const apellido_cliente = button.getAttribute('data-apellido_cliente');
            const fecha_reserva = button.getAttribute('data-fecha_reserva');
            const hora_reserva = button.getAttribute('data-hora_reserva');
            const estado_reserva = button.getAttribute('data-estado_reserva');
            const servicios = button.getAttribute('data-servicios');
            const precios = button.getAttribute('data-precios');

            const form = editModalReserva.querySelector('form');

            if (form) {
                form.querySelector('#edit_cod_reserva').value = cod_servicio;
                form.querySelector('#edit_cedula').value = cedula_cliente;
                form.querySelector('#edit_nombre').value = nombre_cliente + ' ' + apellido_cliente;
                form.querySelector('#edit_fecha').value = fecha_reserva;
                form.querySelector('#edit_hora').value = hora_reserva;
                form.querySelector('#status_edit').value = estado_reserva;

                // 🔥 TABLA SERVICIOS
                const tbody = form.querySelector('#tablaServicios');

                if (tbody) {
                    let html = '';
                    let total = 0;

                    if (servicios && precios) {
                        const listaServicios = servicios.split(' | ');
                        const listaPrecios = precios.split(' | ');

                        listaServicios.forEach((serv, i) => {
                            const precio = parseFloat(listaPrecios[i] || 0);
                            total += precio;

                            html += `
                            <tr>
                                <td>${serv}</td>
                                <td>${precio.toFixed(2)}</td>
                            </tr>
                        `;
                        });
                    }

                    tbody.innerHTML = html;
                    document.getElementById('totalPrecio').innerText = total.toFixed(2);
                }
            }
        });
    }




    function cerrarModal(idModal) {
        $(idModal).modal('hide');

        $(idModal).on('hidden.bs.modal', function () {
            $('.modal-backdrop').remove();
            $('body').removeClass('modal-open');
            $(this).off('hidden.bs.modal');
        });
    }

    function alerta(res) {
        return Swal.fire({
            icon: res.icon,
            title: res.title,
            text: res.text,
            showConfirmButton: true,
            confirmButtonText: 'Aceptar',
            timer: 2000,
            timerProgressBar: true,
            backdrop: false
        });
    }

    // ==========================
    // 🔵 Enviar formulario (Editar)
    // ==========================
    $('#formEditReserva').on('submit', function (e) {
        e.preventDefault();

        // 🔴 VALIDACIÓN SIMPLE
        const inputsInvalidos = $('#formEditReserva .is-invalid').length;

        if (inputsInvalidos > 0) {
            Swal.fire({
                icon: 'warning',
                title: 'Verifica los datos',
                text: 'Existen campos incorrectos para editar la reserva.'
            });
            return;
        }

        $.post('/admin?ruta=reserva', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    $('#formEditReserva')[0].reset();

                    $('#formEditReserva .is-invalid, #formEditReserva .is-valid')
                        .removeClass('is-invalid is-valid');

                    cerrarModal('#editModalReserva');

                    $('#table1').load(location.href + ' #table1>*', '');
                }
            });

        }, 'json');
    });

    $('#formDeleteReserva').on('submit', function (e) {
        e.preventDefault();

        $.ajax({
            url: '/admin?ruta=reserva',
            type: 'POST',
            data: $(this).serialize(),
            success: function (response) {

                let res;
                try {
                    res = typeof response === "string" ? JSON.parse(response) : response;
                } catch (err) {
                    console.error('Respuesta inválida:', response);
                    return;
                }

                Swal.fire({
                    icon: res.icon,
                    title: res.title,
                    text: res.text,
                    confirmButtonText: 'Aceptar'
                }).then(() => {

                    $('#deleteModalReservas').modal('hide');

                    if (res.icon === 'success') {
                        // Recargar tabla
                        $('#table1').load(location.href + ' #table1>*', '');
                    }
                });
            },

        });
    });




    const modalEliminarReserva = document.getElementById('deleteModalReservas');

    if (modalEliminarReserva) {
        modalEliminarReserva.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cod_servicio = button.getAttribute('data-cod_servicio');
            const nombre = button.getAttribute('data-nombre_cliente');
            const apellido = button.getAttribute('data-apellido_cliente');

            const formEliminar = document.getElementById('formDeleteReserva');

            if (formEliminar) {
                formEliminar.querySelector('#cod_reserva_eliminar').value = cod_servicio;
            }

            // Mostrar nombre completo en el modal
            modalEliminarReserva.querySelector('#nombreEliminar').textContent =
                nombre + ' ' + apellido;
        });
    }

    // Recalcular total dinámicamente
    $(document).on('input', '.precio-servicio', function () {
        let nuevoTotal = 0;
        $('.precio-servicio').each(function () {
            nuevoTotal += parseFloat($(this).val()) || 0;
        });
        $('#totalPrecio').text(`$${nuevoTotal.toFixed(2)}`);
    });

    // ✅ Limpiar modal al cerrar
    $('#editModalReserva').on('hidden.bs.modal', function () {
        const form = $('#formEditReserva')[0];
        form.reset();
        $('#formEditReserva .is-invalid, #formEditReserva .is-valid').removeClass('is-invalid is-valid');
        $('#formEditReserva .invalid-feedback, #formEditReserva .valid-feedback').hide();
        $('#tablaServicios').empty();
        $('#totalPrecio').text('$0.00');
    });

    // ===============================
    // 🔵 VALIDAR HORA DISPONIBLE
    // ===============================
    $('#edit_hora').on('input change', function () {

        console.log("==== VALIDANDO HORA ====");

        const hora = $(this).val().trim();
        const fecha = $('#edit_fecha').val();

        console.log("Hora input:", hora);
        console.log("Fecha input:", fecha);

        $.ajax({
            type: 'POST',
            url: '/admin?ruta=reserva',
            data: {
                buscar_horas: true,
                fecha_reserva: fecha
            },
            dataType: 'json',

            success: function (res) {


                if (res.success) {

                    console.log("Horas ocupadas:", res.ocupadas);

                    const horaOcupada = res.ocupadas.includes(hora);

                    if (horaOcupada) {

                        $('#edit_hora').addClass('is-invalid');

                        if ($('#edit_hora').next('.invalid-feedback').length === 0) {
                            $('#edit_hora').after(
                                '<div class="invalid-feedback">❌ Esta hora no está disponible</div>'
                            );
                        }
                    } else {


                        $('#edit_hora').removeClass('is-invalid');
                        $('#edit_hora').next('.invalid-feedback').remove();
                    }
                }
            }
        });
    });


    // ===============================
    // 🔵filtrado de fechas 
    // ===============================
    $('#fecha_inicio, #fecha_fin').on('change', function () {
        let fechaInicio = $('#fecha_inicio').val();
        let fechaFin = $('#fecha_fin').val();

        $('#tablaReservas tr').each(function () {

            let fechaTexto = $(this).find('td:eq(3)').text().trim();

            if (fechaTexto === '') {
                return;
            }

            let fechaReserva = fechaTexto.split('/').reverse().join('-');

            let mostrar = true;
            if (fechaInicio && fechaReserva < fechaInicio) {

                mostrar = false;

            }
            if (fechaFin && fechaReserva > fechaFin) {

                mostrar = false;

            }
            if (mostrar) {

                $(this).fadeIn(200);

            } else {

                $(this).fadeOut(200);

            }
        });
    });

    $('#btnLimpiarFecha').on('click', function () {

        $('#fecha_inicio').val('');
        $('#fecha_fin').val('');

        $('#tablaReservas tr').show();

    });



    $('.btnReporte').on('click', function (e) {

        e.preventDefault();

        let formulario = $(this).closest('form');

        Swal.fire({
            title: 'Reporte General de Reservas',
            text: '¿Desea generar el reporte en PDF?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Generar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {

            if (result.isConfirmed) {

                formulario[0].submit();

            }

        });

    });



    $('.btnReporteestadistico').on('click', function (e) {

        e.preventDefault();

        let formulario = $(this).closest('form');

        Swal.fire({
            title: 'Realizar Reporte Estadístico',
            text: '¿Desea generar el reporte estadístico de reservas en PDF?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Generar Reporte',
            cancelButtonText: 'Cancelar'
        }).then((result) => {

            if (result.isConfirmed) {

                formulario[0].submit();

            }

        });

    });



    $('button[name="pdfr"], button[name="pdfe"]').on('click', function () {

        let mensaje = $(this).attr('name') === 'pdfr'
            ? 'Reporte por fechas generado con éxito.'
            : 'Reporte por especialista generado con éxito.';

        setTimeout(function () {

            Swal.fire({
                icon: 'success',
                title: 'Reporte realizado',
                text: mensaje,
                timer: 6000,
                showConfirmButton: false
            });

        }, 300);

    });


    const fecha = document.getElementById("edit_fecha");

    // Fecha mínima: hoy
    if (fecha) {
        const hoy = new Date();
        const year = hoy.getFullYear();
        const month = String(hoy.getMonth() + 1).padStart(2, "0");
        const day = String(hoy.getDate()).padStart(2, "0");

        fecha.min = `${year}-${month}-${day}`;
    }

    const hora = document.getElementById("edit_hora");
    const mensajeHoraEdit = document.getElementById("mensajeHoraEdit");

    if (hora) {

        const formatoHora = /^(0?[1-9]|1[0-2]):[0-5][0-9] (am|pm)$/i;

        hora.addEventListener("input", function () {

            let valor = this.value;

            // Convertir AM/PM a minúsculas internamente
            valor = valor.replace(/AM/g, "am");
            valor = valor.replace(/PM/g, "pm");

            // Permitir únicamente números, :, espacio y letras a/p/m
            valor = valor.replace(/[^0-9: aApPmM]/g, "");

            // Máximo 8 caracteres
            valor = valor.substring(0, 8);

            this.value = valor;

            // Si está vacío, no mostrar mensaje
            if (valor === "") {
                mensajeHoraEdit.style.display = "none";
                this.setCustomValidity("");
                return;
            }

            // Validación EN TIEMPO REAL
            if (!formatoHora.test(valor)) {

                mensajeHoraEdit.textContent =
                    "Formato de hora inválido. Use 10:00 am o 10:00 pm.";

                mensajeHoraEdit.style.display = "block";

                this.setCustomValidity(
                    "Formato de hora inválido. Use 10:00 am o 10:00 pm."
                );

            } else {

                // Formato correcto
                mensajeHoraEdit.style.display = "none";

                this.setCustomValidity("");
            }
        });

        hora.addEventListener("blur", function () {

            const valor = this.value.trim();

            if (valor !== "" && !formatoHora.test(valor)) {

                mensajeHoraEdit.textContent =
                    "Formato de hora inválido. Use 10:00 am o 10:00 pm.";

                mensajeHoraEdit.style.display = "block";

                this.setCustomValidity(
                    "Formato de hora inválido. Use 10:00 am o 10:00 pm."
                );

            } else {

                mensajeHoraEdit.style.display = "none";

                this.setCustomValidity("");
            }
        });
    }


});
