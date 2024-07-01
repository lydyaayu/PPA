$(document).ready(function () {
    get_posts("{{user_info2.username}}");
});
function sign_out() {
    $.removeCookie("mytoken", { path: "/" });
    alert("Signed out!");
    window.location.href = "/login";
}
// Kegiatan Hari ini
$(document).ready(function () {
    checkAndClearActivities();
});
function checkAndClearActivities() {
    let lastAccessDate = localStorage.getItem('lastAccessDate');
    let currentDate = new Date().toISOString().split('T')[0]; // Get current date in YYYY-MM-DD format

    if (lastAccessDate !== currentDate) {
        localStorage.setItem('lastAccessDate', currentDate);
        clearActivities();
    }
}
function clearActivities() {
    $.ajax({
        type: "POST",
        url: "/clear_activities",
        success: function (response) {
            alert(response["msg"]);
            show_act();
        },
        error: function (xhr, status, error) {
            console.error('Error clearing activities:', error);
            alert('Error clearing activities');
        }
    });
}

$(document).ready(function () {
    show_act();
});
function show_act() {
    $('#act-list').empty();
    $.ajax({
        type: "GET",
        url: "/act",
        data: {},
        success: function (response) {
            let rows = response['acts'];
            for (let i = 0; i < rows.length; i++) {
                let act = rows[i]['act'];
                let num = rows[i]['num'];
                let done = rows[i]['done'];

                let temp_html = '';
                if (done === 0) {
                    temp_html = `
                    <li class="fs-5">
                        <h2>${act}</h2>
                        <button onclick="done_act(${num})" type="button" class="btn btn-primary">Selesai</button>
                        <button onclick="delete_act(${num})" type="button" class="btn btn-danger btn-delete" style="margin-left: 10px;">Hapus</button>
                    </li>
                    `;
                } else {
                    temp_html = `
                    <li>
                        <h2 class="done">✅ ${act}</h2>
                        <button onclick="delete_act(${num})" type="button" class="btn btn-danger btn-delete" style="margin-left: 10px;">Hapus</button>
                    </li>
                    `;
                }
                $('#act-list').append(temp_html);
            }
        },
        error: function (xhr, status, error) {
            console.error('Error fetching activities:', error);
            alert('Error fetching activities');
        }
    });
}

function save_act() {
    let act = $('#act').val();
    $.ajax({
        type: "POST",
        url: "/act",
        data: { act_give: act },
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        },
        error: function (xhr, status, error) {
            console.error('Error saving activity:', error);
            alert('Error saving activity');
        }
    });
}

function done_act(num) {
    $.ajax({
        type: "POST",
        url: "/act/done",
        data: { num_give: num },
        success: function () {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            console.error('Error marking activity as done:', error);
            alert('Error marking activity as done');
        }
    });
}

function delete_act(num) {
    $.ajax({
        type: "POST",
        url: "/delete",
        data: { num_give: num },
        success: function (response) {
            alert(response["msg"]);
            show_act();
        },
        error: function (xhr, status, error) {
            console.error('Error deleting activity:', error);
            alert('Error deleting activity');
        }
    });
}

// Kegiatan Minggu Ini
$(document).ready(function () {
    show_act_week();
});
function show_act_week() {
    $('#act-week-list').empty();
    $.ajax({
        type: "GET",
        url: "/act_week",
        data: {},
        success: function (response) {
            let rows = response['acts_week']
            for (let i = 0; i < rows.length; i++) {
                let act_week = rows[i]['act_week'];
                let num = rows[i]['num'];
                let done = rows[i]['done'];

                let temp_html = '';
                if (done === 0) {
                    temp_html = `
                    <li>
                        <h2>${act_week}</h2>
                        <button onclick="done_act_week(${num})" type="button" class="btn btn-primary">Selesai</button>
                        <button onclick="delete_act_week(${num})" type="button" class="btn btn-danger btn-delete" style="margin-left: 10px;">Delete</button>
                    </li>
                    `;
                } else {
                    temp_html = `
                    <li>
                        <h2 class="done">✅ ${act_week}</h2>
                        <button onclick="delete_act_week(${num})" type="button" class="btn btn-danger btn-delete" style="margin-left: 10px;">Delete</button>
                    </li>
                    `;
                } $('#act-week-list').append(temp_html);
            }
        }
    });
}
function save_act_week() {
    let act = $('#act-week').val();
    $.ajax({
        type: "POST",
        url: "/act_week",
        data: { act_week_give: act },
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    });
}
function done_act_week(num) {
    $.ajax({
        type: "POST",
        url: "/act_week/done",
        data: { num_give: num },
        success: function () {
            window.location.reload();
        }
    });
}
function delete_act_week(num) {
    $.ajax({
        type: "POST",
        url: "/delete_week",
        data: { num_give: num },
        success: function (response) {
            alert(response["msg"]);
            show_act_week();
        }
    });
}

// Note
$(document).ready(function () {
    show_note();
});
function show_note() {
    $('#note-list').empty();
    $.ajax({
        type: "GET",
        url: "/note",
        data: {},
        success: function (response) {
            let rows = response['notes']
            for (let i = 0; i < rows.length; i++) {
                let note = rows[i]['note'];
                let num = rows[i]['num'];
                let done = rows[i]['done'];

                let temp_html = '';
                if (done === 0) {
                    temp_html = `
                    <li>
                        <h2>${note}</h2>
                        <button onclick="done_note(${num})" type="button" class="btn btn-primary">Selesai</button>
                        <button onclick="delete_note(${num})" type="button" class="btn btn-danger btn-delete" style="margin-left: 10px;">Delete</button>
                    </li>
                    `;
                } else {
                    temp_html = `
                    <li>
                        <h2 class="done">✅ ${note}</h2>
                        <button onclick="delete_note(${num})" type="button" class="btn btn-danger btn-delete" style="margin-left: 10px;">Delete</button>
                    </li>
                    `;
                } $('#note-list').append(temp_html);
            }
        }
    });
}
function save_note() {
    let note = $('#note').val();
    $.ajax({
        type: "POST",
        url: "/note",
        data: { note_give: note },
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    });
}
function done_note(num) {
    $.ajax({
        type: "POST",
        url: "/note/done",
        data: { num_give: num },
        success: function () {
            window.location.reload();
        }
    });
}
function delete_note(num) {
    $.ajax({
        type: "POST",
        url: "/delete_note",
        data: { num_give: num },
        success: function (response) {
            alert(response["msg"]);
            show_note();
        }
    });
}
