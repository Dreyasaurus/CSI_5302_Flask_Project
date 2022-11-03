let unliked = document.getElementById("unliked");
let liked = document.getElementById("liked");
console.log(unliked);
console.log(liked);
unliked.addEventListener("click",  function(evt) {
	unliked.style.display="none";
	liked.style.display="";
});

liked.addEventListener("click",  function(evt) {
	liked.style.display="none";
	unliked.style.display="";
});