// Galerías de «Conociendo nuestros territorios»: al pasar el mouse sobre una
// galería, las fotos avanzan solas; al salir, se detiene en la que esté.
// Se usa delegación de eventos en el documento para que funcione también
// después de navegar entre páginas sin recargar.
(function () {
  var INTERVALO_MS = 1800;
  var activa = null;
  var temporizador = null;

  function siguiente(galeria) {
    var opciones = galeria.querySelectorAll(':scope > input[type="radio"]');
    if (opciones.length < 2) return;
    var actual = Array.prototype.findIndex.call(opciones, function (o) { return o.checked; });
    opciones[(actual + 1) % opciones.length].checked = true;
  }

  function detener() {
    clearInterval(temporizador);
    temporizador = null;
    activa = null;
  }

  document.addEventListener('mouseover', function (evento) {
    var galeria = evento.target.closest && evento.target.closest('.territory-gallery');
    if (!galeria || galeria === activa) return;
    detener();
    activa = galeria;
    siguiente(galeria);
    temporizador = setInterval(function () { siguiente(galeria); }, INTERVALO_MS);
  });

  document.addEventListener('mouseout', function (evento) {
    if (!activa) return;
    var destino = evento.relatedTarget;
    if (!destino || !activa.contains(destino)) detener();
  });
})();
