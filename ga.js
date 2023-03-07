function listViews() {
    var propertyId = "UA-XXXXXXX-X"; // Replace this with your actual property ID
    var accountId = "123456"; // Replace this with your actual account ID
    
    var accounts = Analytics.Management.Accounts.list();
    var account;
    for (var i = 0; i < accounts.items.length; i++) {
      if (accounts.items[i].id == accountId) {
        account = accounts.items[i];
        break;
      }
    }
    
    var webProperties = Analytics.Management.Webproperties.list(account.id);
    var webProperty;
    for (var i = 0; i < webProperties.items.length; i++) {
      if (webProperties.items[i].id == propertyId) {
        webProperty = webProperties.items[i];
        break;
      }
    }
    
    var profiles = Analytics.Management.Profiles.list(account.id, webProperty.id);
    var sheet = SpreadsheetApp.getActiveSheet();
    sheet.clear();
    sheet.appendRow(["View ID", "View Name"]);
    for (var i = 0; i < profiles.items.length; i++) {
      sheet.appendRow([profiles.items[i].id, profiles.items[i].name]);
    }
  }