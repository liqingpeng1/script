/**
*模拟器 页面顶部的Tab切换
*/
function simulaterManTab(e){
    var url = window.location.href;
    var id = $(e).attr("id");
    if(id == "car_simulater_tab"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/M_simulater_view/M_simulater_page");
    }else if(id == "car_simulaterSetting_tab"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/M_simulater_view/M_simulaterSetting_page");
    }else{
        alert(id)
    }
}