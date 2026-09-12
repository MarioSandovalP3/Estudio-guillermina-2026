console.log('Abrio moneda.js');

const regexSoloLetras = /^[a-zA-ZÁÉÍÓÚáéíóúñÑ\s]+$/;
const regexNoPermitidos = /[^a-zA-ZÁÉÍÓÚáéíóúñÑ\s]/g;

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

$(document).ready(function () {
    $('#formRegistrarMoneda').on('submit', function (e) {
        e.preventDefault();

        const valor = $('#nombre_moneda').val();
        if (!regexSoloLetras.test(valor)) {
            $('#nombre_moneda').val(valor.replace(regexNoPermitidos, '')).focus();
            return;
        }

        $.post('/admin?ruta=moneda', $(this).serialize(), function (res) {
            alerta(res).then(() => {
                if (res.icon === 'success') {
                    $('#formRegistrarMoneda')[0].reset();
                    $('#formRegistrarMoneda').parsley().reset();
                    cerrarModal('#primary');
                    $('#table1').load(location.href + ' #table1>*', '');
                }
            });
        }, 'json');
    });

    $('#formEdimoneda').on('submit', function (e) {
        e.preventDefault();

        const valor = $('#edit_nombre_moneda').val();
        if (!regexSoloLetras.test(valor)) {
            $('#edit_nombre_moneda').val(valor.replace(regexNoPermitidos, '')).focus();
            return;
        }

        $.post('/admin?ruta=moneda', $(this).serialize(), function (res) {
            alerta(res).then(() => {
                if (res.icon === 'success') {
                    $('#formEdimoneda')[0].reset();
                    $('#editModal .is-invalid, #editModal .is-valid').removeClass('is-invalid is-valid');
                    cerrarModal('#editModal');
                    $('#table1').load(location.href + ' #table1>*', '');
                }
            });
        }, 'json');
    });

    $('#elimodal').on('submit', function (e) {
        e.preventDefault();

        $.post('/admin?ruta=moneda', $(this).serialize(), function (res) {
            alerta(res).then(() => {
                if (res.icon === 'success' || res.icon === 'warning') {
                    $('#elimodal')[0].reset();
                    cerrarModal('#deleteModal');
                    $('#table1').load(location.href + ' #table1>*', '');
                }
            });
        }, 'json');
    });

    $('#nombre_moneda, #edit_nombre_moneda').on('input', function () {
        const originalValue = $(this).val();
        const filteredValue = originalValue.replace(regexNoPermitidos, '');
        // maxlength
        const maxAttr = this.getAttribute && this.getAttribute('maxlength');
        const maxLen = maxAttr ? parseInt(maxAttr, 10) : 0;
        if (maxLen > 0 && this.value.length >= maxLen) {
            if ($(this).next('.invalid-feedback').length === 0) {
                $(this).after('<div class="invalid-feedback"></div>');
            }
            $(this).next('.invalid-feedback').text('limite de caracteres alcanzado').show();
            $(this).addClass('is-invalid').removeClass('is-valid');
            return;
        }

        if (originalValue !== filteredValue) {
            $(this).val(filteredValue);
            $(this).next('.invalid-feedback').text('En este campo solo se permiten letras.').show();
            $(this).addClass('is-invalid').removeClass('is-valid');
        } else {
            $(this).next('.invalid-feedback').hide();
            $(this).removeClass('is-invalid');
        }
    });

    $('#nombre_moneda').blur(function () {
        let buscar = $(this).val();
        if (buscar === '') return;

        $.post('/admin?ruta=moneda', { buscar: buscar }, function (response) {
            if (response.existe === true) {
                Swal.fire({
                    title: 'Advertencia',
                    text: 'Esta moneda ya está registrada.',
                    icon: 'warning',
                    timer: 3000,
                    timerProgressBar: true,
                    showConfirmButton: false,
                    backdrop: false
                });
                $('#nombre_moneda').val('').focus();
            }
        }, 'json');
    });
});

const modalEditarMoneda = document.getElementById('editModal');

if (modalEditarMoneda) {
    modalEditarMoneda.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const cod_moneda = button.getAttribute('data-cod_moneda');
        const nombre_moneda = button.getAttribute('data-nombre_moneda');
        const status = button.getAttribute('data-status');
        const formEditar = modalEditarMoneda.querySelector('form');

        if (formEditar) {
            formEditar.querySelector('#edit_cod_moneda').value = cod_moneda;
            formEditar.querySelector('#edit_nombre_moneda').value = nombre_moneda;
            formEditar.querySelector('#edit_estado').value = status;
        }
    });
}

const modalEliminarMoneda = document.getElementById('deleteModal');

if (modalEliminarMoneda) {
        modalEliminarMoneda.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const cod_moneda = button.getAttribute('data-cod_moneda');
            const nombre_moneda = button.getAttribute('data-nombre_moneda');
            const formEliminar = document.getElementById('elimodal');

            if (formEliminar) {
                formEliminar.querySelector('#MonedaCod').value = cod_moneda;
            }

            modalEliminarMoneda.querySelector('#nombreEliminar').textContent = nombre_moneda;
        });
    }
