if(window.addEventListener) {
  window.addEventListener('load', function () {
  var canvas, context, tool, save_select, color;

  function init () {
    // Find the canvas element.
    canvas = document.getElementById('imageView');

    canvas.onselectstart = function(){return false;}
    canvas.onmousedown = function(){return false;}

    //save_select = document.getElementById('options');
    //save_select.addEventListener('change', ev_save_change, false);
    //save_select.value="";

    var saveButton = document.getElementById("saveButton");
    saveButton.addEventListener("click", canvas_save, false);

    context = canvas.getContext('2d');


    //make the background white
    //context.fillStyle = '#fff'; //white
    //context.fillRect(0,0,canvas.width,canvas.height);//x,y,w,h
    //draw some selectable color palettes
    context.fillStyle = '#000'; //black
    context.fillRect(0,0,30,30);//x,y,w,h
    context.fillStyle = '#f80'; //orange
    context.fillRect(30,0,30,30);
    context.fillStyle = '#00f';//blue
    context.fillRect(60,0,30,30);

    // Pencil tool instance.
    tool = new tool_pencil();

    // Attach the mousedown, mousemove and mouseup event listeners.
    canvas.addEventListener('mousedown', ev_canvas, false);
    canvas.addEventListener('mousemove', ev_canvas, false);
    canvas.addEventListener('mouseup',   ev_canvas, false);
  }

  function draw_background()
  {
        context.fillStyle = '#f8f';//white
        context.fillRect(0,0,canvas.width,canvas.height);
  }

  function canvas_save()
  {
       document.getElementById("actionInput").value = "save";

       var dataURL = canvas.toDataURL();
       document.getElementById("data").value = dataURL;

       document.getElementById("imgForm").submit();
  }

  function canvas_load(dataURL)
  {
        var imageObj = new Image();
        imageObj.src = dataURL;
        context.drawImage(imageObj, 0, 0);
  }

  function ev_save_change(ev){

      canvas_save();

      //save the canvas
      /*var save_option = document.getElementById('options');
      var dataURL;
      var data;
      if (save_option.value == "save")
      {
          save_option.value = "";
          dataURL=canvas.toDataURL();
          //document.getElementById("canvasImg").src=dataURL;
          data=context.getImageData(0,0,400,300);
          document.getElementById("fname").value = dataURL;
          document.getElementById('imgForm').submit();
            
      }*/

  }

  // This painting tool works like a drawing pencil which tracks the mouse 
  // movements.
  function tool_pencil () {
    var tool = this;
    this.started = false;

    // This is called when you start holding down the mouse button.
    // This starts the pencil drawing.
    this.mousedown = function (ev) {
        var x,y;
        x=ev._x;
        y=ev._y;

        if (x<30&&y<30)
        {
            color="black";
        }
        else if (x<60&&y<30)
        {
            color="orange";        
        }
        else if (x<90&&y<30)
        {
            color="blue";
        }
        else
        {
            context.beginPath();
            tool.started = true;
        }
    };

    // This function is called every time you move the mouse. Obviously, it only 
    // draws if the tool.started state is set to true (when you are holding down 
    // the mouse button).
    this.mousemove = function (ev) {
      if (tool.started&&ev._y>30) {
        context.lineTo(ev._x, ev._y);
        context.strokeStyle=color;
        context.stroke();
      }
    };

    // This is called when you release the mouse button.
    this.mouseup = function (ev) {
      if (tool.started) {
        tool.mousemove(ev);
        tool.started = false;
      }
    };
  }

  // The general-purpose event handler. This function just determines the mouse 
  // position relative to the canvas element.
  function ev_canvas (ev) {
    if (ev.layerX || ev.layerX == 0) { // Firefox
      ev._x = ev.layerX;
      ev._y = ev.layerY;
    } else if (ev.offsetX || ev.offsetX == 0) { // Opera
      ev._x = ev.offsetX;
      ev._y = ev.offsetY;
    }

    // Call the event handler of the tool.
    var func = tool[ev.type];
    if (func) {
      func(ev);
    }
  }

  init();

}, false); }

