
function add_mac_address() {
    console.log('click')
    $('#mac_address').toggle();
}


function submit_mac_address() {
    event.preventDefault();

    $.ajax({
        url: "/add_mac",
        type: "POST",
        data: {
            mac: $('#mac').val(),
            device: $('#device option:selected').val(),
            person: $('#person_id').val()
        },
        success : function(data) {
            if (data['status'] == 'error') {
                $('#form_errors').html(data['html']);
            }
            else  {
                $('#mac_listing').append(data['html']);
                $('#form_errors').html("");
                $('#mac_address').toggle();
                $('#mac').val("");
            }
        }
    });
};

$('#post_add_person_form').on("submit", function () {
    event.preventDefault();
    console.log('create post is working!');

    $.ajax({
        url: "/add",
        type: "POST",
        data: {
            last_name: $('#last_name').val(),
            first_name: $('#first_name').val()
        },
        // handle a successful response
        success : function(data) {
            if (data['status'] == 'error') {
                $('#form_errors').html(data['html']);
            }
            else {
                $('#person').html(data['html']);
                $('#add_mac_address_button').bind('click', add_mac_address)
                $('#post_add_mac_form').bind('submit', submit_mac_address)
            }
        },
    });
});
