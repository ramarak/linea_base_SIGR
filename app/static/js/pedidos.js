(function () {
    const tabla = document.getElementById("tabla-pedidos");
    if (!tabla) {
        return;
    }

    function refrescar() {
        fetch("/pedidos/api/estados")
            .then(function (respuesta) {
                if (!respuesta.ok) {
                    return [];
                }
                return respuesta.json();
            })
            .then(function (pedidos) {
                pedidos.forEach(function (pedido) {
                    const fila = tabla.querySelector('[data-pedido-id="' + pedido.id + '"]');
                    if (!fila) {
                        return;
                    }
                    const celda = fila.querySelector(".estado");
                    if (celda) {
                        celda.textContent = pedido.estado.replace(/_/g, " ");
                    }
                });
            })
            .catch(function () {
                /* La línea base tolera un fallo puntual de red. */
            });
    }

    setInterval(refrescar, 5000);
})();
