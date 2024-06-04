(function (cjs, an) {

var p; // shortcut to reference prototypes
var lib={};var ss={};var img={};
lib.webFontTxtInst = {}; 
var loadedTypekitCount = 0;
var loadedGoogleCount = 0;
var gFontsUpdateCacheList = [];
var tFontsUpdateCacheList = [];
lib.ssMetadata = [];



lib.updateListCache = function (cacheList) {		
	for(var i = 0; i < cacheList.length; i++) {		
		if(cacheList[i].cacheCanvas)		
			cacheList[i].updateCache();		
	}		
};		

lib.addElementsToCache = function (textInst, cacheList) {		
	var cur = textInst;		
	while(cur != null && cur != exportRoot) {		
		if(cacheList.indexOf(cur) != -1)		
			break;		
		cur = cur.parent;		
	}		
	if(cur != exportRoot) {		
		var cur2 = textInst;		
		var index = cacheList.indexOf(cur);		
		while(cur2 != null && cur2 != cur) {		
			cacheList.splice(index, 0, cur2);		
			cur2 = cur2.parent;		
			index++;		
		}		
	}		
	else {		
		cur = textInst;		
		while(cur != null && cur != exportRoot) {		
			cacheList.push(cur);		
			cur = cur.parent;		
		}		
	}		
};		

lib.gfontAvailable = function(family, totalGoogleCount) {		
	lib.properties.webfonts[family] = true;		
	var txtInst = lib.webFontTxtInst && lib.webFontTxtInst[family] || [];		
	for(var f = 0; f < txtInst.length; ++f)		
		lib.addElementsToCache(txtInst[f], gFontsUpdateCacheList);		

	loadedGoogleCount++;		
	if(loadedGoogleCount == totalGoogleCount) {		
		lib.updateListCache(gFontsUpdateCacheList);		
	}		
};		

lib.tfontAvailable = function(family, totalTypekitCount) {		
	lib.properties.webfonts[family] = true;		
	var txtInst = lib.webFontTxtInst && lib.webFontTxtInst[family] || [];		
	for(var f = 0; f < txtInst.length; ++f)		
		lib.addElementsToCache(txtInst[f], tFontsUpdateCacheList);		

	loadedTypekitCount++;		
	if(loadedTypekitCount == totalTypekitCount) {		
		lib.updateListCache(tFontsUpdateCacheList);		
	}		
};
// symbols:
// helper functions:

function mc_symbol_clone() {
	var clone = this._cloneProps(new this.constructor(this.mode, this.startPosition, this.loop));
	clone.gotoAndStop(this.currentFrame);
	clone.paused = this.paused;
	clone.framerate = this.framerate;
	return clone;
}

function getMCSymbolPrototype(symbol, nominalBounds, frameBounds) {
	var prototype = cjs.extend(symbol, cjs.MovieClip);
	prototype.clone = mc_symbol_clone;
	prototype.nominalBounds = nominalBounds;
	prototype.frameBounds = frameBounds;
	return prototype;
	}


(lib.yellow = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#DFDC01").s().p("AHaU3IulmOItW93ICtmOQDqBsGbhmIPCexIpK3hISNGiIEMJpIliQkQheC0jBAAQhZAAhugmg");
	this.shape.setTransform(131.4,137.3);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,262.9,274.7);


(lib.Tween1 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#666666").s().p("AiYA+QgPgPAAgXQAAgVAPgQQAQgRAXAAQARAAANAKIADACIgBgyQAHgQAPAKIAABeIAAAEQAAAJgCAIQgEAMgKAJQgRARgVAAQgXAAgQgRgAiJAAQgJAKAAANQAAAPAJAJQAKAKAOAAQANAAAKgKIAFgGQAGgHAAgLIAAgCIgBgFQgDgJgHgHQgJgIgLgBIgDAAQgOAAgKAJgAj4BNIgmgoIgjAnQgOAEAAgSIAjgnIgegeQgKgVATABIAiAkIAiglQATgBgKAVIgdAfIAmAoQABAOgKAAIgEAAgACbA8QgNgyA+ADQAhACgQgQQgRgRgpAOQgEgHgBgLQBBgWAVArQAUApgrAgQgRAFgNAAQgXAAgNgRgAC2AzQAcAWAQgqIgOgBQg3AAAZAVgAEPApIAAhZQAHgQAPAKIAAAZIAhgBQAQAHgKAPIgnAAIAAAwQADAYAdgLIAJAPQgTAJgOAAQgbAAgDgkgAjUBHIgBhYQAHgRAPALIAABeQgGAFgGAAQgFAAgEgFgAAlBJIAAgIIgBgzIgEgNQgGgOgXAEQgWACAFBQIgTAAQgNhiApgDQAmgDAOATQAMgPAYgDQAYgCANAPQAMAQgBAXQgCAXACAcIgVAAIAAgoQABgSgGgPQgGgNgXADQgSACgBAvIACAigAjTgzQgDgEAAgFQAAgFADgEQAEgEAGAAQAFAAAEAEQAEAEAAAFQAAAFgEAEQgEAEgFAAQgGAAgEgEg");

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-33.5,-7.9,67.2,15.8);


(lib.Symbol3 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#666666").s().p("AhsAsIAHgQQArATAXgRQAJgUg3gCQgngKASgmQAYgaA6AWQAKANgPAFQgNgLgUAAQgiAAAJAVQAIAGAYgBQAzALgPAkQgQATgcAAQgVAAgcgLgAAHAjQgNgxA+ADQAhACgRgRQgRgRgqAOQgFgRASgGQBJgIABAyQgBAwABAMQgYADgTAAQgpAAgJgSgAAhAkQAcAEAQgEIAAgeIgSgBQgwAAAWAfgAjbAjQgNgxA+ADQAhACgQgRQgRgRgqAOQgFgRASgGQBJgIAAAyQAAAwABAMQgZADgSAAQgpAAgKgSgAjAAkQAbAEARgEIAAgeIgSgBQgwAAAWAfgADHA0IABgoQABgRgIgQQgHgPgZADQgZADAIBSIgWAAQgLhkAsgDQAsgEAMARQAMASgBAVQgCAXACAcg");
	this.shape.setTransform(22.2,5.5);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = getMCSymbolPrototype(lib.Symbol3, new cjs.Rectangle(0,0,44.5,11.1), null);


(lib.orange = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#F7A832").s().p("A1UR9QBqjshqmZIepvUI3cJYIGXyQIJokSIQmFZQEJCGh2FfImHOpI9vNmg");
	this.shape.setTransform(136.5,131.9);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,273.1,263.8);


(lib.light_yellow = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FFD632").s().p("A3bEfIifmSQDyhaDalrMAgaALHI3HqJIReoQIJzD3IHzPnQBZEblMCiIuvF6g");
	this.shape.setTransform(165.9,103.5);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,331.9,207);


(lib.light_pink = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#F187B7").s().p("AoeS6MAKogglIpzXRIohxWIDup3IPfoCQEZhdCnFKIGIOpIrOetImRClQhdjyltjTg");
	this.shape.setTransform(103.5,166.2);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,207.1,332.5);


(lib.light_blue = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#9BD8F7").s().p("Ax7MQInsvrQhXkaFNigIOxl1IeeL6ICcGUQjzBXjcFqMggVgLWIXDKTIxiIJg");
	this.shape.setTransform(165.8,103.5);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,331.6,207);


(lib.green = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#39AA34").s().p("AqCV9ImJupILS+tIGRilQBcDyFuDVMgKrAgjIJ13QIIfRXIjuJ3IvhIAQg9AVg5AAQjHAAiBkCg");
	this.shape.setTransform(103.6,166.3);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,207.1,332.5);


(lib.dark_pink = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#EA5098").s().p("AH1VWIvM+tIJRXfIyOmcIkQppIFewlQCHkIFfB3IOmGLINfdyIirGPQjshrmZBog");
	this.shape.setTransform(131.7,136.9);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,263.4,273.8);


(lib.circle = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#B4B3AE").s().p("AozIwQjqjoAAlIQAAlHDqjpQDqjnFJAAQC3AACYBGIATAJQBxA4BhBgQDpDpAAFHQAAFIjpDoQjqDolKAAQlJAAjqjog");
	this.shape.setTransform(79.8,79.2);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,159.5,158.4);


(lib.blue = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#009FE3").s().p("AycPQQkIiFB1lfIGFuqIdutpIGQCpQhrDsBrGZI+nPXIXbpaImWSRIpnETg");
	this.shape.setTransform(136.4,132);

	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(0,0,272.8,264);


(lib.logo = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// timeline functions:
	this.frame_58 = function() {
		/* Stop at This Frame
		The  timeline will stop/pause at the frame where you insert this code.
		Can also be used to stop/pause the timeline of movieclips.
		*/
		exportRoot.goon = true
		this.stop();
	}

	// actions tween:
	this.timeline.addTween(cjs.Tween.get(this).wait(58).call(this.frame_58).wait(1));

	// mask (mask)
	var mask = new cjs.Shape();
	mask._off = true;
	mask.graphics.p("EhAHBAIMAAAiAQMCAQAAAMAAACAQgAr6riQh+B6hLCNQgZAvgTAwQhICzAADOQAAG0E9E1QE/EzHBABQHCgBE+kzQE+k1AAm0QAAmzk+k0Qk+k0nCAAQnBAAk/E0g");
	mask.setTransform(0.4,0.7);

	// 8
	this.instance = new lib.light_blue("synched",0);
	this.instance.parent = this;
	this.instance.setTransform(122.9,49.8,0.515,0.515,0,0,0,390.4,207.8);
	this.instance.alpha = 0;
	this.instance._off = true;

	var maskedShapeInstanceList = [this.instance];

	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}

	this.timeline.addTween(cjs.Tween.get(this.instance).wait(48).to({_off:false},0).wait(1).to({regX:165.8,regY:103.5,scaleX:0.57,scaleY:0.57,x:-18.4,y:-15.1,alpha:0.111},0).wait(1).to({scaleX:0.62,scaleY:0.62,x:-44,y:-26.3,alpha:0.222},0).wait(1).to({scaleX:0.68,scaleY:0.68,x:-69.6,y:-37.5,alpha:0.333},0).wait(1).to({scaleX:0.73,scaleY:0.73,x:-95.2,y:-48.6,alpha:0.444},0).wait(1).to({scaleX:0.79,scaleY:0.79,x:-120.7,y:-59.9,alpha:0.556},0).wait(1).to({scaleX:0.84,scaleY:0.84,x:-146.3,y:-71,alpha:0.667},0).wait(1).to({scaleX:0.89,scaleY:0.89,x:-171.9,y:-82.2,alpha:0.778},0).wait(1).to({scaleX:0.95,scaleY:0.95,x:-197.5,y:-93.4,alpha:0.889},0).wait(1).to({scaleX:1,scaleY:1,x:-223,y:-104.6,alpha:1},0).wait(1).to({x:-223.1,y:-105},0).wait(1));

	// 7
	this.instance_1 = new lib.blue("synched",0);
	this.instance_1.parent = this;
	this.instance_1.setTransform(107,-38.3,0.436,0.436,0,0,0,381.1,43.4);
	this.instance_1.alpha = 0;
	this.instance_1._off = true;

	var maskedShapeInstanceList = [this.instance_1];

	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}

	this.timeline.addTween(cjs.Tween.get(this.instance_1).wait(42).to({_off:false},0).wait(1).to({regX:136.4,regY:132,scaleX:0.5,scaleY:0.5,x:-26.7,y:10.2,alpha:0.111},0).wait(1).to({scaleX:0.56,scaleY:0.56,x:-53.8,y:20,alpha:0.222},0).wait(1).to({scaleX:0.62,scaleY:0.62,x:-80.9,y:29.8,alpha:0.333},0).wait(1).to({scaleX:0.69,scaleY:0.69,x:-108,y:39.6,alpha:0.444},0).wait(1).to({scaleX:0.75,scaleY:0.75,x:-135,y:49.4,alpha:0.556},0).wait(1).to({scaleX:0.81,scaleY:0.81,x:-162.1,y:59.3,alpha:0.667},0).wait(1).to({scaleX:0.88,scaleY:0.88,x:-189.1,y:69.1,alpha:0.778},0).wait(1).to({scaleX:0.94,scaleY:0.94,x:-216.2,y:78.9,alpha:0.889},0).wait(1).to({scaleX:1,scaleY:1,x:-243.3,y:88.8,alpha:1},0).wait(1).to({regY:131.9,x:-243.8,y:88.2},0).wait(7));

	// 6
	this.instance_2 = new lib.green("synched",0);
	this.instance_2.parent = this;
	this.instance_2.setTransform(44.2,-83.7,0.444,0.444,0,0,0,207.1,-58.4);
	this.instance_2.alpha = 0;
	this.instance_2._off = true;

	var maskedShapeInstanceList = [this.instance_2];

	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}

	this.timeline.addTween(cjs.Tween.get(this.instance_2).wait(36).to({_off:false},0).wait(1).to({regX:103.6,regY:166.3,scaleX:0.51,scaleY:0.51,x:-12.8,y:39.2,alpha:0.111},0).wait(1).to({scaleX:0.57,scaleY:0.57,x:-24,y:62.5,alpha:0.222},0).wait(1).to({scaleX:0.63,scaleY:0.63,x:-35.1,y:85.7,alpha:0.333},0).wait(1).to({scaleX:0.69,scaleY:0.69,x:-46.2,y:109,alpha:0.444},0).wait(1).to({scaleX:0.75,scaleY:0.75,x:-57.4,y:132.2,alpha:0.556},0).wait(1).to({scaleX:0.82,scaleY:0.82,x:-68.5,y:155.4,alpha:0.667},0).wait(1).to({scaleX:0.88,scaleY:0.88,x:-79.7,y:178.7,alpha:0.778},0).wait(1).to({scaleX:0.94,scaleY:0.94,x:-90.8,y:201.9,alpha:0.889},0).wait(1).to({scaleX:1,scaleY:1,x:-102,y:225.2,alpha:1},0).wait(1).to({x:-102.5,y:226.2},0).wait(13));

	// 5
	this.instance_3 = new lib.yellow("synched",0);
	this.instance_3.parent = this;
	this.instance_3.setTransform(-27,-108.9,0.49,0.49,0,0,0,42,-104.9);
	this.instance_3.alpha = 0;
	this.instance_3._off = true;

	var maskedShapeInstanceList = [this.instance_3];

	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}

	this.timeline.addTween(cjs.Tween.get(this.instance_3).wait(30).to({_off:false},0).wait(1).to({regX:131.4,regY:137.3,scaleX:0.55,scaleY:0.55,x:25.1,y:36.1,alpha:0.111},0).wait(1).to({scaleX:0.6,scaleY:0.6,x:33.3,y:62.3,alpha:0.222},0).wait(1).to({scaleX:0.66,scaleY:0.66,x:41.5,y:88.4,alpha:0.333},0).wait(1).to({scaleX:0.72,scaleY:0.72,x:49.7,y:114.6,alpha:0.444},0).wait(1).to({scaleX:0.77,scaleY:0.77,x:58,y:140.8,alpha:0.556},0).wait(1).to({scaleX:0.83,scaleY:0.83,x:66.2,y:167,alpha:0.667},0).wait(1).to({scaleX:0.89,scaleY:0.89,x:74.4,y:193.2,alpha:0.778},0).wait(1).to({scaleX:0.94,scaleY:0.94,x:82.6,y:219.4,alpha:0.889},0).wait(1).to({scaleX:1,scaleY:1,x:90.9,y:245.5,alpha:1},0).wait(1).to({x:90.6,y:245.6},0).wait(19));

	// 4
	this.instance_4 = new lib.light_yellow("synched",0);
	this.instance_4.parent = this;
	this.instance_4.setTransform(-120,-57.5,0.516,0.516,0,0,0,-57.3,0);
	this.instance_4.alpha = 0;
	this.instance_4._off = true;

	var maskedShapeInstanceList = [this.instance_4];

	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}

	this.timeline.addTween(cjs.Tween.get(this.instance_4).wait(24).to({_off:false},0).wait(1).to({regX:165.9,regY:103.5,scaleX:0.57,scaleY:0.57,x:20.7,y:8.2,alpha:0.111},0).wait(1).to({scaleX:0.62,scaleY:0.62,x:46.2,y:20.5,alpha:0.222},0).wait(1).to({scaleX:0.68,scaleY:0.68,x:71.6,y:32.7,alpha:0.333},0).wait(1).to({scaleX:0.73,scaleY:0.73,x:97.2,y:45,alpha:0.444},0).wait(1).to({scaleX:0.79,scaleY:0.79,x:122.6,y:57.3,alpha:0.556},0).wait(1).to({scaleX:0.84,scaleY:0.84,x:148.1,y:69.5,alpha:0.667},0).wait(1).to({scaleX:0.89,scaleY:0.89,x:173.6,y:81.8,alpha:0.778},0).wait(1).to({scaleX:0.95,scaleY:0.95,x:199.1,y:94,alpha:0.889},0).wait(1).to({scaleX:1,scaleY:1,x:224.6,y:106.3,alpha:1},0).wait(1).to({regX:166,x:225.6,y:106.2},0).wait(25));

	// 3
	this.instance_5 = new lib.orange();
	this.instance_5.parent = this;
	this.instance_5.setTransform(-108.9,40.4,0.456,0.456,0,0,0,-104.6,219.6);
	this.instance_5.alpha = 0;
	this.instance_5._off = true;

	var maskedShapeInstanceList = [this.instance_5];

	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}

	this.timeline.addTween(cjs.Tween.get(this.instance_5).wait(18).to({_off:false},0).wait(1).to({regX:136.5,regY:131.9,scaleX:0.52,scaleY:0.52,x:28.2,y:-9.3,alpha:0.111},0).wait(1).to({scaleX:0.58,scaleY:0.58,x:55.4,y:-19,alpha:0.222},0).wait(1).to({scaleX:0.64,scaleY:0.64,x:82.5,y:-28.8,alpha:0.333},0).wait(1).to({scaleX:0.7,scaleY:0.7,x:109.6,y:-38.6,alpha:0.444},0).wait(1).to({scaleX:0.76,scaleY:0.76,x:136.7,y:-48.4,alpha:0.556},0).wait(1).to({scaleX:0.82,scaleY:0.82,x:163.8,y:-58.1,alpha:0.667},0).wait(1).to({scaleX:0.88,scaleY:0.88,x:191,y:-67.9,alpha:0.778},0).wait(1).to({scaleX:0.94,scaleY:0.94,x:218.1,y:-77.7,alpha:0.889},0).wait(1).to({scaleX:1,scaleY:1,x:245.2,y:-87.5,alpha:1},0).wait(1).to({x:246.1,y:-88},0).wait(31));

	// 2
	this.instance_6 = new lib.light_pink();
	this.instance_6.parent = this;
	this.instance_6.setTransform(-48.9,123.5,0.519,0.519,0,0,0,0,389.9);
	this.instance_6.alpha = 0;
	this.instance_6._off = true;

	var maskedShapeInstanceList = [this.instance_6];

	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}

	this.timeline.addTween(cjs.Tween.get(this.instance_6).wait(12).to({_off:false},0).wait(1).to({regX:103.5,regY:166.2,scaleX:0.57,scaleY:0.57,x:16.1,y:-18.3,alpha:0.111},0).wait(1).to({scaleX:0.63,scaleY:0.63,x:27.4,y:-43.9,alpha:0.222},0).wait(1).to({scaleX:0.68,scaleY:0.68,x:38.7,y:-69.6,alpha:0.333},0).wait(1).to({scaleX:0.73,scaleY:0.73,x:50,y:-95.3,alpha:0.444},0).wait(1).to({scaleX:0.79,scaleY:0.79,x:61.3,y:-121,alpha:0.556},0).wait(1).to({scaleX:0.84,scaleY:0.84,x:72.5,y:-146.6,alpha:0.667},0).wait(1).to({scaleX:0.89,scaleY:0.89,x:83.8,y:-172.3,alpha:0.778},0).wait(1).to({scaleX:0.95,scaleY:0.95,x:95.1,y:-198,alpha:0.889},0).wait(1).to({scaleX:1,scaleY:1,x:106.4,y:-223.6,alpha:1},0).wait(1).to({regY:166.3,x:106.3,y:-223.7},0).wait(37));

	// 1
	this.instance_7 = new lib.dark_pink();
	this.instance_7.parent = this;
	this.instance_7.setTransform(56.6,162.3,0.612,0.612,0,0,0,220.8,380.9);
	this.instance_7.alpha = 0;
	this.instance_7._off = true;

	var maskedShapeInstanceList = [this.instance_7];

	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}

	this.timeline.addTween(cjs.Tween.get(this.instance_7).wait(6).to({_off:false},0).wait(1).to({regX:131.7,regY:136.9,scaleX:0.66,scaleY:0.66,x:-7.8,y:-15.5,alpha:0.111},0).wait(1).to({scaleX:0.7,scaleY:0.7,x:-17.8,y:-44.1,alpha:0.222},0).wait(1).to({scaleX:0.74,scaleY:0.74,x:-27.8,y:-72.6,alpha:0.333},0).wait(1).to({scaleX:0.78,scaleY:0.78,x:-37.7,y:-101.1,alpha:0.444},0).wait(1).to({scaleX:0.83,scaleY:0.83,x:-47.7,y:-129.7,alpha:0.556},0).wait(1).to({scaleX:0.87,scaleY:0.87,x:-57.7,y:-158.2,alpha:0.667},0).wait(1).to({scaleX:0.91,scaleY:0.91,x:-67.6,y:-186.7,alpha:0.778},0).wait(1).to({scaleX:0.96,scaleY:0.96,x:-77.6,y:-215.3,alpha:0.889},0).wait(1).to({scaleX:1,scaleY:1,x:-87.6,y:-243.8,alpha:1},0).wait(1).to({regX:220.8,regY:381.4,x:1.5,y:0.2},0).wait(43));

	// 0
	this.instance_8 = new lib.circle("synched",0);
	this.instance_8.parent = this;
	this.instance_8.setTransform(1.4,0.2,0.378,0.378,0,0,0,79.1,79.1);
	this.instance_8.alpha = 0;

	this.timeline.addTween(cjs.Tween.get(this.instance_8).wait(1).to({regX:79.8,regY:79.2,scaleX:0.44,scaleY:0.44,x:1.8,y:0.3,alpha:0.1},0).wait(1).to({scaleX:0.5,scaleY:0.5,alpha:0.2},0).wait(1).to({scaleX:0.56,scaleY:0.56,alpha:0.3},0).wait(1).to({scaleX:0.63,scaleY:0.63,x:1.9,alpha:0.4},0).wait(1).to({scaleX:0.69,scaleY:0.69,x:2,alpha:0.5},0).wait(1).to({scaleX:0.75,scaleY:0.75,alpha:0.6},0).wait(1).to({scaleX:0.81,scaleY:0.81,alpha:0.7},0).wait(1).to({scaleX:0.88,scaleY:0.88,alpha:0.8},0).wait(1).to({scaleX:0.94,scaleY:0.94,x:2.1,alpha:0.9},0).wait(1).to({scaleX:1,scaleY:1,x:2.2,y:0.4,alpha:1},0).wait(1).to({x:1.5,y:0.2},0).wait(48));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-28.5,-29.7,60.3,59.9);


