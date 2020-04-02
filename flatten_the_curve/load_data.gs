function load_all() {
  load_country('nl')
  load_country('it')
  load_country('cn')
  load_country('be')
  load_country('de')
  load_country('wereld')
  load_hosp_nl()
  
  set_last_update('Main','a2')
}

function set_last_update(sheetname,cell_position) {
  var spreadsheet = SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/.../');
  var sheet = spreadsheet.getSheetByName(sheetname);
  var cell = sheet.getRange(cell_position);
  cell.setValue('Laatst bijgewerkt: '+new Date());
}

function load_country(c) {
  Logger.log('Fetching '+ c)

  var query = 'SELECT * FROM '+ c +' c ORDER BY c.report_date ASC'
  if (c != 'wereld') {
    c = c.toUpperCase()
  }
  var sheetname = 'Data '+c.toUpperCase()

  fetch_mysql_data(query,sheetname)

  Logger.log('Fetched '+ c)
}

function load_hosp_nl() {
  Logger.log('Fetching hosp NL')
  
  var query = 'SELECT c.report_date AS Datum,ch.Aantal,cp.Nieuw,cp.Groeifactor \
  FROM covid c \
LEFT JOIN `covid_hosp_nl` ch \
    ON c.report_date = ch.Datum \
LEFT JOIN covid_hosp_nl_prep cp \
    ON ch.Datum = cp.Datum \
 WHERE c.country_region = "Netherlands" \
   AND (c.province_state IS NULL OR c.province_state = "Netherlands" ) \
  ORDER BY c.report_date'
    
  var sheetname = 'Data hosp NL'
  
  fetch_mysql_data(query,sheetname)
  
  Logger.log('Fetched hosp NL')
}

function fetch_mysql_data(query,sheetname) { 
  
  var conn = Jdbc.getConnection('jdbc:mysql://ip:3306/db', 'user', 'passwd');
  
  var stmt = conn.createStatement();
  var start = new Date(); // Get script starting time
  
  stmt.setQueryTimeout(30);
  var rs = stmt.executeQuery(query);

  var spreadsheet = SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/.../');
  var sheet = spreadsheet.getSheetByName(sheetname);
  sheet.clear();
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