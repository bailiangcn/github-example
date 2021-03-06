//打开area.xml文件，读取区域列表
//生成区域的选择菜单
if (window.XMLHttpRequest) {
    // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp=new XMLHttpRequest();
}
else {
    // code for IE6, IE5
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
//读取服务组信息

xmlhttp.open("GET","./addressdata/area.xml",false);
xmlhttp.send();
xmlDoc=xmlhttp.responseXML;
var x=xmlDoc.getElementsByTagName("regional");
//生成区域的选择菜单
for (i=0;i<x.length;i++) {
    if (x[i].getElementsByTagName("valid")[0].childNodes[0].nodeValue==1) {
        var option=document.createElement("option");
        option.text = x[i].getElementsByTagName("name")[0]
            .childNodes[0].nodeValue; 
        option.value = x[i].getElementsByTagName("datafile")[0]
            .childNodes[0].nodeValue;
        option.id = "reg"+x[i].getElementsByTagName("id")[0]
            .childNodes[0].nodeValue;
        document.form1.regional.options.add(option);	  
    }
}

//通过读取xml文件，设置区域、小区、楼号
//生成小区的选择菜单
function getCommunity(){
    //清空地址信息
    document.form2.message.value='';
    document.form2.server.value='';
    document.getElementById('servicename').innerHTML=""; 
    //获得区域下拉框的对象
     var sltregional=document.form1.regional;
    //获得小区下拉框的对象
     var sltcommunity=document.form1.community;
    //获得楼号下拉框的对象
    var slthouse=document.form1.house;
    //清空小区、楼号下拉框，仅留提示选项
    sltcommunity.length=1;
    slthouse.length=1;
    //如果选择了有效区域
    if ( sltregional.selectedIndex >0){
        //取得小区xml文件名，生成小区选择列表
        var xmlfilename="./addressdata/"+
            sltregional.options[sltregional.selectedIndex].value+".xml";
        if (window.XMLHttpRequest) {
            // code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp=new XMLHttpRequest();
        }
        else {
            // code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.open("GET",xmlfilename,false);
        xmlhttp.send();
        xmlDoc=xmlhttp.responseXML;
        var x=xmlDoc.getElementsByTagName("community");
                              
        //生成小区的选择菜单
        for (i=0;i<x.length;i++) {
            if (x[i].nodeType==1){
                txt=x[i].getAttribute("name");
                var option=document.createElement("option");
                option.text = txt; 
                option.value = txt;
                sltcommunity.options.add(option);	  
            }
        }
    }
    makeMessage();
}

//生成楼号的选择菜单
function getHouse(){
    //清空地址信息
    document.form2.message.value=''
    document.form2.server.value='';
    document.getElementById('servicename').innerHTML=""; 
    //获得区域下拉框的对象
    var sltregional=document.form1.regional;
    //获得小区下拉框的对象
    var sltcommunity=document.form1.community;
    //获得楼号下拉框的对象
    var slthouse=document.form1.house;
    //清空楼号下拉框，仅留提示选项
    slthouse.length=1;
    if ( sltcommunity.selectedIndex >0){
        //取得小区xml文件名，生成小区选择列表
        var xmlfilename="./addressdata/"+sltregional.
            options[sltregional.selectedIndex].value+".xml";
        var regid=sltregional.options[sltregional.selectedIndex].id;
        if (window.XMLHttpRequest) {
            // code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp=new XMLHttpRequest();
        }
        else {
            // code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.open("GET",xmlfilename,false);
        xmlhttp.send();
        xmlDoc=xmlhttp.responseXML;
        //取得选择的小区名称,生成楼号列表
        var x=xmlDoc.getElementsByTagName("community")
            [sltcommunity.selectedIndex-1].childNodes;
        var y;
        var txt="";
        var service="";
        //生成楼号的选择菜单
        for (i=0;i<x.length;i++) {
            if (x[i].nodeType==1){
                y=x[i].childNodes;
                for (j=0;j<y.length;j++){
                    if (y[j].nodeType==1){
                        switch (y[j].nodeName){
                            case "number":
                                txt=x[i].childNodes[j].textContent;
                                break;
                            case "id":
                                houseid="house"+x[i].childNodes[j].textContent;
                        } 
                    }
                }
                var option=document.createElement("option");
                option.text = txt; 
                option.value = houseid;
                option.regid=regid;
                slthouse.options.add(option);	  
            }
        }
    }
    makeMessage();
}

//生成短信字符串
function makeMessage(){
    var tamess="";
    var tempnum=0;
    var selectnum=0;
    if (document.form1.regional.selectedIndex != 0){ //选择了大区
        if (document.form1.community.selectedIndex != 0){//选择了小区
            tamess += document.form1.community.value+" ";
            if (document.form1.house.selectedIndex != 0){//选择了楼号
                selectnum=document.form1.house.selectedIndex;
                tamess += document.form1.house.options[selectnum].text + "号楼 ";
                if (document.form1.unit.selectedIndex != 0){//选择了单元
                    tempnum=Number(document.form1.unit.value) +countUnit();
                    tamess += tempnum+ "单元 ";
                    if (document.form1.layer.selectedIndex != 0){//选择了层位
                        tempnum=Number(document.form1.layer.value) +countLayer();
                        tamess += tempnum + "层 ";
                        if (document.form1.number.selectedIndex != 0) {//选择了门牌
                            tempnum=Number(document.form1.number.value) +countNumber();
                            tamess += tempnum+ "室";
                            }
                    }
                }
            }
        }
	}
    document.form2.message.value=tamess;
}
//计算单元基数加10
function countUnit(){
    var res=0;
    if (document.form1.unitdec1.checked){res+=1}
    if (document.form1.unitdec2.checked){res+=1}
    if (document.form1.unitdec3.checked){res+=1}
    document.getElementById("unitdec").innerHTML="+"+res*10;
    return res*10;
}
//计算层位基数加10
function countLayer(){
    var res=0;
    if (document.form1.layerdec1.checked){res+=1}
    if (document.form1.layerdec2.checked){res+=1}
    if (document.form1.layerdec3.checked){res+=1}
    document.getElementById("layerdec").innerHTML="+"+res*10;
    return res*10;
}
//计算门牌基数加10
function countNumber(){
    var res=0;
    if (document.form1.numberdec1.checked){res+=1}
    if (document.form1.numberdec2.checked){res+=1}
    if (document.form1.numberdec3.checked){res+=1}
    document.getElementById("numberdec").innerHTML="+"+res*10;
    return res*10;
}
//向服务器提交短信内容
function postmess(mess,phone){
    alert("posting message:"+mess+":"+phone);
}
function makeHouse(){
//查询该楼的服务信息和电话，生成地址字符串
makeMessage();
var slthouse=document.form1.house;
if ( slthouse.selectedIndex >0){
    var areaid=slthouse.options[slthouse.selectedIndex].regid;
    var houseid=slthouse.options[slthouse.selectedIndex].value;
    checkservice(areaid.substr(3),houseid.substr(5));
    }
else{
    document.form2.server.value='';
    document.getElementById('servicename').innerHTML=""; 
    }
}
//向服务器查询服务组及电话
function checkservice(areaid,houseid){
    xmlhttp.onreadystatechange = handleStateChange;   
    var localurl=document.referrer;
    //如果末尾有#去掉
    if (localurl.charAt(localurl.length-1)=="#"){
    localurl=localurl.substring(0,localurl.length-1)}
    var qur= localurl+"src/ajax.ks/findser?areaid="+
        areaid+"&houseid="+houseid;
    //发送请求到的URL地址
    xmlhttp.open("GET", qur, true);
    xmlhttp.send();
};
function handleStateChange() {        
    if(xmlhttp.readyState == 4) {                
        if(xmlhttp.status == 200) {
            res=xmlhttp.responseText;
            if (res!=""){
                var arr=res.split(":");
                document.form2.server.value=arr[1];
                if (arr[0] != ''){
                    document.getElementById('servicename').innerHTML="第"
                        +arr[0]+"组"; }
                else{ document.getElementById('servicename').innerHTML="默认组"; 

                }
             }
        }
    };
}
function clearform(){
    document.form2.reset();
    document.getElementById('servicename').innerHTML=""; 
}
