let unliked = document.getElementById("unliked");
let liked = document.getElementById("liked");

function handleInsert(id){
	console.log(id);
	
   fetch('/player/'+id, {
     method: 'POST',
     header: {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
       }
     }) .then((response) => response.json())
  .then((data) => {
	  if(data.message ==='success'){
		  location.href = id;
	  }
	});
}

function handleRemove(id){
	console.log(id);
	
   fetch('/player/'+id, {
     method: 'DELETE',
     header: {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
       }
     }) .then((response) => response.json())
  .then((data) => {
	  if(data.message ==='success'){
		  location.href = id;
	  }
	});
}