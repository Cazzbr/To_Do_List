from wx import App, Frame, Panel, ScrolledWindow, Icon, BITMAP_TYPE_ICO, StaticText, TextCtrl, Button, CheckBox, Control, BoxSizer, FlexGridSizer, Menu,ID_ANY, ID_ABOUT, ID_EXIT, ID_SETUP, MenuBar, EVT_MENU, EVT_BUTTON, EVT_SIZE, EVT_CHECKBOX, EVT_TEXT_ENTER, EVT_TEXT, MessageDialog, Dialog, OK, DisplaySize, Notebook, VERTICAL, HORIZONTAL, CENTER, ALIGN_CENTER_VERTICAL, ALIGN_RIGHT, EXPAND, TE_CENTRE, TE_MULTILINE, TE_READONLY, TE_PROCESS_ENTER, TE_PASSWORD, ALL, TOP, LEFT, RIGHT, BOTTOM, NO_BORDER, SUNKEN_BORDER, DefaultPosition, DefaultSize, DefaultValidator
from wx.lib.scrolledpanel import ScrolledPanel
from wx.lib.stattext import GenStaticText
from datetime import date, datetime, timedelta
from types import SimpleNamespace
from LoginGUI import LoginGUI
import DBConnection as DB
from pt import pt
from en import en
from sys import executable, argv
from os import execl

# Setting up SimpleNamespace for language support
class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)

# Creating a "Global" dictionary for language support
language_support = {}
language_support.update({"pt": NestedNamespace(pt)})
language_support.update({"en": NestedNamespace(en)})                

# Defining a funcion to handle the init os the app
def To_Do_List_init():
    Usr_ID = None
    # Verifica se existe usuário para auto loguin
    with DB.Session() as session:
        Usr_data = session.query(DB.Users).filter(DB.Users.auto == True).first()

    if Usr_data == None:
        app_l = App(False)
        frame_l = LoginGUI(None, "To DO List")
        app_l.MainLoop()
        Usr_ID = frame_l.Usr_ID
    else:
        Usr_ID = Usr_data.id

    if Usr_ID != None:
        with DB.Session() as session:
            user = session.query(DB.Users).filter(DB.Users.id == Usr_ID).first()

        app = App(False)
        frame = To_DO_Window(None, 'To Do List', Usr_ID, user.lang)
        #import wx.lib.inspection
        #wx.lib.inspection.InspectionTool().Show()
        app.MainLoop()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = executable
    execl(python, python, * argv)

