# -*- coding: utf-8 -*-
"""
Camera Grid App - 安卓横屏相机格子应用
8行x50列数据，可视区域显示4行，默认显示第3-6行
上下滑动每次移动一整行（离散滑动），滑动时不触发格子选中
格子宽度=高度×2，支持左右连续滑动
格子区域占屏幕高度50%，自适应屏幕大小
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp


class VisibleCell(Button):
    """可视格子类"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_row = 0
        self.data_col = 0
        self.data_index = 0
        self.background_color = (1, 1, 1, 1)
        self.color = (0, 0, 0, 1)
        self.font_size = dp(12)
        self.background_normal = ''
        self.background_down = ''
        self.size_hint_x = None
        self.size_hint_y = None


class GridWidget(BoxLayout):
    """顶部网格组件，占屏幕高度50%"""
    def __init__(self, rows=8, cols=50, visible_rows=4, default_start_row=2, on_cell_selected=None, **kwargs):
        super().__init__(**kwargs)
        self.rows = rows
        self.cols = cols
        self.visible_rows = visible_rows
        self.current_start_row = default_start_row
        self.on_cell_selected = on_cell_selected
        self.size_hint_y = 0.5
        self.orientation = 'vertical'
        
        # 数据存储
        self.cell_data = []
        for i in range(rows * cols):
            self.cell_data.append(["", False])
        
        # 默认选中第3行第1列 (row=2, col=0, index=100)
        self.current_index = 2 * cols + 0  # 第3行第1列
        self.cell_data[self.current_index][1] = True
        
        # 触摸追踪
        self.touch_start_pos = None
        self.is_vertical_swiping = False  # 是否正在垂直滑动
        
        self.visible_cells = []
        
        self.scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_y=False,
            do_scroll_x=True,
            bar_width=dp(8)
        )
        
        self.inner_container = BoxLayout(
            size_hint=(None, 1),
            orientation='horizontal'
        )
        
        self.grid_layout = GridLayout(
            rows=visible_rows,
            cols=cols,
            spacing=dp(1),
            padding=(dp(5), dp(2), dp(5), dp(2)),
            size_hint=(None, 1),
        )
        
        cell_height = dp(50)
        cell_width = cell_height * 2
        total_width = cell_width * cols + dp(1) * (cols - 1) + dp(10)
        
        self.grid_layout.width = total_width
        self.inner_container.width = total_width
        
        for i in range(visible_rows * cols):
            cell = VisibleCell()
            cell.width = cell_width
            cell.height = cell_height
            cell.bind(on_release=self.on_visible_cell_release)  # 用 on_release 而不是 on_press
            self.visible_cells.append(cell)
            self.grid_layout.add_widget(cell)
        
        self.inner_container.add_widget(self.grid_layout)
        self.scroll_view.add_widget(self.inner_container)
        self.add_widget(self.scroll_view)
        
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.spacing = dp(1)
        
        Clock.schedule_once(self.update_cell_sizes, 0.1)
        Window.bind(on_resize=self.on_window_resize)
    
    def on_window_resize(self, instance, width, height):
        Clock.schedule_once(self.update_cell_sizes, 0.1)
    
    def update_cell_sizes(self, dt):
        """更新格子尺寸"""
        view_height = self.scroll_view.height
        
        if view_height > 0:
            padding = dp(4)
            spacing_total = dp(1) * (self.visible_rows - 1)
            available_height = view_height - padding - spacing_total
            row_height = available_height / self.visible_rows
            cell_width = row_height * 2
            
            for cell in self.visible_cells:
                cell.width = cell_width
                cell.height = row_height
            
            total_width = cell_width * self.cols + dp(1) * (self.cols - 1) + dp(10)
            self.grid_layout.width = total_width
            self.inner_container.width = total_width
            
            self.cell_width = cell_width
            self.cell_height = row_height
            
            font_size = min(dp(14), row_height * 0.35)
            for cell in self.visible_cells:
                cell.font_size = font_size
            
            self.refresh_visible_cells()
    
    def refresh_visible_cells(self):
        """刷新可视格子显示"""
        for i, cell in enumerate(self.visible_cells):
            visible_row = i // self.cols
            visible_col = i % self.cols
            
            data_row = self.current_start_row + visible_row
            data_index = data_row * self.cols + visible_col
            
            cell.data_row = data_row
            cell.data_col = visible_col
            cell.data_index = data_index
            
            text, is_current = self.cell_data[data_index]
            cell.text = text
            
            if is_current:
                cell.background_color = (0.2, 0.6, 1, 1)
                cell.color = (1, 1, 1, 1)
            else:
                cell.background_color = (1, 1, 1, 1)
                cell.color = (0, 0, 0, 1)
    
    def on_visible_cell_release(self, instance):
        """点击格子释放 - 只有不是滑动时才执行"""
        if not self.is_vertical_swiping:
            self.select_cell(instance.data_index)
    
    def select_cell(self, index):
        """选择格子"""
        self.cell_data[self.current_index][1] = False
        
        self.current_index = index
        self.cell_data[index][1] = True
        
        row = index // self.cols
        if row < self.current_start_row:
            self.current_start_row = row
        elif row >= self.current_start_row + self.visible_rows:
            self.current_start_row = row - self.visible_rows + 1
        
        self.refresh_visible_cells()
        self.scroll_to_cell_horizontal(index)
        
        if self.on_cell_selected:
            cell_content = self.cell_data[index][0]
            self.on_cell_selected(cell_content)
    
    def scroll_to_cell_horizontal(self, index):
        """水平滚动"""
        col = index % self.cols
        
        scroll_x = self.scroll_view.scroll_x
        view_width = self.scroll_view.width
        total_width = self.grid_layout.width
        max_scroll = total_width - view_width
        
        if max_scroll <= 0:
            return
        
        visible_left = scroll_x * max_scroll
        visible_right = visible_left + view_width
        
        cell_x = (self.cell_width + self.spacing) * col
        cell_right = cell_x + self.cell_width
        
        if cell_right > visible_right or cell_x < visible_left:
            cell_center_x = cell_x + self.cell_width / 2
            target_scroll = cell_center_x - view_width / 2
            new_scroll_x = target_scroll / max_scroll
            new_scroll_x = max(0, min(1, new_scroll_x))
            self.scroll_view.scroll_x = new_scroll_x
    
    def scroll_up(self):
        """上滑：可视区域上移"""
        if self.current_start_row > 0:
            self.current_start_row -= 1
            self.refresh_visible_cells()
            print(f"可视区域: 第{self.current_start_row + 1}行 到 第{self.current_start_row + self.visible_rows}行")
    
    def scroll_down(self):
        """下滑：可视区域下移"""
        if self.current_start_row + self.visible_rows < self.rows:
            self.current_start_row += 1
            self.refresh_visible_cells()
            print(f"可视区域: 第{self.current_start_row + 1}行 到 第{self.current_start_row + self.visible_rows}行")
    
    def on_touch_down(self, touch):
        """触摸开始"""
        if self.collide_point(*touch.pos):
            self.touch_start_pos = (touch.x, touch.y)
            self.is_vertical_swiping = False
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        """触摸移动 - 检测是否是垂直滑动"""
        if self.touch_start_pos is not None:
            start_x, start_y = self.touch_start_pos
            delta_y = abs(touch.y - start_y)
            delta_x = abs(touch.x - start_x)
            
            # 如果垂直移动距离大于水平移动且超过阈值，标记为垂直滑动
            if delta_y > dp(30) and delta_y > delta_x:
                self.is_vertical_swiping = True
        
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        """触摸结束 - 处理滑动"""
        if self.touch_start_pos is not None:
            start_x, start_y = self.touch_start_pos
            delta_y = touch.y - start_y
            
            # 如果是垂直滑动，执行滑动操作
            if self.is_vertical_swiping and abs(delta_y) > dp(30):
                if delta_y > 0:
                    self.scroll_down()
                else:
                    self.scroll_up()
            
            self.touch_start_pos = None
            # is_vertical_swiping 会在下次 on_touch_down 时重置
        
        return super().on_touch_up(touch)
    
    def move_to_next(self):
        """移动到下一个格子"""
        self.cell_data[self.current_index][1] = False
        
        self.current_index += 1
        if self.current_index >= self.rows * self.cols:
            self.current_index = 0
        
        self.cell_data[self.current_index][1] = True
        
        row = self.current_index // self.cols
        if row < self.current_start_row:
            self.current_start_row = row
        elif row >= self.current_start_row + self.visible_rows:
            self.current_start_row = row - self.visible_rows + 1
        
        self.refresh_visible_cells()
        self.scroll_to_cell_horizontal(self.current_index)
        
        return self.cell_data[self.current_index][0]
    
    def set_current_cell_text(self, text):
        """设置当前格子内容"""
        self.cell_data[self.current_index][0] = str(text) if text else ""
        self.refresh_visible_cells()


