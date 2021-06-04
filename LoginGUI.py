from wx import App, Frame, Panel, StaticText, ID_ANY, TextCtrl, Button, CheckBox, FlexGridSizer, BoxSizer, EXPAND, TE_PASSWORD, CENTER, VERTICAL, ALIGN_RIGHT, ALIGN_CENTER_VERTICAL, EVT_BUTTON, TE_PROCESS_ENTER, EVT_TEXT_ENTER
import DBConnection as DB

class LoginGUI(Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title, lang = "en"):
        self.Usr_ID = None
        # Inicializa o dicionário com linguas (inglês é default)
        if lang == "br":
            self.lang_w = {"Title_L":f"{title} - Loguin", "Title_N":"To Do List - Nova conta", "Login":"Loguin:", "Password":"Senha:", "PasswordC": "Confirme a senha:", "newAccC":"Cancelar", "autol": "Ativar auto login?", "newAcc":"Nova Conta"}
        else:
            self.lang_w = {"Title_L":f"{title} - Login", "Title_N":"To Do List - New Account", "Login":"Login:","Password":"Password:", "PasswordC": "Reenter Password:", "newAccC":"Cancel", "autol": "Turn on Auto Login?", "newAcc":"New Account"}
        # Inicializa a Frame com o título na lingua correta
        Frame.__init__(self, parent, title=self.lang_w["Title_L"])
        # Cria o sizer para a frame
        sizer = BoxSizer()
        self.SetSizer(sizer)
        # Cria o Painel para loguin
        self.login_panel = login(self, self.lang_w)
        sizer.Add(self.login_panel, 1, EXPAND)
        self.newacc_panel = newAcc(self, self.lang_w)
        sizer.Add(self.newacc_panel, 1, EXPAND)
        self.newacc_panel.Hide()
        # Cria a barra de status
        self.CreateStatusBar()
        # Mostra a frame com o painel de loguin
        self.Show(True)
    
    def showNewAcc(self):
        # Modifica o título da janela de acordo com a lingua
        self.SetTitle(self.lang_w["Title_N"])
        # Cria o Painel de nova conta
        self.newacc_panel.Show()
        self.login_panel.Hide()
        # Chama a funcão para clacular a visibilidade dos itens novamente
        self.Layout()
    
    def showLogin(self):
        # Modifica o título da janela de acordo com a lingua
        self.SetTitle(self.lang_w["Title_L"])
        # Cria o Painel de login novamente
        self.login_panel.Show()
        self.newacc_panel.Hide()
        # Chama a funcão para clacular a visibilidade dos itens novamente
        self.Layout()

class login(Panel):
    def __init__(self, parent, lang_w):
        Panel.__init__(self, parent)
        # Inicializa as variáveis
        self.parent = parent

        # Cria os Widgets do Painel
        login_L = StaticText(self, ID_ANY, lang_w["Login"])
        self.login_E = TextCtrl(self, size=(150,-1), style=TE_PROCESS_ENTER)
        pw_L = StaticText(self, ID_ANY, lang_w["Password"])
        self.pw_E = TextCtrl(self,  size=(150,-1), style=TE_PASSWORD | TE_PROCESS_ENTER)
        self.autol_CB = CheckBox(self, label=lang_w["autol"])
        n_acc_B = Button(self, ID_ANY, lang_w["newAcc"])
        # Sizer dos itens de login (username e password).
        main_sizer = FlexGridSizer(cols=2, vgap=10, hgap=10)
        main_sizer.Add(login_L, 0, ALIGN_CENTER_VERTICAL | ALIGN_RIGHT)
        main_sizer.Add(self.login_E, 0)
        main_sizer.Add(pw_L, 0, ALIGN_CENTER_VERTICAL)
        main_sizer.Add(self.pw_E, 0)
        # Placement do sizer externo
        sizer = BoxSizer(VERTICAL)
        sizer.AddStretchSpacer(prop=1)
        sizer.Add(main_sizer, 0, CENTER)
        sizer.AddSpacer(10)
        sizer.Add(self.autol_CB, 0, CENTER)
        sizer.AddSpacer(30)
        sizer.Add(n_acc_B, 0, CENTER)
        sizer.AddStretchSpacer(prop=1)
        self.SetSizer(sizer)
        # Eventos da interface.
        self.Bind(EVT_BUTTON, self.onNewAccClick, n_acc_B)
        self.Bind(EVT_TEXT_ENTER, self.onEntryEnter, self.login_E)
        self.Bind(EVT_TEXT_ENTER, self.onEntryEnter, self.pw_E)

    
    def onNewAccClick(self, e):
        self.parent.showNewAcc()
    
    def onEntryEnter(self, e):
        usr = self.login_E.GetValue()
        pw = self.pw_E.GetValue()
        autol = self.autol_CB.GetValue()

        with DB.Session() as session:
            usr_data = session.query(DB.Users).filter(DB.Users.usr == usr).first()
            if usr_data == None:
                print("O usuário informado não existe, digite corretamente o nome de usuário!")
            else:
                if (usr, pw) == (usr_data.usr, usr_data.passw):
                    if autol:
                        session.query(DB.Users).filter(DB.Users.usr == usr).update({"auto":True}, synchronize_session="fetch")
                        session.commit()
                    self.parent.Usr_ID = usr_data.id
                    self.parent.Destroy()
                else:
                    print("A senha informada está incorreta, tente novamente")


