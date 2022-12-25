function requestForCount(input = false, reset = false) {
    var data = { "name": input.name, "value": input.value };
    const domain = location.protocol + '//' + location.host

    var url = domain + "/restauracje/licznik_restauracji_dla_filtrow/";
    if (input) {
        url = url + "?" + input.name + "=" + input.value + "&checked=" + input.checked;
    }
    if (reset) {
        url = url + "?reset=true";
    }
    fetch(url,
        {
            method: 'get',
        }
    )
        .then(response => response.json())
        .then(data => {
            var restaurants_count = document.getElementById('restaurants_count');
            restaurants_count.textContent = "(" + data.count + ")"
        })
};

function createSpanInfo(text) {
    const addressInfo = document.createElement('span');
    addressInfo.textContent = text;
    addressInfo.classList.add("text-left", "text-red", "text-bold", "w-100", "margin-t-10", "margin-b-10", "container-text");
    return addressInfo
}

function createAddressItem(data) {
    const addressItem = document.createElement('a');
    addressItem.classList.add("address_item", "text-left", "text-grey", "w-100", "flex", "no-wrap", "j-left", "a-center", "container-text", "margin-t-10", "margin-b-10", "pointer", "result-item", "border-r");
    addressItem.textContent = data.display_name;
    addressItem.href = '?sorted=distance&lon=' + data.lon + '&lat=' + data.lat + '&place_name=' + data.display_name;
    return addressItem
}

function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var longitude = position.coords.longitude;
            var latitude = position.coords.latitude;
            var url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`;

            const resultsBox = document.getElementById('results-box');
            const resultsList = document.getElementById('results-list');

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data) {
                        resultsBox.style.display = 'Flex';
                        resultsList.innerHTML = '';

                        var addressInfo = createSpanInfo("Pobrano lokalizację automatyczie:");
                        var addressItem = createAddressItem(data);

                        resultsList.appendChild(addressInfo);
                        resultsList.appendChild(addressItem);
                    } else {
                        resultsBox.style.display = 'None';
                        resultsList.innerHTML = '';
                    }
                });
        });
    } else {
        return false;
    }
}

function sendRequestForLocation(inputField) {
    const resultsBox = document.getElementById('results-box');
    const resultsList = document.getElementById('results-list');

    inputField.addEventListener('keyup', function (event) {
        if (event.key === ' ' || event.key === 'Enter') {
            const address = inputField.value;
            const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(address)}&countrycodes=pl&limit=10&format=json&sort=asc&addressdetails=1`;

            const address_arr = address.split(' ');

            if (address_arr.length >= 2) {
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        if (data.length >= 1) {
                            resultsBox.style.display = 'Flex';
                            resultsList.innerHTML = '';

                            var addressInfo = createSpanInfo("Pobrano listę lokalizacji");
                            resultsList.appendChild(addressInfo);
                            
                            data.forEach(item => {
                                var addressItem = createAddressItem(item);
                                resultsList.appendChild(addressItem);
                            });
                        } else {
                            resultsBox.style.display = 'Flex';
                            resultsList.innerHTML = '';

                            var addressInfo = createSpanInfo("Brak wyników. Spróbuj wpisać inną frazę.");
                            resultsList.appendChild(addressInfo);
                        }
                    });
            } else {
                resultsBox.style.display = 'None';
                resultsList.innerHTML = '';
            }
        }
        if ((inputField.value).length == 0) {
            resultsBox.style.display = 'None';
            resultsList.innerHTML = '';
        }
    });
}

function searchLocation(location = false) {
    const inputField = document.getElementById('address-input');

    inputField.addEventListener('focus', function (event) {
        var location = getUserLocation();
    });
    sendRequestForLocation(inputField)
}



function clearFilters(clear_button) {
    var all_inputs = document.querySelectorAll('input.filter_sorted:checked');
    all_inputs.forEach((element) => {
        element.checked = 0;
        document.getElementById("filters_counter").innerHTML = "(0)";
        var parent = element.parentNode;
        parent.querySelector('span.filter_sorted').style.color = '#2F313E';
    });
    requestForCount(input = false, reset = true);
}

function filtersCounter(element) {

    var input = element.querySelector('input');
    var label = element.querySelector('span.filter_sorted');
    if (input.checked) {
        input.checked = 0
        label.style.color = "black";
    } else {
        input.checked = 1
        label.style.color = "#CA001C";
    }

    requestForCount(input);

    var all_inputs = document.querySelectorAll('input.filter_sorted:checked');
    var count = all_inputs.length;
    document.getElementById("filters_counter").innerHTML = "(" + count + ")";
}

function addToBasket(food) {

    sessionStorage.setItem('scrollpos', window.scrollY);

    var main = document.getElementById('main');
    var freeze__container = document.getElementById('freeze__container');
    var basket = document.getElementById('basekt_popup');
    main.classList.add('freeze');
    freeze__container.classList.add('active');
    basket.classList.add('active');

    var product_in_basket = document.getElementById("product_in_basket");
    var product_id = (food.id).replace("product_id_", "");

    product_in_basket.value = product_id;

    var srcset = document.getElementById("srcset_basket");
    var srcset_input = document.getElementById("srcset_basket_" + product_id);
    srcset.srcset = srcset_input.value;

    var src = document.getElementById("src_basket");
    var src_input = document.getElementById("src_basket_" + product_id);
    src.src = src_input.value;

    var product_name = document.getElementById("product_name");
    var product_name_input = document.getElementById("product_name_" + product_id);
    product_name.innerHTML = product_name_input.value;

    var product_price = document.getElementById("product_price");
    var product_price_input = document.getElementById("product_price_" + product_id);
    product_price.innerHTML = product_price_input.value;
}

function closeBasket(x_close) {
    var main = document.getElementById('main');
    var basket = document.getElementById('basekt_popup');
    var freeze__container = document.getElementById('freeze__container');
    main.classList.remove('freeze');
    basket.classList.remove('active');
    freeze__container.classList.remove('active');

    var scrollpos = sessionStorage.getItem('scrollpos');
    if (scrollpos) {
        window.scrollTo(0, scrollpos);
        sessionStorage.removeItem('scrollpos');
    }
}

function addOneQty(plus) {
    var food_qty = document.getElementById('food_qty');
    var qty = parseInt(food_qty.value);
    food_qty.value = qty + 1;

    var product_in_basket = document.getElementById("product_in_basket");
    var product_price_input = document.getElementById("product_price_" + product_in_basket.value);
    var product_price = document.getElementById("product_price");
    product_price.innerHTML = (food_qty.value * product_price_input.value).toFixed(2);
}

function remOneQty(plus) {
    var food_qty = document.getElementById('food_qty');
    var qty = parseInt(food_qty.value);
    if (qty > 1) {
        food_qty.value = qty - 1;
    } else {
        food_qty.value = 1;
    }

    var product_in_basket = document.getElementById("product_in_basket");
    var product_price_input = document.getElementById("product_price_" + product_in_basket.value);
    var product_price = document.getElementById("product_price");
    product_price.innerHTML = (food_qty.value * product_price_input.value).toFixed(2);
}

const inputSearchField = document.getElementById('inputSearchField');
const submitButton = document.getElementById('submitButton');

if (inputSearchField) {
    inputSearchField.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            submitButton.click();
        }
    });
}

window.addEventListener("DOMContentLoaded", function () {
    searchLocation();
    
    var all_inputs = document.querySelectorAll('input.filter_sorted:checked');
    var count = all_inputs.length;
    var filters_counter = document.getElementById("filters_counter");
    filters_counter.innerHTML = "(" + count + ")";
});
