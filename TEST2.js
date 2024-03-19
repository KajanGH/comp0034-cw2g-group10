const { DeckGL, ColumnLayer } = deck;
const token =
  'pk.eyJ1IjoiZGlhbmFtZW93IiwiYSI6ImNqcmh4aWJnOTIxemI0NXA0MHYydGwzdm0ifQ.9HakB25m0HLT-uDY2yat7A';
const dataUrl =
  'https://raw.githubusercontent.com/KajanGH/data/main/fem.json';

// Function to calculate sum of ages within a range
function calculateElevationInRange(d, startAge, endAge) {
  let sum = 0;
  for (let i = startAge; i <= endAge; i++) {
    sum += d[`age_${i}`] || 0; // Adding age_i value, defaulting to 0 if undefined
  }
  return sum;
}

// Function to find the maximum elevation value in the provided data
function findScale(data, startAge, endAge) {
  let max = 0;
  data.forEach((d) => {
    const elevation = calculateElevationInRange(d, startAge, endAge);
    if (elevation > max) {
      max = elevation;
    }
  });
  max = 40000 / max; // Adjusted as per your requirement
  return max;
}

function findMax(data, startAge, endAge) {
    let max = 0;
    data.forEach((d) => {
      const elevation = calculateElevationInRange(d, startAge, endAge);
      if (elevation > max) {
        max = elevation;
      }
    }); // Adjusted as per your requirement
    return max;
  }

function findMin(data, startAge, endAge) {
    let max = Infinity;
    data.forEach((d) => {
      const elevation = calculateElevationInRange(d, startAge, endAge);
      if (elevation < max) {
        max = elevation;
      }
    }); // Adjusted as per your requirement
    return max;
  }

function ryb2rgb(r, y, b) {

    // Remove the whiteness from the color.
    var w = Math.min(r, y, b);
    r -= w;
    y -= w;
    b -= w;

    var my = Math.max(r, y, b);

    // Get the green out of the yellow and blue
    var g = Math.min(y, b);
    y -= g;
    b -= g;

    if (b && g) {
        b *= 2.0;
        g *= 2.0;
    }

    // Redistribute the remaining yellow.
    r += y;
    g += y;

    // Normalize to values.
    var mg = Math.max(r, g, b);
    if (mg) {
        var n = my / mg;
        r *= n;
        g *= n;
        b *= n;
    }

    // Add the white back in.
    r += w;
    g += w;
    b += w;

    // And return back the ryb typed accordingly.
    return [r, g, b];
}

// Fetch the data first
fetch(dataUrl)
  .then((response) => response.json())
  .then((data) => {
    const startAge = 0;
    const endAge = 5;
    

    // Create DeckGL instance inside the fetch callback
    new DeckGL({
      mapboxApiAccessToken: token,
      mapStyle: 'mapbox://styles/mapbox/dark-v10',
      initialViewState: {
        container: 'map',
        longitude: -1.932311,
        latitude: 51.923,
        pitch: 60,
        bearing: -32,
        minZoom: 5,
        zoom: 7,
      },

      controller: true,
      layers: [
        new ColumnLayer({
          id: 'column',
          data, // Pass the fetched data
          diskResolution: 12,
          radius: 1000,
          elevationScale: findScale(data, startAge, endAge),
          getPosition: (d) => [d.Longitude, d.Latitude],
          getFillColor: (d) => 
            ryb2rgb((findScale(data, startAge, endAge) * 255 * calculateElevationInRange(d, startAge, endAge) / 40000), // Adjusted as per your requirement
            255 - (findScale(data, startAge, endAge) * 255 * calculateElevationInRange(d, startAge, endAge) / 40000),
            255),
          getElevation: (d) => calculateElevationInRange(d, startAge, endAge),
        }),
      ],
    });
  })
  .catch((error) => console.error('Error fetching data:', error));
