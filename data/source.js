jsonData=0
nodes = []
labelAnchors = []
labelAnchorLinks = []

$(document).ready(function(){
	getJSON("data.json");
});

function drawGraph(){
	graph = d3.layout.force().charge(-500).linkDistance(50).size([vWidth,vHeight]);
	graph.nodes
}

function setViewport(){
	visual = d3.select(".visual");
	vWidth = $(".visual").width();
	vHeight = $(".visual").height();
	viewport = visual.append("svg").attr("width",vWidth).attr("height",vHeight).attr("id","dataVis");
	n = jsonData.files.length;
}

function getJSON(file){
	d3.json(file,function(json){
		jsonData = json;
		dirtitle = $("#dir").text();
		dirtitle += jsonData.dir;
		$("#dir").text(dirtitle);
		setViewport();
	});
}