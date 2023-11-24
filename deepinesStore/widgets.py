from PyQt5 import QtGui, QtWidgets as w
from PyQt5.QtCore import pyqtSignal, Qt, QEvent

from deepinesStore.demoted_actions import browse


class G:
	def __init__(self, name, contact=None):
		self.name = name
		self.contact = contact

class ContactListWidget(w.QListWidget):
	def viewportEvent(self, event):
		if event.type() == QEvent.HoverMove:
			pos = event.pos()
			item = self.itemAt(pos)
			if item:
				contact = item.data(Qt.UserRole)
				if contact:
					self.viewport().setCursor(Qt.PointingHandCursor)
				else:
					self.viewport().setCursor(Qt.ArrowCursor)
			else:
				self.viewport().setCursor(Qt.ArrowCursor)
		return super().viewportEvent(event)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.itemClicked.connect(self.on_item_click)

	def on_item_click(self, item):
		contact = item.data(Qt.UserRole)
		if contact:
			if contact.startswith('@'):
				browse(f'https://t.me/{contact[1:]}')
			else:
				browse(f'mailto:{contact}')

class ClickableLabel(w.QLabel):
	clicked = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.clicked.emit()

class LinkLabel(w.QLabel):
	def on_link_clicked(self, link):
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

