document.addEventListener('DOMContentLoaded', function() {

  // Create the map with 2 layers
  var map = L.map('map').setView([0, 0], 3);
  var globalLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap'
  }).addTo(map),
  localLayer = L.tileLayer('https://storage.googleapis.com/beyond_rgb/ndvi/{z}/{x}/{y}.png', {tms: true, opacity: 0.7, attribution: ""});

  var groupLayer = L.layerGroup([globalLayer, localLayer]);

  groupLayer.addTo(map);

  fetch(`/pixels`)
  .then(response => response.json())
  .then(image => {

    const spectral_index_name = image[0].spectral_index_name;
    const spectral_index_equation = image[0].spectral_index_equation;
    const mei = image[0].mei;
    const vigs = image[0].vigs;
    const pqkmeans = image[0].pqkmeans;

    console.log(mei);
    console.log(vigs);
    console.log(pqkmeans);
    console.log(spectral_index_name);
    console.log(spectral_index_equation);

    if (mei != "") {
      document.querySelector('#get_mei').addEventListener('click', () => get_mei(mei));
    }
    if (vigs != "") {
      document.querySelector('#get_vigs').addEventListener('click', () => get_vigs(vigs));
    }
    if (pqkmeans != "") {
      document.querySelector('#get_pqkmeans').addEventListener('click', () => get_pqkmeans(pqkmeans));
    }
    if (spectral_index_name != "") {
      document.querySelector('#get_spectral_index').addEventListener('click', () => get_spectral_index(spectral_index_name, spectral_index_equation));
    }
  })

});

function get_mei(mei) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      mei:mei,
    })
  });
}

function get_vigs(vigs) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      vigs:vigs,
    })
  });
}

function get_pqkmeans(pqkmeans) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      pqkmeans:pqkmeans,
    })
  });
}
function get_spectral_index(spectral_index_name, spectral_index_equation) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      spectral_index_name:spectral_index_name,
      spectral_index_equation:spectral_index_equation,
    })
  });
}