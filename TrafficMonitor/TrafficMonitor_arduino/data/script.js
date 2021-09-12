var maxWifiNetworks = 5;
var peers = [];

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
    }).fail(function() {
        $('#alert-text').show();
        $('#alert-text').addClass('alert-danger');
        $('#alert-text').text('Error');
    });
}

function configure(json) {
    $('#config').show();

    console.log(json);

    populateNetworksList();
    populatePeersList();
}

function onKeyPressed(event) {
    if (event.keyCode == 13) {
        onSaveButtonClicked(event);
    }
}

function populateNetworksList(selectedNetwork) {
    let networks = $('#networks-list-select');

    $.getJSON('/yoyo/networks', function (json) {
        if(json.length > 0) {
            networks.empty();
            //Order the networks by signal strength and limit to top n
            json = json.sort((a, b) => parseInt(b.RSSI) - parseInt(a.RSSI));
            var ssidList = json.slice(0, maxWifiNetworks).map(i => {
                return i.SSID;
            });

            //The selected network will always remain:
            if(selectedNetwork && !ssidList.includes(selectedNetwork)) ssidList.push(selectedNetwork); 

            $.each(ssidList, function (key, entry) {
                let network = $('<option></option>');

                network.attr('value', entry).text(entry);
                if(entry == selectedNetwork) network.attr('selected', true);

                networks.append(network);
            });

            $('#networks-list-select').attr('disabled', false);
            $('#password').attr('disabled', false);
        }
        
        if($('#networks-list-select option').length == 0) {
            networks.append('<option>No Networks Found</option>');
        }

        setTimeout(function() {
            populateNetworksList($('#networks-list-select').children("option:selected").val());
        }, 10000);
    });
}

function populatePeersList() {
    $.getJSON('/yoyo/peers', function (json) {
        if(json.length > 0) {
            var newPeers = json.map(i => { return i.IP;});
            newPeers.forEach(ip => { if(!peers.includes(ip)) addPeer(ip); });
            peers.forEach(ip => { if(!newPeers.includes(ip)) removePeer(ip); });

            peers = newPeers;
        }
    });

    setTimeout(function() {
        populatePeersList();
    }, 15000);
}

function addPeer(ip) {
    console.log("addPeer > " + ip);

    let peersListDiv = $('#peers-list');

    let span = $('<span></span>');
    span.attr('id', ip);

    let image = $('<img></img>');
    image.attr('class', 'peer-image');
    image.attr('src', "http://" + ip + "/icon.svg");

    peersListDiv.append(span);
    span.append(image);
}

function removePeer(ip) {
    console.log("removePeer > " + ip);

    $('span[id="' + ip + '"]').remove();
}

function onSaveButtonClicked(event) {
    event.preventDefault();

    var data = {
        ssid: $('#networks-list-select').children("option:selected").val(),
        password: $('#password').val()
    };

    var request = {
        type: "POST",
        url: "/yoyo/credentials",
        data: JSON.stringify(data),
        dataType: 'json',
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
    }

    //json validation fails on Safari - but if defaults to text then fails on Windows/Android
    if (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1 && navigator.userAgent.indexOf('Chromium') == -1) {
        request.dataType = 'text';
    }

    $.ajax(request);
}