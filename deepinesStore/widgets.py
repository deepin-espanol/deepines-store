from PyQt5 import QtGui, QtWidgets as w
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QEasingCurve, QPropertyAnimation, QEvent, pyqtSlot, QSize, QRect, QPoint
from PyQt5.QtGui import QLinearGradient, QPainter, QBrush, QColor, QPalette

from deepinesStore.demoted_actions import browse, open_telegram_link

class G:
	def __init__(self, name, contact=None):
		self.name = name
		self.contact = contact


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
		self.scroll_animation = QPropertyAnimation(self.verticalScrollBar(), b"value", self)
		self.scroll_animation.setDuration(1000)  # 1 second for smooth scroll
		self.scroll_animation.setEasingCurve(QEasingCurve.OutQuad)

		self.app_instance = w.QApplication.instance()
		self.updateStyleSheet()
		# if palette changes...
		self.app_instance.paletteChanged.connect(self.onPaletteChanged)
		self.destroyed.connect(self.on_destroyed)

	def on_destroyed(self):
		try:
			self.app_instance.paletteChanged.disconnect(self.onPaletteChanged)
		except Exception:
			pass

	def event(self, event):
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
		painter.end()

	def hideEvent(self, event):
		self.timer.stop()
		if hasattr(self, 'scroll_animation'):
			self.scroll_animation.stop()
		super().hideEvent(event)

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

	return list_widget


class StateOverlayWidget(w.QFrame):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.setAttribute(Qt.WA_StyledBackground, True)
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
		self.primary_label.setWordWrap(True)
		self.primary_label.setSizePolicy(w.QSizePolicy.Policy.Expanding, w.QSizePolicy.Policy.Minimum)
		self.primary_label.setStyleSheet("color: #fff; background-color: rgba(0, 0, 0, 0);")
		self.primary_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
		self.verticalLayout.addWidget(self.primary_label)

		# Secondary Text (QLabel)
		self.secondary_label = w.QLabel(self)
		font2 = self.secondary_label.font()
		font2.setPointSize(14)
		self.secondary_label.setFont(font2)
		self.secondary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.secondary_label.setWordWrap(True)
		self.secondary_label.setSizePolicy(w.QSizePolicy.Policy.Expanding, w.QSizePolicy.Policy.Minimum)
		self.secondary_label.setStyleSheet("color: #fff; background-color: rgba(0, 0, 0, 0);")
		self.secondary_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
		self.secondary_label.setOpenExternalLinks(True)
		self.secondary_label.hide()
		self.verticalLayout.addWidget(self.secondary_label)

		# Custom Widget Layout
		self.custom_layout = w.QVBoxLayout()
		self.custom_layout.setContentsMargins(0, 0, 0, 0)
		self.custom_layout.setSpacing(10)
		self.verticalLayout.addLayout(self.custom_layout)

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

	def set_media(self, media_path: str, is_movie: bool = False, size=150, pixmap=None):
		if self.current_movie:
			self.current_movie.stop()
			self.current_movie = None

		if is_movie and media_path:
			self.current_movie = QtGui.QMovie(media_path, parent=self)
			self.current_movie.setScaledSize(QSize(size, size))
			self.media_label.setMovie(self.current_movie)
			self.current_movie.start()
		elif not media_path and not pixmap:
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

		if pixmap:
			self.media_label.setPixmap(pixmap)
			self.media_label.setScaledContents(False)
		elif is_movie:
			self.current_movie = QtGui.QMovie(media_path)
			self.current_movie.setScaledSize(QSize(size, size))
			self.media_label.setMovie(self.current_movie)
			self.current_movie.start()
		else:
			pixmap = QtGui.QPixmap(media_path)
			pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.media_label.setPixmap(pixmap)
			self.media_label.setScaledContents(False)

	def add_custom_widget(self, widget):
		self.custom_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignHCenter)

	def set_text(self, primary_text, secondary_text=None):
		if primary_text:
			if '<a ' in primary_text or '&lt;a ' in primary_text:
				primary_text = f"<style>a {{ color: #00c0ff; text-decoration: none; }}</style>{primary_text}"
			self.primary_label.setText(primary_text)
			self.primary_label.show()
		else:
			self.primary_label.hide()

		if secondary_text:
			self.secondary_label.setText(secondary_text)
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