(lib.ASANXIDMET = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// timeline functions:
	this.frame_24 = function() {
		this.stop();
	}

	// actions tween:
	this.timeline.addTween(cjs.Tween.get(this).wait(24).call(this.frame_24).wait(1));

	// xidmet
	this.instance = new lib.Tween1("synched",0);
	this.instance.parent = this;
	this.instance.setTransform(87.9,7.9);
	this.instance.alpha = 0;

	this.timeline.addTween(cjs.Tween.get(this.instance).to({x:144.1,alpha:1},24).wait(1));

	// asan
	this.instance_1 = new lib.Symbol3();
	this.instance_1.parent = this;
	this.instance_1.setTransform(82.2,10.5,1,1,0,0,0,22.2,5.5);
	this.instance_1.alpha = 0;

	this.timeline.addTween(cjs.Tween.get(this.instance_1).to({x:20.6,alpha:1},24).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(54.4,0,67.2,16.1);


// stage content:
(lib.prj = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});

	// timeline functions:
	this.frame_0 = function() {
		this.stop()
		this.time = 4
		this.goon = false
		this.finish = false
		this.addEventListener("tick", fl_RotateContinuously.bind(this));
		function fl_RotateContinuously() {
			if (this.goon == true) {
				console.log("GO!!!")
				exportRoot.play()
				this.goon = false
			}
			if (this.finish == true) {
				if (this.time >= 0.4) {
					this.time -= 0.1
				} else {
					this.time = 0.3
					this.finish = false
				}
			}
			this.movieClip_1.rotation += this.time;
		}
	}
	this.frame_8 = function() {
		this.stop();
		this.finish = true;
	}

	// actions tween:
	this.timeline.addTween(cjs.Tween.get(this).call(this.frame_0).wait(8).call(this.frame_8).wait(1));

	// logo
	this.movieClip_1 = new lib.logo();
	this.movieClip_1.parent = this;
	this.movieClip_1.setTransform(198.8,95.3,0.182,0.18,0,0,0,0.8,0.8);

	this.timeline.addTween(cjs.Tween.get(this.movieClip_1).wait(9));

	// txt
	this.instance = new lib.ASANXIDMET();
	this.instance.parent = this;
	this.instance.setTransform(225.2,95.6,2.498,2.498,0,0,0,87.9,8.2);
	this.instance._off = true;

	this.timeline.addTween(cjs.Tween.get(this.instance).wait(8).to({_off:false},0).wait(1));

}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(349,117.3,149.3,148);
// library properties:
lib.properties = {
	id: '3F63CCB6D2D1104694351256E9E34981',
	width: 450,
	height: 192,
	fps: 35,
	color: "#FFFFFF",
	opacity: 0.00,
	webfonts: {},
	manifest: [],
	preloads: []
};



