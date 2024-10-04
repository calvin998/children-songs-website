var playlist_data = [];

//The pixel amount scrolled before back to top button appears
var scrollAmount = 150;

$(document).ready( function() {
	$('#song_index').DataTable({
		'columnDefs': [{'targets':[1], 'visible':false, 'searchable':true }]
    });
	
	loadPlaylist();
	initPlayListTable();
	
	$(window).scroll( function() {
	  if ($(this).scrollTop() > scrollAmount) {
	    $("#toTopButton").fadeIn();
	  } else {
	    $("#toTopButton").fadeOut();
	  }
	});

	$("#toTopButton").click( function(e) {
	  $("html, body").animate({scrollTop: 0}, 200);
	});
});

function showPlaylist(){
	$('#all_songs').hide();
	$('#playlist').show();
    $("#toTopButton").hide();
	initPlayListTable();
}

function initPlayListTable(){	
	$('#playlist_table').DataTable( {
        data: playlist_data,
		paging: false,
		searching: false,
		sorting:false,
		destroy: true, /*destroy old table*/
        columns: [
			{ title: "Id", visible:false },
			{ title: "Playlist" }
        ],
        'language': { 'emptyTable': 'No songs in playlist' }
    } );
	updatePlaylistCount();
}

function showAllSongs(){
	$('#playlist').hide();
	$('#all_songs').show();
}

function addToPlaylist(i) {
	// do not add if already exists
	var hasSong = false;
	for (j = 0; j < playlist_data.length; j++) {
	  if( playlist_data[j][0] == i ){
		  hasSong = true; break;
	  }
	}

    if(!hasSong){
		pushToPlaylist(i);
	}

	// update UI no matter what (because some buttons can't updated before DataTable loads that page)
	$('.add_'+i).hide();
	$('.remove_'+i).show();

	updatePlaylistCount();

	// save it
	savePlaylist();
}

function pushToPlaylist(i){
	playlist_data.push([
			i, 
			"<a href='#' onclick='showSong("+i+")'>"+song_dict[i]+"</a>" + 
			"<button class='btn small_btn red_btn' onclick='removeFromPlaylist("+i+")'><i class='fa fa-trash'></i> Remove</button>"]);	
}

function removeFromPlaylist(i){
	// update list
	var temp = [];
	for (j = 0; j < playlist_data.length; j++) {
	  if( playlist_data[j][0] != i )
		  temp.push(playlist_data[j]);
	}
	playlist_data = temp;

	// update UI
	$('.add_'+i).show();
	$('.remove_'+i).hide();

	initPlayListTable();
	savePlaylist();
}

function savePlaylist(){
	var s = [];
	for (j = 0; j < playlist_data.length; j++) {
		s.push(playlist_data[j][0]);
	}
	localStorage.songs = s;
}

function loadPlaylist(){
	var s = localStorage.songs;
	if(s == undefined || s.length < 1)
		return;

	var ss = JSON.parse("[" + s + "]");
	for (j = 0; j < ss.length; j++) {
		pushToPlaylist(ss[j]);
	}
}

function updatePlaylistCount(){
	$('#pl_link').html("My Playlist ("+playlist_data.length+")");
}

function showSong(i){
	$('#playarea').html( $('#song_'+i).html());		
	$('#playarea').show();
	$("html, body").animate({
        scrollTop: $("#playarea").offset().top-10
    }, 750);
}




