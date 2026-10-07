// Cierre automático de sesión al cerrar la pestaña o el navegador
window.addEventListener("beforeunload", function () {
    const csrfToken = document.querySelector(
        '[name=csrfmiddlewaretoken]'
    )?.value;

    if (!csrfToken) return;

    const datos = new FormData();
    datos.append("csrfmiddlewaretoken", csrfToken);

    navigator.sendBeacon("/logout/", datos);
});