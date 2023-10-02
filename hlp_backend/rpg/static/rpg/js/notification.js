// Function to show the notification popup
function showNotification(message) {
    console.log("showNotification called with message: " + message);
    var notification = $("#notification-popup");
    notification.find(".notification-content").text(message); // Update the notification message
    notification.fadeIn().delay(3000).fadeOut();
}

// Call this function when an incorrect login attempt occurs
// You can do this in your Django view after an incorrect login attempt
// For example:
// if login_failed:
//   showNotification();