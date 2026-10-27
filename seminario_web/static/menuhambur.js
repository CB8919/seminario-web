
document.addEventListener("DOMContentLoaded", () => {
    const botonMenu = document.getElementById("menu-toggle");
    const menuNavegacion = document.getElementById("menu-navegacion");

    if (!botonMenu || !menuNavegacion) {
        return;
    }

    botonMenu.addEventListener("click", () => {
        const menuAbierto = menuNavegacion.classList.toggle("menu-abierto");

        botonMenu.setAttribute("aria-expanded", menuAbierto);
        botonMenu.setAttribute(
            "aria-label",
            menuAbierto ? "Cerrar menú" : "Abrir menú"
        );
    });
});


