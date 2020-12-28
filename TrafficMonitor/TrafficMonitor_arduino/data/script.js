function init() {
    $('#config').hide();
    $('#nextstep').hide();
    $('#alert-text').hide();

    $('#save-button').click(onSaveButtonClicked);
    $('#password').keypress(onKeyPressed);

    $('#networks-list-select').attr('disabled', true);
    $('#password').attr('disabled', true);

    $.getJSON('/yoyo/credentials', function (json) {
        $('#config').show();
        configure(json);
    });
}

function configure(json) {
    $('#config').show();

    console.log(json);

    populateNetworksList("");
}

function onKeyPressed(event) {
    if (event.keyCode == 13) {
        onSaveButtonClicked(event);
    }
}

function populateNetworksList(selectedNetwork) {
    let networks = $('#networks-list-select');

    $.getJSON('/yoyo/networks', function (json) {
        networks.empty();
        $.each(json, function (key, entry) {
            let network = $('<option></option>');

            network.attr('value', entry.SSID).text(entry.SSID);
            if(entry.SSID == selectedNetwork) network.attr('selected', true);

            networks.append(network);
        });

        if($('#networks-list-select option').length > 0) {
            $('#networks-list-select').attr('disabled', false);
            $('#password').attr('disabled', false);
        }
        else {
            networks.append('<option>No Networks Found</option>');
            setTimeout(populateNetworksList, 10000);
        }
    });
}

function onSaveButtonClicked(event) {
    event.preventDefault();

    var data = {
        ssid: $('#networks-list-select').children("option:selected").val(),
        password: $('#password').val()
    };

    //NB dataType is 'text' otherwise json validation fails on Safari
    $.ajax({
        type: "POST",
        url: "/yoyo/credentials",
        data: JSON.stringify(data),
        dataType: 'text',
        contentType: 'application/json; charset=utf-8',
        cache: false,
        timeout: 15000,
        async: false,
        success: function(response, textStatus, jqXHR) {
            console.log(response);
            $('#config').hide();
            $('#alert-text').show();
            $('#alert-text').removeClass('alert-danger');
            $('#alert-text').addClass('alert-success');
            $('#alert-text').text('Saved');
            $('#nextstep').show();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
            $('#alert-text').show();
            $('#alert-text').addClass('alert-danger');
            $('#alert-text').text('Couldn\'t Save');
        }
    });
}