// bootstrap callback support:

(lib.Stage = function(canvas) {
	createjs.Stage.call(this, canvas);
}).prototype = p = new createjs.Stage();

p.setAutoPlay = function(autoPlay) {
	this.tickEnabled = autoPlay;
}
p.play = function() { this.tickEnabled = true; this.getChildAt(0).gotoAndPlay(this.getTimelinePosition()) }
p.stop = function(ms) { if(ms) this.seek(ms); this.tickEnabled = false; }
p.seek = function(ms) { this.tickEnabled = true; this.getChildAt(0).gotoAndStop(lib.properties.fps * ms / 1000); }
p.getDuration = function() { return this.getChildAt(0).totalFrames / lib.properties.fps * 1000; }

p.getTimelinePosition = function() { return this.getChildAt(0).currentFrame / lib.properties.fps * 1000; }

an.bootcompsLoaded = an.bootcompsLoaded || [];
if(!an.bootstrapListeners) {
	an.bootstrapListeners=[];
}

an.bootstrapCallback=function(fnCallback) {
	an.bootstrapListeners.push(fnCallback);
	if(an.bootcompsLoaded.length > 0) {
		for(var i=0; i<an.bootcompsLoaded.length; ++i) {
			fnCallback(an.bootcompsLoaded[i]);
		}
	}
};

an.compositions = an.compositions || {};
an.compositions['3F63CCB6D2D1104694351256E9E34981'] = {
	getStage: function() { return exportRoot.getStage(); },
	getLibrary: function() { return lib; },
	getSpriteSheet: function() { return ss; },
	getImages: function() { return img; }
};

an.compositionLoaded = function(id) {
	an.bootcompsLoaded.push(id);
	for(var j=0; j<an.bootstrapListeners.length; j++) {
		an.bootstrapListeners[j](id);
	}
}

an.getComposition = function(id) {
	return an.compositions[id];
}



})(createjs = createjs||{}, AdobeAn = AdobeAn||{});
var createjs, AdobeAn;