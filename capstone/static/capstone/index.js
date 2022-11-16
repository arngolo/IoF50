document.addEventListener('DOMContentLoaded', function() {

  // Create the map with 2 layers
  var map = L.map('map').setView([0, 0], 3);
  var globalLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap'
  }).addTo(map),
  localLayer = L.tileLayer('https://storage.googleapis.com/beyond_rgb/lulc/{z}/{x}/{y}.png', {tms: true, opacity: 0.7, attribution: ""});

  var groupLayer = L.layerGroup([globalLayer, localLayer]);

  groupLayer.addTo(map);

  fetch(`/pixels`)
  .then(response => response.json())
  .then(image => {

    const image_name = image[0].image_name;
    // const normalized_difference = image[0].normalized_difference;
    const mei = image[0].mei;
    const vigs = image[0].vigs;
    const pqkmeans = image[0].pqkmeans;
    console.log(image_name);
    console.log(mei);
    console.log(vigs);
    console.log(pqkmeans);
    if (image_name != "") {
      document.querySelector('#get_remote_image').addEventListener('click', () => get_pixels(image_name));
    }
    if (mei != "") {
      document.querySelector('#get_mei').addEventListener('click', () => get_mei(mei));
    }
    if (vigs != "") {
      document.querySelector('#get_vigs').addEventListener('click', () => get_vigs(vigs));
    }
    if (pqkmeans != "") {
      document.querySelector('#get_pqkmeans').addEventListener('click', () => get_pqkmeans(pqkmeans));
    }
    // else if (normalized_difference != "") {
    //   document.querySelector('#get_nd').addEventListener('click', () => get_normalized_difference(normalizedDifference));
    // }
  })

});

function get_pixels(image_name) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      image_name:image_name,
    })
  });
}

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
// function get_normalized_difference(normalized_difference) {
//   fetch(`/pixels`, {
//     method: 'PUT',
//     body: JSON.stringify({
//       normalized_difference:normalized_difference,
//     })
//   });
// }