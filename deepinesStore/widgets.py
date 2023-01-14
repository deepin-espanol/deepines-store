from PyQt5 import QtCore, QtGui, QtWidgets
import webbrowser


class G:
	def __init__(self, name, contact=None):
		self.name = name
		self.contact = contact


class ContactListWidget(QtWidgets.QListWidget):
	def viewportEvent(self, event):
		if event.type() == QtCore.QEvent.HoverMove:
			pos = event.pos()
			item = self.itemAt(pos)
			if item:
				contact = item.data(QtCore.Qt.UserRole)
				if contact:
					self.viewport().setCursor(QtCore.Qt.PointingHandCursor)
				else:
					self.viewport().setCursor(QtCore.Qt.ArrowCursor)
			else:
				self.viewport().setCursor(QtCore.Qt.ArrowCursor)
		return super().viewportEvent(event)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.itemClicked.connect(self.on_item_click)

	def on_item_click(self, item):
		contact = item.data(QtCore.Qt.UserRole)
		if contact:
			if contact.startswith('@'):
				webbrowser.open(f'https://t.me/{contact[1:]}')
			else:
				webbrowser.open(f'mailto:{contact}')


def add_people_to_list(people, list_widget):
	group_box = QtWidgets.QGroupBox()
	layout = QtWidgets.QVBoxLayout()
	for person in people:
		item = QtWidgets.QListWidgetItem()
		item.setText(person.name)
		item.setData(QtCore.Qt.UserRole, person.contact)
		if person.contact:
			font = item.font()
			font.setUnderline(True)
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

