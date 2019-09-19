var parse = require('csv-parse')
var moment = require('moment')
var fs = require('fs')

var data_original = []
var data_smoothed = []
var data_24hr = []

var data_forecast = []

var parser = parse({delimiter: ','}, function(err, data){
    for (var i = 0; i < data.length; i++) {
        var d = data[i]
        var millis = d[0]
        data_original.push([moment(d[0]).valueOf(), d[1]])
        data_smoothed.push([moment(d[0]).valueOf(), d[2]])
        data_24hr.push([moment(d[0]).valueOf(), d[3]])
    }

    var d = {
        'values': [data_original, data_smoothed, data_24hr],
        'names': ['Original Power Consumption', "Smoothed Power Consumption", "Smoothed Power Consumption (24h)"],
        'colors': ['red', 'green', 'orange']
    }

    fs.writeFile('./data.js', JSON.stringify(d))
});

var parser2 = parse({delimiter: ','}, function(err, data){
    for (var i = 0; i < data.length; i++) {
        var d = data[i]
        data_forecast.push([moment(d[0]).valueOf(), d[1]])
    }

    var d = {
        'values': [data_forecast],
        'names': ['Forecasted Power Consumption'],
        'colors': ['red']
    }

    fs.writeFile('./data_forecast.js', JSON.stringify(d))
});

// fs.createReadStream(__dirname+'/january.csv').pipe(parser);
fs.createReadStream(__dirname+'/prediction.csv').pipe(parser2);
