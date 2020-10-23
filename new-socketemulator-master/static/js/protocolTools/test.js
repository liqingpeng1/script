/**
*test 页面顶部的Tab且换
*/
function testManTab(e){
    var url = window.location.href;
    var id = $(e).attr("id");
    if(id == "test"){
        $(location).attr('href', "http://" + window.location.host + "/protocolTools/test_view/test_page");
    }else{
        alert(id)
    }
}