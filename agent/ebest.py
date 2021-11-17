import configparser
import win32com.client
import pythoncom

class XASession:
    login_state = 0

    def OnLogin(self, code, msg):
        if code =="0000":
            print(code, msg)
            XASession.login_state = 1
        else:
            print(code, msg)

    def OnDisconnect(self):
        print("Session disconnected")
        XASession.login_state = 0

class EBest:
    def __init__(self, mode = None):
        if mode not in ["PROD", "DEMO"]:
            raise Exception("Need to run_mode(PROD or DEMO)")
        run_mode = "EBEST_"+mode
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.user = config[run_mode]['user']
        self.passwd = config[run_mode]['passwd']
        self.cert_passwd = config[run_mode]['cert_passwd']
        self.host = config[run_mode]['host']
        self.port = config[run_mode]['port']
        self.account = config[run_mode]['account']

        self.xa_session_client = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)

    def login(self):
        self.xa_session_client.ConnectServer(self.host, self.port)
        self.xa_session_client.Login(self.user, self.passwd, self.cert_passwd, 0, 0)
        while XASession.login_state == 0:
            pythoncom.PumpwaitingMessages()

    def logout(self):
         #result = self.xa_session_client_Logout()
         # #if result:
         XASession.login_state = 0
         self.xa_session_client.DisconncetServer()   

class XAQuery:
    RES_PATH = "C:\\eBEST\\xingAPI\\Res\\"
    tr_run_state = 0

    def OnReceiveData(self, code):
        print("OnReceiveData", code)
        XAQuery.tr_run_state = 1

    def OnReceiveMessage(self, error, code, message):
        print("OnreceiveMessage", error, code, message)


