// Import CSV data to process in app
const fs = require('fs');
var csv = require("fast-csv");

fs.readFile('../output/scored_songs.csv','utf8',function(error,data) {
	
	// Error handling
	if (error) {
		throw error;
	}
	
	//Otherwise, create the necessary data object
	var str = data;
	
	csv
	  .fromString(str, {headers:true})
	  .on("data",function(data) {
	      console.log(data);
	})
	  .on("end",function() {
		  console.log("Imported all data successfully");
	  });
});

