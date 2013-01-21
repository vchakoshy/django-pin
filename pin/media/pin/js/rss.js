var feedobj = $('#feed-ul-v2');
var loadingobj;
var a_url = a_url || "";
var extend_query = extend_query || "";

function load_posts(page) {
	$.get(a_url + '?older=' + page + '&' + extend_query, function(response) {
		if (response == 0) {
			loadingobj.hide();
		} else {
			var $boxes = $(response);
			feedobj.append($boxes);
			loadingobj.hide();
			start_loading = 0;
			ana_ajax(a_url + '?older=' + page + '&' + extend_query);
		}
	});
}


$(window).scroll(function() {
	loadingobj = $(".loading");
	var break_point = $(document).height() - ($(window).height() * 2.02);
	if ($(window).scrollTop() >= break_point) {
		var next_page = $('#feed-ul-v2 span:last').attr('data-next');
		if (next_page && start_loading == 0) {
			start_loading = 1;
			loadingobj.show();
			load_posts(next_page);
		}
	}
});

/* live part
 */

var socket = io.connect(node_url);
socket.on('data', function(data) {
	$.ajax({
		url : node_fetch_url + '?older=' + lastId,
		success : function(html) {
			if (html != 0) {
				html = $(html);
				$('#feed-ul-v2').prepend(html).fadeIn('slow');
				var ch = $("#feed-ul-v2 div:first-child")[0];
				lastId = $(ch).attr('rel');
			}
		},
	});
}); 