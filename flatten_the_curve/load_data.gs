// google script to load data to a google spreadsheet

function load_all() {
  load_nl()
  load_it()
  load_wereld()
}

function load_nl() {
  Logger.log('Fetching NL')
  
  var query = 'SELECT * FROM covid WHERE country_region = "Netherlands" AND province_state IS NULL ORDER BY report_date ASC'
  var sheetname = 'Data NL'
  
  fetch_mysql_data(query,sheetname)
  
  Logger.log('Fetched NL')
}

function load_it() {
  Logger.log('Fetching IT')
  
  var query = 'SELECT * FROM covid WHERE country_region = "Italy" ORDER BY report_date ASC'
  var sheetname = 'Data IT'
  
  fetch_mysql_data(query,sheetname)
  
  Logger.log('Fetched IT')
}

function load_wereld() {
  Logger.log('Fetching wereld')
  
  var query = 'SELECT "aggregate" AS file,report_date,NULL AS fips,NULL AS city,NULL AS province_state,"wereld" AS country_region,NULL AS last_update,NULL AS lat,NULL AS lon,sum(confirmed) AS confirmed,sum(death) AS death,sum(recovered) AS recovered,sum(active) AS active,NULL AS combined_key FROM covid GROUP BY report_date ORDER BY report_date ASC'
  var sheetname = 'Data wereld'
  
  fetch_mysql_data(query,sheetname)
  
  Logger.log('Fetched wereld')
}

function fetch_mysql_data(query,sheetname) { 
  
  var conn = Jdbc.getConnection('jdbc:mysql://ipaddress:3306/database', 'user', 'passwd'); // hostname doesn't work, use IP

  var stmt = conn.createStatement();
  var start = new Date(); // Get script starting time
  
  var rs = stmt.executeQuery(query); // It sets the limit of the maximum nuber of rows in a ResultSet object

  var spreadsheet = SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/..../');
  //var doc = SpreadsheetApp.getActiveSpreadsheet(); // Returns the currently active spreadsheet
  var sheet = spreadsheet.getSheetByName(sheetname);
  sheet.clear();
  //SpreadsheetApp.setActiveSheet(doc.getSheets()[sheetnum]);
  var cell = sheet.getRange('a1');
  var row = 0;
  var getCount = rs.getMetaData().getColumnCount(); // Mysql table column name count.
  
  for (var i = 0; i < getCount; i++){  
     cell.offset(row, i).setValue(rs.getMetaData().getColumnName(i+1)); // Mysql table column name will be fetch and added in spreadsheet.
  }  
  
  var row = 1; 
  while (rs.next()) {
    for (var col = 0; col < rs.getMetaData().getColumnCount(); col++) { 
      cell.offset(row, col).setValue(rs.getString(col + 1)); // Mysql table column data will be fetch and added in spreadsheet.
    }
    row++;
  }
  
  rs.close();
  stmt.close();
  conn.close();
  var end = new Date(); // Get script ending time
  Logger.log('Time elapsed: ' + (end.getTime() - start.getTime())); // To generate script log. To view log click on View -> Logs.
}