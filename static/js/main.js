(function($) {
  var currentLang = $('html').attr('lang');
  function getApiUrl(url) {
    return `https://data2.xalqnazorati.uz${url}`;
  }

  function getApiAuthToken() {
    return 'token 156d860c1900e489b21bf6ef55b75957974e514c';
  }

  function getCurrentLang() {
    return currentLang || 'ru';
  }


  function initSelect2() {
    $('[data-plugin="select2"]').select2({
      language: 'ru',
      placeholder: '',
      //allowClear: true
    });
  }

  function showContent() {
    $('.preloader').remove();
    $('.content').addClass('show');
  }

  var form1 = null;

  function initForm1() {
    form1 = {
      $map: $('#form1-map'),
      map: null,
      mapMarker: null,
      $addressSelect: $('[data-role="form1-address-select"]'),
      $districtInput: $('[data-role="form1-district-input"]'),
      $streetInput: $('[data-role="form1-street-input"]'),
      $communityInput: $('[data-role="form1-community-input"]'),
      $houseInput: $('[data-role="form1-house-input"]')
    };

    initForm1Map();

    initForm1AddressSelect();
  }

  function initForm1Map() {
    DG.then(function() {
      form1.map = DG.map('form1-map', {
        center: [41.2995, 69.2401],
        zoom: 16
      });

      form1.mapMarker = DG.marker([41.2995, 69.2401]).addTo(form1.map);

      showContent();
    });
  }

  function showForm1Map(latLng) {
    form1.$map.addClass('show');

    form1.map.setView(latLng);
    form1.mapMarker.setLatLng(latLng);
  }

  function initForm1AddressSelect() {
    form1.$addressSelect.select2({
      minimumInputLength: 3,
      ajax: {
        delay: 1000,
        url: getApiUrl(`/${$('html').attr('lang')}/v1/suggestions`),
        headers: {
          'Authorization': getApiAuthToken(),
        },
        dataType: 'json',
        data: function(params) {
          return {
            q: params.term
          };
        },
        processResults: function(response) {
          return {
            results: response.results.map((item) => ({
              id: 'district' + item.district.id + '-street' + item.id,
              text: `${getCurrentLang() === 'ru' ? item.address_ru : getCurrentLang() === 'oz' ? item.address_oz : item.address_uz}`,
              details: item
            }))
          };
        }
      }
    });

    form1.$addressSelect.on('select2:select', function(e) {
      var selectedData = e.params.data;

      showForm1AddressDetails();

      setForm1Data(selectedData.details);
    });
  }

  function showForm1AddressDetails() {
    $('#form1-address-details').addClass('show');
  }

  function setForm1Data(data) {
    if (data.district !== undefined) {
      form1.$districtInput.val(`${getCurrentLang() === 'ru' ? data.district.name_ru : getCurrentLang() === 'oz' ?  data.district.name_oz : data.district.name_uz}`);
    }

    if (data.name_ru !== undefined) {
      form1.$streetInput.val(`${getCurrentLang() === 'ru' ? data.name_ru : getCurrentLang() === 'oz' ?  data.name_oz : data.name_uz}`);
    }
    //
    // if (data.community !== undefined) {
    //   form1.$communityInput.val(data.community.name);
    // }
    //
    // if (data.house !== undefined) {
    //   form1.$houseInput.val(data.house.number);
    //
    //   showForm1Map([
    //     parseFloat(data.house.latitude),
    //     parseFloat(data.house.longitude)
    //   ]);
    // }
  }

  var form2 = null;

  function initForm2() {
    form2 = {
      $map: $('#form2-map'),
      map: null,
      mapMarker: null,
      $districtSelect: $('[data-role="form2-district-select"]'),
      $streetTypeSelect: $('[data-role="form2-street-type-select"]'),
      $streetSelect: $('[data-role="form2-street-select"]'),
      $houseSelect: $('[data-role="form2-house-select"]'),
      $communityInput: $('[data-role="form2-community-input"]'),
      districtId: null,
      streetType: null,
      streetId: null
    };

    initForm2DistrictSelect();

    initForm2StreetTypeSelect();

    initForm2StreetSelect();

    initForm2HouseSelect();
  }

  function initForm2Map(latLng) {
    DG.then(function() {
      form2.map = DG.map('form2-map', {
        center: latLng,
        zoom: 16
      });

      form2.mapMarker = DG.marker(latLng).addTo(form2.map);
    });
  }

  function showForm2Map(latLng) {
    form2.$map.addClass('show');

    if (!form2.map) {
      initForm2Map(latLng);

      return;
    }

    form2.map.setView(latLng);
    form2.mapMarker.setLatLng(latLng);
  }

  function hideForm2Map() {
    form2.$map.removeClass('show');
  }

  function initForm2DistrictSelect() {
    form2.$districtSelect.select2({
      minimumResultsForSearch: Infinity,
      ajax: {
        url: getApiUrl(`/${$('html').attr('lang')}/v1/districts`),
        headers: {
          'Authorization': getApiAuthToken(),
        },
        dataType: 'json',
        processResults: function(response) {
          return {
            results: response.results.map((item)=>({
              id: item.id,
              text: `${(getCurrentLang() === 'ru') ? item.name_ru + ' район' : (getCurrentLang() === 'oz' )? item.name_oz+' тумани' : item.name_uz+ ' tumani'}`
            }))
          };
        }
      }
    });
    form2.$districtSelect.on('select2:select', function(e) {
      var selectedData = e.params.data;
      if (form2.districtId !== null && selectedData.id !== form2.districtId) {
        form2.streetType = null;
        form2.streetId = null;

        form2.$streetTypeSelect.val(null).trigger('change');
        form2.$streetSelect.val(null).trigger('change');
        form2.$houseSelect.prop('disabled', true).val(null).trigger('change');
        form2.$communityInput.val('');

        hideForm2Map();
      } else {
        form2.$streetTypeSelect.prop('disabled', false);
        form2.$streetSelect.prop('disabled', false);
      }

      form2.districtId = selectedData.id;
    });
  }

  function initForm2StreetTypeSelect() {
    form2.$streetTypeSelect.on('select2:select', function(e) {
      var selectedData = e.params.data;

      form2.streetType = selectedData.id;
      form2.streetId = null;

      form2.$streetSelect.val(null).trigger('change');
      form2.$houseSelect.prop('disabled', true).val(null).trigger('change');
      form2.$communityInput.val('');

      hideForm2Map();
    });
  }

  function initForm2StreetSelect() {
    form2.$streetSelect.select2({
      minimumInputLength: 1,
      ajax: {
        delay: 1000,
        url: getApiUrl(`/${$('html').attr('lang')}/v1/streets`),
        headers: {
          'Authorization': getApiAuthToken(),
        },
        dataType: 'json',
        data: function(params) {
          var data = {
            district_id: form2.districtId,
            q: params.term
          };

          if (form2.streetType) {
            data.type = form2.streetType;
          }

          return data;
        },

        processResults: function(response) {
          return {
            results: response.results.map( (item) => ({
              id: item.id,
              text:`${(getCurrentLang() === 'ru') ? item.full_name_ru : (getCurrentLang() === 'oz' )? item.full_name_oz : item.full_name_uz}`
            }))
          };
        }
      }
    });

    form2.$streetSelect.on('select2:select', function(e) {
      form2.$houseSelect.prop('disabled', false);

      var selectedData = e.params.data;

      if (form2.streetId !== null && selectedData.id !== form2.streetId) {
        form2.$houseSelect.val(null).trigger('change');
        form2.$communityInput.val('');

        hideForm2Map();
      } else {
        form2.$houseSelect.prop('disabled', false);
      }

      form2.streetId = selectedData.id;
    });
  }

  function initForm2HouseSelect() {
    form2.$houseSelect.select2({
      minimumInputLength: 1,
      ajax: {
        delay: 1000,
        url: getApiUrl(`/${$('html').attr('lang')}/v1/houses`),
        headers: {
          'Authorization': getApiAuthToken(),
          'Accept-Language': getCurrentLang()
        },
        dataType: 'json',
        data: function(params) {
          return {
            street_id: form2.streetId,
            q: params.term
          };
        },
        processResults: function(response) {
          return {
            results: response.results.map((item) => ({
            id: item.id,
            text: item.number,
            details: item
          }))
          }
        }
      }
    });

    form2.$houseSelect.on('select2:select', function(e) {
      var selectedData = e.params.data;
      if (selectedData.details.community !== undefined) {
        form2.$communityInput.val(`${(getCurrentLang() === 'ru') ? selectedData.details.community.name_ru : (getCurrentLang() === 'oz' ) ? selectedData.details.community.name_oz : selectedData.details.community.name_uz}`);
      }

      showForm2Map([
        parseFloat(selectedData.details.latitude),
        parseFloat(selectedData.details.longitude)
      ]);
    });
  }


  $(document).ready(function() {
    initSelect2();

    initForm1();

    initForm2();

  });
})(jQuery);