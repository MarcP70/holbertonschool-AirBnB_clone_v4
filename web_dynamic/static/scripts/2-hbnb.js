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
  });

  const apiUrl = 'http://127.0.0.1:5001/api/v1/status/';

  // Function to update API status
  const updateApiStatus = () => {
    $.ajax({
      type: 'GET',
      url: apiUrl,
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

  // Initially update API status
  updateApiStatus();
});
