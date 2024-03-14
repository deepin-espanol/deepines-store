from PyQt5 import QtGui, QtWidgets as w
from PyQt5.QtCore import pyqtSignal, Qt, QTimer

from deepinesStore.demoted_actions import browse, open_telegram_link

class G:
	def __init__(self, name, contact=None):
		self.name = name
		self.contact = contact

# FIXME: Need to revisit this! AI is not a good coder!
class CreditsListWidget(w.QListWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.itemClicked.connect(self.on_item_click)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setStyleSheet("background-color: transparent;")
		self.setAutoFillBackground(True)
		self.setFrameShape(w.QFrame.Shape.NoFrame)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.scroll)
		self.timer.start(30)  # scroll every 30 ms
		self.setVerticalScrollMode(w.QAbstractItemView.ScrollPerPixel)
		self.setMouseTracking(True) # enable mouse tracking
		self.is_paused = False
		
	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.is_paused = True
			self.timer.stop()
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.is_paused = False
			self.timer.start()
		super().mouseReleaseEvent(event)

	def mouseMoveEvent(self, event):
		pos = self.mapFromGlobal(QtGui.QCursor.pos())
		'''
		if self.rect().contains(pos):
			self.is_paused = True
			self.timer.stop()
		else:
			self.is_paused = False
			self.timer.start()
		'''

	def on_item_click(self, item):
		contact = item.data(Qt.UserRole)
		if contact:
			if contact.startswith('@'):
				open_telegram_link(contact[1:])
			else:
				browse(f'mailto:{contact}')

	def scroll(self):
		if self.is_paused:
			return
		current_value = self.verticalScrollBar().value()
		if current_value == self.verticalScrollBar().maximum():
			self.verticalScrollBar().setValue(0)
		else:
			self.verticalScrollBar().setValue(current_value + 1)

class ClickableLabel(w.QLabel):
	clicked = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.clicked.emit()

class LinkLabel(w.QLabel):
	def on_link_clicked(self, link):
		if link.startswith("https://t.me/"):
			open_telegram_link(link[13:])
		else:
			browse(link)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTextInteractionFlags(Qt.TextBrowserInteraction)
		self.linkActivated.connect(self.on_link_clicked)

def add_people_to_list(people, list_widget):
	group_box = w.QGroupBox()
	layout = w.QVBoxLayout()
	for person in people:
		item = w.QListWidgetItem()
		item.setText(person.name)
		item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
		item.setData(Qt.UserRole, person.contact)
		if person.contact:
			font = item.font()
			item.setFont(font)
			item.setForeground(QtGui.QColor('#4b71fa'))
			if person.contact.startswith('@'):
				item.setToolTip(f'Telegram: {person.contact}')
			else:
				item.setToolTip(f'Email: {person.contact}')
		list_widget.addItem(item)
	layout.addWidget(list_widget)
	group_box.setLayout(layout)
	return group_box

