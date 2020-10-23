/**
*protocols 页面顶部的协议切换
*/
function m300ProtocolManTab(e){
    var url = window.location.href;
    var id = $(e).attr("id");
    if(id == "P_heartBeat_m300_msg"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_heartBeat_m300_page");
    }else if(id == "socketSetting"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/socketSetting_page");
    }else if(id == "P_userDefined_m300_msg"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_userDefined_m300_page");
    }else if(id == "P_login_m300_msg"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_login_m300_page");
    }else if(id == "P_version_m300_msg"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_version_m300_page");
    }else if(id == "P_GPS_m300_msg"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_GPS_m300_page");
    }else if(id == "P_CAN_m300_msg"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_CAN_m300_page");
    }else if(id == "P_alarm_m300_msg"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_alarm_m300_page");
    }else if(id == "P_travelAct_m300_msg"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_travelAct_m300_page");
    }else{
        alert(id)
    }
}
