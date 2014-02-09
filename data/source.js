$(document).ready(function(){
	visual = d3.select(".visual");
	vWidth = $(".visual").width();
	vHeight = $(".visual").height();
	viewport = visual.append("svg").attr("width",vWidth).attr("height",vHeight).attr("id","dataVis");	

	graph = d3.layout.force()
					.gravity(.01)
					.distance(200)
					.charge(-10000)
					.size([vWidth,vHeight]);

	getJSON("data.json");
});

function getJSON(file){
	d3.json(file,function(error,json){
		dirtitle = $("#dir").text();
		dirtitle += json.dir;
		dir = json.dir;
		$("#dir").text(dirtitle);
		colors = d3.scale.category20();
		graph
			.nodes(json.files)
			.links(json.fileLinks)
			.start();

		var link = viewport.selectAll(".link")
					.data(json.fileLinks)
					.enter().append("line")
					.attr("class","link")
					.on("mouseover", function(d){
						$("line").css("stroke","#999");
						$(this).css("stroke","#e7191d");
					})
					.on("click",function(d){

					})
					.style("stroke-width", function(d){ return d.weight*5});

		var node = viewport.selectAll(".node")
					.data(json.files)
					.enter().append("g")
					.attr("class","node")
					.on("click", function(d){
						
					})
					.call(graph.drag);

		node.append("text")
				.attr("dx",25)
				.attr("dy", "0.5em")
				.text(function(d){return d.name;});

		node.append("circle")
			.attr("r",10)
			.on("mouseover",function(){
				$(this).attr("r",20);
			})
			.on("mouseout",function(){
				$(this).attr("r",10);
			})
			.style("fill", function(d){ return colors(d.category);});

		graph.on("tick",function(){
			link.attr("x1", function(d){ return d.source.x;})
				.attr("y1", function(d){ return d.source.y;})
				.attr("x2", function(d){ return d.target.x;})
				.attr("y2", function(d){ return d.target.y;});

			node.attr("transform", function(d){ return "translate(" + d.x + "," + d.y + ")";});
		});
	});
}