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
				.call(d3.behavior.zoom().scaleExtent([1,8]).on("zoom", redraw)).on("dblclick.zoom", null);

	graph = d3.layout.force()
					.gravity(0.1)
					.distance(200)
					.charge(400)
					.size([vWidth,vHeight]);

	getJSON("data.json");
	
	$(".close").click(function(){
		$(".file,#onefile,#twofile,#onefilename").css("display","none");
	});
});

function redraw(){
	viewport.attr("transform","translate(" + d3.event.translate + ")"+ " scale(" + d3.event.scale + ")");
}

function randColor(){
	r = Math.floor(Math.random()*256);
	g = Math.floor(Math.random()*256);
	b = Math.floor(Math.random()*256);
	return 'rgb('+r+','+g+','+b+')'
}

function getJSON(file){
	d3.json(file,function(error,json){
		jsonData = json;
		dirtitle = $("#dir").text();
		dirtitle += json.dir;
		dir = json.dir;
		$("#dir").html("<b>"+dirtitle+"</b>");
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
						file1 = d.source.stream.split("\n");
						file2 = d.target.stream.split("\n");
						file1name = d.source.name;
						file2name = d.target.name;
						if(file2.length<file1.length){
							file1 = [file2, file2 = file1][0];
							file1name = [file2name, file2name = file1name][0];
						}

						file1HTML="";
						file2HTML="";
						used = [];
						for(var i=0;i<file2.length;++i){
							used.push(false);
						}
						pair = 0;
						for(var i=0;i<file1.length;++i){
							if(pair<d.pairing.length && i==d.pairing[pair][0]){
								color = randColor();
								file1[i] = '<div class="line" style="background-color:'+color+';">' + file1[i] + "</div>";
								file2[d.pairing[pair][1]] = '<div class="line" style="background-color:'+color+';">' + file2[d.pairing[pair][1]] + "</div>";
								used[d.pairing[pair][1]]=true;
								++pair;
							}
							else{
								file1[i] = '<div class="line">' + file1[i] + '</div>';
							}
						}
						for(var i=0;i<file1.length;++i)
							file1HTML += file1[i];
						for(var i=0;i<file2.length;++i){
							if(used[i]==false){
								file2[i] = '<div class="line">' + file2[i] + '</div>';
							}
							file2HTML += file2[i];
						}

						$("#file1").html(file1HTML);
						$("#file2").html(file2HTML);
						$("#file1name").text(file1name);
						$("#file2name").text(file2name);
						$(".file").css("display","block");
						$("#twofile").css("display","block");
					})
					.style("stroke-width", function(d){ return d.weight*5})
					.style("stroke-opacity", function(d){ return Math.sin(d.weight);});

		link.append("title")
				.text(function(d){return d.weight;});

		var node = viewport.selectAll(".node")
					.data(json.files)
					.enter().append("g")
					.attr("class","node")
					.on("dblclick", function(d){
						htm = d.stream.split("\n");
						for(var i=0;i<htm.length;++i)
							htm[i] = "<div class='line'>" + htm[i] + "</div>";

						$("#onefilename").html(d.name);
						$("#onefile").html(htm);
						$("#onefile").css("display","block");
						$("#onefilename").css("display","block");
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