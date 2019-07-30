var titles = document.getElementsByClassName('title')
for (var i = 0; i < titles.length; i++) {
    console.log(titles[i].innerHTML)
}


$('#rating_sort').on("click", function () {
    reorderMyData();
});

var reorderMyData = function () {
    var order = get_ratings_and_sort
    // https://stackoverflow.com/questions/929519/dynamically-arranging-divs-using-jquery
    var div = $("#make-reorderable-by-rating");
    var children = div.children();
    div.empty();
    for (var i = 0; i < order.length; i++) {
        div.append(children[order[i]])
    }
}

var div = $("#make-reorderable-by-rating");
var children = div.children();
console.log(children)


// http://jsfiddle.net/bittu4u4ever/ezYJh/1/
var divList = $(".listing-item");
divList.sort(function (a, b) {
    return $(a).data("listing-price") - $(b).data("listing-price")
});

$("#list").html(divList);