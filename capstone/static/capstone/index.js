document.addEventListener('DOMContentLoaded', function() {

      // Create the map with 2 layers
      var map = L.map('map').setView([0, 0], 3);
      var globalLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'OpenStreetMap'
      }).addTo(map),
      localLayer = L.tileLayer('https://storage.googleapis.com/beyond_rgb/maptiles/{z}/{x}/{y}.png');
  
      var groupLayer = L.layerGroup([globalLayer, localLayer]);
  
      groupLayer.addTo(map);

    const image_name = "LANDSAT/LC09/C02/T1/LC09_182066_20220611";

  // var ee = require('@google/earthengine');
  // console.log(ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318'));
  document.querySelector('#get_remote_image').addEventListener('click', () => get_pixels(image_name));
  });

function get_pixels(image_name) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      image_name:image_name,
    })
  });
}