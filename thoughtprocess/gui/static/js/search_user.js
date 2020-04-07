var input = document.getElementById("mySearch");


input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        myFunction();
    }
});


function myFunction() {
    user_id = document.getElementById("mySearch").value;
    window.document.location = "search?user_id=" + user_id;
}