# -*- coding: utf-8 -*-
"""
PiDashboard Widgets
"""
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimeLine, pyqtSignal
from PyQt5.QtGui import *
from lib import pi_charts, pi_mixins, utils
from lib.decorators import threaded_method

WIDGETS = {
    'stack': lambda *args: PiStackedWidget(*args),
    'widget': lambda *args: PiWidget(*args),
    'icon': lambda *args: PiIcon(*args),
    'label': lambda *args: PiLabel(*args),
    'linechart': lambda *args: pi_charts.PiLineChart(*args),
    'piechart': lambda *args: pi_charts.PiPieChart(*args),
    'pushbutton': lambda *args: PiPushButton(*args),
    'textedit': lambda *args: PiTextEdit(*args),
    'toggleswitch': lambda *args: PiToggleSwitch(*args),
    'vbarchart': lambda *args: pi_charts.PiVBarChart(*args),
    'pbar': lambda *args: PiProgressBar(*args),
    'vframe': lambda *args: PiFrameVertical(*args),
    'hframe': lambda *args: PiFrameHorizontal(*args),
    'page-turner': lambda *args: PiPageTurner(*args),
    'groupbox': lambda *args: PiGroupBox(*args)
}


class PiFrameVertical(QtWidgets.QFrame, pi_mixins.StashMixin, pi_mixins.LayoutMixin):
    def __init__(self, etree, control, parent=None):
        QtWidgets.QFrame.__init__(self)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        pi_mixins.StashMixin._init(self)
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)
        self.setFixedHeight(8)

    def paintEvent(self, event):
        QtWidgets.QFrame.paintEvent(self, event)
        return self._paint_frame(event)


class PiFrameHorizontal(QtWidgets.QFrame, pi_mixins.StashMixin, pi_mixins.LayoutMixin):
    COMP_SEPARATOR = '=='

    def __init__(self, etree, control, parent=None):
        QtWidgets.QFrame.__init__(self)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        pi_mixins.StashMixin._init(self)
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_show_when(self, value):
        temp_str = value.split(self.COMP_SEPARATOR)
        self.setVisible(temp_str[0] == temp_str[1])

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)

    def paintEvent(self, event):
        QtWidgets.QFrame.paintEvent(self, event)
        return self._paint_frame(event)


class PiIcon(QtWidgets.QLabel, pi_mixins.StashMixin, pi_mixins.LayoutMixin):
    ALIGN = {'left': Qt.AlignLeft, 'right': Qt.AlignRight, 'center': Qt.AlignHCenter}

    def __init__(self, etree, control, parent=None):
        QtWidgets.QLabel.__init__(self)
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_text(self, value):
        self.setText(value)

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)
        self.setFixedHeight(8)

    def attribute_initsize(self, value):
        self.initsize = [int(x) for x in value.split(',')]
        self.resize(*self.initsize)

    def attribute_align(self, value):
        self.setAlignment(self.ALIGN[value.lower()])

    def attribute_wrap(self, value):
        self.setWordWrap(value.lower() in ['true', 't', '1'])


class PiStackedWidget(QtWidgets.QStackedWidget, pi_mixins.LayoutMixin):
    def __init__(self, etree, control, parent=None):
        QtWidgets.QStackedWidget.__init__(self)
        self.setLayout(QtWidgets.QStackedLayout())
        self.setObjectName('stacked_widget')
        self.fader_widget = self.currentWidget()
        self.current_index = 0
        self.initsize = None
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)

    def attribute_initsize(self, value):
        self.initsize = [int(x) for x in value.split(',')]
        self.resize(*self.initsize)

    def setCurrentIndex(self, index):
        self.fader_widget = PiFaderWidget(self.currentWidget(), self.widget(index))
        QtWidgets.QStackedWidget.setCurrentIndex(self, index)

    def nextPage(self):
        new_index = self.current_index + 1
        if new_index >= self.count():
            new_index = 0
        tries = 0
        if self.widget(new_index).isEnabled():
            self.current_index = new_index
            return self.setCurrentIndex(new_index)

        while not self.widget(new_index).isEnabled():

            tries += 1
            new_index += 1

            if new_index >= self.count():
                new_index = 0

            if tries > self.count():
                # no pages enabled
                return
        self.current_index = new_index
        self.setCurrentIndex(self.current_index)


