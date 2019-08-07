queue()
    .defer(d3.json, "/get_data")
    .await(makeGraphs);

function makeGraphs(error, pitchesData) {
    var ndx = crossfilter(pitchesData);

    pitchesData.forEach(function (d) {
        d.votes = parseInt(d.votes);
    });

    show_users(ndx);
    show_votes_per_user(ndx);

    dc.renderAll();

    function show_users(ndx) {
        let user_dim = ndx.dimension(dc.pluck('username'));
        let user_group = user_dim.group();

        dc.pieChart('#user-pie')
            .height(330)
            .radius(90)
            .transitionDuration(1500)
            .dimension(user_dim)
            .group(user_group);
    }

    function show_votes_per_user(ndx) {
        let user_dim = ndx.dimension(dc.pluck('username'));
        var votes_person = user_dim.group().reduceSum(dc.pluck('votes'));
        console.log(votes_person.top(Infinity))

        dc.barChart("#user-votes-chart")
            .width(300)
            .height(300)
            .margins({
            top: 10,
            right: 50,
            bottom: 30,
            left: 50
            })
            .dimension(user_dim)
            .group(votes_person)
            .transitionDuration(500)
            .x(d3.scale.ordinal())
            .xUnits(dc.units.ordinal)
            .xAxisLabel("User")
            .yAxis().ticks(4);
    }


}

