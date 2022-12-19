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

  // for index in database display layer.....
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
    const pqkmeans_labels = image[0].pqkmeans_labels;
    const kmeans_labels = image[0].kmeans_labels;

    console.log(mei);
    console.log(vigs);
    console.log(pqkmeans);
    console.log(kmeans);
    console.log(spectral_index_name);
    console.log(spectral_index_equation);
    console.log(spectral_index_color_palette);
    if (spectral_index_color_palette.includes('diverging')) {
      console.log(spectral_index_color_palette.replace('diverging', ''));
    }
    console.log(band_stack_list);
    console.log(k_value);
    console.log(num_subdimensions);
    console.log(ks_value);
    console.log(sample_size);
    console.log(pqkmeans_labels);
    console.log(kmeans_labels);

    if (mei != "") {
      document.querySelector('#get_mei').addEventListener('click', () => get_mei(mei, spectral_index_color_palette));
    }
    if (vigs != "") {
      document.querySelector('#get_vigs').addEventListener('click', () => get_vigs(vigs, spectral_index_color_palette));
    }
    if (pqkmeans != "") {
      document.querySelector('#get_pqkmeans').addEventListener('click', () => get_pqkmeans(pqkmeans, band_stack_list, k_value, num_subdimensions, ks_value, sample_size, spectral_index_color_palette));
    }
    if (kmeans != "") {
      document.querySelector('#get_kmeans').addEventListener('click', () => get_kmeans(kmeans, band_stack_list, k_value, spectral_index_color_palette));
    }
    if (spectral_index_name != "") {
      document.querySelector('#get_spectral_index').addEventListener('click', () => get_spectral_index(spectral_index_name, spectral_index_equation, spectral_index_color_palette));
    }

    // add legend on checkbox
    map.on('overlayadd', function(e){
      console.log("e.name:", e.name)
      if (e.name == "lulc pqkmeans" || e.name == "lulc kmeans") {
        // Categorical legend
        if (e.name == "lulc pqkmeans") {
          var data = JSON.parse(pqkmeans_labels);
        }
        else {
          var data = JSON.parse(kmeans_labels);
        }
        var color = d3.scaleOrdinal()
          .domain(data)
          .range(d3.schemeCategory10);

        d3.select(".my_categorical_legend")
          .selectAll("div")
          .data(data)
          .enter()
          .append("div")
          .style("width", '20px')
          .style("background-color", function(d){ return color(d)})
          .text(function(d) { return d; });
      }
      else {
        // Sequential and diverging type of legend
        document.querySelector("#top_value").innerHTML = 255; // legend top value

        var data = [...Array(180).keys()];
        if (spectral_index_color_palette.includes('diverging')) {
        var color = d3.scaleDiverging() // source: https://www.d3indepth.com/scales/
                      .domain([0, 250])
                      .interpolator(d3[`interpolate${spectral_index_color_palette.replace('diverging', '')}`]);
        }
        else {
          var color = d3.scaleSequential()
                        .domain([0, 250])
                        .interpolator(d3[`interpolate${spectral_index_color_palette}`]); // other sequential interpolaters: Viridis, Inferno, Magma, Plasma, Warm, Cool, Rainbow, CubehelixDefault
        }
        d3.select(".my_sequential_legend")
          .selectAll("div")
          .data(data)
          .enter()
          .append("div")
          .style("width", '60px')
          .style("background-color", function(d){ return color(d)});
      }

      document.querySelector("#bottom_value").innerHTML = 0; // legend bottom value
    })

    // remove legend on checkbox
    map.on('overlayremove', function(e){
      document.querySelector(".my_categorical_legend").innerHTML = '';
      document.querySelector(".my_sequential_legend").innerHTML = '';
      document.querySelector("#top_value").innerHTML = '';
      document.querySelector("#bottom_value").innerHTML = '';
    })



  })

  // messages timer
  var info_messages = document.getElementsByClassName('alert');

  setTimeout(function(){
      for (var i = 0; i < info_messages.length; i ++) {
          // Set display attribute as !important, neccessary when using bootstrap
          info_messages[i].setAttribute('style', 'display:none !important');
      }
  }, 3000);

});

function get_mei(mei, spectral_index_color_palette) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      mei:mei,
      spectral_index_color_palette:spectral_index_color_palette
    })
  });
}

function get_vigs(vigs, spectral_index_color_palette) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      vigs:vigs,
      spectral_index_color_palette:spectral_index_color_palette
    })
  });
}

function get_pqkmeans(pqkmeans, band_stack_list, k_value, num_subdimensions, ks_value, sample_size, spectral_index_color_palette) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      pqkmeans:pqkmeans,
      band_stack_list:band_stack_list,
      k_value:k_value,
      num_subdimensions:num_subdimensions,
      ks_value:ks_value,
      sample_size:sample_size,
      spectral_index_color_palette:spectral_index_color_palette
    })
  });
}

function get_kmeans(kmeans, band_stack_list, k_value, spectral_index_color_palette) {
  fetch(`/pixels`, {
    method: 'PUT',
    body: JSON.stringify({
      kmeans:kmeans,
      band_stack_list:band_stack_list,
      k_value:k_value,
      spectral_index_color_palette:spectral_index_color_palette
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