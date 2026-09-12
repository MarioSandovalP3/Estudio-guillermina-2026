console.log("Compras JS cargado");

let carrito = [];

$(document).ready(function () {

    // =====================================================
    // FORMATEAR MONEDA
    // =====================================================
    function formatearMoneda(valor) {
        return '$' + parseFloat(valor || 0).toFixed(2);
    }


    function formatearFechaCompra(valor) {

        if (!valor) {
            return 'Sin fecha';
        }

        const texto = String(valor);
        const fechaNumerica = texto.match(/(\d{4})-(\d{2})-(\d{2})/);

        if (fechaNumerica) {
            return `${fechaNumerica[3]}/${fechaNumerica[2]}/${fechaNumerica[1]}`;
        }

        const fecha = new Date(valor);

        if (Number.isNaN(fecha.getTime())) {
            return texto.replace(/\s+GMT.*$/, '');
        }

        return `${String(fecha.getUTCDate()).padStart(2, '0')}/${String(fecha.getUTCMonth() + 1).padStart(2, '0')}/${fecha.getUTCFullYear()}`;
    }


    // =====================================================
    // FECHA ACTUAL
    // =====================================================
    function fechaHoy() {

        const hoy = new Date();

        const yyyy = hoy.getFullYear();
        const mm = String(hoy.getMonth() + 1).padStart(2, '0');
        const dd = String(hoy.getDate()).padStart(2, '0');

        return `${yyyy}-${mm}-${dd}`;
    }


    // =====================================================
    // MOSTRAR MENSAJE ROJO
    // =====================================================
    function mostrarError(campo, mensaje) {

        const input = $(campo);

        input.addClass('is-invalid');

        let error = input.next('.mensaje-error');

        if (error.length === 0) {

            input.after(
                '<div class="mensaje-error"></div>'
            );

            error = input.next('.mensaje-error');
        }

        error
            .text(mensaje)
            .css({
                'color': 'red',
                'font-size': '13px',
                'margin-top': '4px'
            })
            .show();
    }


    // =====================================================
    // QUITAR MENSAJE
    // =====================================================
    function quitarError(campo) {

        const input = $(campo);

        input.removeClass('is-invalid');

        input.next('.mensaje-error').hide();
    }


    // =====================================================
    // VALIDAR FECHA
    // =====================================================
    function validarFecha(campo) {

        const fecha = $(campo).val();

        if (fecha === '') {
            mostrarError(
                campo,
                'La fecha de compra es obligatoria.'
            );
            return false;
        }

        if (fecha < fechaHoy()) {

            mostrarError(
                campo,
                'No se permite seleccionar una fecha anterior a la actual.'
            );

            return false;
        }

        quitarError(campo);

        return true;
    }


    // =====================================================
    // ACTUALIZAR PRECIO DEL PRODUCTO
    // =====================================================
    function actualizarPrecioProducto(
        selectSelector,
        precioSelector,
        infoSelector
    ) {

        const option =
            $(selectSelector).find('option:selected');

        const precio =
            parseFloat(option.data('precio')) || 0;

        const marca =
            option.data('marca') || '—';

        const categoria =
            option.data('categoria') || '—';

        const tipo =
            option.data('tipo') || '—';

        $(precioSelector).val(
            precio.toFixed(2)
        );

        if (infoSelector) {

            $(infoSelector).html(`
                <span><b>Marca:</b> ${marca}</span> ·
                <span><b>Categoría:</b> ${categoria}</span> ·
                <span><b>Tipo:</b> ${tipo}</span>
            `);
        }

        quitarError(precioSelector);
    }


    // =====================================================
    // AGREGAR PRODUCTO
    // =====================================================
    function agregarProductoDesdeFormulario(
        selectSelector,
        cantidadSelector,
        precioSelector,
        tableSelector,
        totalSelector,
        totalInputSelector
    ) {

        const select = $(selectSelector);

        const option =
            select.find('option:selected');

        const cod = select.val();

        const nombre = option.text();

        const marca =
            option.data('marca') || '—';

        const categoria =
            option.data('categoria') || '—';

        const tipo =
            option.data('tipo') || '—';

        const precio =
            parseFloat($(precioSelector).val()) ||
            parseFloat(option.data('precio')) ||
            0;

        const cantidad =
            parseFloat($(cantidadSelector).val()) || 0;


        // VALIDAR CANTIDAD
        if (!cantidad || cantidad <= 0) {

            mostrarError(
                cantidadSelector,
                'Ingrese una cantidad válida.'
            );

            return false;
        }


        if (cantidad > 999) {

            mostrarError(
                cantidadSelector,
                'La cantidad máxima es de 3 caracteres.'
            );

            return false;
        }


        // VALIDAR PRECIO
        if (precio <= 0) {

            mostrarError(
                precioSelector,
                'Ingrese un precio válido.'
            );

            return false;
        }


        quitarError(cantidadSelector);
        quitarError(precioSelector);


        const subtotal =
            precio * cantidad;


        carrito.push({

            cod_producto: cod,

            cantidad: cantidad,

            precio: precio,

            nombre: nombre,

            marca: marca,

            categoria: categoria,

            tipo: tipo
        });


        $(tableSelector + ' tbody').append(`

            <tr data-index="${carrito.length - 1}">

                <td>${nombre}</td>

                <td>${marca}</td>

                <td>${categoria}</td>

                <td>${tipo}</td>

                <td>${cantidad}</td>

                <td>${precio.toFixed(2)}</td>

                <td>${subtotal.toFixed(2)}</td>

                <td>

                    <button
                        type="button"
                        class="btn btn-danger btn-sm eliminar-item">
                        X
                    </button>

                </td>

            </tr>

        `);


        actualizarTotal(
            tableSelector,
            totalSelector,
            totalInputSelector
        );


        $(cantidadSelector).val('');

        $(precioSelector).val(
            precio.toFixed(2)
        );


        return true;
    }


    // =====================================================
    // ACTUALIZAR TOTAL
    // =====================================================
    function actualizarTotal(
        tableSelector,
        totalSelector,
        totalInputSelector
    ) {

        let total = 0;

        $(tableSelector + ' tbody tr').each(
            function () {

                const subtotal =
                    parseFloat(
                        $(this).find('td').eq(6).text()
                    ) || 0;

                total += subtotal;
            }
        );


        $(totalSelector).text(
            formatearMoneda(total)
        );

        $(totalInputSelector).val(
            total.toFixed(2)
        );
    }


    // =====================================================
    // RENDERIZAR CARRITO
    // =====================================================
    function renderizarCarrito(
        tableSelector,
        totalSelector,
        totalInputSelector,
        items
    ) {

        const tbody =
            $(tableSelector + ' tbody');

        tbody.html('');

        carrito = items || [];


        carrito.forEach(function (item, index) {

            const subtotal =
                (parseFloat(item.precio) || 0) *
                (parseFloat(item.cantidad) || 0);


            tbody.append(`

                <tr data-index="${index}">

                    <td>${item.nombre || ''}</td>

                    <td>${item.marca || '—'}</td>

                    <td>${item.categoria || '—'}</td>

                    <td>${item.tipo || '—'}</td>

                    <td>${item.cantidad}</td>

                    <td>
                        ${parseFloat(item.precio || 0).toFixed(2)}
                    </td>

                    <td>${subtotal.toFixed(2)}</td>

                    <td>

                        <button
                            type="button"
                            class="btn btn-danger btn-sm eliminar-item">
                            X
                        </button>

                    </td>

                </tr>

            `);
        });


        actualizarTotal(
            tableSelector,
            totalSelector,
            totalInputSelector
        );
    }


    // =====================================================
    // LIMPIAR MODAL REGISTRAR
    // =====================================================
    function limpiarModalRegistrar() {

        carrito = [];

        $('#detalleCompra tbody').html('');

        $('#totalCompra').text(
            formatearMoneda(0)
        );

        $('#total').val('0');

        $('#precio').val('');

        $('#cantidad').val('');

        $('#formRegistrarCompra')[0].reset();

        $('#fecha_compra').val(
            fechaHoy()
        );

        $('#fecha_compra').attr(
            'min',
            fechaHoy()
        );

        $('#precio, #cantidad, #fecha_compra')
            .removeClass('is-invalid');

        $('.mensaje-error').hide();

        actualizarPrecioProducto(
            '#producto',
            '#precio',
            '#productoInfo'
        );
    }


    // =====================================================
    // LIMPIAR MODAL EDITAR
    // =====================================================
    function limpiarModalEditar() {

        carrito = [];

        $('#detalleCompraEditar tbody').html('');

        $('#edit_totalCompra').text(
            formatearMoneda(0)
        );

        $('#edit_total').val('0');

        $('#edit_precio').val('');

        $('#edit_cantidad').val('');

        $('#formEditarCompra')[0].reset();

        $('#edit_fecha_compra').val(
            fechaHoy()
        );

        $('#edit_fecha_compra').attr(
            'min',
            fechaHoy()
        );

        $('#edit_precio, #edit_cantidad, #edit_fecha_compra')
            .removeClass('is-invalid');

        $('.mensaje-error').hide();

        actualizarPrecioProducto(
            '#edit_producto',
            '#edit_precio',
            '#edit_productoInfo'
        );
    }


    // =====================================================
    // REFRESCAR TABLA
    // =====================================================
    function refrescarTablaCompras() {

        $.get(
            '/admin?ruta=compra',
            function (html) {

                const wrapper =
                    $('<div></div>').html(html);

                const nuevaTabla =
                    wrapper.find('#table1').html();

                $('#table1').html(
                    nuevaTabla
                );


                if (
                    $.fn.DataTable.isDataTable(
                        '#table1'
                    )
                ) {

                    $('#table1')
                        .DataTable()
                        .destroy();
                }


                $('#table1').DataTable({

                    language: {

                        url:
                            '//cdn.datatables.net/plug-ins/1.13.7/i18n/es-ES.json'
                    }

                });

            }
        );
    }


    // =====================================================
    // CAMBIO PRODUCTO
    // =====================================================
    $('#producto').on(
        'change',
        function () {

            actualizarPrecioProducto(
                '#producto',
                '#precio',
                '#productoInfo'
            );
        }
    );


    $('#edit_producto').on(
        'change',
        function () {

            actualizarPrecioProducto(
                '#edit_producto',
                '#edit_precio',
                '#edit_productoInfo'
            );
        }
    );


    // =====================================================
    // FECHA MÍNIMA
    // =====================================================
    $('#fecha_compra').attr(
        'min',
        fechaHoy()
    );

    $('#edit_fecha_compra').attr(
        'min',
        fechaHoy()
    );


    $('#fecha_compra').val(
        fechaHoy()
    );

    $('#edit_fecha_compra').val(
        fechaHoy()
    );


    actualizarPrecioProducto(
        '#producto',
        '#precio',
        '#productoInfo'
    );

    actualizarPrecioProducto(
        '#edit_producto',
        '#edit_precio',
        '#edit_productoInfo'
    );


    // =====================================================
    // VALIDAR FECHA AL CAMBIAR
    // =====================================================
    $('#fecha_compra, #edit_fecha_compra')
        .on('change', function () {

            validarFecha(this);

            if ($(this).val() < fechaHoy()) {

                $(this).val(
                    fechaHoy()
                );
            }
        });


    // =====================================================
    // BLOQUEAR FECHAS ANTERIORES
    // =====================================================
    $('#fecha_compra, #edit_fecha_compra')
        .on('keydown', function () {

            const campo = $(this);

            setTimeout(function () {

                if (
                    campo.val() &&
                    campo.val() < fechaHoy()
                ) {

                    campo.val(
                        fechaHoy()
                    );

                    mostrarError(
                        campo,
                        'No se permiten fechas anteriores a la actual.'
                    );

                }

            }, 0);
        });


    // =====================================================
    // CANTIDAD - SOLO NÚMEROS
    // MÁXIMO 3 CARACTERES
    // =====================================================
    $(document).on(
        'input',
        '#cantidad, #edit_cantidad',
        function () {

            const campo = $(this);

            let valor = campo.val();


            // ELIMINAR TODO LO QUE NO SEA NÚMERO
            valor = valor.replace(
                /[^0-9]/g,
                ''
            );


            // MÁXIMO 3 CARACTERES
            if (valor.length > 3) {

                valor =
                    valor.substring(0, 3);

                mostrarError(
                    campo,
                    'Máximo 3 caracteres.'
                );

            } else {

                quitarError(campo);
            }


            campo.val(valor);
        }
    );


    // =====================================================
    // BLOQUEAR TECLAS CANTIDAD
    // =====================================================
    $(document).on(
        'keydown',
        '#cantidad, #edit_cantidad',
        function (e) {

            const teclasPermitidas = [

                'Backspace',
                'Delete',

                'ArrowLeft',
                'ArrowRight',

                'ArrowUp',
                'ArrowDown',

                'Tab',
                'Home',
                'End'
            ];


            if (
                teclasPermitidas.includes(
                    e.key
                )
            ) {
                return;
            }


            if (
                e.ctrlKey ||
                e.metaKey
            ) {
                return;
            }


            if (
                e.key.length === 1 &&
                !/[0-9]/.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(
                    this,
                    'Solo se permiten números.'
                );

                return;
            }


            if (
                $(this).val().length >= 3 &&
                e.key.length === 1
            ) {

                e.preventDefault();

                mostrarError(
                    this,
                    'Máximo 3 caracteres.'
                );
            }

        }
    );


    // =====================================================
    // PEGAR CANTIDAD
    // =====================================================
    $(document).on(
        'paste',
        '#cantidad, #edit_cantidad',
        function (e) {

            const campo = $(this);

            const texto =
                (
                    e.originalEvent.clipboardData ||
                    window.clipboardData
                ).getData('text');


            if (!/^[0-9]+$/.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se permiten números.'
                );

                return;
            }


            if (
                campo.val().length +
                texto.length > 3
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 3 caracteres.'
                );
            }

        }
    );


    // =====================================================
    // PRECIO
    // MÁXIMO 10 ENTEROS + 2 DECIMALES
    // =====================================================
    $(document).on(
        'input',
        '#precio, #edit_precio',
        function () {

            const campo = $(this);

            let valor = campo.val();


            // SOLO NÚMEROS Y PUNTO
            valor = valor.replace(
                /[^0-9.]/g,
                ''
            );


            // SOLO UN PUNTO
            const partes =
                valor.split('.');


            if (partes.length > 2) {

                valor =
                    partes[0] +
                    '.' +
                    partes.slice(1).join('');
            }


            let enteros = partes[0] || '';

            let decimales =
                partes[1] || '';


            // MÁXIMO 10 ENTEROS
            if (enteros.length > 10) {

                enteros =
                    enteros.substring(0, 10);

                mostrarError(
                    campo,
                    'El precio permite máximo 10 números enteros.'
                );
            }


            // MÁXIMO 2 DECIMALES
            if (decimales.length > 2) {

                decimales =
                    decimales.substring(0, 2);

                mostrarError(
                    campo,
                    'El precio permite máximo 2 decimales.'
                );
            }


            valor = enteros;


            if (
                partes.length > 1 ||
                decimales.length > 0
            ) {

                valor +=
                    '.' + decimales;
            }


            campo.val(valor);


            if (
                enteros.length <= 10 &&
                decimales.length <= 2
            ) {

                quitarError(campo);
            }

        }
    );


    // =====================================================
    // BLOQUEAR TECLAS PRECIO
    // =====================================================
    $(document).on(
        'keydown',
        '#precio, #edit_precio',
        function (e) {

            const campo = $(this);

            const valor =
                campo.val();


            const teclasPermitidas = [

                'Backspace',
                'Delete',

                'ArrowLeft',
                'ArrowRight',

                'ArrowUp',
                'ArrowDown',

                'Tab',
                'Home',
                'End'
            ];


            if (
                teclasPermitidas.includes(
                    e.key
                )
            ) {
                return;
            }


            if (
                e.ctrlKey ||
                e.metaKey
            ) {
                return;
            }


            // SOLO NÚMEROS Y PUNTO
            if (
                e.key.length === 1 &&
                !/[0-9.]/.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Solo se permiten números y un punto decimal.'
                );

                return;
            }


            // NO PERMITIR SEGUNDO PUNTO
            if (
                e.key === '.' &&
                valor.includes('.')
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'El precio solo puede tener un punto decimal.'
                );

                return;
            }


            const partes =
                valor.split('.');


            // MÁXIMO 10 ENTEROS
            if (
                !valor.includes('.') &&
                partes[0].length >= 10 &&
                /[0-9]/.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 10 números enteros.'
                );

                return;
            }


            // MÁXIMO 2 DECIMALES
            if (
                valor.includes('.') &&
                valor.split('.')[1].length >= 2 &&
                /[0-9]/.test(e.key)
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 2 decimales.'
                );

            }

        }
    );


    // =====================================================
    // PEGAR PRECIO
    // =====================================================
    $(document).on(
        'paste',
        '#precio, #edit_precio',
        function (e) {

            const campo = $(this);

            const texto =
                (
                    e.originalEvent.clipboardData ||
                    window.clipboardData
                ).getData('text');


            if (!/^[0-9]+(\.[0-9]{0,2})?$/.test(texto)) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Ingrese un precio válido.'
                );

                return;
            }


            const partes =
                texto.split('.');


            if (partes[0].length > 10) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 10 números enteros.'
                );

                return;
            }


            if (
                partes[1] &&
                partes[1].length > 2
            ) {

                e.preventDefault();

                mostrarError(
                    campo,
                    'Máximo 2 decimales.'
                );

                return;
            }

        }
    );


    // =====================================================
    // AGREGAR PRODUCTO
    // =====================================================
    $('#agregarProducto').on(
        'click',
        function () {

            agregarProductoDesdeFormulario(

                '#producto',

                '#cantidad',

                '#precio',

                '#detalleCompra',

                '#totalCompra',

                '#total'
            );
        }
    );


    $('#agregarProductoEditar').on(
        'click',
        function () {

            agregarProductoDesdeFormulario(

                '#edit_producto',

                '#edit_cantidad',

                '#edit_precio',

                '#detalleCompraEditar',

                '#edit_totalCompra',

                '#edit_total'
            );
        }
    );


    // =====================================================
    // ELIMINAR ITEM
    // =====================================================
    $(document).on(
        'click',
        '.eliminar-item',
        function () {

            const table =
                $(this)
                    .closest('table')
                    .attr('id');

            const index =
                $(this)
                    .closest('tr')
                    .data('index');


            if (
                index !== undefined
            ) {

                carrito.splice(
                    index,
                    1
                );
            }


            $(this)
                .closest('tr')
                .remove();


            $('#' + table + ' tbody tr')
                .each(function (i) {

                    $(this)
                        .attr(
                            'data-index',
                            i
                        );
                });


            if (
                table ===
                'detalleCompraEditar'
            ) {

                actualizarTotal(

                    '#detalleCompraEditar',

                    '#edit_totalCompra',

                    '#edit_total'
                );

            } else {

                actualizarTotal(

                    '#detalleCompra',

                    '#totalCompra',

                    '#total'
                );
            }

        }
    );


    // =====================================================
    // REGISTRAR COMPRA
    // =====================================================
    $('#formRegistrarCompra').on(
        'submit',
        function (e) {

            e.preventDefault();

            const form = this;

            const btn =
                $(form).find(
                    'button[type="submit"]'
                );


            // VALIDAR FECHA
            if (
                !validarFecha(
                    '#fecha_compra'
                )
            ) {
                return;
            }


            let total =
                parseFloat(
                    $('#total').val()
                ) || 0;


            if (
                carrito.length === 0 ||
                total <= 0
            ) {

                mostrarError(
                    '#detalleCompra',
                    'Debe agregar productos a la compra.'
                );

                return;
            }


            let data =
                $(form).serializeArray();


            data.push({

                name: 'productos',

                value:
                    JSON.stringify(
                        carrito
                    )
            });


            btn.prop(
                'disabled',
                true
            );


            $.ajax({

                url:
                    '/admin?ruta=compra',

                type:
                    'POST',

                data:
                    $.param(data),

                dataType:
                    'json',

                success:
                    function (res) {

                        Swal.fire(res)
                            .then(function () {

                                if (
                                    res.icon ===
                                    'success'
                                ) {

                                    limpiarModalRegistrar();

                                    $('#modalRegistrarCompra')
                                        .modal('hide');

                                    refrescarTablaCompras();
                                }


                                btn.prop(
                                    'disabled',
                                    false
                                );

                            });

                    },

                error:
                    function () {

                        Swal.fire({

                            icon:
                                'error',

                            title:
                                'Error',

                            text:
                                'Error en el servidor'
                        });


                        btn.prop(
                            'disabled',
                            false
                        );
                    }
            });

        }
    );


    // =====================================================
    // EDITAR COMPRA
    // =====================================================
    $(document).on(
        'click',
        '.btnEditarCompra',
        function () {

            const cod =
                $(this).data('id');


            $('#edit_cod_compra')
                .val(cod);


            limpiarModalEditar();


            $.get(

                '/admin?ruta=compra',

                {
                    detalle_compra: 1,
                    cod_compra: cod
                },

                function (res) {

                    if (
                        !res ||
                        !res.compra
                    ) {

                        Swal.fire({

                            icon:
                                'error',

                            title:
                                'Error',

                            text:
                                'No se pudo cargar la compra.'
                        });

                        return;
                    }


                    $('#edit_fecha_compra')
                        .val(
                            res.compra.fecha_compra ||
                            ''
                        );


                    $('#edit_cod_proveedor')
                        .val(
                            res.compra.cod_proveedor ||
                            ''
                        );


                    const detalle =
                        Array.isArray(
                            res.detalle
                        )
                            ? res.detalle
                            : [];


                    const items =
                        detalle.map(
                            function (item) {

                                return {

                                    cod_producto:
                                        item.cod_producto,

                                    cantidad:
                                        item.cantidad,

                                    precio:
                                        item.precio_unitario,

                                    nombre:
                                        item.nombre_producto,

                                    marca:
                                        item.marca ||
                                        '—',

                                    categoria:
                                        item.categoria ||
                                        '—',

                                    tipo:
                                        item.tipo ||
                                        '—'
                                };

                            }
                        );


                    renderizarCarrito(

                        '#detalleCompraEditar',

                        '#edit_totalCompra',

                        '#edit_total',

                        items
                    );


                    $('#modalEditarCompra')
                        .modal('show');

                }
            );
        }
    );


    // =====================================================
    // ACTUALIZAR COMPRA
    // =====================================================
    $('#formEditarCompra').on(
        'submit',
        function (e) {

            e.preventDefault();

            const form = this;

            const btn =
                $(form).find(
                    'button[type="submit"]'
                );


            if (
                !validarFecha(
                    '#edit_fecha_compra'
                )
            ) {
                return;
            }


            let total =
                parseFloat(
                    $('#edit_total').val()
                ) || 0;


            if (
                carrito.length === 0 ||
                total <= 0
            ) {

                mostrarError(
                    '#detalleCompraEditar',
                    'Debe agregar productos a la compra.'
                );

                return;
            }


            let data =
                $(form).serializeArray();


            data.push({

                name:
                    'productos',

                value:
                    JSON.stringify(
                        carrito
                    )
            });


            btn.prop(
                'disabled',
                true
            );


            $.ajax({

                url:
                    '/admin?ruta=compra',

                type:
                    'POST',

                data:
                    $.param(data),

                dataType:
                    'json',

                success:
                    function (res) {

                        Swal.fire(res)
                            .then(function () {

                                if (
                                    res.icon ===
                                    'success'
                                ) {

                                    limpiarModalEditar();

                                    $('#modalEditarCompra')
                                        .modal('hide');

                                    refrescarTablaCompras();
                                }


                                btn.prop(
                                    'disabled',
                                    false
                                );

                            });

                    },

                error:
                    function () {

                        Swal.fire({

                            icon:
                                'error',

                            title:
                                'Error',

                            text:
                                'Error en el servidor'
                        });


                        btn.prop(
                            'disabled',
                            false
                        );
                    }
            });

        }
    );


    // =====================================================
    // VER COMPRA
    // =====================================================
    $(document).on(
        'click',
        '.btnDetalleCompra',
        function () {

            const cod = $(this).data('id');

            $.get(
                '/admin?ruta=compra',
                {
                    detalle_compra: 1,
                    cod_compra: cod
                },
                function (res) {

                    if (!res || !res.compra) {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'No se pudo cargar el comprobante.'
                        });
                        return;
                    }

                    const compra = res.compra;
                    const detalle = Array.isArray(res.detalle)
                        ? res.detalle
                        : [];

                    $('#factura_codigo').text(compra.cod_compra || cod);
                    $('#factura_proveedor').text(compra.proveedor || 'Sin proveedor');
                    $('#factura_rif').text(compra.rif || 'Sin RIF');
                    $('#factura_fecha').text(formatearFechaCompra(compra.fecha_compra));
                    $('#factura_status').text(
                        compra.status == 1 ? 'Completada' : 'Cancelada'
                    );
                    $('#factura_total').text(formatearMoneda(compra.total));

                    const filas = detalle.map(function (item) {
                        const cantidad = parseFloat(item.cantidad) || 0;
                        const precio = parseFloat(item.precio_unitario) || 0;

                        return `
                            <tr>
                                <td>${item.nombre_producto || 'Sin producto'}</td>
                                <td class="text-end">${cantidad}</td>
                                <td class="text-end">${formatearMoneda(precio)}</td>
                                <td class="text-end">${formatearMoneda(cantidad * precio)}</td>
                            </tr>
                        `;
                    }).join('');

                    $('#factura_detalle').html(
                        filas || '<tr><td colspan="4" class="text-center">Sin productos</td></tr>'
                    );

                    $('#modalVerCompra').modal('show');
                }
            ).fail(function () {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error en el servidor al cargar el comprobante.'
                });
            });
        }
    );


    // =====================================================
    // DESCARGAR COMPROBANTE EN PDF
    // =====================================================
    $(document).on(
        'click',
        '#btnDescargarFactura',
        function () {

            const tituloAnterior = document.title;
            const codigo = $('#factura_codigo').text() || 'compra';

            document.title = `Comprobante-compra-${codigo}`;

            const restaurarTitulo = function () {
                document.title = tituloAnterior;
                window.removeEventListener('afterprint', restaurarTitulo);
            };

            window.addEventListener('afterprint', restaurarTitulo);
            window.print();
        }
    );


    // =====================================================
    // CARGAR ID ELIMINAR
    // =====================================================
    $(document).on(
        'click',
        '.btnEliminarCompra',
        function () {

            $('#cod_compra_eliminar')
                .val(
                    $(this).data('id')
                );
        }
    );


    // =====================================================
    // ELIMINAR COMPRA
    // =====================================================
    $('#formEliminarCompra').on(
        'submit',
        function (e) {

            e.preventDefault();


            $.post(

                '/admin?ruta=compra',

                $(this).serialize(),

                function (res) {

                    Swal.fire(res)
                        .then(function () {

                            if (
                                res.icon ===
                                'success'
                            ) {

                                refrescarTablaCompras();
                            }


                            $('#modalEliminarCompra')
                                .modal('hide');

                        });

                },

                'json'
            );

        }
    );


    // =====================================================
    // LIMPIEZA AL CERRAR MODALES
    // =====================================================
    $('#modalRegistrarCompra').on(
        'hidden.bs.modal',
        function () {

            limpiarModalRegistrar();
        }
    );


    $('#modalEditarCompra').on(
        'hidden.bs.modal',
        function () {

            limpiarModalEditar();
        }
    );

});