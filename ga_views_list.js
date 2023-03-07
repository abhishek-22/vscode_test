function listViews() {
  var propertyIds = ["UA-XXXXXXX-X", "UA-YYYYYYY-Y"]; // Replace these with your actual property IDs
  var accountId = "123456"; // Replace this with your actual account ID
  var sheetName = "Views List"; // Name of the sheet to write the output to
  
  var accounts = Analytics.Management.Accounts.list();
  var account;
  for (var i = 0; i < accounts.items.length; i++) {
    if (accounts.items[i].id == accountId) {
      account = accounts.items[i];
      break;
    }
  }
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  if (!sheet) {
    sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet(sheetName);
    sheet.appendRow(["Property ID", "View ID", "View Name"]);
  }
  
  for (var j = 0; j < propertyIds.length; j++) {
    var propertyId = propertyIds[j];
    var webProperties = Analytics.Management.Webproperties.list(account.id);
    var webProperty;
    for (var i = 0; i < webProperties.items.length; i++) {
      if (webProperties.items[i].id == propertyId) {
        webProperty = webProperties.items[i];
        break;
      }
    }
    
    var profiles = Analytics.Management.Profiles.list(account.id, webProperty.id);
    for (var i = 0; i < profiles.items.length; i++) {
      sheet.appendRow([propertyId, profiles.items[i].id, profiles.items[i].name]);
    }
  }
}
