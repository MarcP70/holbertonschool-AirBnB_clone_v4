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
});
