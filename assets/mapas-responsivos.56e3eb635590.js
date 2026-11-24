// Mantém as áreas clicáveis alinhadas às artes, inclusive ao mudar de tamanho de tela.
(() => {
  'use strict';

  const maps = Array.from(document.querySelectorAll('img[usemap]')).map((image) => {
    const map = document.getElementById(image.getAttribute('usemap').slice(1));
    const width = Number(image.dataset.mapWidth || image.getAttribute('width'));
    const height = Number(image.dataset.mapHeight || image.getAttribute('height'));
    const areas = Array.from(map.querySelectorAll('area[coords]')).map((area) => ({
      area,
      // Guardar os valores originais evita acumular arredondamentos a cada resize.
      coords: area.getAttribute('coords').split(',').map(Number),
    }));

    const update = () => {
      const bounds = image.getBoundingClientRect();
      if (!bounds.width || !bounds.height) return; // Arte oculta por um breakpoint.
      areas.forEach(({ area, coords }) => {
        area.coords = coords.map((value, index) => Math.floor(
          value * (index % 2 ? bounds.height / height : bounds.width / width)
        )).join(',');
      });
    };

    image.addEventListener('load', update);
    update();
    return { image, update };
  });

  if ('ResizeObserver' in window) {
    const updates = new Map(maps.map(({ image, update }) => [image, update]));
    const observer = new ResizeObserver((entries) => {
      entries.forEach(({ target }) => updates.get(target)());
    });
    maps.forEach(({ image }) => observer.observe(image));
  } else {
    window.addEventListener('resize', () => maps.forEach(({ update }) => update()));
  }
})();
