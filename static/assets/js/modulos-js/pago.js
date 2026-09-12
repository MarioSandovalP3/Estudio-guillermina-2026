document.addEventListener('DOMContentLoaded', function() {
    const formRegistrarPago = document.getElementById('formRegistrarPago');
    const formAnularPago = document.getElementById('formAnularPago');
    const filtroInicio = document.getElementById('filtroInicio');
    const filtroFin = document.getElementById('filtroFin');
    const btnLimpiar = document.getElementById('btnLimpiar');
    const tabla = document.querySelector('#table1');
    const filas = tabla ? tabla.querySelectorAll('tbody tr') : [];

    function filtrar() {
        const inicio = filtroInicio && filtroInicio.value ? new Date(filtroInicio.value) : null;
        const fin = filtroFin && filtroFin.value ? new Date(filtroFin.value) : null;

        filas.forEach(fila => {
            const fechaTexto = fila.children[2]?.textContent.trim();
            const fecha = fechaTexto ? new Date(fechaTexto) : null;

            let visible = true;
            if (inicio && fecha && fecha < inicio) visible = false;
            if (fin && fecha && fecha > fin) visible = false;

            fila.style.display = visible ? '' : 'none';
        });
    }

    function limpiar() {
        if (filtroInicio) filtroInicio.value = '';
        if (filtroFin) filtroFin.value = '';
        filas.forEach(fila => fila.style.display = '');
    }

    if (filtroFin && filtroInicio && filas.length) {
        filtroFin.addEventListener('change', filtrar);
        filtroInicio.addEventListener('change', filtrar);
    }

    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', function(e) {
            e.preventDefault();
            limpiar();
        });
    }

    const formPDFHeader = document.getElementById('formPDFHeader');
    const formExcelHeader = document.getElementById('formExcelHeader');
    const btnHeaderPDF = document.getElementById('btnHeaderPDF');
    const btnHeaderExcel = document.getElementById('btnHeaderExcel');

    function copyFiltersTo(form) {
        if (!form) return;
        form.innerHTML = '';
        const inputs = ['filtroInicio','filtroFin','cod_tipo_pago','status'];
        inputs.forEach(name => {
            const el = document.getElementById(name);
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = name;
            input.value = el ? el.value : '';
            form.appendChild(input);
        });
    }

    if (formPDFHeader && btnHeaderPDF) {
        btnHeaderPDF.addEventListener('click', function(e) {
            e.preventDefault();
            copyFiltersTo(formPDFHeader);
            formPDFHeader.submit();
        });
    }

    if (formExcelHeader && btnHeaderExcel) {
        btnHeaderExcel.addEventListener('click', function(e) {
            e.preventDefault();
            copyFiltersTo(formExcelHeader);
            formExcelHeader.submit();
        });
    }

    if (window.jQuery && $('#formPDF').length) {
        $('#formPDF').on('submit', function() {
            setTimeout(function() {
                Swal.fire({
                    title: 'Éxito',
                    text: 'Reporte Generado.',
                    icon: 'success'
                });
            }, 1000);
        });
    }

    function alertaPago(config) {
        return Swal.fire({
            ...config,
            timer: config.timer ?? 2000,
            timerProgressBar: true,
            backdrop: false,
            showConfirmButton: config.showConfirmButton ?? true,
            confirmButtonText: config.confirmButtonText ?? 'Aceptar'
        });
    }

    const clienteSelect = document.getElementById('cedula_cliente');
    const servicioSelect = document.getElementById('cod_servicio');
    const bloqueServicioPago = document.getElementById('bloqueServicioPago');
    const montoInput = document.getElementById('monto');
    const detalleServicioPago = document.getElementById('detalleServicioPago');
    const fechaPago = document.getElementById('fecha_pago');
    const usarFechaServicio = document.getElementById('usar_fecha_servicio');
    let fechaServicioActual = '';

    function mostrarDetalleServicio() {
        const option = servicioSelect.options[servicioSelect.selectedIndex];
        if (!option || !option.value) {
            if (detalleServicioPago) detalleServicioPago.style.display = 'none';
            if (montoInput) montoInput.value = '';
            return;
        }

        const precioData = option.dataset.precio;
        const preciosListData = option.dataset.precios;
        let precio = null;
        if (typeof precioData !== 'undefined' && precioData !== '') {
            precio = parseFloat(precioData);
        } else if (typeof preciosListData !== 'undefined' && preciosListData) {
           
            try {
                const partes = preciosListData.split(' | ');
                let suma = 0;
                partes.forEach(p => { const v = parseFloat(p||0); if (!isNaN(v)) suma += v; });
                precio = suma > 0 ? suma : null;
            } catch (err) {
                precio = null;
            }
        }
        const fecha = option.dataset.fechaRealizacion || '';
        // almacenar la fecha del servicio 
        fechaServicioActual = fecha;

        if (montoInput) {
            if (precio !== null) {
                montoInput.value = precio.toFixed(2);
                montoInput.placeholder = '';
                montoInput.readOnly = true;
            } else {
                montoInput.value = '';
                montoInput.placeholder = 'Ingrese monto';
                montoInput.readOnly = false;
            }
        }
        if (detalleServicioPago) {
            detalleServicioPago.style.display = 'block';
            const montoTexto = (precio !== null) ? `${precio.toFixed(2)} $` : 'Pendiente';
            detalleServicioPago.innerHTML = `Servicio seleccionado: <strong>${option.text}</strong><br>` +
                `Fecha de realización: <strong>${fecha || 'Sin fecha'}</strong><br>` +
                `Monto automático: <strong>${montoTexto}</strong>`;
        }

        // Si el checkbox está activado, usar la fecha del servicio
        if (usarFechaServicio && usarFechaServicio.checked) {
            if (fecha) {
                if (fechaPago) {
                    fechaPago.value = fecha;
                    fechaPago.setAttribute('min', fecha);
                    fechaPago.setAttribute('max', fecha);
                }
            } else {
                alertaPago({ icon: 'error', title: 'Sin fecha', text: 'El servicio no tiene fecha registrada.' });
                usarFechaServicio.checked = false;
            }
        }
    }

    if (clienteSelect && servicioSelect) {
        function resetServicio() {
            servicioSelect.querySelectorAll('option').forEach(function(option) {
                if (!option.value) {
                    option.hidden = false;
                    option.disabled = false;
                    return;
                }

                option.hidden = true;
                option.disabled = true;
            });

            servicioSelect.value = '';
            servicioSelect.disabled = true;
            if (bloqueServicioPago) bloqueServicioPago.style.display = 'none';
            if (detalleServicioPago) detalleServicioPago.style.display = 'none';
            if (montoInput) montoInput.value = '';
        }

        function actualizarServiciosPorCliente() {
            const cedula = clienteSelect.value;
            const ahora = new Date();
            const fechaHoy = `${ahora.getFullYear()}-${String(ahora.getMonth() + 1).padStart(2, '0')}-${String(ahora.getDate()).padStart(2, '0')}`;
            let hayVisible = false;
            let primerServicio = null;

            servicioSelect.querySelectorAll('option').forEach(function(option) {
                if (!option.value) {
                    option.hidden = false;
                    option.disabled = false;
                    return;
                }

                const coincide = !!cedula &&
                    option.dataset.cliente === cedula &&
                    option.dataset.fechaRealizacion === fechaHoy;
                option.hidden = !coincide;
                option.disabled = !coincide;

                if (coincide && !primerServicio) {
                    primerServicio = option;
                    hayVisible = true;
                }
            });

            servicioSelect.value = primerServicio ? primerServicio.value : '';
            servicioSelect.disabled = !hayVisible;
            if (bloqueServicioPago) bloqueServicioPago.style.display = hayVisible ? 'block' : 'none';

            if (hayVisible) {
                mostrarDetalleServicio();
            } else {
                if (detalleServicioPago) detalleServicioPago.style.display = 'none';
                if (montoInput) montoInput.value = '';
            }
        }

        resetServicio();
        clienteSelect.addEventListener('change', actualizarServiciosPorCliente);

        const modalRegistrarPago = document.getElementById('modalRegistrarPago');
        if (modalRegistrarPago) {
            modalRegistrarPago.addEventListener('show.bs.modal', function () {
                const ahora = new Date();
                const fechaHoy = `${ahora.getFullYear()}-${String(ahora.getMonth() + 1).padStart(2, '0')}-${String(ahora.getDate()).padStart(2, '0')}`;
                const serviciosDeHoy = Array.from(servicioSelect.options).filter(function (option) {
                    return option.value && option.dataset.fechaRealizacion === fechaHoy;
                });

                servicioSelect.querySelectorAll('option').forEach(function (option) {
                    if (!option.value) {
                        option.hidden = false;
                        option.disabled = false;
                        return;
                    }

                    const esDeHoy = option.dataset.fechaRealizacion === fechaHoy;
                    option.hidden = !esDeHoy;
                    option.disabled = !esDeHoy;
                });

                if (!serviciosDeHoy.length) {
                    resetServicio();
                    return;
                }

                // Al abrir, mantener visibles todas las reservas de hoy,
                // aunque pertenezcan a clientes distintos.
                clienteSelect.value = serviciosDeHoy[0].dataset.cliente || '';
                servicioSelect.disabled = false;
                if (bloqueServicioPago) bloqueServicioPago.style.display = 'block';
                servicioSelect.value = serviciosDeHoy[0].value;
                mostrarDetalleServicio();
            });
        }
    }

    if (servicioSelect) {
        servicioSelect.addEventListener('change', function () {
            const option = servicioSelect.options[servicioSelect.selectedIndex];
            if (option && option.value && clienteSelect) {
                clienteSelect.value = option.dataset.cliente || '';
            }
            mostrarDetalleServicio();
        });
    }

    // fecha a la fecha actual (no pasado ni futuro)
    if (fechaPago) {
        const hoy = new Date();
        const anio = hoy.getFullYear();
        const mes = String(hoy.getMonth() + 1).padStart(2, '0');
        const dia = String(hoy.getDate()).padStart(2, '0');
        const fechaHoy = `${anio}-${mes}-${dia}`;
        // Establecer min y max para que sólo pueda seleccionarse la fecha actual
        fechaPago.setAttribute('min', fechaHoy);
        fechaPago.setAttribute('max', fechaHoy);
        // Establecer la fecha por defecto a hoy
        fechaPago.value = fechaHoy;

        // cambio de fecha
        fechaPago.addEventListener('change', function () {
            if (!this.value) {
                alertaPago({ icon: 'error', title: 'Fecha requerida', text: 'Debe seleccionar una fecha de pago.' });
                return;
            }

            // permitir fecha hoy o la fecha del servicio seleccionada
            if (this.value !== fechaHoy && this.value !== fechaServicioActual) {
                alertaPago({ icon: 'error', title: 'Fecha inválida', text: 'La fecha de pago debe ser la fecha actual o la fecha del servicio.' });
                this.value = '';
            }
        });
    }

    const inputCodPagoAnular = document.getElementById('cod_pago_a_anular');
    let filaPagoAnular = null;
    let clientePagoAnular = 'Cliente no disponible';
    let fechaPagoAnular = 'Sin fecha';
    if (inputCodPagoAnular) {
        document.addEventListener('click', function(event) {
            const btn = event.target.closest('.btn-anular');
            if (!btn) return;

            const codPago = btn.dataset.codPago || btn.getAttribute('data-cod-pago');
            const cliente = btn.dataset.cliente || btn.getAttribute('data-cliente') || 'Cliente no disponible';
            const fechaPago = btn.dataset.fechaPago || btn.getAttribute('data-fecha-pago') || 'Sin fecha';
            if (codPago) {
                inputCodPagoAnular.value = codPago;
                filaPagoAnular = btn.closest('tr');
                clientePagoAnular = cliente;
                fechaPagoAnular = fechaPago;
            } else {
                inputCodPagoAnular.value = '';
                filaPagoAnular = null;
                clientePagoAnular = 'Cliente no disponible';
                fechaPagoAnular = 'Sin fecha';
            }
        });
    }

    if (formRegistrarPago) {
        formRegistrarPago.addEventListener('submit', function(e) {
            e.preventDefault();

            //  la fecha debe ser la fecha actual
            if (fechaPago) {
                const valorFecha = fechaPago.value ? fechaPago.value.trim() : '';
                const hoy = new Date();
                const anio = hoy.getFullYear();
                const mes = String(hoy.getMonth() + 1).padStart(2, '0');
                const dia = String(hoy.getDate()).padStart(2, '0');
                const fechaHoy = `${anio}-${mes}-${dia}`;
                if (!valorFecha) {
                    alertaPago({ icon: 'error', title: 'Fecha requerida', text: 'Seleccione la fecha de pago.' });
                    return;
                }
                // permitir fecha hoy o la fecha del servicio (si se seleccionó el checkbox o coincide)
                if (valorFecha !== fechaHoy && valorFecha !== fechaServicioActual) {
                    alertaPago({ icon: 'error', title: 'Fecha inválida', text: 'La fecha de pago debe ser la fecha actual o la fecha del servicio.' });
                    return;
                }
            }

            fetch('/admin?ruta=pagos', {
                method: 'POST',
                body: new FormData(formRegistrarPago)
            })
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('No se pudo registrar el pago.');
                }
                return response.json();
            })
            .then(function(res) {
                if (res && res.icon === 'success') {
                    const modal = document.getElementById('modalRegistrarPago');
                    const clienteSeleccionado = clienteSelect && clienteSelect.selectedIndex >= 0 ? clienteSelect.options[clienteSelect.selectedIndex] : null;
                    const nombreCliente = clienteSeleccionado ? clienteSeleccionado.textContent.trim() : 'Cliente no seleccionado';
                    const fechaRegistrada = fechaPago && fechaPago.value ? fechaPago.value : 'Sin fecha';

                    formRegistrarPago.reset();
                    if (montoInput) montoInput.value = '';
                    if (detalleServicioPago) detalleServicioPago.style.display = 'none';
                    if (window.jQuery && $('#table1').length) {
                        $('#table1').load(location.href + ' #table1>*', '');
                    }

                    const mostrarExito = function() {
                        document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
                            backdrop.remove();
                        });
                        document.body.classList.remove('modal-open');

                        alertaPago({
                            icon: res.icon,
                            title: res.title,
                            text: res.text,
                            confirmButtonText: 'Aceptar'
                        });

                        window.dispatchEvent(new CustomEvent('pago-registrado', {
                            detail: {
                                cliente: nombreCliente,
                                fecha: fechaRegistrada
                            }
                        }));
                    };

                    if (modal && window.bootstrap) {
                        modal.addEventListener('hidden.bs.modal', mostrarExito, { once: true });
                        bootstrap.Modal.getOrCreateInstance(modal).hide();
                    } else {
                        mostrarExito();
                    }
                } else {
                    alertaPago({
                        icon: res.icon || 'error',
                        title: res.title || 'Error',
                        text: res.text || 'No se pudo registrar el pago.'
                    });
                }
            })
            .catch(function() {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'No se pudo conectar con el servidor.'
                });
            });
        });
    }

    if (formAnularPago) {
        formAnularPago.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!inputCodPagoAnular || !inputCodPagoAnular.value.trim()) {
                alertaPago({
                    icon: 'error',
                    title: 'Error',
                    text: 'Debe seleccionar un pago para anular.'
                });
                return;
            }

            fetch('/admin?ruta=pagos', {
                method: 'POST',
                body: new FormData(formAnularPago)
            })
                .then(function(response) {
                    if (!response.ok) throw new Error('No se pudo anular el pago.');
                    return response.json();
                })
                .then(function(res) {
                    if (res.icon === 'success' && filaPagoAnular) {
                        filaPagoAnular.children[8].innerHTML = '<span class="badge bg-danger">Anulado</span>';
                        const boton = filaPagoAnular.querySelector('.btn-anular');
                        if (boton) {
                            boton.disabled = true;
                            boton.removeAttribute('data-bs-toggle');
                            boton.removeAttribute('data-bs-target');
                        }
                    }

                    const mostrarResultado = function() {
                        document.querySelectorAll('.modal-backdrop').forEach(function(backdrop) {
                            backdrop.remove();
                        });
                        document.body.classList.remove('modal-open');
                        alertaPago({
                            icon: res.icon || 'error',
                            title: res.title || 'Error',
                            text: res.text || 'No se pudo anular el pago.'
                        });

                        if (res && res.icon === 'success') {
                            window.dispatchEvent(new CustomEvent('pago-anulado', {
                                detail: {
                                    cliente: clientePagoAnular,
                                    fecha: fechaPagoAnular
                                }
                            }));
                        }
                    };

                    const modal = document.getElementById('modalAnularPago');
                    if (modal && window.bootstrap) {
                        modal.addEventListener('hidden.bs.modal', mostrarResultado, { once: true });
                        bootstrap.Modal.getOrCreateInstance(modal).hide();
                    } else {
                        mostrarResultado();
                    }
                    formAnularPago.reset();
                })
                .catch(function() {
                    alertaPago({
                        icon: 'error',
                        title: 'Error',
                        text: 'No se pudo conectar con el servidor.'
                    });
                });
        });
    }
});