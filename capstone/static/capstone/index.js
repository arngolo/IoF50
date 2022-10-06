document.addEventListener('DOMContentLoaded', function() {
  const array = "[1, 2, 3, 4]";

  // var ee = require('@google/earthengine');
  // console.log(ee.Image('LANDSAT/LC08/C01/T1/LC08_044034_20140318'));
  document.querySelector('#get_remote_image').addEventListener('click', () => push_pixels(array));
  });

function push_pixels(array) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      remote_image:array,
    })
  });
}