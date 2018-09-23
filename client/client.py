import wx
from wx.adv import AnimationCtrl
from wx.lib.pubsub import pub
import os
import json
import random
import time
import urllib2
#import requests
import threading
import shutil
import hashlib
import requests

DEFAULT_LANGUAGES = ["it", "en", "es", "ar", "zh", "ru", "fr"]
DATAFILE = "data.json"
BASE_URL ='http://ec2-52-56-218-193.eu-west-2.compute.amazonaws.com'
PUBID = "status.update"

myEVT_UPDATE = wx.NewEventType()
EVT_UPDATE = wx.PyEventBinder(myEVT_UPDATE, 1)
class UpdateEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event
        """
        return self._value

def filemd5(filename, block_size=2**20):
    f = open(filename, 'rb')
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    f.close()
    return md5.hexdigest()



def getAudioToUpload(url, audio):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')

    counter = 0
    response = urllib2.urlopen(req, data=json.dumps(audio).encode())
    data = json.load(response)

    return data['data']

def postEvent(parent, value):
    evt = UpdateEvent(myEVT_UPDATE, -1, value)
    wx.PostEvent(parent, evt)

def upload(url, formatted_data, parent, update_audio, send_audio):
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')

    counter = 0

    audio = []
    for el in formatted_data:
        for step in el['steps']:
            if step["audio"]:
                md5 = filemd5(os.path.join("audio", step["audio"]))
                audio.append({"name":step["audio"], "md5":md5})

    while counter <= 5:
        try:
            #status.SetStatusText("Connecting...")
            postEvent(parent, "Connecting...")
            response = urllib2.urlopen(req, data=json.dumps(formatted_data).encode())
            """audio = getAudioToUpload(update_audio, audio)
            for el in audio:
                with open(os.path.join('audio', el['name'])) as f:
                    files = {'file': f}
                    response = requests.post(send_audio, files=files)
            """

            #status.SetStatusText("Data uploaded.")
            postEvent(parent, "Data uploaded!")
            break
        except urllib2.HTTPError as e:
            dial = wx.MessageDialog(None, "The server couldn't fulfill the request. Error code: {}".format(e.code), 'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            #status.SetStatusText("Connection error")
            postEvent(parent, "Connection error!")
            break
        except urllib2.URLError as e:
            dial = wx.MessageDialog(None, "We failed to reach the server. Error: {}".format(e.reason), 'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            #status.SetStatusText("Connection error")
            postEvent(parent, "Connection error!")
            break
        except Exception as e:
            counter += 1
            if counter > 5:
                dial = wx.MessageDialog(None, "Unknown error: {}".format(str(e)), 'Error', wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
                #status.SetStatusText("Unknown error")
                postEvent(parent, "Unknown error")
                break



class ConnectingDialog(wx.Dialog):
    def __init__(self, parent, title, thread):
        super(ConnectingDialog, self).__init__(parent, title = title, size = (350,120))
        panel = wx.Panel(self)
        self.thread = thread
        self.animation = AnimationCtrl(panel)
        self.animation.LoadFile("load.gif")
        self.animation.Play()
        self.label = wx.StaticText(panel, label="Uploading to the server")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.animation, 1,  wx.ALL, 5)
        hbox.Add(self.label, 2,  wx.TOP|wx.BOTTOM|wx.EXPAND|wx.ALIGN_CENTER, 25)
        panel.SetSizer(hbox)

        self.Bind(wx.EVT_CLOSE, self.onClose)
        wx.CallLater(100, self.update, 1, 0, self.label)


    def update(self, count, tick, label):

        if not self.thread.isAlive():
                self.Destroy()
                return

        if tick >= 8:
            tick = 0
            text = "Uploading to the server" + '.'*count
            label.SetLabel(text)
            if count > 4:
                count = 0
            else:
                count+=1

        wx.CallLater(100, self.update, count, tick+1, label)


    def onClose(self, event):
        if event.CanVeto():
            event.Veto()
            return
        else:
            self.Destroy()



class MainWindow(wx.Frame):
    def __init__(self, parent, title, data, config):
        # A "-1" in the size parameter instructs wxWidgets to use the default size.
        # In this case, we select 200px width and the default height.
        super(MainWindow, self).__init__(parent, title=title, size=(720, 520))
        self.data = data
        self.selected_exam = None
        self.config = config
        self.UPDATE_URL = config['server'] + '/update_exams'
        self.UPDATE_AUDIO = config['server'] + '/audio_md5'
        self.SEND_AUDIO = config['server'] + '/upload_audio'
        self.saved = True
        self.Centre()
        self.status = self.CreateStatusBar() # A Statusbar in the bottom of the window

        self.initUI(DEFAULT_LANGUAGES)
        #pub.subscribe(self.statusUpdate, PUBID)
        self.Bind(EVT_UPDATE, self.statusUpdate)
        self.Show()

    def initUI(self, languages):
        self.panel = wx.Panel(self)

        self.Bind(wx.EVT_CLOSE, self.onExit)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        filemenu = wx.Menu()
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        nitem = filemenu.Append(wx.ID_NEW, "&New exam","Add a new exam")
        rnitem = filemenu.Append(wx.ID_ANY, "&Rename", "Rename current exam")
        rmitem = filemenu.Append(wx.ID_DELETE, "Delete", "Remove current exam")
        fitem = filemenu.Append(wx.ID_SAVE)
        uitem = filemenu.Append(wx.ID_ANY, "&Upload","Upload data to server")
        filemenu.AppendSeparator()
        settingsitem = filemenu.Append(wx.ID_ANY,"Settings","Configure settings")
        filemenu.AppendSeparator()
        exititem = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        self.Bind(wx.EVT_MENU, self.onSave, fitem)
        self.Bind(wx.EVT_MENU, self.onSettings, settingsitem)
        self.Bind(wx.EVT_MENU, self.onExit, exititem)
        self.Bind(wx.EVT_MENU, self.onNew, nitem)
        self.Bind(wx.EVT_MENU, self.onRename, rnitem)
        self.Bind(wx.EVT_MENU, self.onDelete, rmitem)
        self.Bind(wx.EVT_MENU, self.onUpload, uitem)

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        vbox.Add(-1,10)

        self.choices = [i for i in self.data.keys()]
        self.cb = wx.ComboBox(self.panel, choices=self.choices, style=wx.CB_SORT|wx.TE_PROCESS_ENTER,size=(150,-1))
        self.cb.SetHint("Esami")
        #self.cb.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.refreshComboSet)
        self.cb.Bind(wx.EVT_TEXT_ENTER, self.onEnter)
        self.cb.Bind(wx.EVT_COMBOBOX, self.onExamSelect)
        hbox.Add(self.cb,1, wx.LEFT|wx.ALIGN_LEFT, 10 )


        self.languages = wx.Choice(self.panel, choices=languages, size=(80,-1))
        self.languages.Bind(wx.EVT_CHOICE, self.onLang)
        self.languages.Disable()
        hbox.Add(self.languages, 0, wx.LEFT|wx.ALIGN_RIGHT, 10)

        """self.audioButton = wx.Button(self.panel, label="audio")
        self.audioButton.Bind(wx.EVT_BUTTON, self.onClicked)
        self.audioButton.Disable()
        hbox.Add(self.audioButton, 0, wx.LEFT|wx.ALIGN_LEFT, 40)

        self.audioLabel = wx.StaticText(self.panel, label="", size=(300,-1))
        hbox.Add(self.audioLabel, 0, wx.RIGHT|wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 10)"""


        vbox.Add(hbox, 0, wx.LEFT|wx.RIGHT, 10)

        self.titleText = wx.TextCtrl(self.panel)
        self.titleText.SetHint("titolo")
        self.titleText.Bind(wx.EVT_TEXT, self.onTextChange)
        self.titleText.Disable()
        vbox.Add(self.titleText, 0, wx.ALL|wx.EXPAND,10)

        self.text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE)
        self.text.Bind(wx.EVT_TEXT, self.onTextChange)
        self.text.Disable()
        vbox.Add(self.text, 1, wx.ALL|wx.EXPAND, 10)



        self.panel.SetSizer(vbox)
        self.panel.Layout()

    def updateCombox(self, exam=None):
        self.choices = [i for i in self.data.keys()]
        self.cb.Set(self.choices)
        self.languages.SetSelection(0)
        self.languages.Enable()
        if exam != None:
            self.cb.SetSelection(self.cb.FindString(exam))
            self.selected_exam = exam
            self.text.SetValue(self.data[exam][self.languages.GetStringSelection()])
            self.status.SetStatusText("Editing {}".format(self.selected_exam))
        else:
            self.selected_exam = None
            self.cb.SetSelection(wx.NOT_FOUND)
            self.cb.SetValue("")
            self.text.ChangeValue("")
            self.languages.SetSelection(wx.NOT_FOUND)
            self.languages.Disable()
            self.text.Disable()
            """self.audioButton.Disable()
            self.audioLabel.SetLabel("")"""
            self.status.SetStatusText("")
        self.text.SetFocus()
        self.saved = False

    def onClicked(self, event):
        openFileDialog = wx.FileDialog(frame, "Open", "", "", "Audio files(*.mp3)|*.mp3", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        res = openFileDialog.ShowModal()
        if res == wx.ID_OK:
            path = openFileDialog.GetPath()
            shutil.copyfile(path, os.path.join("audio", os.path.basename(path)))
            self.saved = False
            language=self.languages.GetStringSelection()
            self.data[self.selected_exam]["audio_"+language] = os.path.basename(path)
            #self.audioLabel.SetLabel(os.path.basename(path))
            self.panel.Layout()
            self.Layout()

    def onSave(self, e):
        for el in self.data.keys():
            for lang in DEFAULT_LANGUAGES:
                if not lang in self.data[el].keys():
                    self.data[el][lang] = "" 

        with open(DATAFILE, "w") as f:
            json.dump(self.data, f, indent=4)
            self.saved = True

    def onNew(self, e):
        dlg = wx.TextEntryDialog(frame, 'Enter the new exam name','New exam')
        dlg.SetValue("Exam{}".format(len(list(self.data.keys()))))
        if dlg.ShowModal() == wx.ID_OK:
            exam = dlg.GetValue()
            if exam in self.data:
                dial = wx.MessageDialog(None, 'An exam named {} already exists!'.format(exam), 'Error', wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
            else:
                self.data[exam] = {}
                for l in DEFAULT_LANGUAGES:
                    self.data[exam][l] = ""
                self.updateCombox(exam)


    def onRename(self, e):
        if not self.selected_exam:
            dial = wx.MessageDialog(None, "No exam selected", 'Error', wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            return

        old_exam = self.selected_exam
        dlg = wx.TextEntryDialog(frame, 'Enter the new exam name','Rename exam')
        if dlg.ShowModal() == wx.ID_OK:
            exam = dlg.GetValue()
            if exam in self.data:
                dial = wx.MessageDialog(None, 'An exam named {} already exists!'.format(exam), 'Error', wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
            else:
                self.data[exam] = self.data[old_exam]
                del data[old_exam]
                self.updateCombox(exam)

    def onDelete(self, e):
        exam = self.selected_exam
        dial = wx.MessageDialog(None, 'Are you sure you want to remove {}?'.format(exam), 'Confirm', wx.YES_NO | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            del data[exam]
            self.selected_exam = None
            self.status.PopStatusText()
            self.updateCombox()


    def onUpload(self, e):
        formatted_data = []
        for exam in list(self.data.keys()):
            d = {}
            d["name"] = exam
            d["steps"] = []

            for lang in list(self.data[exam].keys()):
                if "audio_" in lang:
                    continue
                if "audio_"+lang in self.data[exam]:
                    audio = self.data[exam]["audio_"+lang]
                else:
                    audio = None
                d["steps"].append({"language":lang, "description":self.data[exam][lang], "audio":audio})

            formatted_data.append(d)

        t = threading.Thread(target=upload, args=[self.UPDATE_URL, formatted_data, self, self.UPDATE_AUDIO, self.SEND_AUDIO])
        t.start()

        ConnectingDialog(self, "Uploading", t).ShowModal()

        def check():
            if not t.isAlive():
                if self.selected_exam == None:
                    msg = ""
                else:
                    msg = "Editing {}".format(self.selected_exam)
                wx.CallLater(5000, lambda: self.status.PushStatusText(msg))
            else:
                wx.CallLater(1000, check)

        check()
        #upload(self.UPDATE_URL, formatted_data, self.status, self.UPDATE_AUDIO, self.SEND_AUDIO)

    def statusUpdate(self, evt):
        self.status.SetStatusText(evt.GetValue())

    def onExit(self, e):
        if not self.saved:
            d = wx.MessageDialog(None, 'There are unsaved changes. Are you sure you want to quit?', 'WARNING', wx.YES_NO |wx.NO_DEFAULT| wx.ICON_QUESTION)
            res = d.ShowModal()
            if res == wx.ID_YES:
                self.Destroy()
        else:
            self.Destroy()

    def onSettings(self, e):
        dlg = wx.TextEntryDialog(frame, "URL del server. Non toccare se non te l'ho detto io",'Configuration')
        dlg.SetValue(self.config["server"])
        if dlg.ShowModal() == wx.ID_OK:
            self.config["server"] = dlg.GetValue()
            with open("config.json", "w") as f:
                json.dump(self.config, f, indent=4)



    def onTextChange(self, e):
        exam = self.selected_exam
        language = self.languages.GetStringSelection()
        self.data[exam][language] = e.GetString()
        self.saved = False

    def onLang(self, e):
        language= e.GetString()
        exam = self.selected_exam
        if language in self.data[exam]:
            self.text.ChangeValue(self.data[exam][language])
            """if "audio_"+language in self.data[self.selected_exam]:
                self.audioLabel.SetLabel(self.data[self.selected_exam]["audio_"+language])
            else:
                self.audioLabel.SetLabel("No audio associated")"""
        else:
            self.data[exam][language] = ""
            self.text.SetValue("")
            #self.audioLabel.SetLabel("")
            #self.audioButton.Disable()
        self.text.SetFocus()


    def onExamSelect(self, e):
        self.selected_exam =e.GetString()
        print("selected {}".format(self.selected_exam))
        self.status.PushStatusText("Editing {}".format(self.selected_exam))
        self.languages.SetSelection(0)
        self.languages.Enable()
        language=self.languages.GetStringSelection()
        #self.titleText.Enable()
        #self.titleText.ChangeValue(self.data[self.selected_exam][language])
        self.text.Enable()
        self.text.ChangeValue(self.data[self.selected_exam][language])
        self.text.SetFocus()

        """self.audioButton.Enable()
        if "audio_"+language in self.data[self.selected_exam]:
            self.audioLabel.SetLabel(self.data[self.selected_exam]["audio_"+language])
        else:
            self.audioLabel.SetLabel("No audio associated")"""

        self.cb.Set(self.choices)

        self.Layout()
        self.panel.Layout()

    def onEnter(self, e):
        textEntered=e.GetString()

        if textEntered:
            matching = [s for s in self.choices if textEntered.lower() in s.lower()]
            self.cb.Set(matching)
            self.ignoreEvtText = True
            #self.st.SetValue(textEntered)

        self.cb.Popup()

    def refreshComboSet(self, e):
        print("refresh")
        #self.ignoreEvtText = True





if __name__ == '__main__':
    try:
        with open(DATAFILE, "r") as f:
            data = json.load(f)
    except (IOError, ValueError):
        data = {}

    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except (IOError, ValueError):
        config = {
            "server" : BASE_URL
        }

    if not os.path.isdir("audio"):
        os.mkdir("audio")

    app = wx.App()
    frame = MainWindow(None, "Radiologia", data, config)
    app.MainLoop()
