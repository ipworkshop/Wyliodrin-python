var numnum = 0;
//var numxml = 0;
var requestArray = new Array();
function GetXmlHttpObject(available){
    this.xmlhttp=false;
    this.available = available;
    try {
        // Firefox, Opera 8.0+, Safari
        this.xmlhttp=new XMLHttpRequest();
    } catch (e){
        // Internet Explorer
        try{
            this.xmlhttp=new ActiveXObject("Msxml2.XMLHTTP");
        }catch (e){
            this.xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
    }
    //return xmlHttp;
}

function vPage(iid,urlstr){
    numxml = -1;
    for (var i=0; i<requestArray.length; i++){
        if (requestArray[i].available == 1){
            numxml = i;
            break;
        }
    }
    if (numxml == -1){
        numxml = requestArray.length;
        requestArray[numxml] = new GetXmlHttpObject(1);
    }
    //xmlHttp = xmlArray[numxml];
    var useLoad = arguments[2];
    if (requestArray[numxml].xmlhttp != false){
        requestArray[numxml].available = 0;
        requestArray[numxml].xmlhttp.open("GET",urlstr,true);
        requestArray[numxml].xmlhttp.send(null);
        requestArray[numxml].div = iid;
        requestArray[numxml].xmlhttp.onreadystatechange=function(){
            if(requestArray[numxml].xmlhttp.readyState==4){
                if (requestArray[numxml].xmlhttp.responseText != '') document.getElementById(requestArray[numxml].div).innerHTML = requestArray[numxml].xmlhttp.responseText;
                requestArray[numxml].available = 1;
            }
        }
        if (useLoad == null) document.getElementById(iid).innerHTML = '<div class="loading">Loading...</div>' + document.getElementById(requestArray[numxml].div).innerHTML;    
    }else{
        alert ("Your browser does not support AJAX"); 
        return;
    }
}