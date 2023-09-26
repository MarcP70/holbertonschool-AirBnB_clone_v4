$(document).ready(function () {
  const selectedAmenities = {};

  $('input[type=checkbox]').change(function () {
    const amenityId = $(this).data('id');
    const amenityName = $(this).data('name');

    if (this.checked) {
      selectedAmenities[amenityId] = amenityName;
    } else {
      delete selectedAmenities[amenityId];
    }

    $('#selected_amenities').text(Object.values(selectedAmenities).join(', '));
    updatePlaces();
  });

  const apiUrlStatus = 'http://127.0.0.1:5001/api/v1/status/';

  // Function to update API status
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
    $.ajax({
      type: 'POST',
      url: apiUrlPlacesSearch,
      contentType: 'application/json',
      data: JSON.stringify({}),
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

  // Initially update API status
  updateApiStatus();
  // Initially update places
  updatePlaces();
});
