/**
*messages 页面顶部的协议切换
*/
function messageManTab(e){
    var url = window.location.href;
    var id = $(e).attr("id");
    if(id == "terminalHeartBeat_msg"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/message_view/heartBeat_msg_page");
    }else if(id == "terminalRegister_msg"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/message_view/terminalRegister_msg_page");
    }else if(id == "terminalVersionInfoUpload_msg"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/message_view/terminalVersionInfoUpload_msg_page");
    }else if(id == "dataUpstreamTransport_msg"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/message_view/dataUpstreamTransport_msg_page");
    }else if(id == "location_msg"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/message_view/location_msg_page");
    }else if(id == "userDefined_msg"){
        $(location).attr('href', "http://" + window.location.host + "/messageTools/message_view/userDefined_msg_page");
    }else{
        alert(id)
    }
}