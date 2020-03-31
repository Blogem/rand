function load_all() {
  load_nl()
  load_it()
  load_cn()
  load_wereld()
  load_hosp_nl()
  
  set_last_update('Main','a2')
}

function set_last_update(sheetname,cell_position) {
  var spreadsheet = SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/.../');
  var sheet = spreadsheet.getSheetByName(sheetname);
  var cell = sheet.getRange(cell_position);
  cell.setValue('Laatst bijgewerkt: '+new Date());
}
  
function load_nl() {
  Logger.log('Fetching NL')
  
  var query = 'SELECT \
                c.file \
               ,c.report_date \
               ,c.fips \
               ,c.city \
               ,c.province_state \
               ,c.country_region \
               ,c.last_update \
               ,c.lat \
               ,c.lon \
               ,c.confirmed \
               ,c.death \
               ,c.recovered \
               ,c.active \
               ,c.combined_key \
               ,cp.confirmed_new \
               ,cp.death_new \
               ,cp.death_rate \
               ,cp.growth_rate \
               FROM covid c \
               JOIN covid_prep_nl cp \
                 ON c.report_date = cp.report_date \
               WHERE c.country_region = "Netherlands" \
                 AND (c.province_state IS NULL \
                      OR c.province_state = "Netherlands") \
               ORDER BY c.report_date ASC'
  var sheetname = 'Data NL'
  
  fetch_mysql_data(query,sheetname)
  
  Logger.log('Fetched NL')
}

function load_it() {
  Logger.log('Fetching IT')
  
  var query = 'SELECT \
                c.file \
               ,c.report_date \
               ,c.fips \
               ,c.city \
               ,c.province_state \
               ,c.country_region \
               ,c.last_update \
               ,c.lat \
               ,c.lon \
               ,c.confirmed \
               ,c.death \
               ,c.recovered \
               ,c.active \
               ,c.combined_key \
               ,cp.confirmed_new \
               ,cp.death_new \
               ,cp.death_rate \
               ,cp.growth_rate \
               FROM covid c \
               JOIN covid_prep_it cp \
                 ON c.report_date = cp.report_date \
               WHERE c.country_region = "Italy" \
                 AND c.province_state IS NULL \
               ORDER BY c.report_date ASC'
  var sheetname = 'Data IT'
  
  fetch_mysql_data(query,sheetname)
  
  Logger.log('Fetched IT')
}

function load_cn() {
  Logger.log('Fetching CN')
  
  var query = 'SELECT \
                c.file \
               ,c.report_date \
               ,c.fips \
               ,c.city \
               ,c.province_state \
               ,c.country_region \
               ,c.last_update \
               ,c.lat \
               ,c.lon \
               ,c.confirmed \
               ,c.death \
               ,c.recovered \
               ,c.active \
               ,c.combined_key \
               ,c.confirmed - cl.confirmed AS confirmed_new \
               ,c.death - cl.death AS death_new \
               ,c.death / c.confirmed AS death_rate \
               ,(c.confirmed - cl.confirmed) / (cl.confirmed - cll.confirmed) AS growth_rate \
               FROM covid_china c \
               LEFT JOIN covid_china cl \
                 ON cl.report_date = DATE_ADD(c.report_date, INTERVAL -1 DAY) \
               LEFT JOIN covid_china cll \
                 ON cll.report_date = DATE_ADD(c.report_date, INTERVAL -2 DAY) \
               ORDER BY c.report_date ASC'
  var sheetname = 'Data CN'
  
  fetch_mysql_data(query,sheetname)
  
  Logger.log('Fetched CN')
}

function load_wereld() {
  Logger.log('Fetching wereld')
  
  var query = 'SELECT \
                c.file \
               ,c.report_date \
               ,c.fips \
               ,c.city \
               ,c.province_state \
               ,c.country_region \
               ,c.last_update \
               ,c.lat \
               ,c.lon \
               ,c.confirmed \
               ,c.death \
               ,c.recovered \
               ,c.active \
               ,c.combined_key \
               ,c.confirmed - cl.confirmed AS confirmed_new \
               ,c.death - cl.death AS death_new \
               ,c.death / c.confirmed AS death_rate \
               ,(c.confirmed - cl.confirmed) / (cl.confirmed - cll.confirmed) AS growth_rate \
               FROM covid_world c \
               LEFT JOIN covid_world cl \
                 ON cl.report_date = DATE_ADD(c.report_date, INTERVAL -1 DAY) \
               LEFT JOIN covid_world cll \
                 ON cll.report_date = DATE_ADD(c.report_date, INTERVAL -2 DAY) \
               ORDER BY c.report_date ASC'
  var sheetname = 'Data wereld'
  
  fetch_mysql_data(query,sheetname)
  
  Logger.log('Fetched wereld')
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