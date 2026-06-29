# -*- coding: utf-8 -*-
import platform
from os import system
import subprocess
from PyQt5.Qt import Qt
from PyQt5.QtCore import QRect, QTimer, QRectF, pyqtSlot
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtWidgets import QApplication
from deepinesStore.settings import SettingsManager
from deepinesStore.appearance import AppearanceManager


class AppearanceMixin:
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app_mgr = AppearanceManager.get_instance()
		self.border_radius = self.app_mgr.radius

		# Connect to signals
		self.app_mgr.radius_changed.connect(self._on_radius_changed)

		# Delay applying stylesheet slightly until UI is fully initialized
		QTimer.singleShot(50, self.update_dynamic_stylesheet)

	@pyqtSlot(int)
	def _on_radius_changed(self, radius: int):
		self.border_radius = radius
		self.update_blur_region()
		self.update_dynamic_stylesheet()

	def update_dynamic_stylesheet(self):
		bg_color = "rgba(30, 30, 30, 200)"

		# Determine target widget ID
		target_id = "#centralwidget"
		if self.objectName() == "LoadingScreen":
			target_id = "#LoadingScreen_central"

		r = 0 if self.isMaximized() else self.border_radius

		style = f"""
		{target_id}{{
			background-color: {bg_color};
			border: 1.5px solid rgba(60, 60, 60, 120);
			border-radius: {r}px;
		}}
		#btn_close, #btn_minimize, #btn_zoom {{
			min-width: 36px;
			min-height: 36px;
			border-radius: 10px;
			background-color: transparent;
		}}
		#btn_minimize:hover, #btn_zoom:hover, #btn_close:hover {{
			background-color: rgba(50, 50, 50, 100);
		}}
		"""

		if target_id == "#LoadingScreen_central":
			style += """
			QLabel{
				color: #b5c5d1;
			}
			"""

		self.setStyleSheet(style)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.update_blur_region()

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			window = self.windowHandle()
			if window:
				window.startSystemMove()
		super().mousePressEvent(event)

	def changeEvent(self, event):
		from PyQt5.QtCore import QEvent
		super().changeEvent(event)
		if event.type() == QEvent.WindowStateChange:
			self.update_blur_region()
			self.update_dynamic_stylesheet()

	def update_blur_region(self):
		if platform.system() != 'Windows':
			w = self.width()
			h = self.height()
			r = 0 if self.isMaximized() else self.border_radius

			if r <= 0:
				subprocess.Popen(f'xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION 0 -id {int(self.winId())}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
				return

			path = QPainterPath()
			path.addRoundedRect(QRectF(0, 0, w, h), r, r)
			region = QRegion(path.toFillPolygon().toPolygon())
			rects = list(region.rects())

			# X11 xprop has a 64-element limit (16 rectangles).
			# Merge adjacent rectangles with the smallest width differences until we are under the limit.
			while len(rects) > 15:
				best_diff = float('inf')
				best_idx = 0
				for i in range(len(rects) - 1):
					diff = abs(rects[i].width() - rects[i+1].width())
					if diff < best_diff:
						best_diff = diff
						best_idx = i

				r1 = rects[best_idx]
				r2 = rects[best_idx+1]

				# Merge strictly inside (narrowest boundaries) to prevent blurred lines outside the border
				new_x = max(r1.x(), r2.x())
				new_right = min(r1.x() + r1.width(), r2.x() + r2.width())
				new_y = min(r1.y(), r2.y())
				new_bottom = max(r1.y() + r1.height(), r2.y() + r2.height())

				merged = QRect(new_x, new_y, new_right - new_x, new_bottom - new_y)
				rects.pop(best_idx)
				rects[best_idx] = merged

			rect_str = ','.join([f"{rc.x()},{rc.y()},{rc.width()},{rc.height()}" for rc in rects])
			subprocess.Popen(f'xprop -f _KDE_NET_WM_BLUR_BEHIND_REGION 32c -set _KDE_NET_WM_BLUR_BEHIND_REGION {rect_str} -id {int(self.winId())}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

class GeometryMixin:
	def showEvent(self, event):
		settings = SettingsManager.get_instance()
		geometry_data = settings.get("geometry")

		if geometry_data and not hasattr(self, '_geometry_restored'):
			try:
				if all(k in geometry_data for k in ("x", "y", "w", "h")):
					target_rect = QRect(geometry_data["x"], geometry_data["y"], geometry_data["w"], geometry_data["h"])
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
			settings = SettingsManager.get_instance()
			settings.set("geometry", data)
		super().closeEvent(event)
