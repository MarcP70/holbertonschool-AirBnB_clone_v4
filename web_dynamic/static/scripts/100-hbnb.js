$(document).ready(function () {
  const selectedAmenities = {};
  const selectedStates = {};
  const selectedCities = {};

  // Function to update the selected amenities display
  const updateSelectedAmenities = () => {
    $('#selected_amenities').text(Object.values(selectedAmenities).join(', '));
  };

  // Function to update the selected locations display
  const updateSelectedStates = () => {
    const stateNames = Object.values(selectedStates).filter(Boolean).join(', ');
    updateSelectedLocations(stateNames);
  };

  const updateSelectedCities = () => {
    const cityNames = Object.values(selectedCities).filter(Boolean).join(', ');
    updateSelectedLocations(cityNames);
  };

  const updateSelectedLocations = (locations) => {
    $('#selected_locations').text(locations);
  };


  $('input[type=checkbox]').change(function () {
    const id = $(this).data('id');
    const name = $(this).data('name');
    const type = $(this).data('type');

    if (this.checked) {
      if (type === 'amenity') selectedAmenities[id] = name;
      else if (type === 'state') selectedStates[id] = name;
      else if (type === 'city') selectedCities[id] = name;
    } else {
      if (type === 'amenity') delete selectedAmenities[id];
      else if (type === 'state') delete selectedStates[id];
      else if (type === 'city') delete selectedCities[id];
    }

    updateSelectedAmenities();
    updateSelectedLocations();
  });

  const apiUrlStatus = 'http://127.0.0.1:5001/api/v1/status/';
  const updateApiStatus = () => {
    $.ajax({
      type: 'GET',
      url: apiUrlStatus,
      success: (data) => {
        if (data.status === 'OK') {
          $('#api_status').addClass('available');
        } else {
          $('#api_status').removeClass('available');
        }
      },
      error: () => {
        $('#api_status').removeClass('available');
      }
    });
  };

  const apiUrlPlacesSearch = 'http://127.0.0.1:5001/api/v1/places_search/';

  const updatePlaces = () => {
    const requestData = {
      amenities: Object.keys(selectedAmenities),
      states: Object.keys(selectedStates),
      cities: Object.keys(selectedCities)
    };

    $.ajax({
      type: 'POST',
      url: apiUrlPlacesSearch,
      contentType: 'application/json',
      data: JSON.stringify(requestData),
      success: (data) => {
        displayPlaces(data);
      },
      error: () => {
        console.error('Error loading places.');
      }
    });
  };

  const displayPlaces = (places) => {
    const placesSection = $('.places');
    placesSection.empty();

    places.forEach((place) => {
      const article = $('<article></article>');
      article.append(`<div class="title_box">
                        <h2>${place.name}</h2>
                        <div class="price_by_night">$${place.price_by_night}</div>
                      </div>
                      <div class="information">
                        <div class="max_guest">${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}</div>
                        <div class="number_rooms">${place.number_rooms} Bedroom${place.number_rooms !== 1 ? 's' : ''}</div>
                        <div class="number_bathrooms">${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}</div>
                      </div>
                      <div class="description">${place.description}</div>`);

      placesSection.append(article);
    });
  };

  updateApiStatus();
  updatePlaces();

  $('button').click(() => {
    updatePlaces();
  });
});
