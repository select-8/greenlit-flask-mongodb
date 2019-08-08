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

    // $('.vote_button').click(function () {
    //     var buttId = $(this).attr("id");
    //     var divId = buttId.replace("vote-", "");

    //     $(window).on('load', function () {
    //         var elmnt = document.getElementById(divid)
    //         elmnt.scrollIntoView();
    //     });

    // });

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
});
