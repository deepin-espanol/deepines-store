from PyQt5 import QtGui, QtWidgets as w
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QEasingCurve, QPropertyAnimation, QEvent, pyqtSlot, QSize
from PyQt5.QtGui import QLinearGradient, QPainter, QBrush, QColor, QPalette

from deepinesStore.demoted_actions import browse, open_telegram_link

class G:
	def __init__(self, name, contact=None):
		self.name = name
		self.contact = contact

class NoClickableStyle(w.QProxyStyle):
	def __init__(self, parent=None, skip_indices=[]):
		super().__init__(parent)
		self.skip_indices = skip_indices

	def drawControl(self, element, option, painter, widget=None):
		if element == w.QStyle.CE_ItemViewItem:
			index = option.index
			if index.isValid() and index.row() in self.skip_indices:
				option.state &= ~w.QStyle.State_Enabled
				option.state &= ~w.QStyle.State_MouseOver
		super().drawControl(element, option, painter, widget)

class ClickableList(w.QListWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setAutoFillBackground(True)
		self.setFrameShape(w.QFrame.Shape.NoFrame)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			super().mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			event.ignore()
		else:
			super().mouseMoveEvent(event)

	def set_skip_item_action_indices(self, skip_indices=[]):
		self.setStyle(NoClickableStyle(self.style(), skip_indices))

	# Accessibility!!
	def keyPressEvent(self, event):
		if event.key() in (Qt.Key_Enter, Qt.Key_Return):
			current_item = self.currentItem()
			if current_item:
				current_item.setSelected(True)
				self.itemClicked.emit(current_item)
		else:
			super().keyPressEvent(event)

class CreditsListWidget(w.QListWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.itemClicked.connect(self.on_item_click)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setObjectName("lw_credits")
		self.setAutoFillBackground(False)
		self.setFrameShape(w.QFrame.Shape.NoFrame)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.scroll)
		self.timer.start(30)  # scroll every 30 ms
		self.setVerticalScrollMode(w.QAbstractItemView.ScrollPerPixel)
		self.setMouseTracking(True)  # enable mouse tracking
		self.is_paused = False
		self.fade_height = 50  # Height of fade effect at top and bottom

		# Setup animation for smooth scrolling
		self.scroll_animation = QPropertyAnimation(self.verticalScrollBar(), b"value")
		self.scroll_animation.setDuration(1000)  # 1 second for smooth scroll
		self.scroll_animation.setEasingCurve(QEasingCurve.OutQuad)

		self.app_instance = w.QApplication.instance()
		self.updateStyleSheet()
		# if palette changes...
		self.app_instance.paletteChanged.connect(self.onPaletteChanged)

	def event(self, event):
		if event.type() == QEvent.Move:
			self.updateStyleSheet()

		return super().event(event)

	@pyqtSlot()
	def onPaletteChanged(self):
		self.updateStyleSheet()

	def updateStyleSheet(self):
		if hasattr(self, 'app_instance') is False:
			return

		palette = self.app_instance.palette()
		hover_color = palette.color(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight)
		font_scale = self.app_instance.font().pointSize() / 12

		self.setStyleSheet(f"""
		#lw_credits {{
			background-color: transparent;
			border: 0px;
			font-size: {12 * font_scale}px;
		}}
		#lw_credits:item:selected {{
			background-color: palette(highlight);
			color: palette(highlightedText);
			border-radius: 8px;
		}}
		#lw_credits:item:hover:!selected {{}}
		#lw_credits:item:hover:selected {{
			background-color: {hover_color.name()};
		}}
		""")

	def set_skip_item_action_indices(self, skip_indices=[]):
		self.setStyle(NoClickableStyle(self.style(), skip_indices))

	def paintEvent(self, event):
		super().paintEvent(event)
		# Get window color from parent's palette
		window_color = self.parent().palette().color(QPalette.ColorRole.Window)

		# Draw gradient overlay
		painter = QPainter(self.viewport())
		painter.setRenderHint(QPainter.Antialiasing)

		# Create gradient for fading
		gradient = QLinearGradient(0, 0, 0, self.height())
		gradient.setColorAt(0, window_color)
		gradient.setColorAt(self.fade_height / self.height(), QColor(0, 0, 0, 0))
		gradient.setColorAt(1 - self.fade_height / self.height(), QColor(0, 0, 0, 0))
		gradient.setColorAt(1, window_color)

		# Draw gradient overlay
		painter.fillRect(self.rect(), QBrush(gradient))

	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.is_paused = True
			self.timer.stop()
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.is_paused = False
			self.timer.start()
		super().mouseReleaseEvent(event)

	def mouseMoveEvent(self, event):
		pos = self.mapFromGlobal(QtGui.QCursor.pos())
		if self.rect().contains(pos):
			self.is_paused = True
			self.timer.stop()
		else:
			self.is_paused = False
			self.timer.start()

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
		max_value = self.verticalScrollBar().maximum()
		if current_value == max_value:
			self.scroll_animation.setStartValue(max_value)
			self.scroll_animation.setEndValue(0)
			self.scroll_animation.start()
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
	empty_item = w.QListWidgetItem()
	list_widget.addItem(empty_item)
	empty_item.setFlags(Qt.NoItemFlags)

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

	empty_item = w.QListWidgetItem()
	list_widget.addItem(empty_item)
	empty_item.setFlags(Qt.NoItemFlags)

	list_widget.set_skip_item_action_indices([0, len(people) + 1])

	return list_widget


class StateOverlayWidget(w.QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.setStyleSheet("background-color: transparent;")

		self.verticalLayout = w.QVBoxLayout(self)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setSpacing(10)

		self.topSpacer = w.QSpacerItem(20, 40, w.QSizePolicy.Policy.Minimum, w.QSizePolicy.Policy.Expanding)
		self.verticalLayout.addItem(self.topSpacer)

		# Media (Movie/Pixmap)
		self.media_label = w.QLabel(self)
		self.media_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.verticalLayout.addWidget(self.media_label, alignment=Qt.AlignmentFlag.AlignHCenter)

		# Primary Text (LinkLabel)
		self.primary_label = LinkLabel(self)
		font = self.primary_label.font()
		font.setPointSize(16)
		self.primary_label.setFont(font)
		self.primary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.primary_label.setWordWrap(False)
		self.primary_label.setSizePolicy(w.QSizePolicy.Policy.Expanding, w.QSizePolicy.Policy.Minimum)
		self.primary_label.setStyleSheet("color: #fff; background-color: rgba(0, 0, 0, 0);")
		self.primary_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
		self.verticalLayout.addWidget(self.primary_label, alignment=Qt.AlignmentFlag.AlignHCenter)

		# Secondary Text (QLabel)
		self.secondary_label = w.QLabel(self)
		font2 = self.secondary_label.font()
		font2.setPointSize(14)
		self.secondary_label.setFont(font2)
		self.secondary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.secondary_label.setWordWrap(False)
		self.secondary_label.setSizePolicy(w.QSizePolicy.Policy.Expanding, w.QSizePolicy.Policy.Minimum)
		self.secondary_label.setStyleSheet("color: #fff; background-color: rgba(0, 0, 0, 0);")
		self.secondary_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
		self.secondary_label.hide()
		self.verticalLayout.addWidget(self.secondary_label, alignment=Qt.AlignmentFlag.AlignHCenter)

		# Action Button
		self.action_button = w.QPushButton(self)
		self.action_button.hide()
		self.action_button.setStyleSheet("""
			QPushButton {
				padding: 8px 16px;
				border-radius: 5px;
				background-color: rgb(45, 45, 45);
				border: 2px solid rgb(65, 159, 217);
				color: white;
				font-size: 14px;
			}
			QPushButton:hover {
				background-color: rgb(65, 159, 217);
			}
		""")
		self.verticalLayout.addWidget(self.action_button, alignment=Qt.AlignmentFlag.AlignHCenter)

		self.verticalSpacer = w.QSpacerItem(20, 40, w.QSizePolicy.Policy.Minimum, w.QSizePolicy.Policy.Expanding)
		self.verticalLayout.addItem(self.verticalSpacer)
		self.current_movie = None

	def set_media(self, media_path, is_movie=False, size=150):
		if self.current_movie:
			self.current_movie.stop()
			self.current_movie = None

		if not media_path:
			self.media_label.hide()
			return

		self.media_label.show()

		if media_path: # Hardcoded for now...
			if 'strawhats-one-piece' in media_path:
				size = 350
			elif 'raccoon' in media_path:
				size = 300
			elif 'Deepines' in media_path:
				size = 300

		self.media_label.setMinimumSize(size, size)
		self.media_label.setMaximumSize(size, size)
		self.media_label.setSizePolicy(w.QSizePolicy.Policy.Fixed, w.QSizePolicy.Policy.Fixed)

		if is_movie:
			self.current_movie = QtGui.QMovie(media_path)
			self.current_movie.setScaledSize(QSize(size, size))
			self.media_label.setMovie(self.current_movie)
			self.current_movie.start()
		else:
			pixmap = QtGui.QPixmap(media_path)
			self.media_label.setPixmap(pixmap)
			self.media_label.setScaledContents(True)

	def set_text(self, primary_text, secondary_text=None):
		if primary_text:
			if '<a ' in primary_text or '&lt;a ' in primary_text:
				primary_text = f"<style>a {{ color: #00c0ff; text-decoration: none; }}</style>{primary_text}"
			self.primary_label.setText(primary_text)
			self.primary_label.adjustSize()
			self.primary_label.show()
		else:
			self.primary_label.hide()

		if secondary_text:
			self.secondary_label.setText(secondary_text)
			self.secondary_label.adjustSize()
			self.secondary_label.show()
		else:
			self.secondary_label.hide()

	def set_action(self, button_text, callback=None):
		if button_text:
			self.action_button.setText(button_text)
			self.action_button.show()
			try:
				self.action_button.clicked.disconnect()
			except TypeError:
				pass
			if callback:
				self.action_button.clicked.connect(callback)
		else:
			self.action_button.hide()