class PiPage(QtWidgets.QWidget, pi_mixins.LayoutMixin):
    def __init__(self, etree, style, control, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.enabled = True
        self.setEnabled(True)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.setStyleSheet(style)
        self.initsize = None

        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)

    def attribute_initsize(self, value):
        self.initsize = [int(x) for x in value.split(',')]
        self.resize(*self.initsize)


class PiPageTurner(QtWidgets.QWidget, pi_mixins.LayoutMixin):
    def __init__(self, etree, style, control, parent=None):
        QtWidgets.QWidget.__init__(self)
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_active(self, value):
        self.setEnabled(True)


class PiFaderWidget(QtWidgets.QWidget):
    def __init__(self, old_widget, new_widget):
        self.pixmap_opacity = 1.0
        QtWidgets.QWidget.__init__(self, new_widget)

        self.old_pixmap = QPixmap(new_widget.size())
        old_widget.render(self.old_pixmap)

        self.timeline = QTimeLine()
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(333)
        self.timeline.start()

        self.resize(new_widget.size())
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setOpacity(self.pixmap_opacity)
        painter.drawPixmap(0, 0, self.old_pixmap)
        painter.end()

    def animate(self, value):
        self.pixmap_opacity = 1.0 - value
        self.repaint()


class PiWidget(QtWidgets.QWidget, pi_mixins.LayoutMixin):
    def __init__(self, etree, control, parent=None):
        QtWidgets.QWidget.__init__(self)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.initsize = None
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)

    def attribute_initsize(self, value):
        self.initsize = [int(x) for x in value.split(',')]
        self.resize(*self.initsize)


class PiDeskWidget(PiWidget, pi_mixins.DraggableMixin):
    def __init__(self, etree, style, pi_dash, parent=None):
        PiWidget.__init__(self, etree, pi_dash, parent)
        self.pi_dash = pi_dash
        self.setStyleSheet(style)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnBottomHint |
            Qt.NoDropShadowWindowHint |
            Qt.CustomizeWindowHint)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self._init_menu()
        pi_mixins.DraggableMixin.__init__(self)

    def _init_menu(self):
        self.addAction(QtWidgets.QAction('About PiDashboard', self, triggered=self.pi_dash.about.show))
        self.addAction(QtWidgets.QAction('Preferences', self, triggered=self.pi_dash.config.show))
        self.addAction(QtWidgets.QAction('Next Page', self, triggered=self.pi_dash.next_page))
        self.addAction(QtWidgets.QAction('Quit', self, triggered=self.pi_dash.quit))
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def position(self):
        return '%s,%s' % (self.x(), self.y())

    def setPosition(self, position):
        self.move(*[int(x) for x in position.split(',')])

    def show(self):
        self.setWindowOpacity(0)
        self.fade_in()
        return super(PiDeskWidget, self).show()

    @threaded_method
    def fade_in(self):
        time.sleep(1)
        for i in range(0, 101, 5):
            self.setWindowOpacity(i * 0.01)
            self.update()
            time.sleep(0.02)


class PiLabel(QtWidgets.QLabel, pi_mixins.LayoutMixin):
    ALIGN = {'left': Qt.AlignLeft, 'right': Qt.AlignRight, 'center': Qt.AlignHCenter}

    def __init__(self, etree, control, parent=None):
        QtWidgets.QLabel.__init__(self)
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_text(self, value):
        self.setText(value)

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)
        self.setFixedHeight(8)

    def attribute_initsize(self, value):
        self.initsize = [int(x) for x in value.split(',')]
        self.resize(*self.initsize)

    def attribute_align(self, value):
        self.setAlignment(self.ALIGN[value.lower()])

    def attribute_wrap(self, value):
        self.setWordWrap(value.lower() in ['true', 't', '1'])


class PiPushButton(QtWidgets.QPushButton, pi_mixins.LayoutMixin):
    DEFAULT_COLOR = '#ffffff'  # For color buttons

    def __init__(self, etree, control, parent=None):
        QtWidgets.QPushButton.__init__(self)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_text(self, value):
        self.setText(value)

    def get_value(self):
        if self.data.color:
            return self.data.color
        return self.text()

    def set_value(self, value):
        if self.data.color:
            self.data.color = value or self.DEFAULT_COLOR
            style = 'background-color: %s;' % self.data.color
            # return self.layout().itemAt(0).widget().setStyleSheet(style)
        return self.setText(value)


