document.addEventListener('DOMContentLoaded', function() {
   
    const mensajeEl = document.getElementById('mensajePagoPersonalData');
    const mensaje = mensajeEl ? JSON.parse(mensajeEl.dataset.mensaje || 'null') : null;

    if (mensaje) {
        Swal.fire({
            icon: mensaje.icon,
            title: mensaje.title,
            text: mensaje.text,
            confirmButtonText: 'Aceptar'
        });
    }

    const formRegistrar = document.getElementById('formRegistrarPagoPersonal');
    const formAnular = document.getElementById('formAnularPagoPersonal');
    const servicioSelect = document.getElementById('cod_servicio_personal');
    const detalle = document.getElementById('detalleServicioPersonal');
    const tableEl = document.getElementById('pagospersonalTable');
    const fechaPagoPersonal = document.getElementById('fecha_pago_personal');

    if (window.flatpickr) {
        flatpickr('#hora_pago_personal', {
            allowInput: true,
            dateFormat: 'H:i',
            enableTime: true,
            minuteIncrement: 5,
            noCalendar: true,
            time_24hr: true
        });
    }

    // DataTable
    if (tableEl && window.jQuery && window.jQuery.fn && window.jQuery.fn.DataTable) {
        $('#pagospersonalTable').DataTable({
            responsive: true,
            autoWidth: false,
            language: {
                processing: 'Procesando...',
                search: 'Buscar:',
                lengthMenu: 'Mostrar _MENU_ registros',
                info: 'Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
                infoEmpty: 'Mostrando registros del 0 al 0 de un total de 0 registros',
                infoFiltered: '(filtrado de un total de _MAX_ registros)',
                loadingRecords: 'Cargando...',
                zeroRecords: 'No se encontraron resultados',
                emptyTable: 'Ningún dato disponible en esta tabla',
                paginate: { first: 'Primero', previous: 'Anterior', next: 'Siguiente', last: 'Último' },
                aria: { sortAscending: ': Activar para ordenar la columna de manera ascendente', sortDescending: ': Activar para ordenar la columna de manera descendente' }
            }
        });
    }

    // Mostrar detalle al seleccionar servicio
    function mostrarDetalleServicio(option) {
        if (!option || !option.value) {
            if (detalle) detalle.style.display = 'none';
            return;
        }
        const precio = parseFloat(option.dataset.precio || 0);
        if (detalle) {
            detalle.style.display = 'block';
            detalle.innerHTML = `Servicio seleccionado: <strong>${option.text}</strong><br>Cliente: <strong>${option.dataset.cliente || 'Sin cliente'}</strong><br>Especialista: <strong>${option.dataset.especialista || 'Sin especialista'}</strong><br>Monto total del servicio: <strong>${precio.toFixed(2)} $</strong>`;
        }
    }

    if (servicioSelect) {
        servicioSelect.addEventListener('change', function() {
            mostrarDetalleServicio(servicioSelect.options[servicioSelect.selectedIndex]);
        });
    }

    // fecha a la fecha actual (no pasado ni futuro)
    if (fechaPagoPersonal) {
        const hoy = new Date();
        const anio = hoy.getFullYear();
        const mes = String(hoy.getMonth() + 1).padStart(2, '0');
        const dia = String(hoy.getDate()).padStart(2, '0');
        const fechaHoy = `${anio}-${mes}-${dia}`;
        fechaPagoPersonal.setAttribute('min', fechaHoy);
        fechaPagoPersonal.setAttribute('max', fechaHoy);
        // Establecer la fecha por defecto a hoy
        fechaPagoPersonal.value = fechaHoy;

        fechaPagoPersonal.addEventListener('change', function () {
            if (!this.value) {
                Swal.fire({ icon: 'error', title: 'Fecha requerida', text: 'Debe seleccionar una fecha de pago.' });
            } else if (this.value !== fechaHoy) {
                Swal.fire({ icon: 'error', title: 'Fecha inválida', text: 'La fecha de pago debe ser la fecha actual.' });
                this.value = '';
            }
        });
    }

    // Manejo del registro (submit)
    if (formRegistrar) {
        formRegistrar.addEventListener('submit', function(e) {
            e.preventDefault();
            //  la fecha debe ser la fecha actual
            if (fechaPagoPersonal) {
                const valorFecha = fechaPagoPersonal.value ? fechaPagoPersonal.value.trim() : '';
                const hoy = new Date();
                const anio = hoy.getFullYear();
                const mes = String(hoy.getMonth() + 1).padStart(2, '0');
                const dia = String(hoy.getDate()).padStart(2, '0');
                const fechaHoy = `${anio}-${mes}-${dia}`;
                if (!valorFecha) {
                    Swal.fire({ icon: 'error', title: 'Fecha requerida', text: 'Seleccione la fecha de pago.' });
                    return;
                }
                if (valorFecha !== fechaHoy) {
                    Swal.fire({ icon: 'error', title: 'Fecha inválida', text: 'La fecha de pago debe ser la fecha actual.' });
                    return;
                }
            }

            const horaInput = document.getElementById('hora_pago_personal');
            if (horaInput && horaInput.value && horaInput.value.length === 5) {
                horaInput.value = `${horaInput.value}:00`;
            }

            fetch('/admin?ruta=pagospersonal', { method: 'POST', body: new FormData(formRegistrar) })
                .then(function(response) {
                    if (!response.ok) throw new Error('Error en la solicitud');
                    return response.json();
                })
                .then(function(res) {
                    if (res && res.icon === 'success') {
                        const modal = document.getElementById('modalRegistrarPagoPersonal');
                        formRegistrar.reset();
                        if (detalle) detalle.style.display = 'none';
                        $('#pagospersonalTable').load(location.href + ' #pagospersonalTable>*', '');

                        const mostrarExito = function() {
                            document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
                                backdrop.remove();
                            });
                            document.body.classList.remove('modal-open');
                            if (res.notificacion) {
                                window.dispatchEvent(new CustomEvent('pago-personal-registrado'));
                            }
                            Swal.fire({
                                icon: res.icon,
                                title: res.title,
                                text: res.text,
                                timer: 1600,
                                showConfirmButton: false,
                                backdrop: false
                            });
                        };

                        if (modal && window.bootstrap) {
                            modal.addEventListener('hidden.bs.modal', mostrarExito, { once: true });
                            bootstrap.Modal.getOrCreateInstance(modal).hide();
                        } else {
                            mostrarExito();
                        }
                        return;
                    }

                    // Si el servidor devuelve errores por campos, mostrarlos
                    if (res && res.errors) {
                        const mensajes = [];
                        for (const k in res.errors) {
                            if (Object.prototype.hasOwnProperty.call(res.errors, k)) {
                                mensajes.push(res.errors[k]);
                            }
                        }
                        Swal.fire({ icon: 'error', title: res.title || 'Error', html: mensajes.join('<br>') });
                        return;
                    }

                    Swal.fire({ icon: res && res.icon ? res.icon : 'error', title: res && res.title ? res.title : 'Error', text: res && res.text ? res.text : 'No se pudo procesar la solicitud.' });
                })
                .catch(function() {
                    Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo conectar con el servidor.' });
                });
        });
    }

    
    const inputAnular = document.getElementById('cod_pago_personal_a_anular');
    let filaPagoPersonalAnular = null;
    if (inputAnular) {
        document.querySelectorAll('.btn-anular-personal').forEach(function(btn) {
            btn.addEventListener('click', function() {
                const cod = btn.dataset.codPagoPersonal || btn.getAttribute('data-cod-pago-personal');
                if (cod) {
                    inputAnular.value = cod;
                    filaPagoPersonalAnular = btn.closest('tr');
                }
            });
        });
    }

    // Anular pago personal
    if (formAnular) {
        formAnular.addEventListener('submit', function(e) {
            e.preventDefault();
            fetch('/admin?ruta=pagospersonal', { method: 'POST', body: new FormData(formAnular) })
                .then(function(response) {
                    if (!response.ok) throw new Error('Error en la solicitud');
                    return response.json();
                })
                .then(function(res) {
                    if (res && res.icon === 'success') {
                        if (filaPagoPersonalAnular) {
                            filaPagoPersonalAnular.children[9].innerHTML = '<span class="badge bg-danger">Anulado</span>';
                            const boton = filaPagoPersonalAnular.querySelector('.btn-anular-personal');
                            if (boton) {
                                boton.disabled = true;
                                boton.removeAttribute('data-bs-toggle');
                                boton.removeAttribute('data-bs-target');
                            }
                        }

                        const modal = document.getElementById('modalAnularPagoPersonal');
                        const mostrarExito = function() {
                            document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
                                backdrop.remove();
                            });
                            document.body.classList.remove('modal-open');
                            Swal.fire({
                                icon: res.icon,
                                title: res.title,
                                text: res.text || 'El pago personal se anuló correctamente.',
                                timer: 1400,
                                showConfirmButton: false,
                                backdrop: false
                            });
                        };

                        if (modal && window.bootstrap) {
                            modal.addEventListener('hidden.bs.modal', mostrarExito, { once: true });
                            bootstrap.Modal.getOrCreateInstance(modal).hide();
                        } else {
                            mostrarExito();
                        }
                        formAnular.reset();
                        return;
                    }
                    Swal.fire({ icon: res && res.icon ? res.icon : 'error', title: res && res.title ? res.title : 'Error', text: res && res.text ? res.text : 'No se pudo anular el pago personal.' });
                })
                .catch(function() {
                    Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo conectar con el servidor.' });
                });
        });
    }
});