# Panel class derived from wx.Panel for every task on the app, intended to be used on the "To DO" page and "Done" as well
class To_Do_Task(Panel):
    def __init__(self, parent, task):
        # Initializing the Panel attributes
        Panel.__init__(self, parent, style=SUNKEN_BORDER)
        self.lang = parent.lang
        self.task = task
        self.parent = parent
        if task.prio != None:
            self.prio = task.prio
        else:
            self.prio = ""
        if task.dia_c != None:
            self.date_conc = task.dia_c
        else:
            self.date_conc = ""
        
        # Crearing the sizers
        sizer = BoxSizer(HORIZONTAL)
        prio_sizer = BoxSizer(VERTICAL)
        main_sizer = FlexGridSizer(cols=2, vgap=5, hgap=5)
        main_sizer.AddGrowableCol(1, 1)
        main_sizer.AddGrowableRow(1, 1)
        date_sizer = BoxSizer(VERTICAL)
        btn_sizer = BoxSizer(VERTICAL)
        
        # Elements of the CB created
        cb = CheckBox(self, label=language_support[self.lang].to_do_task.done)
        
        # Elements of the prio_sizer
        prio_L = StaticText(self, ID_ANY, language_support[self.lang].to_do_task.prio)
        self.prio_E = TextCtrl(self, ID_ANY, str(self.prio), size=(60,-1), style= TE_PROCESS_ENTER | TE_CENTRE)
        prio_sizer.Add(prio_L, 0, CENTER)
        prio_sizer.Add(self.prio_E, 0, CENTER)
        
        # Elements of the main_sizer
        titulo_L = StaticText(self, ID_ANY, language_support[self.lang].to_do_task.title)
        titulo = StaticText(self, ID_ANY, f"{task.title.capitalize()}") 
        desc_L = StaticText(self, ID_ANY, language_support[self.lang].to_do_task.desc)
        desc = TextCtrl(self, ID_ANY, value=task.descr.capitalize(), style=TE_READONLY | NO_BORDER | TE_MULTILINE)
        main_sizer.Add(titulo_L, 0, ALIGN_RIGHT)
        main_sizer.Add(titulo)
        main_sizer.Add(desc_L, 0, ALIGN_CENTER_VERTICAL)
        main_sizer.Add(desc, 1, EXPAND)
        
        # Elements of the date_sizer
        date_i = StaticText(self, ID_ANY, language_support[self.lang].to_do_task.date_i)
        date_i_db = StaticText(self, ID_ANY, f"{task.dia}")
        date_c = StaticText(self, ID_ANY, language_support[self.lang].to_do_task.date_c)
        date_c_db = StaticText(self, ID_ANY, f"{self.date_conc}")
        date_sizer.Add(date_i, 0, CENTER)
        date_sizer.Add(date_i_db, 0, CENTER)
        date_sizer.Add(date_c, 0, CENTER)
        date_sizer.Add(date_c_db,0, CENTER)
        

        # Elements of the btn_sizer
        self.edit_btn = Button(self, ID_ANY, language_support[self.lang].to_do_task.edit_btn)
        del_btn = Button(self, ID_ANY, language_support[self.lang].to_do_task.del_btn)
        btn_sizer.Add(self.edit_btn, 0, CENTER)
        btn_sizer.AddSpacer(5)
        btn_sizer.Add(del_btn, 0, CENTER)

        # Sizer os Sizers
        sizer.Add(cb, 0, ALIGN_CENTER_VERTICAL)
        sizer.Add(prio_sizer, 0, ALIGN_CENTER_VERTICAL | LEFT | RIGHT, 10)
        sizer.Add(main_sizer, 1, EXPAND)
        sizer.Add(date_sizer, 0, ALIGN_CENTER_VERTICAL | LEFT | RIGHT, 10)
        sizer.Add(btn_sizer, 0, ALIGN_CENTER_VERTICAL)
        
        # Set the sizer for the border
        border_sizer = BoxSizer(VERTICAL)
        border_sizer.Add(sizer, 0, EXPAND | ALL, 10)
        
        # Set the last sizer to the Panel
        self.SetSizer(border_sizer)
        
        cb.SetValue(self.task.done)
        
        # Bindings for the tasks
        self.Bind(EVT_CHECKBOX, self.onDoneCBClick, cb)
        self.Bind(EVT_TEXT_ENTER, self.setPrio, self.prio_E)
        self.Bind(EVT_BUTTON, lambda e, task_id=self.task.id: self.onEditButton(e, task_id), self.edit_btn)
        self.Bind(EVT_BUTTON, lambda e, task_id=self.task.id: self.onDelButton(e, task_id), del_btn)
        
    def onEditButton(self, e, task_id):
        self.parent.main_window.editTask(task_id)
    
    def onDelButton(self, e, task_id):
        with DB.Session() as session:
            session.query(DB.Data).filter(DB.Data.id == task_id).delete()
            session.commit()
        self.parent.updatePage()
    
    def onDoneCBClick(self, e):          
        obj = e.GetEventObject()
        checked = obj.IsChecked()
        with DB.Session() as session:
            session.query(DB.Data).filter(DB.Data.id == self.task.id).update({"done":checked}, synchronize_session="fetch")
            if checked:
                session.query(DB.Data).filter(DB.Data.id == self.task.id).update({"prio":None, "dia_c":datetime.today()}, synchronize_session="fetch")
            else:
                session.query(DB.Data).filter(DB.Data.id == self.task.id).update({"dia_c":None}, synchronize_session="fetch")
            session.commit()
        self.parent.main_window.To_Do_Panel.updatePage()
        self.parent.main_window.Done_Panel.updatePage() 
     
    def setPrio(self, e):
        obj = e.GetEventObject()
        prio = obj.GetValue()
        try:
            prio_int = int(prio)
        except:
            obj.SetValue("")
        else:
            with DB.Session() as session:
                session.query(DB.Data).filter(DB.Data.id == self.task.id).update({"prio":prio}, synchronize_session="fetch")
                session.commit()
        self.parent.main_window.To_Do_Panel.updatePage()
        self.parent.main_window.Done_Panel.updatePage()
        #self.parent.main_window.SetFocus()

