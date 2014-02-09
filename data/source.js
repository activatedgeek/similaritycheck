$(document).ready(function(){
	$(".file,#onefile,#twofile").css("display","none");
	visual = d3.select(".visual");
	vWidth = $(".visual").width();
	vHeight = $(".visual").height();
	viewport = visual.append("svg")
				.attr("width",vWidth)
				.attr("height",vHeight)
				.attr("id","dataVis")
				.attr("pointer-events", "all")
				.call(d3.behavior.zoom().on("zoom", redraw)).on("dblclick.zoom", null);

	graph = d3.layout.force()
					.gravity(0.1)
					.distance(200)
					.charge(-400)
					.size([vWidth,vHeight]);

	getJSON("data.json");
	
	$(".close").click(function(){
		$(".file,#onefile,#twofile").css("display","none");
	});
});

function redraw(){
	viewport.attr("transform","translate(" + d3.event.translate + ")"+ " scale(" + d3.event.scale + ")");
}

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
					.on("mouseout",function(d){
						$("line").css("stroke","#999");
					})
					.on("click",function(d){
						$("#file1").html(d.source.stream);
						$("#file2").html(d.target.stream);
						$(".file").css("display","block");
						$("#twofile").css("display","block");
					})
					.style("stroke-width", function(d){ return d.weight*5});

		var node = viewport.selectAll(".node")
					.data(json.files)
					.enter().append("g")
					.attr("class","node")
					.on("dblclick", function(d){
						$("#onefile").html(d.stream);
						$("#onefile").css("display","block");
						$(".file").css("display","block");
					})
					.call(graph.drag);

		node.append("text")
				.attr("dx",25)
				.attr("dy", "0.5em")
				.text(function(d){return d.name;});

		node.append("circle")
			.attr("r",10)
			.on("mouseover",function(d){
				$(this).attr("r",20);
			})
			.on("mouseout",function(d){
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