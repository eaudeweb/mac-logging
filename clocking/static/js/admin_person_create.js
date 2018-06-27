$('#admin_add_user_form').on("submit", function (event) {
    event.preventDefault();
    $.ajax({
        url: "/admin_add_user",
        type: "POST",
        data: {
            email: $('#email').val(),
            password: $('#password').val(),
            confirm_password: $('#confirm_password').val()
        },
        success : function(data) {
            if (data['status'] == 'error') {
                $('#user_form_errors').html(data['html']);
            }
            else {
                $('#admin_user').html(data['html']);
            }
        }
    });
});

$('#admin_add_person_form').on("submit", function (event) {
    event.preventDefault();
    $.ajax({
        url: "/admin_add_person",
        type: "POST",
        data: {
            last_name: $('#last_name').val(),
            first_name: $('#first_name').val(),
            dept: $('#dept option:selected').val(),
            user_id: $('#user_id').val()
        },
        success : function(data) {
            if (data['status'] == 'error') {
                $('#person_form_errors').html(data['html']);
            }
            else {
                $('#add_mac_address_button').bind('click', add_mac_address);
                $('#admin_create_person').html(data['html']);
            }
        }
    });
});

function add_mac_address() {
  $('#mac_address').toggle();
}

function submit_mac_address(event) {
    event.preventDefault();
    $.ajax({
        url: "/add_mac",
        type: "POST",
        data: {
            mac: $('#mac').val(),
            device: $('#device option:selected').val(),
            person: $('#person_id').val(),
            priority: $('#priority option:selected').val()

        },
        success : function(data) {
            if (data['status'] == 'error') {
                $('#mac_form_errors').html(data['html']);
            }
            else  {
                $('#mac_listing').append(data['html']);
                $('#mac_form_errors').html("");
                $('#mac_address').toggle();
                $('#mac').val("");
            }
        }
    });
};

$('#add_mac_address_button').bind('click', add_mac_address);

$('#post_add_mac_form').bind('submit', submit_mac_address);

function toggle_edit() {
    $('#post_edit_person_form').toggle();
    $('#person_details').toggle();
}

$('#toggle_edit_person').bind('click', toggle_edit);

function post_edit_person(event) {
    event.preventDefault();

    var person_id = $('#post_edit_person_form').data('person-id');
    $('#dept option:selected').val();

    $.ajax({
        url: "/admin_edit/" + person_id,
        type: "POST",
        data: {
            last_name: $('#last_name').val(),
            first_name: $('#first_name').val(),
            dept: $('#dept option:selected').val()
        },
        success : function(data) {
            if (data['status'] == 'error') {
                $('#person_form_errors').html(data['html']);
            }
            else {
                $('#post_edit_person_form').toggle();
                $('#person_details').toggle();
                $('#person_edit_container').html(data['html']);
                $('#toggle_edit_person').bind('click', toggle_edit);
                $('#post_edit_person_form').bind('submit', post_edit_person);
            }
        }
    });
}

$('#post_edit_person_form').bind('submit', post_edit_person);