# Panel class derived from wx.Panel for the "To Do" and "Done" tabs of the wx.Notebook
class To_Do_Page(ScrolledPanel):
    def __init__(self, parent, main_window, done, ifEmptyText):
        ScrolledPanel.__init__(self, parent)
        self.SetAutoLayout(True)
        self.SetupScrolling(scroll_x=False)
        
        self.lang = main_window.lang
        self.main_window = main_window
        self.done = done
        self.ifEmptyText = ifEmptyText
        
        self.sizer = BoxSizer(VERTICAL)
        
        self.create()
        
        # Add Sizer for the margins
        margin_sizer = BoxSizer(HORIZONTAL)
        margin_sizer.Add(self.sizer, 1, ALL, 20)
        
        self.SetSizer(margin_sizer)
    
    def create(self):
        # Recebe todas as tarefas do banco de dados:
        with DB.Session() as session:
            Tasks = session.query(DB.Data).filter(DB.Data.user_id == self.main_window.Usr_ID, DB.Data.done == self.done).order_by(DB.Data.prio).all()
        
        if not Tasks:
            self.sizer.Add(StaticText(self, ID_ANY, self.ifEmptyText), 0 , CENTER | ALL, 100)
        else:
            for task in Tasks:
                self.addTask(task)
        
    def addTask(self, task):
        T = To_Do_Task(self, task)
        if self.done:
            T.prio_E.Disable()
            T.edit_btn.Disable()
        self.sizer.Add(T, 1, EXPAND | BOTTOM, 10)
        self.main_window.Layout()
    
    def updatePage(self):
        for i in self.sizer.GetChildren():
            widget = i.GetWindow()
            self.sizer.Hide(widget)
            widget.Destroy()
        self.create()
        self.Layout()
        self.Fit()
        self.FitInside()
        
# Panel class derived from wx.Panel for the "New" wx.Notebook tab (create new tasks).
class newTask(Panel):
    def __init__(self, parent, main_window, task_id=None):
        self.Usr_ID = main_window.Usr_ID 
        self.lang = main_window.lang
        self.main_window = main_window
        Panel.__init__(self, parent)
        titulo = StaticText(self, ID_ANY, language_support[self.lang].new_page.title)
        self.titulo_E = TextCtrl(self)
        desc = StaticText(self, ID_ANY, language_support[self.lang].new_page.desc)
        self.desc_E = TextCtrl(self, size=(-1, 300),  style=TE_MULTILINE)
        btn = Button(self, ID_ANY, language_support[self.lang].new_page.save_btn)
             
        sizer = BoxSizer(VERTICAL)
        sizer.Add(titulo, 0)
        sizer.Add(self.titulo_E, 0, EXPAND)
        sizer.AddSpacer(20)
        sizer.Add(desc, 0)
        sizer.Add(self.desc_E, 0, EXPAND)
        sizer.AddSpacer(20)
        sizer.Add(btn)
        
        margin_sizer = BoxSizer(HORIZONTAL)
        margin_sizer.Add(sizer, 1, ALL, 50)
        self.SetSizer(margin_sizer)
        
        self.Bind(EVT_BUTTON, lambda e, task_id = task_id:self.onSaveBtn(e, task_id), btn)
    
    # Save a new task onto DB
    def onSaveBtn(self, e, editing_task):
        titulo = self.titulo_E.GetValue()
        desc = self.desc_E.GetValue()
        if not editing_task:    
            new_data = self.construir_data(titulo, desc)
            with DB.Session() as session:
                session.add(new_data)
                session.commit()
                session.refresh(new_data)
            self.titulo_E.SetValue("")
            self.desc_E.SetValue("")
        else:
            with DB.Session() as session:
                session.query(DB.Data).filter(DB.Data.id == editing_task).update({"title":titulo, "descr":desc}, synchronize_session="fetch")
                session.commit()
            self.main_window.Note.DeletePage(self.main_window.Note.GetSelection())
            del self.main_window.editingTasks[editing_task]
        
        # Update To Do Page and switch to It.
        self.main_window.To_Do_Panel.updatePage()
        self.main_window.ChangeNotebooktab(0)
    
   # Create an instance of the data class from SQLAlchemy database class. 
    def construir_data(self, T, D):
        new_data = DB.Data()
        new_data.done = False
        new_data.prio = None
        new_data.title = T
        new_data.descr = D
        new_data.dia = datetime.today()
        new_data.user_id = self.Usr_ID
        return new_data

