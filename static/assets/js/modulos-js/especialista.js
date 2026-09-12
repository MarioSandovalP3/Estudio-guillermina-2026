console.log('Abrió .js');
document.addEventListener('DOMContentLoaded', function () {

    const regexEspecialista = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$/;
    const regexCedula = /^[0-9]+$/;

    function mostrarError(input, mensaje) {
        $(input).addClass('is-invalid').removeClass('is-valid');
        if ($(input).next('.invalid-feedback').length === 0) {
            $(input).after('<div class="invalid-feedback">' + mensaje + '</div>');
        } else {
            $(input).next('.invalid-feedback').text(mensaje).show();
        }
    }

    function validarCaracteres(input, regex, mensaje) {
        const original = input.value;
        let nuevoValor = '';
        for (let i = 0; i < original.length; i++) {
            if (regex.test(original[i])) nuevoValor += original[i];
        }
        if (nuevoValor !== original) {
            input.value = nuevoValor;
            mostrarError(input, mensaje);
        } else {
            $(input).removeClass('is-invalid').addClass('is-valid');
            $(input).next('.invalid-feedback').hide();
        }
    }

    // Bloqueo en tiempo real
    $('#especialista, #edit_especialista').on('input', function () {
        validarCaracteres(this, /^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]$/, 'en este campo Solo se permiten letras.');
    });
    $('#searchCedula, #cedula_reg').on('input', function () {
        validarCaracteres(this, /^[0-9]$/, 'En este campo Solo se permiten números.');
    });

    // ==========================
    // 🟢 REGISTRAR
    // ==========================
    $('#primary').on('show.bs.modal', function () {
        $('#especialidad')[0].reset();
        $('#especialidad').find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        $('#especialidad').find('.invalid-feedback').hide();
        $('#especialidad').parsley().reset();
    });




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


    $('#especialidad').on('submit', function (e) {

        e.preventDefault();

        if (!$(this).parsley().validate()) return;

        $.post('/admin?ruta=especialidad', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    // Limpiar formulario
                    $('#especialidad')[0].reset();

                    // Limpiar validaciones de Parsley
                    $('#especialidad').parsley().reset();

                    // Cerrar modal
                    cerrarModal('#primary');

                    // Actualizar tabla en tiempo real
                    $('#table1').load(
                        location.href + ' #table1>*',
                        ''
                    );
                }

            });

        }, 'json');

    });

    // ==========================
    // 🟡 EDITAR
    // ==========================
    $('#formEditEspecialidad').on('submit', function (e) {

        e.preventDefault();

        $.post(
            '/admin?ruta=especialidad',
            $(this).serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (res.icon === 'success') {

                        $('#formEditEspecialidad')[0].reset();

                        cerrarModal('#editModal');

                        $('#table1').load(location.href + ' #table1>*');

                    }

                });

            },
            'json'
        );

    });


    $('#elimodal').on('submit', function (e) {
        e.preventDefault();
        $.post(
            '/admin?ruta=especialidad', $(this).serialize(), function (res) {
                alerta(res).then(() => {
                    cerrarModal('#deleteModal');
                    if (res.icon === 'success' || res.icon === 'warning') {
                        $('#table1').load(location.href + ' #table1>*', '');
                    }
                });

            }, 'json');
    });


    // ============================
    // 🔡 BLOQUEO DE CARACTERES Y PARSLEY
    // ============================
    function validateInput(input) {
        const original = input.value;
        input.value = input.value.replace(regexNoPermitidos, '');
        if (input.value !== original) {
            $(input).next('.invalid-feedback').text('En este campo solo se permiten letras.').show();
            $(input).addClass('is-invalid').removeClass('is-valid');
        } else {
            $(input).parsley().validate();
        }
    }

    $('#especialidad input, #formEditEspecialidad input').on('input', function () {
        validateInput(this);
    });

    window.Parsley.on('field:error', function () {
        this.$element.addClass('is-invalid').removeClass('is-valid');
        this.$element.next('.invalid-feedback').show();
    });

    window.Parsley.on('field:success', function () {
        this.$element.removeClass('is-invalid').addClass('is-valid');
        this.$element.next('.invalid-feedback').hide();
    });

    // ============================
    //  MODALES: EDITAR Y ELIMINAR
    // ============================
    $('#editModal').on('show.bs.modal', function (event) {

        var button = $(event.relatedTarget);

        // Cédula actual del registro
        $('#edit_cedula_actual').val(
            button.data('cedula')
        );

        // Seleccionar especialidad registrada
        $('#edit_especialista').val(
            button.data('especialista')
        );

        // Seleccionar personal registrado
        $('#edit_cedula').val(
            button.data('cedula')
        );

        // Seleccionar estado
        $('#edit_estado').val(
            button.data('status')
        );

    });


    const modalEliminar = document.getElementById('deleteModal');

    if (modalEliminar) {
        modalEliminar.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cedula = button.getAttribute('data-cedula');
            const nombre = button.getAttribute('data-nombre');

            const formEliminar = document.getElementById('elimodal');

            if (formEliminar) {
                formEliminar.querySelector('#especialidadCodigo').value = cedula;
            }

            modalEliminar.querySelector('#nombreEliminar').textContent = nombre;

        });
    }

    // ============================
    // 🔁 BOTONES CERRAR
    // ============================
    $('#primary .btn-light-secondary, #editModal .btn-light-secondary, #deleteModal .btn-light-secondary').on('click', function () {
        $(this).closest('form')[0].reset();
        $(this).closest('form').find('.is-invalid, .is-valid').removeClass('is-invalid is-valid');
        $(this).closest('form').find('.invalid-feedback').hide();
        $(this).closest('form').parsley().reset();
    });

    // ============================
    // 🔍 FILTRO DE CÉDULAS
    // ============================
    const inputSearch = document.getElementById("searchCedula");
    const selectCedula = document.getElementById("cedula_reg");

    inputSearch.addEventListener('input', function () {
        const filter = inputSearch.value.toLowerCase();
        let hasMatch = false;

        for (let option of selectCedula.options) {
            const txt = option.text.toLowerCase();
            if (txt.includes(filter)) {
                option.style.display = '';
                hasMatch = true;
            } else {
                option.style.display = 'none';
            }
        }
        selectCedula.style.display = hasMatch ? 'block' : 'none';
    });

    selectCedula.addEventListener('change', function () {
        inputSearch.value = this.options[this.selectedIndex].text;
        this.style.display = 'none';
    });

});


$('#especialista, #cedula_reg').change(function () {

    let especialidad = $('#especialista').val();
    let cedula = $('#cedula_reg').val();

    if (!especialidad || !cedula) return;

    $.post('/admin?ruta=especialidad',
        {
            buscar: 1,
            especialista: especialidad,
            cedula: cedula
        },
        function (response) {

            if (response.existe === true) {

                Swal.fire({
                    title: 'Advertencia',
                    text: 'Esta especialidad ya está asignada a este personal.',
                    icon: 'warning'
                });

                $('#especialista').val('');
                $('#cedula_reg').val('');
                $('#especialista').focus();
            }

        },
        'json'
    );

});