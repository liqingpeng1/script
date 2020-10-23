from flask import Flask, redirect

from views.protocolTools.setting_view import setting_view
from views.protocolTools.setting_process import setting_process
from views.protocolTools.protocolReport_view import protocolReport_view
from views.protocolTools.protocolReport_process import protocolReport_process
from views.protocolTools.M_carSimulater_view import M_carSimulater_view
from views.protocolTools.M_carSimulater_process import M_carSimulater_process
from views.protocolTools.test_view import test_view

from views.m300Tools.P_m300Protocol_view import P_m300Protocol_view
from views.m300Tools.P_m300Protocol_process import P_m300Protocol_process
from views.m300Tools.M_m300Simulater_view import M_m300Simulater_view
from views.m300Tools.M_m300Simulater_process import M_m300Simulater_process

from views.messageTools.msgSetting_view import msgSetting_view
from views.messageTools.msgSetting_process import msgSetting_process
from views.messageTools.message_view import message_view
from views.messageTools.message_process import message_process
from views.messageTools.M_simulater_view import M_simulater_view
from views.messageTools.M_simulater_process import M_simulater_process

from views.otherTools.mapTools_view import mapTools_view
from views.otherTools.mapTools_process import mapTools_process

app = Flask(__name__)
app.register_blueprint(setting_view,url_prefix = "/protocolTools/setting_view")
app.register_blueprint(setting_process,url_prefix = "/protocolTools/setting_process")
app.register_blueprint(protocolReport_view,url_prefix = "/protocolTools/protocolReport_view")
app.register_blueprint(protocolReport_process,url_prefix = "/protocolTools/protocolReport_process")
app.register_blueprint(M_carSimulater_view,url_prefix = "/protocolTools/M_carSimulater_view")
app.register_blueprint(M_carSimulater_process,url_prefix = "/protocolTools/M_carSimulater_process")
app.register_blueprint(test_view,url_prefix = "/protocolTools/test_view")

app.register_blueprint(P_m300Protocol_view,url_prefix = "/m300Tools/P_m300Protocol_view")
app.register_blueprint(P_m300Protocol_process,url_prefix = "/m300Tools/P_m300Protocol_process")
app.register_blueprint(M_m300Simulater_view,url_prefix = "/m300Tools/M_m300Simulater_view")
app.register_blueprint(M_m300Simulater_process,url_prefix = "/m300Tools/M_m300Simulater_process")

app.register_blueprint(msgSetting_view,url_prefix = "/messageTools/msgSetting_view")
app.register_blueprint(msgSetting_process,url_prefix = "/messageTools/msgSetting_process")
app.register_blueprint(message_view,url_prefix = "/messageTools/message_view")
app.register_blueprint(message_process,url_prefix = "/messageTools/message_process")
app.register_blueprint(M_simulater_view,url_prefix = "/messageTools/M_simulater_view")
app.register_blueprint(M_simulater_process,url_prefix = "/messageTools/M_simulater_process")

app.register_blueprint(mapTools_view,url_prefix = "/otherTools/mapTools_view")
app.register_blueprint(mapTools_process,url_prefix = "/otherTools/mapTools_process")

@app.route('/')
def hello():
    return redirect('/messageTools/message_view/heartBeat_msg_page')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')