class PiGroupBox(QtWidgets.QGroupBox, pi_mixins.LayoutMixin):
    def __init__(self, etree, control, parent=None):
        QtWidgets.QGroupBox.__init__(self)
        self.setWindowTitle("-------")
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setObjectName('group_box')
        self.initsize = None
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)

    def attribute_initsize(self, value):
        self.initsize = [int(x) for x in value.split(',')]
        self.resize(*self.initsize)

    def attribute_title(self, value):
        self.title = value


class PiTextEdit(QtWidgets.QTextEdit, pi_mixins.LayoutMixin):
    """ QTextEdit that sends editingFinished event when text changed and focus lost.
        https://gist.github.com/hahastudio/4345418
    """
    editingFinished = QtCore.pyqtSignal()

    def __init__(self, etree, control, parent=None):
        QtWidgets.QTextEdit.__init__(self)
        self._changed = False
        self.setTabChangesFocus(True)
        self.textChanged.connect(self._handle_text_changed)
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def _handle_text_changed(self):
        self._changed = True

    def focusOutEvent(self, event):
        if self._changed:
            self.editingFinished.emit()
        super(PiTextEdit, self).focusOutEvent(event)

    def get_value(self):
        return self.toPlainText()

    def setTextChanged(self, state=True):
        self._changed = state

    def sethtml(self, html):
        QtWidgets.QTextEdit.sethtml(self, html)
        self._changed = False

    def setText(self, text):
        QtWidgets.QTextEdit.setText(self, text)
        self._changed = False

    def set_value(self, value):
        return self.setText(value)


class PiToggleSwitch(QtWidgets.QFrame, pi_mixins.LayoutMixin):
    editingFinished = QtCore.pyqtSignal(name='editingFinished')

    def __init__(self, etree, control, parent=None):
        QtWidgets.QPushButton.__init__(self)
        self.enabled = False  # Holds switch state
        self.bgcolor_slider = utils.window_bgcolor()  # Background color of the slider
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def mouseReleaseEvent(self, event):
        self.set_value(not self.get_value())
        self.editingFinished.emit()

    def paintEvent(self, event):
        QtWidgets.QFrame.paintEvent(self, event)
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        if self.enabled:
            self.paint_slider_on(painter)
        else:
            self.paint_slider_off(painter)
        painter.end()

    def paint_slider_on(self, painter):
        self_width = int((self.width() / 2) - 2)
        self_height = int(self.height() - 2)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(60, 90, 150, 200)))
        painter.drawRoundedRect(self.contentsRect(), 3, 3)
        painter.setBrush(QtGui.QBrush(self.bgcolor_slider))
        painter.drawRoundedRect(self_width + 3, 1, self_width, self_height, 2, 2)
        painter.setPen(QtGui.QColor(255, 255, 255, 220))
        painter.drawText(2, 1, self_width, self_height, Qt.AlignCenter | Qt.AlignVCenter, 'On')

    def paint_slider_off(self, painter):
        self_width = int((self.width() / 2) - 2)
        self_height = int(self.height() - 2)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 50)))
        painter.drawRoundedRect(self.contentsRect(), 3, 3)
        painter.setBrush(QtGui.QBrush(self.bgcolor_slider))
        painter.drawRoundedRect(3, 1, self_width, self_height, 2, 2)
        painter.setPen(QtGui.QColor(0, 0, 0, 150))
        painter.drawText(self_width + 3, 1, self_width, self_height, Qt.AlignCenter | Qt.AlignVCenter, 'Off')

    def get_value(self):
        return self.enabled

    def set_value(self, enabled=True):
        self.enabled = enabled
        self.update()


