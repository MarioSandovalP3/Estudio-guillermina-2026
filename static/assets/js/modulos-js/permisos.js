console.log("Abrio permisos    ");


document.addEventListener('DOMContentLoaded', function () {


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


    // =====================================================
    // REGISTRAR PERMISOS
    // =====================================================
    $('#formRegistrarpermisos').on('submit', function (e) {
        e.preventDefault();


        $.post('/admin?ruta=permisos', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    // =========================
                    // LIMPIAR FORMULARIO
                    // =========================
                    $('#formRegistrarpermisos')[0].reset();

                    // desmarcar checkboxes
                    $('#formRegistrarpermisos input[type="checkbox"]').prop('checked', false);

                    // =========================
                    // CERRAR MODAL
                    // =========================
                    cerrarModal('#modalPermisos');

                    // =========================
                    // RECARGAR TABLA
                    // =========================
                    $('#table1').load(location.href + ' #table1>*', '');
                }
            });

        }, 'json');
    });


    $('#formEditarpermiso').on('submit', function (e) {
        e.preventDefault();

        // =========================
        // VALIDACIÓN PARSLEY
        // =========================
        if (!$(this).parsley().validate()) return;


        $.post('/admin?ruta=permisos', $(this).serialize(), function (res) {

            alerta(res).then(() => {

                if (res.icon === 'success') {

                    // =========================
                    // LIMPIAR FORM
                    // =========================
                    $('#formEditarpermiso')[0].reset();
                    $('#formEditarpermiso').parsley().reset();

                    // =========================
                    // CERRAR MODAL
                    // =========================
                    cerrarModal('#modalEditar');

                    // =========================
                    // RECARGAR TABLA
                    // =========================
                    $('#table1').load(location.href + ' #table1>*');
                }
            });

        }, 'json');
    });


    $('#formEliminapermiso').on('submit', function (e) {
        e.preventDefault();

        const formulario = $(this);
        const codPermiso = $('#cod_permiso_eliminar').val();

        $.post(
            '/admin?ruta=permisos',
            formulario.serialize(),
            function (res) {

                alerta(res).then(() => {

                    if (res.icon === 'success') {
                        $('tr[data-cod-permiso="' + codPermiso + '"]').fadeOut(300, function () {
                            $(this).remove();
                        });
                    }

                    cerrarModal('#modalEliminar');
                });

            },
            'json'
        );
    });

    const modalEditar = document.getElementById('modalEditar');

    modalEditar.addEventListener('show.bs.modal', function (event) {

        const button = event.relatedTarget;

        const cedula = button.getAttribute('data-cedula');
        const nombre = button.getAttribute('data-nombre');
        const rol = button.getAttribute('data-rol');
        const status = button.getAttribute('data-status') || "0";
        const permisos = button.getAttribute('data-permisos');

        document.getElementById('edit_cedula').value = cedula;
        document.getElementById('edit_nombr').value = nombre;
        document.getElementById('edit_rol').value = rol;
        document.getElementById('edit_rol_visual').value = rol;

        // ✅ ESTADO CORRECTO
        document.getElementById('edit_status').value = status;

        document.querySelectorAll('.permiso-check').forEach(c => c.checked = false);

        const permisosArray = permisos
            ? permisos.split('|').map(p => p.trim())
            : [];

        document.querySelectorAll('.permiso-check').forEach(check => {
            if (permisosArray.includes(check.value)) {
                check.checked = true;
            }
        });

    });


    const modalEliminar = document.getElementById('modalEliminar');

    if (modalEliminar) {

        modalEliminar.addEventListener('show.bs.modal', function (event) {

            const button = event.relatedTarget;

            const cedula = button.getAttribute('data-cedula');
            const nombre = button.getAttribute('data-nombre');
            const rol = button.getAttribute('data-rol');
            const cod_permiso = button.getAttribute('data-cod_permiso');

            console.log('COD PERMISO DEL BOTON:', cod_permiso);

            document.getElementById('cedulaEliminar').textContent = cedula;
            document.getElementById('nombreEliminar').textContent = nombre;
            document.getElementById('rolEliminar').textContent = rol;

            document.getElementById('cod_permiso_eliminar').value = cod_permiso;

            console.log('COD PERMISO DEL INPUT:', document.getElementById('cod_permiso_eliminar').value);
        });
    }


    $('#checkAllRegistrar').on('change', function () {
        let marcado = this.checked;
        $('#modalPermisos input[name="permisos"]').prop('checked', marcado);
        verificarPermisosRegistrar();
    });

    $('#formRegistrarpermisos').on('change', '[name="cod_rol"], [name="permisos"]', function () {
        verificarPermisosRegistrar();
    });

    function verificarPermisosRegistrar() {
        let formulario = $('#formRegistrarpermisos');
        let cod_rol = formulario.find('[name="cod_rol"]').val();

        if (!cod_rol) return;

        let permisos = formulario.find('[name="permisos"]:checked')
            .map(function () {
                return this.value;
            })
            .get();

        $.ajax({
            url: '/admin?ruta=permisos',
            type: 'POST',
            traditional: true,
            data: {
                buscar: 1,
                cod_rol: cod_rol,
                permisos: permisos
            },
            dataType: 'json',
            success: function (response) {
                if (response.existe === true) {
                    Swal.fire({
                        title: 'Advertencia',
                        text: 'Ese rol ya está registrado con los mismos permisos.',
                        icon: 'warning'
                    });

                    formulario.find('[name="permisos"]').prop('checked', false);
                    $('#checkAllRegistrar').prop('checked', false);
                }
            }
        });
    }

    $(document).ready(function () {

        // Seleccionar todos
        $('#checkAllEditar').on('change', function () {

            $('.permiso-check').prop('checked', this.checked);

        });

        // Actualizar "Seleccionar todos" al marcar/desmarcar permisos
        $('.permiso-check').on('change', function () {

            $('#checkAllEditar').prop(
                'checked',
                $('.permiso-check:checked').length === $('.permiso-check').length
            );

        });

    });
});