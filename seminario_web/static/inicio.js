document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".anime-tarjeta").forEach((tarjeta, index) => {

        const boton = tarjeta.querySelector(".btn-sinopsis");
        const modales = document.querySelectorAll(".modal-sinopsis");
        const modal = modales[index];
        if (!modal) return;
        
        const cerrar = modal.querySelector(".modal-cerrar");

        boton.addEventListener("click", () => {
            modal.hidden = false;
        });

        cerrar.addEventListener("click", () => {
            modal.hidden = true;
        });

        modal.addEventListener("click", (event) => {
            if (event.target === modal) {
                modal.hidden = true;
            }
        });

    });

});