class PiProgressBar(QtWidgets.QProgressBar, pi_mixins.LayoutMixin):
    value_changed = pyqtSignal(int, name='valueChanged')
    align = {'left': Qt.AlignLeft, 'right': Qt.AlignRight, 'center': Qt.AlignHCenter}

    def __init__(self, etree, control, parent=None):
        QtWidgets.QProgressBar.__init__(self)
        self.value = 0  # Holds value
        self.minimum = 0
        self.maximum = 2000
        self.setAlignment(Qt.AlignLeft)
        self.setMinimumHeight(6)
        self.setFixedHeight(6)
        self.setMaximum(int(self.maximum))
        self.setTextVisible(False)
        self.value_changed.connect(self.valueChanged)
        self.degrading = False
        pi_mixins.LayoutMixin._init(self, etree, control, parent)

    def attribute_degrading(self, value):
        self.degrading = value

    def attribute_minimum(self, value):
        if not value:
            value = 0
        self.setMinimum(int(value))

    def attribute_maximum(self, value):
        if not value:
            value = 2000
        self.setMaximum(int(value))

    def attribute_size(self, value):
        values = [int(x) for x in value.split(',')]
        self.setFixedSize(*values)
        self.setFixedHeight(values[1])

    def attribute_initsize(self, value):
        self.initsize = [int(x) for x in value.split(',')]
        self.resize(*self.initsize)

    def valueChanged(self, value):
        pct = int(self.text().replace('%', ''))
        css = "QProgressBar {" \
              "border: 1px solid black;" \
              "padding: .3px;" \
              "border-top-right-radius: 3px;" \
              "border-bottom-right-radius: 3px;" \
              "background: #efefef;" \
              "}" \
              "QProgressBar::chunk {" \
              "background-color: QLinearGradient( " \
              "x1: 0, y1: 0, x2: 1, y2: 0, "
        if self.degrading:
            if pct <= 20:
                css += "stop: 0.1 #06FF87, " \
                       "stop: 0.2 #4AF2A1 );"
            if 20 < pct <= 40:
                css += "stop: 0.3 #B0F566, " \
                       "stop: 0.4 #E8FFB7 );"
            if 40 < pct <= 60:
                css += "stop: 0.5 #FFEDA4, " \
                       "stop: 0.6 #FFAD8B );"
            if 60 < pct <= 80:
                css += "stop: 0.7 #FFAD8B, " \
                       "stop: 0.8 #FFAD8B );"
            if 80 < pct <= 100:
                css += "stop: 0.9 #FFAD8B, " \
                       "stop: 1.0 #FFAD8B );"
        else:
            if pct <= 20:
                css += "stop: 0.1 #FFAD8B, " \
                       "stop: 0.2 #FFAD8B );"
            if 20 < pct <= 40:
                css += "stop: 0.3 #FFAD8B, " \
                       "stop: 0.4 #FFAD8B );"
            if 40 < pct <= 60:
                css += "stop: 0.5 #FFEDA4, " \
                       "stop: 0.6 #FFAD8B );"
            if 60 < pct <= 80:
                css += "stop: 0.7 #B0F566, " \
                       "stop: 0.8 #E8FFB7 );"
            if 80 < pct <= 100:
                css += "stop: 0.9 #06FF87, " \
                       "stop: 1.0 #4AF2A1 );"
        css += "border-top-right-radius: 3px;" \
               "border-bottom-right-radius: 3px;" \
               "border: .5px solid black;" \
               "}"
        self.setStyleSheet(css)

    def attribute_align(self, value):
        self.setAlignment(self.align[value.lower()])

    def attribute_value(self, value):
        self.value = value
        self.setValue(int(value))
        self.value_changed.emit(value)
        self.update()


def widget_factory(q_widget):
    class PiWidgetFactory(q_widget, pi_mixins.LayoutMixin):
        def __init__(self, etree, control, parent=None):
            q_widget.__init__(self)
            self.setObjectName(q_widget.__name__)
            self.setLayout(QtWidgets.QVBoxLayout())
            self.layout().setContentsMargins(0, 0, 0, 0)
            self.layout().setSpacing(0)
            pi_mixins.LayoutMixin._init(self, etree, control, parent)

        def get_value(self):
            for attr in ('toPlainText', 'text'):
                callback = getattr(self, attr, None)
                if callback: return callback()
            raise Exception('Unable to get value.')

        def set_value(self, value):
            for attr in ('setPlainText', 'setText'):
                callback = getattr(self, attr, None)
                if callback: return callback(str(value))
            raise Exception('Unable to get value.')

        def attribute_placeholder(self, value):
            self.setPlaceholderText(value)

    return PiWidgetFactory
