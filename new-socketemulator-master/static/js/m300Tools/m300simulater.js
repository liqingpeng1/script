/**
*m300simulater 页面顶部的tab切换
*/
function m300SimulaterTab(e){
    var url = window.location.href;
    var id = $(e).attr("id");
    if(id == "m300simulater_tab"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/M_m300Simulater_view/M_m300Simulater_page");
    }else if(id == "m300_setting_tab"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/M_m300Simulater_view/M_m300Setting_page");
    }else{
        alert(id)
    }
}