class FlowLayout(w.QLayout):
	def __init__(self, parent=None, margin=-1, hSpacing=-1, vSpacing=-1):
		super().__init__(parent)
		self._hSpace = hSpacing
		self._vSpace = vSpacing
		self.itemList = []
		self.setContentsMargins(margin, margin, margin, margin)

	def __del__(self):
		try:
			item = self.takeAt(0)
			while item:
				item = self.takeAt(0)
		except (RuntimeError, TypeError):
			pass

	def addItem(self, item):
		self.itemList.append(item)
		self.invalidate()

	def horizontalSpacing(self):
		if self._hSpace >= 0:
			return self._hSpace
		return self.smartSpacing(w.QStyle.PixelMetric.PM_LayoutHorizontalSpacing)

	def verticalSpacing(self):
		if self._vSpace >= 0:
			return self._vSpace
		return self.smartSpacing(w.QStyle.PixelMetric.PM_LayoutVerticalSpacing)

	def count(self):
		return len(self.itemList)

	def itemAt(self, index):
		if 0 <= index < len(self.itemList):
			return self.itemList[index]
		return None

	def takeAt(self, index):
		if 0 <= index < len(self.itemList):
			item = self.itemList.pop(index)
			self.invalidate()
			return item
		return None

	def expandingDirections(self):
		return Qt.Orientations(Qt.Orientation(0))

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		height = self.doLayout(QRect(0, 0, width, 0), True)
		return height

	def setGeometry(self, rect):
		super().setGeometry(rect)
		self.doLayout(rect, False)

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QSize()
		for item in self.itemList:
			size = size.expandedTo(item.minimumSize())
		left, top, right, bottom = self.getContentsMargins()
		size += QSize(left + right, top + bottom)
		return size

	def doLayout(self, rect, testOnly):
		x = rect.x()
		y = rect.y()
		lineHeight = 0
		spacing = self.horizontalSpacing()

		# Phase 1: Group items into rows
		rows = []
		current_row = []
		current_row_width = 0

		for item in self.itemList:
			item_width = item.sizeHint().width()
			if current_row and x + item_width > rect.right():
				rows.append((current_row, current_row_width))
				current_row = []
				x = rect.x()
				current_row_width = 0

			current_row.append(item)
			x += item_width + spacing
			current_row_width += item_width + spacing

		if current_row:
			rows.append((current_row, current_row_width))

		# Calculate total height for vertical centering
		total_height = 0
		for row, _ in rows:
			rowHeight = max([item.sizeHint().height() for item in row]) if row else 0
			total_height += rowHeight + self.verticalSpacing()
		if rows:
			total_height -= self.verticalSpacing()

		vertical_offset = (rect.height() - total_height) // 2 if rect.height() > total_height else 0

		# Phase 2: Layout rows with centering and animations
		y = rect.y() + vertical_offset
		for row, row_width in rows:
			actual_row_width = row_width - spacing if row_width > 0 else 0
			x_offset = rect.x() + (rect.width() - actual_row_width) // 2
			x_offset = max(rect.x(), x_offset)
			lineHeight = 0

			for item in row:
				lineHeight = max(lineHeight, item.sizeHint().height())
				if not testOnly:
					target_rect = QRect(QPoint(x_offset, y), item.sizeHint())
					wid = item.widget()
					if wid:
						if not hasattr(wid, '_flow_anim'):
							wid._flow_anim = QPropertyAnimation(wid, b"geometry")
							wid._flow_anim.setDuration(300)
							wid._flow_anim.setEasingCurve(QEasingCurve.OutCubic)
							wid.setGeometry(target_rect)
						else:
							if wid.geometry() != target_rect:
								wid._flow_anim.stop()
								wid._flow_anim.setStartValue(wid.geometry())
								wid._flow_anim.setEndValue(target_rect)
								wid._flow_anim.start()
				x_offset += item.sizeHint().width() + spacing

			y += lineHeight + self.verticalSpacing()

		return total_height

	def smartSpacing(self, pm):
		parent = self.parent()
		if not parent:
			return -1
		elif parent.isWidgetType():
			return parent.style().pixelMetric(pm, None, parent)
		else:
			return parent.spacing()