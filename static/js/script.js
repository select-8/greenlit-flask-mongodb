$(document).ready(function () {
    //variable should be cached for performance
    const p = $("#content");
    p.hide();
    $("#drop-down").click(function () {
        p.slideToggle("slow");
    });
});