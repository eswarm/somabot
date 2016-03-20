/* 
$(function() {
   	$('a#settings').bind('click', function() {
   		var x=5;
   		var y=6;
 	    $.getJSON('/settings', {
 	      	a: x,
 	      	b: y
 	    }, function(data) {});
 	    return false;
   	});
});
*/
function doAjax(arg) {
	console.log(localStorage.getItem("timestamp"));
	var payload = "name="+arg.id+"&id="+localStorage.getItem("timestamp");
    $.ajax({
        url: '/make_drink',
        data: payload,
        type: 'GET',
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

if (localStorage.getItem("timestamp") === null) {
	localStorage.setItem("timestamp", new Date().getTime());
	console.log(localStorage.getItem("timestamp"));
}

function confirmClicked() {
	var select0 = document.getElementById("option_0");
	var select1 = document.getElementById("option_1");
	var select2 = document.getElementById("option_2");
	var select3 = document.getElementById("option_3");
	var payload = "ingredients=" + select0.options[select0.selectedIndex].value + "," + 
				select1.options[select1.selectedIndex].value + "," + 
				select2.options[select2.selectedIndex].value + "," + 
				select3.options[select3.selectedIndex].value;
	$.ajax({
		url: '/settings',
		data: payload,
		type: 'GET',
		success: function(response) {
			console.log(response);
			window.location.reload(true);
		},
		error: function(error) {
			console.log(error);
		}
	});
}

window.onload = function () {
	// Get the modal
	var modal = document.getElementById('myModal');

	// Get the button that opens the modal
	var btn = document.getElementById("myBtn");

	var confirmbtn = document.getElementById("confirm");

	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];

	// When the user clicks the button, open the modal 
	btn.onclick = function() {
	    modal.style.display = "block";
	}

	confirmbtn.onclick = function() {
		confirmClicked();
	}

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
	    modal.style.display = "none";
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	    if (event.target == modal) {
	        modal.style.display = "none";
	    }
	}
}
