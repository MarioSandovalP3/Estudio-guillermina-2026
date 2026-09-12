console.log('Abrio inicios de resrvas  .js');
document.addEventListener('DOMContentLoaded', function () {

  function actualizarResumenServicios() {
    const tablaBody = document.getElementById('tabla-servicios');
    tablaBody.innerHTML = '';

    let total = 0;

    // 🔹 SERVICIOS
    document.querySelectorAll('input[name="servicio[]"]').forEach(function (checkbox) {
      if (checkbox.checked) {
        const label = document.querySelector('label[for="' + checkbox.id + '"]');
        if (!label) return;

        const text = label.innerText.trim();
        const match = text.match(/^(.*?)\s*-\s*\$\s*([\d.,]+)/);

        let nombre = text;
        let precio = 0;

        if (match) {
          nombre = match[1].trim();
          precio = parseFloat(match[2].replace(',', '.'));
        }

        const tr = document.createElement('tr');

        const tdNombre = document.createElement('td');
        tdNombre.textContent = nombre;

        const tdPrecio = document.createElement('td');
        tdPrecio.textContent = `$ ${precio.toFixed(2)}`;

        tr.appendChild(tdNombre);
        tr.appendChild(tdPrecio);

        tablaBody.appendChild(tr);

        total += precio;
      }
    });

    // 🔹 PROMOCIÓN (DESCUENTO)
    let descuento = 0;

    const promo = document.querySelector('input[name="promocion"]:checked');

    if (promo) {
      const label = document.querySelector('label[for="' + promo.id + '"]');
      if (label) {
        const text = label.innerText.trim();
        const match = text.match(/(\d+)\s*%/);

        if (match) {
          descuento = parseFloat(match[1]);
        }
      }
    }

    // 🔹 APLICAR DESCUENTO
    let totalFinal = total;

    if (descuento > 0) {
      totalFinal = total - (total * descuento / 100);
    }

    // 🔹 MOSTRAR TOTAL
    document.getElementById('total-servicios').textContent = `$ ${totalFinal.toFixed(2)}`;
  }

  // eventos servicios
  document.querySelectorAll('input[name="servicio[]"]').forEach(function (checkbox) {
    checkbox.addEventListener('change', actualizarResumenServicios);
  });

  // eventos promociones
  document.querySelectorAll('input[name="promocion"]').forEach(function (checkbox) {
    checkbox.addEventListener('change', actualizarResumenServicios);
  });

  // Inicializar calendario y autocomplete
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'es',
    selectable: true,
    editable: true,
    themeSystem: 'bootstrap5',
    nowIndicator: true,

    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },

    buttonText: {
      today: 'Hoy',
      month: 'Mes',
      week: 'Semana',
      day: 'Día'
    },

    eventTimeFormat: {
      hour: '2-digit',
      minute: '2-digit',
      meridiem: false
    },

    events: [],

    // ✅ Solo fechas válidas (hoy o futuras)
    select: function (info) {
      const fechaSeleccionada = new Date(info.start);
      fechaSeleccionada.setHours(0, 0, 0, 0);

      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0);

      if (fechaSeleccionada < hoy) {
        Swal.fire({
          icon: 'error',
          title: 'Fecha inválida',
          text: '❌ No se puede seleccionar una fecha anterior a hoy.'
        });
        calendar.unselect();
        return;
      }

      document.getElementById('fecha_reserva').value = info.startStr;
      document.getElementById('hora_reserva').value = "";
      new bootstrap.Modal(document.getElementById('modalRegistrar')).show();
    },

    // ✅ Bloqueo 
    dateClick: function (info) {
      const fechaSeleccionada = new Date(info.date);
      fechaSeleccionada.setHours(0, 0, 0, 0);

      const hoy = new Date();
      hoy.setHours(0, 0, 0, 0);

      if (fechaSeleccionada < hoy) {
        Swal.fire({
          icon: 'error',
          title: 'Fecha inválida',
          text: '❌ No se puede seleccionar una fecha anterior a hoy.'
        });
        return;
      }

      document.getElementById('formRegistrar').reset();
      document.getElementById('fecha_reserva').value = info.dateStr;
      new bootstrap.Modal(document.getElementById('modalRegistrar')).show();
    },

    eventClick: function (info) {
      info.jsEvent.preventDefault();
      mostrarDetalles(info.event);
    }
  });

  calendar.render();

  function cargarReservas() {
    $.ajax({
      url: '/admin?ruta=inicio&cargar_reservas=1',
      type: 'GET',
      dataType: 'json',
      success: function (reservas) {

        console.log("RESERVAS:", reservas);


        calendar.getEventSources().forEach(s => s.remove());
        calendar.addEventSource(reservas);

      },
      error: function (xhr) {
        console.error("ERROR:", xhr.responseText);
      }
    });
  }
  cargarReservas();

  $('#formRegistrar').on('submit', function (e) {

    e.preventDefault();

    let formularioValido = true;

    // ==========================
    // BOTÓN GUARDAR
    // ==========================

    let botonGuardar = $(this).find('button[type="submit"]');

    // Evitar doble clic
    if (botonGuardar.prop('disabled')) {
      return false;
    }


    // ==========================
    // VALIDAR SERVICIOS
    // ==========================

    let serviciosSeleccionados =
      $('#formRegistrar input[name="servicio[]"]:checked').length;


    if (serviciosSeleccionados === 0) {

      $('#mensaje-servicio')
        .html('❌ Debe seleccionar al menos un servicio.')
        .fadeIn();

      formularioValido = false;

    } else {

      $('#mensaje-servicio').fadeOut();

    }


    // ==========================
    // VALIDAR PRODUCTOS
    // ==========================

    let productosSeleccionados =
      $('#formRegistrar input[name="producto[]"]:checked').length;


    if (productosSeleccionados === 0) {

      $('#mensaje-producto')
        .html('❌ Debe seleccionar al menos un producto.')
        .fadeIn();

      formularioValido = false;

    } else {

      $('#mensaje-producto').fadeOut();

    }


    // ==========================
    // SI HAY ERRORES NO CONTINUA
    // ==========================

    if (!formularioValido) {

      if (serviciosSeleccionados === 0) {

        $('.modal-scroll-body').animate({

          scrollTop:
            $('#mensaje-servicio').offset().top -
            $('.modal-scroll-body').offset().top +
            $('.modal-scroll-body').scrollTop()

        }, 500);

      } else {

        $('.modal-scroll-body').animate({

          scrollTop:
            $('#mensaje-producto').offset().top -
            $('.modal-scroll-body').offset().top +
            $('.modal-scroll-body').scrollTop()

        }, 500);

      }

      return false;

    }


    // ==========================
    // BLOQUEAR BOTÓN GUARDAR
    // ==========================

    botonGuardar.prop('disabled', true);

    botonGuardar.html(
      '<i class="bi bi-hourglass-split me-1"></i> Guardando...'
    );


    // ==========================
    // DATOS RESERVA
    // ==========================

    const reserva = {

      cedula: $('#cedula').val(),

      nombre_usuario: $('#nombre_usuario').text(),

      fecha_reserva: $('#fecha_reserva').val(),

      hora_reserva: $('#hora_reserva').val(),

      servicio: [],

      producto: [],

      promocion: [],

      especialista: $('#estilista').val()

    };


    // ==========================
    // SERVICIOS SELECCIONADOS
    // ==========================

    $('#formRegistrar input[name="servicio[]"]:checked')
      .each(function () {

        reserva.servicio.push($(this).val());

      });


    // ==========================
    // PRODUCTOS SELECCIONADOS
    // ==========================

    $('#formRegistrar input[name="producto[]"]:checked')
      .each(function () {

        reserva.producto.push($(this).val());

      });


    // ==========================
    // PROMOCIONES OPCIONALES
    // ==========================

    $('#formRegistrar input[name="promocion"]:checked')
      .each(function () {

        reserva.promocion.push($(this).val());

      });


    // ==========================
    // AJAX
    // ==========================

    $.ajax({

      type: 'POST',

      url: '/admin?ruta=inicio',

      data: $(this).serialize(),

      dataType: 'json',

      success: function (resp) {
        if (resp.success) {

          // Actualizar calendario sin recargar la página
          cargarReservas();

          // Actualizar stock de productos sin recargar
          actualizarStockProductos();

          // Limpiar completamente el formulario
          $('#formRegistrar')[0].reset();

          // Limpiar cantidades de productos
          $('input[name^="cantidad_producto"]').val('0');

          // Limpiar selecciones
          $('input[name="servicio[]"]').prop('checked', false);
          $('input[name="producto[]"]').prop('checked', false);
          $('input[name="promocion"]').prop('checked', false);

          // Limpiar cliente, fecha y hora
          $('#cedula').val('');
          $('#nombre_usuario').val('');
          $('#fecha_reserva').val('');
          $('#hora_reserva').val('');

          // Limpiar especialistas
          $('#estilista').val('');
          $('#manicurista').val('');

          // Limpiar mensajes
          $('.mensaje-stock').empty();
          $('#mensaje-nombre-apellido').hide();
          $('#mensaje-servicio').hide();
          $('#mensaje-especialista').hide();
          $('#mensaje-producto').hide();
          $('#error-hora').hide().text('');

          // Limpiar resumen y total
          $('#tabla-servicios').empty();
          $('#total-servicios').text('$ 0.00');

          // Restaurar botón Guardar
          $('#formRegistrar button[type="submit"]')
            .prop('disabled', false)
            .html('<i class="bi bi-save me-1"></i> Guardar');

          // Cerrar modal
          $('#modalRegistrar').modal('hide');

          Swal.fire({
            icon: 'success',
            title: 'Reserva registrada',
            text: 'La reserva se registró correctamente.',
            timer: 1500,
            showConfirmButton: false
          });

        } else {

          $('#formRegistrar button[type="submit"]')
            .prop('disabled', false)
            .html('<i class="bi bi-save me-1"></i> Guardar');

          Swal.fire('Error', resp.message, 'error');
        }
      }



    });

  });

  // ==========================
  // OCULTAR MENSAJE SERVICIO
  // ==========================

  $(document).on('change', 'input[name="servicio[]"]', function () {


    if ($('input[name="servicio[]"]:checked').length > 0) {

      $('#mensaje-servicio').fadeOut();

    }

  });



  $(document).on('change', 'input[name="producto[]"]', function () {

    if ($('input[name="producto[]"]:checked').length > 0) {


      $('#mensaje-producto').fadeOut();
    }
  });



  function mostrarDetalles(evento) {
    const p = evento.extendedProps;

    // Mostrar todos los servicios en línea si hay más de uno
    const serviciosTexto = p.tipos_servicio.length > 1 ? p.tipos_servicio.join(' | ') : p.tipos_servicio[0] || '—';

    // Crear fecha
    const fechaParts = p.fecha.split('-'); // ["YYYY","MM","DD"]
    const fechaLocal = new Date(fechaParts[0], fechaParts[1] - 1, fechaParts[2]); // Meses en JS van de 0 a 11

    document.getElementById('detallesReserva').innerHTML = `
            <p><b>Cédula:</b> ${p.cedula}</p>
            <p><b>Cliente:</b> ${p.cliente}</p>
            <p><b>Servicios:</b> ${serviciosTexto}</p>
            <p><b>Fecha:</b> ${fechaLocal.toLocaleDateString()}</p>
            <p><b>Hora:</b> ${p.hora}</p>
        `;

    new bootstrap.Modal(document.getElementById('modalDetalles')).show();
  }

  document.getElementById("fecha_reserva").min = new Date().toISOString().split("T")[0];

  //validar hora ocupada con fecha
  $('#hora_reserva').on('input change', function () {
    const hora = $(this).val().trim();
    const fecha = $('#fecha_reserva').val();
    const parsleyHora = $('#hora_reserva').parsley();

    if (!hora || !fecha) return;

    $.ajax({
      type: 'POST',
      url: '/admin?ruta=inicio',
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

  // ==================selecionar una promocion  ==================
  $('input[name="promocion"]').on('change', function () {
    const promocionesSeleccionadas = $('input[name="promocion"]:checked');

    $('#mensajePromocion').remove();

    if (promocionesSeleccionadas.length > 1) {
      $(this).prop('checked', false);

      $(this).closest('.border').after(`
            <div id="mensajePromocion" class="text-danger mt-1">
                ⚠️ Solo puede seleccionar una promoción.
            </div>
        `);

      setTimeout(function () {
        $('#mensajePromocion').fadeOut(200, function () {
          $(this).remove();
        });
      }, 3000);
    }
  });



  // ================== AUTOCOMPLETAR CLIENTE POR NOMBRE ==================
  let debounceTimeout;
  let alertaTimeout;

  const regexNombreApellido = /^[a-zA-ZÁÉÍÓÚáéíóúÜüÑñ\s]+$/;

  $('#nombre_usuario').on('input', function () {
    let valor = $(this).val();

    clearTimeout(debounceTimeout);
    clearTimeout(alertaTimeout);

    $('#listaClientes').remove();
    $('#cedula').val('');

    if (/[0-9]/.test(valor)) {
      valor = valor.replace(/[0-9]/g, '');
      $(this).val(valor);

      $('#nombre_usuario').removeClass('is-valid').addClass('is-invalid');

      mostrarMensajeNombre('❌ No se permiten números en el nombre y apellido.');

      return;
    }

    valor = valor.replace(/[^a-zA-ZÁÉÍÓÚáéíóúÜüÑñ\s]/g, '');
    valor = valor.replace(/\s{2,}/g, ' ');
    $(this).val(valor);

    const nombre = valor.trim();

    $('#nombre_usuario').removeClass('is-valid is-invalid');

    if (nombre.length === 0) {
      return;
    }

    if (!regexNombreApellido.test(nombre)) {
      $('#nombre_usuario').addClass('is-invalid');

      mostrarMensajeNombre('❌ Solo se permiten letras y espacios.');

      return;
    }

    if (nombre.length < 3) {
      return;
    }

    debounceTimeout = setTimeout(() => {
      $.ajax({
        type: 'POST',
        url: '/admin?ruta=inicio',
        data: {
          buscar_cliente: 1,
          nombre_usuario: nombre
        },
        dataType: 'json',
        success: function (res) {
          $('#listaClientes').remove();

          if (res.success === true && res.clientes.length > 0) {
            let lista = `
                        <div id="listaClientes"
                             class="list-group position-absolute"
                             style="z-index:1050; width:250px;">
                    `;

            res.clientes.forEach(function (cliente) {
              lista += `
                            <button type="button"
                                class="list-group-item list-group-item-action cliente-item"
                                data-cedula="${cliente.cedula}"
                                data-nombre="${cliente.nombre_usuario}"
                                data-apellido="${cliente.apellido_usuario}">
                                <strong>${cliente.nombre_usuario} ${cliente.apellido_usuario}</strong>
                                <br>
                                <small class="text-muted">
                                    C.I. ${cliente.cedula}
                                </small>
                            </button>
                        `;
            });

            lista += `</div>`;

            $('#nombre_usuario').parent().css('position', 'relative');
            $('#nombre_usuario').parent().append(lista);
            $('#nombre_usuario').removeClass('is-invalid').addClass('is-valid');
          } else {
            $('#nombre_usuario').removeClass('is-valid').addClass('is-invalid');

            alertaTimeout = setTimeout(() => {
              const nombreActual = $('#nombre_usuario').val().trim();

              if (nombreActual === nombre) {
                Swal.fire({
                  icon: 'warning',
                  title: 'Cliente no registrado',
                  text: 'No se encontró ningún cliente con ese nombre.'
                });
              }
            }, 3000);
          }
        },

      });
    }, 500);
  });

  $(document).on('click', '.cliente-item', function () {
    const cedula = $(this).data('cedula');
    const nombre = $(this).data('nombre');
    const apellido = $(this).data('apellido');

    $('#nombre_usuario').val(nombre + ' ' + apellido);
    $('#cedula').val(cedula);

    $('#nombre_usuario').removeClass('is-invalid').addClass('is-valid');

    $('#listaClientes').remove();
  });

  function mostrarMensajeNombre(mensaje) {
    let mensajeError = $('#mensajeNombre');

    if (mensajeError.length === 0) {
      $('#nombre_usuario').after(`
            <div id="mensajeNombre" class="text-danger mt-1">
                ${mensaje}
            </div>
        `);
    } else {
      mensajeError.text(mensaje);
    }

    clearTimeout(window.mensajeNombreTimeout);

    window.mensajeNombreTimeout = setTimeout(() => {
      $('#mensajeNombre').fadeOut(200, function () {
        $(this).remove();
      });
    }, 3000);
  }

  $(document).on('click', function (e) {
    if (!$(e.target).closest('#nombre_usuario, #listaClientes').length) {
      $('#listaClientes').remove();
    }
  });

  // ================== SELECCIONAR CLIENTE ==================
  $(document).on('click', '.cliente-item', function () {

    const cedula = $(this).data('cedula');
    const nombre = $(this).data('nombre');
    const apellido = $(this).data('apellido');

    $('#nombre_usuario').val(nombre + ' ' + apellido);
    $('#cedula').val(cedula);

    $('#nombre_usuario').removeClass('is-invalid').addClass('is-valid');

    $('#listaClientes').remove();
  });


  $(document).ready(function () {
    // Bloquear letras en tiempo real en cédula
    $('#cedula').on('input', function () {
      this.value = this.value.replace(/[^0-9]/g, '');
    });

    // Validar fecha futura (solo hoy o en adelante)
    window.Parsley.addValidator('fechafutura', {
      validateString: function (value) {
        const fecha = new Date(value);
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);
        return fecha >= hoy;
      },
      messages: {
        es: '❌ No se permite seleccionar una fecha anterior a hoy.'
      }
    });

    $('#formRegistrar').parsley();

    $('#cedula, #nombre_usuario,  #hora_reserva').each(function () {
      $(this).attr('data-parsley-required', 'true')
        .attr('data-parsley-error-message', '❌ Este campo es obligatorio.');
    });
  });

  // ✅ Limpieza 
  const modalEl = document.getElementById('modalRegistrar');
  modalEl.addEventListener('hidden.bs.modal', function () {
    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';
  });


  // Reseteo de formulario de registro para el modal de reservas
  $('#modalRegistrar').on('hidden.bs.modal', function () {
    const $form = $(this).find('form');

    // Reset del formulario HTML
    $form[0].reset();

    // Limpiar clases de validación de todos los inputs y selects
    $(this).find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
    $(this).find('.invalid-feedback').hide();

    // Reiniciar Parsley (importante)
    if ($form.parsley) {
      $form.parsley().reset();
    }

    // Limpiar tabla de servicios
    $('#tabla-servicios').empty();
    $('#total-servicios').text('0');

    // Resetear selects a su opción por defecto y limpiar validación
    $(this).find('select').each(function () {
      $(this).val('');
      $(this).prop('selectedIndex', 0);
      $(this).removeClass('is-invalid');
      $(this).removeClass('is-valid');
      $(this).trigger('change');
    });
  });

  window.openRegistrarClienteModal = function () {
    const modalId = 'modalRegistrarCliente';
    const modalElement = document.getElementById(modalId);

    // Quita la clase que centra verticalmente antes de mostrar
    const dialog = modalElement.querySelector('.modal-dialog');
    if (dialog) {
      dialog.classList.remove('modal-dialog-centered');
      dialog.style.position = 'absolute';
      dialog.style.top = '90px';
      dialog.style.left = '60%';
      dialog.style.transform = 'translateX(-50%)';
      dialog.style.zIndex = '5000';
    }

    // Inicializa el modal hijo sin backdrop propio
    const modal = new bootstrap.Modal(modalElement, {
      backdrop: false,
      keyboard: false
    });

    // Mostrar el modal
    modal.show();
  };

  // ==========================
  // VALIDAR HORA
  // ==========================
  const horaInput = document.getElementById('hora_reserva');
  const errorHora = document.getElementById('error-hora');
  const limiteMin = 6 * 60;
  const limiteMax = 20 * 60;

  function convertirAHoras24(hora12) {
    const regex = /^(0?[1-9]|1[0-2]):([0-5][0-9]) (AM|PM)$/i;
    const match = hora12.match(regex);

    if (!match) return null;

    let hh = parseInt(match[1], 10);
    let mm = parseInt(match[2], 10);
    const ampm = match[3].toUpperCase();

    if (ampm === "PM" && hh !== 12) hh += 12;
    if (ampm === "AM" && hh === 12) hh = 0;

    return hh * 60 + mm;
  }

  horaInput.addEventListener('input', function () {

    let valor = horaInput.value;

    // Solo permite números, :, espacios y AM/PM
    valor = valor.replace(/[^0-9: aApPmM]/g, '');
    valor = valor.substring(0, 8);

    horaInput.value = valor;

    // Campo vacío
    if (valor.trim() === '') {
      errorHora.style.display = 'none';
      errorHora.textContent = '';
      return;
    }

    // Verificar formato completo
    const minutos = convertirAHoras24(valor.trim());

    // Todavía está incompleto o tiene formato incorrecto
    if (minutos === null) {
      errorHora.textContent = '⛔ Formato inválido. Use 08:00 AM o 07:00 PM';
      errorHora.style.display = 'block';
      return;
    }

    // Hora fuera del horario permitido
    if (minutos < limiteMin || minutos > limiteMax) {
      errorHora.textContent = '⛔ La hora debe estar entre 06:00 AM y 08:00 PM';
      errorHora.style.display = 'block';
      return;
    }

    // ✅ HORA CORRECTA: OCULTAR MENSAJE
    errorHora.textContent = '';
    errorHora.style.display = 'none';
  });



  $('#modalRegistrar').on('hidden.bs.modal', function () {

    const form = $('#formRegistrar')[0];

    form.reset();

    if ($('#formRegistrar').data('Parsley')) {
      $('#formRegistrar').parsley().reset();
    }

    $('#formRegistrar').find('.parsley-errors-list').remove();
    $('#formRegistrar').find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');

    $('#cedula').val('');
    $('#nombre_usuario').html('');

    $('#fecha_reserva').val('');
    $('#hora_reserva').val('');
    $('#error-hora').hide().text('');

    $('#formRegistrar input[name="servicio[]"]').prop('checked', false);
    $('#mensaje-servicio').hide().text('❌ Debe seleccionar al menos un servicio.');

    $('#tabla-servicios').html('');
    $('#total-servicios').text('0');

    $('#formRegistrar input[name="producto[]"]').prop('checked', false);
    $('#formRegistrar input[name^="cantidad_producto"]').val('0');
    $('.mensaje-stock').html('');
    $('#mensaje-producto').hide().text('❌ Debe seleccionar al menos un producto.');

    $('#formRegistrar input[name="promocion"]').prop('checked', false);

    $('#estilista').val('');
    $('#manicurista').val('');

    $('.form-control').removeClass('is-invalid is-valid');


  });


  $(document).ready(function () {
    let mostrar = false, temporizador;

    $("#modalRegistrar").on("shown.bs.modal", function () {
      mostrar = false;
      clearTimeout(temporizador);
      $("#mensaje-nombre-apellido,#error-hora,#mensaje-servicio,#mensaje-especialista,#mensaje-producto").hide();
      temporizador = setTimeout(function () {
        mostrar = true;
        validar();
      }, 3000);
    });

    function validar() {
      if (!mostrar) return;

      if ($("#nombre_usuario").val().trim() === "") {
        $("#mensaje-nombre-apellido").html('<i class="bi bi-exclamation-circle-fill me-1"></i>Campo obligatorio. Ingrese el nombre y apellido del cliente.').fadeIn(200);
      } else {
        $("#mensaje-nombre-apellido").fadeOut(200);
      }

      if ($("#hora_reserva").val().trim() === "") {
        $("#error-hora").html('<i class="bi bi-exclamation-circle-fill me-1"></i>Campo obligatorio, ingresa hora.').fadeIn(200);
      } else {
        $("#error-hora").fadeOut(200);
      }

      if ($('input[name="servicio[]"]:checked').length === 0) {
        $("#mensaje-servicio").html('<i class="bi bi-exclamation-circle-fill me-1"></i>Debe seleccionar al menos un servicio.').fadeIn(200);
      } else {
        $("#mensaje-servicio").fadeOut(200);
      }

      let estilista = $("#estilista").val() || "";
      let manicurista = $("#manicurista").val() || "";

      if (estilista === "" && manicurista === "") {
        $("#mensaje-especialista").html('<i class="bi bi-exclamation-circle-fill me-1"></i>Debe seleccionar al menos un especialista.').fadeIn(200);
      } else {
        $("#mensaje-especialista").fadeOut(200);
      }

      if ($('input[name="producto[]"]:checked').length === 0) {
        $("#mensaje-producto").html('<i class="bi bi-exclamation-circle-fill me-1"></i>Debe seleccionar al menos un producto.').fadeIn(200);
      } else {
        $("#mensaje-producto").fadeOut(200);
      }
    }

    $("#nombre_usuario").on("input", function () {
      if ($(this).val().trim() !== "") {
        $("#mensaje-nombre-apellido").fadeOut(200);
      } else if (mostrar) {
        $("#mensaje-nombre-apellido").fadeIn(200);
      }
    });



    $('input[name="servicio[]"]').on("change", function () {
      if ($('input[name="servicio[]"]:checked').length > 0) {
        $("#mensaje-servicio").fadeOut(200);
      } else if (mostrar) {
        $("#mensaje-servicio").fadeIn(200);
      }
    });

    $("#estilista,#manicurista").on("change", function () {
      let estilista = $("#estilista").val() || "";
      let manicurista = $("#manicurista").val() || "";

      if (estilista !== "" || manicurista !== "") {
        $("#mensaje-especialista").fadeOut(200);
      } else if (mostrar) {
        $("#mensaje-especialista").html('<i class="bi bi-exclamation-circle-fill me-1"></i>Debe seleccionar al menos un especialista.').fadeIn(200);
      }
    });

    $('input[name="producto[]"]').on("change", function () {
      if ($('input[name="producto[]"]:checked').length > 0) {
        $("#mensaje-producto").fadeOut(200);
      } else if (mostrar) {
        $("#mensaje-producto").fadeIn(200);
      }
    });

    $("#modalRegistrar").on("hidden.bs.modal", function () {
      clearTimeout(temporizador);
      mostrar = false;
      $("#mensaje-nombre-apellido,#error-hora,#mensaje-servicio,#mensaje-especialista,#mensaje-producto").hide();
    });
  });




function actualizarStockProductos() {
  $.getJSON('/admin?ruta=inicio&actualizar_stock=1', function(productos) {
    productos.forEach(p => {
      const label = document.querySelector(`label[for="producto_${p.cod_producto}"]`);
      if (label) label.innerHTML = label.innerHTML.replace(/Stock:\s*\d+/i, `Stock: ${p.stock}`);
    });
  });
}













});










