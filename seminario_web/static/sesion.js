// Cierre automático de sesión al cerrar la pestaña o el navegador
window.addEventListener("beforeunload", function () {
    navigator.sendBeacon("/cerrar-sesion-navegador/");
});