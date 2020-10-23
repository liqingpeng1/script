/**
*carsimulater 页面顶部的tab切换
*/
function carSimulaterTab(e){
    var url = window.location.href;
    var id = $(e).attr("id");
    if(id == "carsimulater_tab"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/M_carSimulater_view/M_carSimulater_page");
    }else if(id == "setting_tab"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/M_carSimulater_view/M_setting_page");
    }else if(id == "carsimulaterData_tab"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/M_carSimulater_view/M_carSimulaterData_page");
    }else{
        alert(id)
    }
}