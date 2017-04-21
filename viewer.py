import gtk
import pango

from utilities import Utilities
import i18n

class ViewerProcess():
    """Viewer process component
    """

    # utilities
    _utilities = None

    # process details
    _programName = "vncviewer"
    _args = []

    def __init__(self):
        """Constructor
        """
        self._utilities = Utilities()

    def getStatus(self):
        """get current status of the vnc process
        """
        st = self._utilities.checkProgramStatus(self._programName)

        return st[0]

    def changeStatus(self):
        """change current status of the vnc proces
        """
        if self.getStatus():
            self._utilities.endProgram(self._programName)
        else:
            self._utilities.startProgram(self._programName,self._args)

    def getProcessInfo(self):
        return self._utilities.getNetworkProcessInfo(self._programName)


class ViewerUI():
    """Viewer UI component for Classroom Kit Activity
    """
    # Constants
    _greenColor = '#00E500'
    _redColor = '#FF0000'

    # UI elements
    _box = None
    _button = None
    _label = None
    _toolbar = None
    _boxAlign = None

    # activity, process
    _activity = None
    _process = None

    def __init__(self, activity, process):
        """Constructor
        """
        self._activity = activity
        self._process = process

    def loadUI(self):
        """Create and show UI
        """
        # Box
        self._box = gtk.VBox()

        # Label
        self._label = gtk.Label()

        # Button
        self._button = gtk.Button()
        self._button.set_size_request(200, 50)
        self._button.connect("clicked", self.buttonClicked)

        # Add button to box
        self._box.pack_start(self._button)

        # Add label to box
        self._box.pack_start(self._label, padding=20)

        # Box Align (xalign, yalign, xscale, yscale)
        self._boxAlign = gtk.Alignment(0.5, 0.5, 0, 0)
        self._boxAlign.add(self._box)

        # Set canvas with box alignment
        self._activity.set_canvas(self._boxAlign)

    def setButtonBG(self, color):
        """Change button bg color
        """
        self._button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(color))

    def setButtonLabel(self, txt):
        """Change button label
        """
        self._button.set_label(txt)

    def buttonClicked(self, widget, data=None):
        """Button clicked event handler
        """
        self._process.changeStatus()
        self.showStatus()

    def setLabelTXT(self, txt):
        """Change label text
        """
        self._label.set_label(txt)

    def showStatus(self):
        """Show VNC status
        """
        state = self._process.getStatus()

        if not state:
            self.setButtonBG(self._greenColor)
            self.setButtonLabel(i18n.CONNECT)
            self.setLabelTXT("")
        else:
            self.setButtonBG(self._redColor)
            self.setButtonLabel(i18n.DISCONNECT)
            self.setLabelTXT(self._process.getProcessInfo())

class Viewer():
    """Viewer component for Classroom Kit Activity
    """
    _activity = None
    _process = None
    _ui = None

    def __init__(self,activity):
        """Constructor
        """
        self._activity = activity
        self._process = ViewerProcess()
        self._ui = ViewerUI(self._activity, self._process)

    def loadUI(self):
        """Load UI
        """
        self._ui.loadUI()

    def showStatus(self):
        """Show Viewer status
        """
        self._ui.showStatus()
