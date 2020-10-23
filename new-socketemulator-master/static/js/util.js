/*
辅助函数js文件
*/

//定义一个获取当前时间的函数
function getCurTime(){
    var myDate = new Date;
    var year = myDate.getFullYear(); //获取当前年
    var mon = myDate.getMonth() + 1; //获取当前月
    if(String(mon).length < 2) mon = "0" + String(mon)
    var date = myDate.getDate(); //获取当前日
    if(String(date).length < 2) date = "0" + String(date)

    var h = myDate.getHours();//获取当前小时数(0-23)
    if(String(h).length < 2) h = "0" + String(h)
    var m = myDate.getMinutes();//获取当前分钟数(0-59)
    if(String(m).length < 2) m = "0" + String(m)
    var s = myDate.getSeconds();//获取当前秒
    if(String(s).length < 2) s = "0" + String(s)
    var week = myDate.getDay();

    var now = year + "-" + mon + "-" + date + " " + h + ":" + m + ":" + s;

    return now;
}

//定义一个获取当前时间戳的函数
function getCutTimestamp(){
    var timestamp = Date.parse(new Date());
//    var timestamp = (new Date()).valueOf()
//    var timestamp=new Date().getTime()
    timestamp = String(timestamp);
    timestamp = timestamp.slice(0,10);
    return timestamp;
}

//时间格式转换为时间搓（返回的时间搓为毫秒格式）
function DateToTimestamp(string) {
    var f = string.split(' ', 2);
    var d = (f[0] ? f[0] : '').split('-', 3);
    var t = (f[1] ? f[1] : '').split(':', 3);
    var time = (new Date(
        parseInt(d[0], 10) || null,
        (parseInt(d[1], 10) || 1) - 1,
        parseInt(d[2], 10) || null,
        parseInt(t[0], 10) || null,
        parseInt(t[1], 10) || null,
        parseInt(t[2], 10) || null
    //)).getTime() / 1000
    )).getTime()
    return time;
}

//时间戳转换为时间（时间戳为毫秒格式）
function formatDate(timeStamp) {
    var d = new Date(timeStamp);
    var year=d.getFullYear();  //取得4位数的年份
    var month=d.getMonth()+1;  //取得日期中的月份，其中0表示1月，11表示12月
    if(month < 10){ month = "0" + month;}
    var date=d.getDate();      //返回日期月份中的天数（1到31）
    if(date < 10){ date = "0" + date;}
    var hour=d.getHours();     //返回日期中的小时数（0到23）
    if(hour < 10){ hour = "0" + hour;}
    var minute=d.getMinutes(); //返回日期中的分钟数（0到59）
    if(minute < 10){ minute = "0" + minute;}
    var second=d.getSeconds(); //返回日期中的秒数（0到59）
    if(second < 10){ second = "0" + second;}
    return year+"-"+month+"-"+date+" "+hour+":"+minute+":"+second;
}