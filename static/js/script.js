$(document).ready(function () {
// unique id is made for contant divs and dropdown buttons in Jinja Loop
// (given type) + <ObjectId>
    function togglePitchDiv() {
        $('.drop_down').click(function () {
            var currentId = $(this).attr("id");
            var flaskMade = currentId.replace("down-drop-", "");
            $('#content-' + flaskMade).slideToggle("slow");
            return false;
    
        });
    };

    const p = $(".panel");
    p.hide();
    togglePitchDiv()

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })
});
