document.addEventListener('DOMContentLoaded', function () {
    const macAddressInput = document.getElementById('mac_address');
    if (macAddressInput) {
        macAddressInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/[^a-fA-F0-9]/g, '');
            let formattedValue = '';
            for (let i = 0; i < value.length; i += 2) {
                if (i > 0) formattedValue += ':';
                formattedValue += value.substr(i, 2);
            }
            e.target.value = formattedValue;
        });
    }
});

function formatIPAddress(input) {
    let value = input.value.replace(/[^0-9]/g, '');
    let formattedValue = '';
    for (let i = 0; i < value.length; i++) {
        if (i > 0 && i % 3 === 0 && formattedValue.split('.').length < 4) {
            formattedValue += '.';
        }
        formattedValue += value[i];
    }
    input.value = formattedValue;

    // IP validation
    const ipParts = formattedValue.split('.');
    if (ipParts.length === 4 && ipParts.every(part => part >= 0 && part <= 255 && part.length <= 3)) {
        input.setCustomValidity('');
    } else {
        input.setCustomValidity('Invalid IP address');
    }
}
