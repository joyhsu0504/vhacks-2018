$( document ).ready(function () {
	if (document.title == "Leif") {
		$( "#nav_leif" ).css( "font-size", "24px" );
	} else if (document.title == "Connections") {
		$( "#nav_connections" ).css( "font-size", "24px" );
	} else if (document.title == "Your Jobs") {
		$( "#nav_jobs" ).css( "font-size", "24px" );
	}
});