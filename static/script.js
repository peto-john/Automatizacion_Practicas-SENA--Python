/*const botonDescarga = document.querySelector('.btn-descarga');

botonDescarga.addEventListener('click', async () => {
    const textoOriginal = botonDescarga.textContent;
    botonDescarga.textContent = "DESCARGANDO...";
    botonDescarga.disabled = true;

    try {
        const response = await fetch("/descargar_csv");

        if (!response.ok) throw new Error("Error al generar el CSV");

        const blob = await response.blob(); // convertimos la respuesta en un Blob
        const url = window.URL.createObjectURL(blob); // creamos un URL temporal

        // Creamos un enlace temporal y lo clickeamos
        const a = document.createElement("a");
        a.href = url;
        a.download = "trafico_aniscopio.csv"; // nombre del archivo
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

    } catch (error) {
        alert("Error: " + error.message);
    } finally {
        botonDescarga.textContent = textoOriginal;
        botonDescarga.disabled = false;
    }
});
*/