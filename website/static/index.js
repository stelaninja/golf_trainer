// Function to delete users
function deleteUser(userId) {
  console.log("Delete User Called");
  fetch("/delete-user", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = "/users";
  });
}

// Fade out flash messages

// setTimeout(function () {
//   $(".alert").remove();
// }, 3000);

$(document).ready(function () {
  setTimeout(function () {
    $(".alert").hide("blind", {}, 500);
  }, 5000);
});
