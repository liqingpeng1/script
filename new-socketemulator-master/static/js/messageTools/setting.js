/**
*setting 页面顶部的协议切换
*/
function settingManTab(e){
    var url = window.location.href;
    var id = $(e).attr("id");
    if(id == "msgSetting"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/msgSetting_view/msgSetting_page");
    }else if(id == "style_labels1"){
        $(location).attr('href', "http://" + window.location.host + "/tab1/style/labels");
    }else{
        alert(id)
    }
}