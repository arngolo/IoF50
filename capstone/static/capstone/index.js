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
    const spectral_index_color_palette = image[0].spectral_index_color_palette;
    const mei = image[0].mei;
    const vigs = image[0].vigs;
    const pqkmeans = image[0].pqkmeans;
    const kmeans = image[0].kmeans;
    const band_stack_list = image[0].band_stack_list;
    const k_value = image[0].k_value;
    const num_subdimensions = image[0].num_subdimensions;
    const ks_value = image[0].ks_value;
    const sample_size = image[0].sample_size;

    console.log(mei);
    console.log(vigs);
    console.log(pqkmeans);
    console.log(kmeans);
    console.log(spectral_index_name);
    console.log(spectral_index_equation);
    console.log(band_stack_list);
    console.log(k_value);
    console.log(num_subdimensions);
    console.log(ks_value);
    console.log(sample_size);

    if (mei != "") {
      document.querySelector('#get_mei').addEventListener('click', () => get_mei(mei));
    }
    if (vigs != "") {
      document.querySelector('#get_vigs').addEventListener('click', () => get_vigs(vigs));
    }
    if (pqkmeans != "") {
      document.querySelector('#get_pqkmeans').addEventListener('click', () => get_pqkmeans(pqkmeans, band_stack_list, k_value, num_subdimensions, ks_value, sample_size));
    }
    if (kmeans != "") {
      document.querySelector('#get_kmeans').addEventListener('click', () => get_kmeans(kmeans, band_stack_list, k_value));
    }
    if (spectral_index_name != "") {
      document.querySelector('#get_spectral_index').addEventListener('click', () => get_spectral_index(spectral_index_name, spectral_index_equation, spectral_index_color_palette));
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

function get_pqkmeans(pqkmeans, band_stack_list, k_value, num_subdimensions, ks_value, sample_size) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      pqkmeans:pqkmeans,
      band_stack_list:band_stack_list,
      k_value:k_value,
      num_subdimensions:num_subdimensions,
      ks_value:ks_value,
      sample_size:sample_size,
    })
  });
}

function get_kmeans(kmeans, band_stack_list, k_value) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      kmeans:kmeans,
      band_stack_list:band_stack_list,
      k_value:k_value,
    })
  });
}

function get_spectral_index(spectral_index_name, spectral_index_equation, spectral_index_color_palette) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      spectral_index_name:spectral_index_name,
      spectral_index_equation:spectral_index_equation,
      spectral_index_color_palette:spectral_index_color_palette
    })
  });
}