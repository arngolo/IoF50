document.addEventListener('DOMContentLoaded', function() {
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