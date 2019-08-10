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
    show_genres_pie(ndx);
    remove_empty_bins();

    dc.renderAll();

    function remove_empty_bins(source_group) {
        return {
            all: function () {
                return source_group.all().filter(function (d) {
                    return d.value != 0;
                });
            }
        };
    }

    function show_users(ndx) {
        let user_dim = ndx.dimension(dc.pluck('username'));
        let user_group = user_dim.group();
        //
        // crossfilter should remove null groups from chart
        let filtered_group = remove_empty_bins(user_group);
        let rowchart = dc.rowChart('#user-chart');
        rowchart
            .height(520)
            .width(350)
            .margins({
                top: 30,
                left: 30,
                right: 30,
                bottom: 30
            })
            .elasticX(true)
            .dimension(user_dim)
            .group(filtered_group)
            .colors(d3.scale.category20())
            .xAxis().ticks(5);
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
                bottom: 40,
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


    function show_genres_pie(ndx) {
        let genre_dim = ndx.dimension(dc.pluck('genre_name'));
        let genre_group = genre_dim.group().reduceCount();

        dc.pieChart('#genre-pie')
            .height(630)
            .radius(180)
            .transitionDuration(1500)
            .dimension(genre_dim)
            .group(genre_group)
            .colors(d3.scale.ordinal().range(
                ['#615A4E', '#B58739', '#B2383E', '#FDF6F6', '#808000', '#000075', '#808000', '#911eb4']))
            .legend(dc.legend().x(0).y(10).itemHeight(10).gap(5))
            .on('pretransition', function (chart) {
                chart.selectAll('text.pie-slice').text(function (d) {
                    return dc.utils.printSingleValue((d.endAngle - d.startAngle) / (2 * Math.PI) * 100) + '%';
                });
            });
    }


}