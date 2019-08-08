$(document).ready(function () {

    function togglePitchDiv() {
        $('.drop_down').click(function () {
            var currentId = $(this).attr("id");
            var flaskMade = currentId.replace("down-drop-", "");
            var pDiv = '#content-' + flaskMade
            $('#content-' + flaskMade).slideToggle("slow");
            pDiv.scrollIntoView();
        });
    };

    const p = $(".panel");
    p.hide();
    togglePitchDiv()

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
});
