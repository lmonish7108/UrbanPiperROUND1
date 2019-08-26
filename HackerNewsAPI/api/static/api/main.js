window.onload = function(){
	if(window._json_response !== undefined){
		window._json_response.forEach(function(val, idx){
			let elmt = "<tr><td><a href="+val.url+">"+val.title+"</a></td><td>"+val.by+"</td><td>"+val.score+"</td><td>"+val.sentiment+"</td></tr>";
			document.querySelector("#json_response_table").innerHTML += elmt;
		});
	}
	$("#titles").empty();
	$("#search_str").val("");
	$("#search_str").bind("input", function(){
		if ($("#search_str").val().length > 2){
			$("#titles option").each(function(){
				if ($("#search_str").val() == $(this).attr("value")){
					window.location.href = $(this).attr("value")
				}
			});
			$("#titles").empty();
			$.ajax({
				url: "/get_search_title/"+$("#search_str").val(),
				context: document.body
				}).done(function(response) {
					window.title_list = JSON.parse(response);
					window.title_list.forEach(function(val, idx){
						$("#titles").append("<option value='"+ val.url +"'>"+val.title+"</option>");
					});

			});
		}
	});
}