class ChangePassDialog(Dialog):
    def __init__(self, parent, lang):
        self.lang = lang
        self.parent = parent
        Dialog.__init__(self, parent, ID_ANY, language_support[self.lang].dialogs.changepass_title)
        sizer = FlexGridSizer(cols=2, vgap=5, hgap=5)
        pw = StaticText(self, ID_ANY, language_support[self.lang].dialogs.pw)
        self.pw_E = TextCtrl(self, ID_ANY, style=TE_PROCESS_ENTER | TE_PASSWORD)
        pw_n = StaticText(self, ID_ANY, language_support[self.lang].dialogs.pw_n)
        self.pw_n_E = TextCtrl(self, ID_ANY, style=TE_PROCESS_ENTER | TE_PASSWORD)
        pw_c = StaticText(self, ID_ANY, language_support[self.lang].dialogs.pw_c)
        self.pw_c_E = TextCtrl(self, ID_ANY, style=TE_PROCESS_ENTER | TE_PASSWORD)
        
        sizer.Add(pw, 0, ALIGN_CENTER_VERTICAL | ALIGN_RIGHT)
        sizer.Add(self.pw_E)
        sizer.Add(pw_n, 0, ALIGN_CENTER_VERTICAL | ALIGN_RIGHT)
        sizer.Add(self.pw_n_E)
        sizer.Add(pw_c, 0, ALIGN_CENTER_VERTICAL | ALIGN_RIGHT)
        sizer.Add(self.pw_c_E) 

        self.Error = StaticText(self, ID_ANY, style=TE_CENTRE)
        
        c_btn = Button(self, ID_ANY, language_support[self.lang].dialogs.b_cancel)
        do_btn = Button(self, ID_ANY, language_support[self.lang].dialogs.b_do_change)
        
        btn_sizer = BoxSizer(HORIZONTAL)
        btn_sizer.Add(c_btn, 0, RIGHT, 10)
        btn_sizer.Add(do_btn,0, LEFT, 10)
        
        border_sizer = BoxSizer(VERTICAL)
        border_sizer.AddStretchSpacer(prop=1)
        border_sizer.Add(sizer, 0, CENTER)
        border_sizer.AddSpacer(10)
        border_sizer.Add(self.Error, 0, LEFT, 10)
        border_sizer.AddSpacer(10)
        border_sizer.Add(btn_sizer, 0, CENTER)
        border_sizer.AddStretchSpacer(prop=1)
        
        # Bindings
        self.Bind(EVT_TEXT_ENTER, self.onEnter, self.pw_E)
        self.Bind(EVT_TEXT_ENTER, self.onEnter, self.pw_n_E)
        self.Bind(EVT_TEXT_ENTER, self.onEnter, self.pw_c_E)
        self.Bind(EVT_TEXT, self.clearError, self.pw_E)
        self.Bind(EVT_TEXT, self.clearError, self.pw_n_E)
        self.Bind(EVT_TEXT, self.clearError, self.pw_c_E)
        
        self.Bind(EVT_BUTTON, self.cancelbtn, c_btn)
        self.Bind(EVT_BUTTON, self.onEnter, do_btn)
        
        self.SetSizer(border_sizer)
    
    def cancelbtn(self, e):
        self.Close()

    def clearError(self, e):
        self.Error.SetLabel("")
    
    def onEnter(self, e):
        pw = self.pw_E.GetValue()
        pw_n = self.pw_n_E.GetValue()
        pw_c = self.pw_c_E.GetValue()
        if pw_n == pw_c and pw_n != "":
            with DB.Session() as session:
                user = session.query(DB.Users).filter(DB.Users.id == self.parent.Usr_ID).first()
                if pw == user.passw:
                    session.query(DB.Users).filter(DB.Users.id == self.parent.Usr_ID).update({"passw":pw_n}, synchronize_session="fetch")
                    session.commit()
                    self.Close()
                else:
                    self.Error.SetLabel(language_support[self.lang].dialogs.e_wrong)
        else:
            if pw_n == "" and pw_c == "":  
                self.Error.SetLabel(language_support[self.lang].dialogs.e_empty)
            else:
                self.Error.SetLabel(language_support[self.lang].dialogs.e_match)

