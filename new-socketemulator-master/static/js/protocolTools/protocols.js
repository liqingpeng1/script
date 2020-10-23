/**
*protocols 页面顶部的协议切换
*/
function protocolManTab(e){
    var url = window.location.href;
    var id = $(e).attr("id");
    if(id == "heartBeat_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/heartBeat_protocol_page");
    }else if(id == "userDefined_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/userDefined_protocol_page");
    }else if(id == "login_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/login_protocol_page");
    }else if(id == "GPS_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/GPS_protocol_page");
    }else if(id == "OBD_CAN_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/OBD_CAN_protocol_page");
    }else if(id == "securityStatus_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/securityStatus_protocol_page");
    }else if(id == "voltageData_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/voltageData_protocol_page");
    }else if(id == "event_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/event_protocol_page");
    }else if(id == "troubleCode_protocol"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/protocolReport_view/troubleCode_protocol_page");
    }else{
        alert(id)
    }
}

