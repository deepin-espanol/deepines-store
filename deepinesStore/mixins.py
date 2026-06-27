# -*- coding: utf-8 -*-
import json
from PyQt5.Qt import Qt
from PyQt5.QtCore import QRect, QTimer
from PyQt5.QtWidgets import QApplication
from deepinesStore.demoted_actions import write_file, config_dir

class EventsMixin:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.drag_position = None
		self._user_modified_geometry = False

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.setProperty("previous_position", self.pos())
			self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
		event.accept()

	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.LeftButton and self.drag_position is not None:
			self.setCursor(Qt.SizeAllCursor)
			if not self.isMaximized():
				self.move(event.globalPos() - self.drag_position)
				self._user_modified_geometry = True
			else:
				self.showNormal()
		event.accept()

	def mouseReleaseEvent(self, event):
		self.setCursor(Qt.ArrowCursor)
		self.drag_position = None

	def keyPressEvent(self, event):
		if self.drag_position is not None and event.key() == Qt.Key_Escape:
			previous_position = self.property("previous_position")
			self.setCursor(Qt.ArrowCursor)
			if previous_position is not None:
				self.move(previous_position)
				self.drag_position = None
			event.accept()
		else:
			event.ignore()

	def resizeEvent(self, event):
		self.drag_position = None
		event.accept()

class GeometryMixin:
	def showEvent(self, event):
		geom_file = config_dir / 'geometry.json'
		if geom_file.exists() and not hasattr(self, '_geometry_restored'):
			try:
				with open(geom_file, 'r') as f:
					data = json.load(f)
					if all(k in data for k in ("x", "y", "w", "h")):
						target_rect = QRect(data["x"], data["y"], data["w"], data["h"])
						valid = False
						app = QApplication.instance()
						desktop = app.desktop()
						for i in range(desktop.screenCount()):
							if desktop.screenGeometry(i).contains(target_rect.center()):
								valid = True
								break
						if valid:
							self.setGeometry(target_rect)
			except Exception as e:
				print(f"Failed to load geometry: {e}")
			self._geometry_restored = True
		super().showEvent(event)
		if not hasattr(self, '_initial_geometry'):
			# Delay capturing initial geometry slightly to allow the window manager to finish placing it
			QTimer.singleShot(200, lambda: setattr(self, '_initial_geometry', self.normalGeometry() if self.isMaximized() else self.geometry()))

	def closeEvent(self, event):
		geom = self.normalGeometry() if self.isMaximized() else self.geometry()
		initial = getattr(self, '_initial_geometry', None)
		
		# If the user moved or resized the window from its initial spot, save the new geometry
		if initial is not None and geom != initial:
			data = {
				"x": geom.x(),
				"y": geom.y(),
				"w": geom.width(),
				"h": geom.height()
			}
			geom_file = config_dir / 'geometry.json'
			try:
				json_bytes = json.dumps(data).encode('utf-8')
				dummy = type('obj', (object,), {'content': json_bytes})
				write_file(dummy, geom_file)
			except Exception as e:
				print(f"Failed to save geometry: {e}")
		super().closeEvent(event)