# Frame class derived from wx.Frame (Main Window of the APP)
class To_DO_Window(Frame):
    """ Main window os the To Do App """
    def __init__(self, parent, title, Usr_ID, lang):
        scrsize = DisplaySize()
        self.Usr_ID = Usr_ID
        self.editingTasks = {}
        self.ShouldRestart = False
        # cria variável para suporte de linguas
        self.lang = lang
        Frame.__init__(self, parent, title=title, size=(int(scrsize[0]*0.5),scrsize[1]), pos=(int(scrsize[0]*0.5),0))
        self.SetIcon(Icon('To_Do.ico', BITMAP_TYPE_ICO))
        # Setting up the menu.
        filemenu = Menu()
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuAbout = filemenu.Append(ID_ABOUT, language_support[self.lang].menu_file.about, language_support[self.lang].menu_file.about_info)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(ID_EXIT, language_support[self.lang].menu_file.exit, language_support[self.lang].menu_file.exit_info)
        
        # Setting up the Config menu
        
        lang_submenu = Menu()
        lang_en = lang_submenu.AppendRadioItem(ID_ANY, language_support[self.lang].lang_submenu.en, language_support[self.lang].lang_submenu.en_info)
        lang_pt = lang_submenu.AppendRadioItem(ID_ANY, language_support[self.lang].lang_submenu.pt, language_support[self.lang].lang_submenu.pt_info)
        if lang == "pt":
            lang_pt.Check(True)
        else:
            lang_en.Check(True)
        
        configmenu = Menu()
        changepassword = configmenu.Append(ID_ANY, language_support[self.lang].menu_config.password, language_support[self.lang].menu_config.password_info)
        configmenu.AppendSeparator()
        langConfig = configmenu.AppendSubMenu(lang_submenu, language_support[self.lang].menu_config.lang, language_support[self.lang].menu_config.lang_info)
        configmenu.AppendSeparator()
        autologinconfig = configmenu.AppendCheckItem(ID_ANY, language_support[self.lang].menu_config.auto, language_support[self.lang].menu_config.auto_info)
        with DB.Session() as session:
            usr_data = session.query(DB.Users).filter(DB.Users.id == self.Usr_ID).first()
        if usr_data.auto:
            autologinconfig.Check(True)
        
        
        # Creating the menubar.
        menuBar = MenuBar()
        menuBar.Append(filemenu, language_support[self.lang].menu.file) # Adding the "filemenu" to the MenuBar
        menuBar.Append(configmenu, language_support[self.lang].menu.config)
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        # Set events for file menu
        self.Bind(EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(EVT_MENU, self.OnExit, menuExit)
        # Set events for config menu
        self.Bind(EVT_MENU, self.changePass, changepassword)
        self.Bind(EVT_MENU, self.AppLangConfig_en, lang_en)
        self.Bind(EVT_MENU, self.AppLangConfig_pt, lang_pt)
        self.Bind(EVT_MENU, self.Autologin_save, autologinconfig)
        
        self.Note = Notebook(self, ID_ANY)
        # Cria paineis para o notebook
        self.To_Do_Panel = To_Do_Page(self.Note, self, False, language_support[self.lang].to_do_page.empty)
        self.Done_Panel = To_Do_Page(self.Note, self, True, language_support[self.lang].done_page.empty)
        self.NewTask_Panel = newTask(self.Note, self)
        # Adiciona os paineis no Notebook
        self.Note.AddPage(self.To_Do_Panel, language_support[self.lang].note.to_do)
        self.Note.AddPage(self.Done_Panel, language_support[self.lang].note.done)
        self.Note.AddPage(self.NewTask_Panel, language_support[self.lang].note.new)
        
        sizer= BoxSizer(VERTICAL)
        sizer.Add(self.Note, 1, EXPAND)
        self.SetSizer(sizer)
        
        # A Statusbar in the bottom of the window
        self.CreateStatusBar()

        self.Show(True)
    
    def editTask(self, task_id):
        try:
            page_num = self.Note.FindPage(self.editingTasks[task_id])
        except:
            self.editingTasks[task_id] = newTask(self.Note, self, task_id)
            self.Note.AddPage(self.editingTasks[task_id], f'{language_support[self.lang].note.edit} {task_id}', select=True)
            with DB.Session() as session:
                Task = session.query(DB.Data).filter(DB.Data.id == task_id).first()
            self.editingTasks[task_id].titulo_E.SetValue(Task.title)
            self.editingTasks[task_id].desc_E.SetValue(Task.descr)
        else:
            self.ChangeNotebooktab(page_num)
    
    # Troca as tabs do notebook
    def ChangeNotebooktab(self, tab):
        self.Note.SetSelection(tab)
    
    # Select the language of the app on Config -> Language  
    def AppLangConfig_en(self, e):
        self.lang = "en"
        self.ChangeAppLang("en")
    
    def AppLangConfig_pt(self, e):
        self.lang = "pt"
        self.ChangeAppLang("pt")
    
    def ChangeAppLang(self, lang):
        with DB.Session() as session:
            session.query(DB.Users).filter(DB.Users.id == self.Usr_ID).update({"lang":lang}, synchronize_session="fetch")
            session.commit()
        restart_program()
    
    # Change password for the current account
    def changePass(self, e):
        chpw = ChangePassDialog(self, self.lang)
        chpw.ShowModal()
        chpw.Destroy()
    
    # Toogle the auto login feature when user click on Config -> Auto logins
    def Autologin_save(self, e):
        obj = e.GetEventObject()
        checked = obj.IsChecked(e.GetId())
        with DB.Session() as session:
            if checked:
                session.query(DB.Users).filter(DB.Users.id == self.Usr_ID).update({"auto":True}, synchronize_session="fetch")
                session.commit()
            else:
                session.query(DB.Users).filter(DB.Users.id == self.Usr_ID).update({"auto":False}, synchronize_session="fetch")
                session.commit()
    
    # definition of the About function, when user click on File -> About
    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = MessageDialog(self, language_support[self.lang].about.descrip, language_support[self.lang].about.title, OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.
    
    # Definition  of the exit function when user click on file -> Exit
    def OnExit(self,e):
        self.Close(True)  # Close the frame.       

# Python standard if name == main script init        
if __name__ == "__main__":
    To_Do_List_init()
