

var counterVal = 0;

function incrementClick() {
updateDisplay(++counterVal);
}


function updateDisplay(val) {
document.getElementById("counter-label").innerHTML = val;
}



var closebtns = document.getElementsByClassName("close");
var i;

/* Loop through the elements, and hide the parent, when clicked on */
for (i = 0; i < closebtns.length; i++) {
  closebtns[i].addEventListener("click", function() {
    this.parentElement.style.display = 'none';
  });
}