class CameraPreview(BoxLayout):
    """相机预览组件"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.camera = None
        self.camera_available = False
        
        self.camera_container = BoxLayout(size_hint=(1, 1))
        self.placeholder_label = Label(
            text='相机预览区域\n点击对焦',
            font_size=dp(24),
            color=(0.5, 0.5, 0.5, 1)
        )
        self.camera_container.add_widget(self.placeholder_label)
        self.add_widget(self.camera_container)
        
        Clock.schedule_once(self.init_camera, 0.5)
        
    def init_camera(self, dt):
        try:
            self.camera_container.clear_widgets()
            self.camera = Camera(play=True, resolution=(1280, 720), size_hint=(1, 1))
            self.camera_container.add_widget(self.camera)
            self.camera_available = True
        except:
            self.camera_container.clear_widgets()
            self.placeholder_label.text = '相机预览区域\n(相机不可用)'
            self.camera_container.add_widget(self.placeholder_label)
            self.camera_available = False
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(f"对焦位置: {touch.pos}")
            return True
        return super().on_touch_down(touch)


class ControlPanel(BoxLayout):
    """右侧控制面板"""
    def __init__(self, on_capture, on_retake, on_next, on_text_changed=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(15)
        self.padding = dp(10)
        
        self.on_capture = on_capture
        self.on_retake = on_retake
        self.on_next = on_next
        self.on_text_changed = on_text_changed
        self.is_captured = False
        self.is_blank_cell = False  # 当前选中的是否是空白格子
        self.counter = 0
        
        self.text_input = TextInput(
            hint_text='识别结果将显示在这里',
            multiline=True,
            font_size=dp(18),
            size_hint_y=0.6,
            padding=dp(10)
        )
        self.text_input.bind(text=self.on_text_input_changed)
        self.add_widget(self.text_input)
        
        button_container = BoxLayout(orientation='horizontal', spacing=dp(15), size_hint_y=0.4)
        
        self.capture_btn = Button(text='拍照', font_size=dp(20), 
                                   background_color=(0.2, 0.7, 0.3, 1), color=(1, 1, 1, 1),
                                   background_normal='', background_down='')
        self.capture_btn.bind(on_press=self.on_capture_press)
        button_container.add_widget(self.capture_btn)
        
        self.retake_btn = Button(text='重拍', font_size=dp(20),
                                  background_color=(0.9, 0.5, 0.1, 1), color=(1, 1, 1, 1),
                                  background_normal='', background_down='')
        self.retake_btn.bind(on_press=self.on_retake_press)
        button_container.add_widget(self.retake_btn)
        
        self.add_widget(button_container)
        
    def on_capture_press(self, instance):
        if self.is_captured:
            self.on_next()
        else:
            self.on_capture()
            
    def on_retake_press(self, instance):
        self.on_retake()
        
    def set_captured_state(self, is_captured):
        self.is_captured = is_captured
        if is_captured:
            self.capture_btn.text = '下一个'
            self.capture_btn.background_color = (0.2, 0.5, 0.9, 1)
        else:
            self.capture_btn.text = '拍照'
            self.capture_btn.background_color = (0.2, 0.7, 0.3, 1)
            
    def set_text(self, text):
        self.text_input.text = str(text)
        
    def get_text(self):
        return self.text_input.text
    
    def clear_text(self):
        self.text_input.text = ''
        
    def get_next_counter(self):
        self.counter += 1
        return self.counter
    
    def on_text_input_changed(self, instance, value):
        """文本框内容变化时的回调"""
        if self.on_text_changed:
            self.on_text_changed(value)
    
    def set_blank_cell_state(self, is_blank):
        """设置当前格子是否是空白格子"""
        self.is_blank_cell = is_blank


class MainLayout(BoxLayout):
    """主布局"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(5)
        self.spacing = dp(5)
        
        self.grid_widget = GridWidget(
            rows=8, 
            cols=50, 
            visible_rows=4,
            default_start_row=2,
            on_cell_selected=self.on_cell_selected
        )
        self.add_widget(self.grid_widget)
        
        bottom_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=0.5)
        
        self.camera_preview = CameraPreview()
        bottom_layout.add_widget(self.camera_preview)
        
        self.control_panel = ControlPanel(
            on_capture=self.on_capture,
            on_retake=self.on_retake,
            on_next=self.on_next,
            on_text_changed=self.on_text_changed
        )
        bottom_layout.add_widget(self.control_panel)
        
        self.add_widget(bottom_layout)
        
    def on_cell_selected(self, cell_content):
        if cell_content:
            self.control_panel.set_text(cell_content)
            self.control_panel.set_captured_state(True)
            self.control_panel.set_blank_cell_state(False)
        else:
            self.control_panel.clear_text()
            self.control_panel.set_captured_state(False)
            self.control_panel.set_blank_cell_state(True)
    
    def on_text_changed(self, text):
        """文本框内容变化时的处理"""
        # 如果当前是空白格子，根据文本框是否有内容来切换按钮
        if self.control_panel.is_blank_cell:
            if text.strip():
                self.control_panel.set_captured_state(True)
            else:
                self.control_panel.set_captured_state(False)
        
    def on_capture(self):
        counter = self.control_panel.get_next_counter()
        self.control_panel.set_text(str(counter))
        self.control_panel.set_captured_state(True)
        
    def on_retake(self):
        counter = self.control_panel.get_next_counter()
        self.control_panel.set_text(str(counter))
        self.control_panel.set_captured_state(True)
        
    def on_next(self):
        text = self.control_panel.get_text()
        self.grid_widget.set_current_cell_text(text)
        new_cell_content = self.grid_widget.move_to_next()
        
        if new_cell_content:
            self.control_panel.set_text(new_cell_content)
            self.control_panel.set_captured_state(True)
        else:
            self.control_panel.clear_text()
            self.control_panel.set_captured_state(False)


class CameraGridApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        return MainLayout()


if __name__ == '__main__':
    CameraGridApp().run()
