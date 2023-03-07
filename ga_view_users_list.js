function listUsersAndRoles() {
    var propertyIds = ["UA-XXXXXXX-X", "UA-YYYYYYY-Y", "UA-ZZZZZZZ-Z"]; // Replace with your actual property IDs
    var accountId = "123456"; // Replace with your actual account ID
    
    var accounts = Analytics.Management.Accounts.list();
    var account;
    for (var i = 0; i < accounts.items.length; i++) {
      if (accounts.items[i].id == accountId) {
        account = accounts.items[i];
        break;
      }
    }
    
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Users List");
    if (!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet("Users List");
    }
    sheet.clear();
    sheet.appendRow(["Property ID", "View ID", "View Name", "User Email", "User Role"]);
    
    for (var p = 0; p < propertyIds.length; p++) {
      var webProperties = Analytics.Management.Webproperties.list(account.id);
      var webProperty;
      for (var i = 0; i < webProperties.items.length; i++) {
        if (webProperties.items[i].id == propertyIds[p]) {
          webProperty = webProperties.items[i];
          break;
        }
      }
      
      var profiles = Analytics.Management.Profiles.list(account.id, webProperty.id);
      for (var i = 0; i < profiles.items.length; i++) {
        var viewId = profiles.items[i].id;
        var viewName = profiles.items[i].name;
        var permissions = Analytics.Management.ProfileUserLinks.list(accountId, webProperty.id, viewId);
        if (permissions.items) {
          for (var j = 0; j < permissions.items.length; j++) {
            sheet.appendRow([propertyIds[p], viewId, viewName, permissions.items[j].userRef.email, permissions.items[j].role]);
          }
        }
      }
    }
  }
  