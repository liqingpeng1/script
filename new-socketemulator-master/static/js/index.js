/**
*页面顶部的tab切换
*/
function  swichTap(e){
    var id = $(e).attr("id")
    if(id == "protocolTools"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/GPS_protocol_page");
    }else if(id == "messageTools"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/message_view/heartBeat_msg_page");
    }else if(id == "m300Tools"){
        $(location).attr('href', "http://" + window.location.host + "/m300Tools/P_m300Protocol_view/P_heartBeat_m300_page");
    }else if(id == "otherTools"){
        $(location).attr('href', "http://" + window.location.host + "/otherTools/mapTools_view/maptool_page");
    }
}
