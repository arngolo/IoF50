document.addEventListener('DOMContentLoaded', function() {

  var openStreetMap = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap'
  });
  var openTopoMap = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'
});
  var satelliteImage = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
  });
  var night_light = L.tileLayer('https://map1.vis.earthdata.nasa.gov/wmts-webmerc/VIIRS_CityLights_2012/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}', {
    attribution: 'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
    minZoom: 0,
    maxZoom: 8,
    format: 'jpg',
    time: '',
    tilematrixset: 'GoogleMapsCompatible_Level'
  });

  ndviLayer = L.tileLayer('https://storage.googleapis.com/beyond_rgb/ndvi/{z}/{x}/{y}.png', {tms: true, opacity: 0.7, attribution: ""});
  meiLayer = L.tileLayer('https://storage.googleapis.com/beyond_rgb/mei/{z}/{x}/{y}.png', {tms: true, opacity: 0.7, attribution: ""});
  vigsLayer = L.tileLayer('https://storage.googleapis.com/beyond_rgb/vigs/{z}/{x}/{y}.png', {tms: true, opacity: 0.7, attribution: ""});
  lulcPqkmeansLayer = L.tileLayer('https://storage.googleapis.com/beyond_rgb/lulc_pqkmeans/{z}/{x}/{y}.png', {tms: true, opacity: 0.7, attribution: ""});
  lulcKmeansLayer = L.tileLayer('https://storage.googleapis.com/beyond_rgb/lulc_kmeans/{z}/{x}/{y}.png', {tms: true, opacity: 0.7, attribution: ""});

  // Create the map with basemaps and custom layers
  var map = L.map('map', {layers: [openStreetMap]}).setView([0, 0], 3);
  var basemaps = {"Open Street Map": openStreetMap, "Open Topo Map": openTopoMap, "Imagery": satelliteImage, "Night Light": night_light}
  var overlaymaps = {"ndvi": ndviLayer, "mei": meiLayer, "vigs": vigsLayer, "lulc pqkmeans": lulcPqkmeansLayer, "lulc kmeans": lulcKmeansLayer}

  L.control.layers(basemaps, overlaymaps, {collapsed: false}).addTo(map);

  fetch(`/pixels`)
  .then(response => response.json())
  .then(image => {

    const spectral_index_name = image[0].spectral_index_name;
    const spectral_index_equation = image[0].spectral_index_equation;
    const mei = image[0].mei;
    const vigs = image[0].vigs;
    const pqkmeans = image[0].pqkmeans;
    const kmeans = image[0].kmeans;

    console.log(mei);
    console.log(vigs);
    console.log(pqkmeans);
    console.log(kmeans);
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
    if (kmeans != "") {
      document.querySelector('#get_kmeans').addEventListener('click', () => get_kmeans(kmeans));
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

function get_kmeans(kmeans) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      kmeans:kmeans,
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