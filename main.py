# Angel Bruce G. Jimenez, Aliah Casabuena
# pHym Meter: Python pH Meter using K-means algorithm

import math

import cv2
import numpy as np
import wx

from skimage import io

msg = """
--------------------
pHym -- a simple pH meter through image processing. To start simply go to `File` then import an image.

--------------------"""

def acquire_ph(img_path, k=5):
    """
    Import an image then process it through cv2.kmeans function.
    k is the number of centroids.
    Returns: dominant color in the image (numpy array).
    """
    image = io.imread(img_path)[:, :, :-1]
    image = np.float32(image.reshape(-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)

    _, labels, palette = cv2.kmeans(image, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    _, counts = np.unique(labels, return_counts=True)

    dominant = palette[np.argmax(counts)]

    return dominant


def ph_indicator(rgb):
    """
    Gets a color, evaluate it whether if it's on the pH scale and returns 
    a brief discription of the level.
    """
    r, g, b = rgb
    color_diffs = []

    levels = {
        (255, 0, 0):    "Strong Acid (<3) -- Grapefruit juice, soda, lemon juice, vinegar and battery acid.",
        (255, 215, 0):  "Weak Acid (3 - 6) -- Milk urine, saliva, and black coffee.",
        (0, 255, 0):    "Neutral (7) -- Blood",
        (0, 0, 255):    "Weak alkali (8-11) -- Sea water baking soda, and ammonia.",
        (148, 0, 211):  "Strong alkali (>11) -- Bleaches, oven cleaner, lye, and liquid drain cleaner." 
    }

    for color in levels.keys():
        cr, cg, cb = color
        color_diff = math.sqrt(abs(r - cr)**2 + abs(g - cg)**2 + abs(b - cb)**2)
        color_diffs.append((color_diff, color))

    return (min(color_diffs)[1], levels[min(color_diffs)[1]])

class MeterPanel(wx.Panel):
    def __init__(self, parent):
        super(MeterPanel, self).__init__(parent)

class MeterFrame(wx.Frame):
    def __init__(self, parent, title):
        WIDTH, HEIGHT = (500, 600)

        super(MeterFrame, self).__init__(parent, title=title, size=(WIDTH,HEIGHT), 
            style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CLOSE_BOX|wx.CAPTION)

        self.Center()        
        self.makeMenuBar()
        self.mainUI()

    def makeMenuBar(self):
        file_menu = wx.Menu()

        import_img = wx.MenuItem(file_menu, wx.ID_ANY, text="Import image...\tCtrl+I", 
            kind=wx.ITEM_NORMAL)

        quit = wx.MenuItem(file_menu, wx.ID_EXIT, '&Quit\tCtrl+Q', kind=wx.ITEM_NORMAL)  

        file_menu.Append(import_img)
        file_menu.AppendSeparator()
        file_menu.Append(quit)

        help_menu = wx.Menu()
        about = wx.MenuItem(help_menu, wx.ID_ANY, text="About\tCtrl+H", kind=wx.ITEM_NORMAL)

        help_menu.Append(about)

        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        menu_bar.Append(help_menu, '&Help')


        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.onImport, import_img)
        self.Bind(wx.EVT_MENU, self.Quit, quit)
        self.Bind(wx.EVT_MENU, self.OnAbout, about)


    def mainUI(self): 
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        info = MeterPanel(notebook)

        notebook.AddPage(info, "Logs")

        self.log = wx.TextCtrl(notebook, pos=(35, 10), value=msg, 
            size=(400, 500), style=wx.TE_MULTILINE|wx.TE_READONLY)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)

        self.Layout()

    def onImport(self, event=None):
        path = ""

        open_file = wx.FileDialog(
                            self, "Open", "", "", 
                            "Image files (*.jpeg,*.png)|*.jpeg;*.png", 
                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
                        )

        if open_file.ShowModal() == wx.ID_OK:
            path = open_file.GetPath()
            self.log.AppendText(f"\n[+] Opened \'{path}\'")             
            _, des = ph_indicator(acquire_ph(path))
            self.log.AppendText(f"\n{des}")

        open_file.Destroy()

    def Quit(self, event):
        self.Close()

    def OnAbout(self, event):
        wx.MessageBox("Angel Bruce G. Jimenez - Aliah Casabuena, 2019",
                      "About pHym",
                      wx.OK|wx.ICON_INFORMATION)

class pH(wx.App):
    def OnInit(self):
        self.frame = MeterFrame(None, title="pH Meter")
        self.frame.Show()

        return True

def main():
    # main function of the program
    pH_meter = pH()
    pH_meter.MainLoop()

if __name__ == "__main__":
    main()