class newAcc(Panel):
    def __init__(self, parent, lang_w):
        Panel.__init__(self, parent)
        self.parent = parent

        login_L = StaticText(self, ID_ANY, lang_w["Login"])
        self.login_E = TextCtrl(self, size=(150,-1), style=TE_PROCESS_ENTER)
        pw_L = StaticText(self, ID_ANY, lang_w["Password"])
        self.pw_E = TextCtrl(self,  size=(150,-1), style=TE_PASSWORD | TE_PROCESS_ENTER)
        pwC_L = StaticText(self, ID_ANY, lang_w["PasswordC"])
        self.pwC_E = TextCtrl(self,  size=(150,-1), style=TE_PASSWORD | TE_PROCESS_ENTER)
        n_acc_B = Button(self, ID_ANY, lang_w["newAccC"])
        # Sizer dos itens de login (username e password).
        main_sizer = FlexGridSizer(cols=2, vgap=10, hgap=10)
        main_sizer.Add(login_L, 0, ALIGN_CENTER_VERTICAL | ALIGN_RIGHT)
        main_sizer.Add(self.login_E, 0)
        main_sizer.Add(pw_L, 0, ALIGN_CENTER_VERTICAL | ALIGN_RIGHT)
        main_sizer.Add(self.pw_E, 0)
        main_sizer.Add(pwC_L, 0, ALIGN_CENTER_VERTICAL)
        main_sizer.Add(self.pwC_E, 0)
        # Placement do sizer externo
        sizer = BoxSizer(VERTICAL)
        sizer.AddStretchSpacer(prop=1)
        sizer.Add(main_sizer, 0, CENTER)
        sizer.AddSpacer(20)
        sizer.Add(n_acc_B, 0, CENTER)
        sizer.AddStretchSpacer(prop=1)
        self.SetSizer(sizer)
        # Eventos da interface.
        self.Bind(EVT_BUTTON, self.onCancelClick, n_acc_B)
        self.Bind(EVT_TEXT_ENTER, self.onEntryEnter, self.login_E)
        self.Bind(EVT_TEXT_ENTER, self.onEntryEnter, self.pw_E)
        self.Bind(EVT_TEXT_ENTER, self.onEntryEnter, self.pwC_E)
    
    def onCancelClick(self, e):
        self.parent.showLogin()
    
    def onEntryEnter(self, e):
        
        usr = self.login_E.GetValue().strip().lower()
        senha = self.pw_E.GetValue().strip()
        senha_c = self.pwC_E.GetValue().strip()
        
        with DB.Session() as session:
            if usr and senha and senha_c:
                if senha == senha_c:
                    usr_db = session.query(DB.Users).filter(DB.Users.usr == usr).first()         
                    if usr_db is None:
                        new_user = DB.Users(usr=usr, passw=senha, auto=False, lang="en")
                        session.add(new_user)
                        session.commit()
                        self.parent.showLogin()
                    else:
                        print("Este Usuário já existe, insira um nome de usuário diferente!")
                else:
                    print("As senhas digitas são diferentes!")
            else:
                print("ERRO: Por favor, defina usuário e senha!")

if __name__ == "__main__":
    app_l = App(False)
    frame_l = LoginGUI(None, "To Do List")
    app_l.MainLoop()
