var express = require('express');
var router = express.Router();
var formidable = require('formidable');
var fs = require('fs');
var http = require('http');
var util = require('util');
var csv = require('csv-parser');
var Chart = require('chart.js');
var spawn = require('child_process').spawn;
require('should');

const lib = require('lib');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { 
      num_graphs: 1, 
      labels: [[]], 
      points: [[]], 
      saved:  [],
      lines:  [[]],
      titles: ['Your Data Here'] 
  });
});

/* Helper functions to generate battery threshold. */
var generate_lines = (labels, value) => {
  var output = [];
  for (var i = 0; i < labels.length; i++) {
      output.push(fill_array(value, labels[i].length));
  }
  return output;
};
var fill_array = (value, length) => {
  var output = [];
  for (var i = 0; i < length; i++) {
      output.push(value);
  }
  return output;
};

/* POST home page. */
router.post('/', function(req, res, next) {
  var form = new formidable.IncomingForm();
  var upload_path = __dirname.replace('/routes', '/uploads/');
  var csv_path = "";
  var split_by = "month";
  form.parse(req);

  // Form handlers
  form.on('fileBegin', function(name, file) {
      file.path = upload_path + file.name;
      csv_path = file.path;
  });
  form.on('file', function(name, file) {
      console.log('Uploaded ' + file.name);
  });
  form.on('field', function(name, value) {
      if (name === 'time-type') {
          split_by = value;
      }
  });
  form.on('end', function() {
      var pythonProcess = spawn('python', ['dummy.py', csv_path]);
      pythonProcess.stdout.on('data', function(data) {
          new_path = data.toString().trim();
          console.log(new_path);
          display_data(new_path);
      });
  });

  // Function called to display data from csv file
  var display_data = (load_path) => {
      var labels = []; var points = []; var saveds = [];
      fs.createReadStream(load_path) // Read local csv file
        .pipe(csv())
        .on('data', function(data) {
            var row = Object.keys(data);
            if (row.length == 3) {
                [label, point, saved] = row;
                labels.push(data[label]);
                points.push(parseFloat(data[point]));
                saveds.push(parseFloat(data[saved]));
            } else {
                [label, point] = row;
                labels.push(data[label]);
                points.push(parseFloat(data[point]));
            }
        })
        .on('end', function() {
            // Make chart from data
            if (split_by === 'year') {
                lib.cherry.treehax['@dev'].split_year(labels, points, saveds, split_callback);
            } else if (split_by === 'month') {
                lib.cherry.treehax['@dev'].split_month(labels, points, saveds, split_callback);
            } else {
                lib.cherry.treehax['@dev'].split_day(labels, points, saveds, split_callback);
            }
        });
  };
  // Callback function to split graphs
  var split_callback = (err, result) => {
      if (err) {
          console.log(err);
      } else {
          var lines = generate_lines(result.labels, 338);
          res.render('index', { 
              num_graphs: result.count,
              labels: result.labels, 
              points: result.points,
              saved:  result.saved,
              lines:  lines,
              titles: result.titles
          });
      }
  };

});

module.exports = router;
