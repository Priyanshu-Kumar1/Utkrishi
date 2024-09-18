from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivy.lang import Builder
from kivy.animation import Animation
from kivymd.uix.button import MDIconButton
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.properties import NumericProperty, ListProperty, VariableListProperty, ColorProperty, StringProperty, ObjectProperty
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.event import EventDispatcher

kv = '''
#:import C kivy.utils.get_color_from_hex

<IconBtn>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix

<SearchBar>
    size_hint: self.default_search_size_hint
    size: self.default_search_size
    default_radius: "15dp", "15dp", "15dp", "15dp"
    radius: self.default_radius
    pos_hint: {'center_x': .5, 'center_y': .5}
    _separator_color: 0,0,0,0
    md_bg_color: self.search_view_color

    MDFloatLayout:
        md_bg_color: root.search_bar_color
        size_hint: 1, 1
        radius: root.radius
        pos_hint: {"x": 0, "center_y": .5}
        canvas.before:
            Color:
                rgba: root.border_color  # Initial border color (transparent)
            Line:
                width: 1.5  # Border width
                rounded_rectangle: [self.x, self.y, self.width, self.height] + root.radius

        canvas.after:
            Color:
                rgba: root._separator_color

            Line:
                width: 1  # Border width
                points: self.x, self.y, self.width, self.y
    
        IconBtn:
            icon: root.left_icon
            _left_icon: root.left_icon
            icon_color: root.left_icon_color
            pos_hint: {'x': .01, 'center_y': .5}
            size_hint: None, None
            size: "30dp", "30dp"
            theme_text_color: 'Custom'
            text_color: 0, 0, 0, 1
            on_release: root.close_search_view()
            
        TextInput:
            hint_text: "Search..."
            background_color: 0,0,0,0
            pos_hint: {'center_x': .51, 'center_y': .5}
            cursor_color: 0,0,0,1
            font_size: dp(18)
            size_hint: .78, 1
            multiline: False
            input_type: "text"
            keyboard_suggestions: True
            padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            on_touch_up: if self.collide_point(*args[1].pos): root.on_input_focus(self)
            on_text_validate: root.searched()
            on_text: root.text = self.text

        IconBtn:
            icon: root.right_icon
            theme_icon_color: "Custom"
            icon_color: root.right_icon_color
            icon_size: "24dp"
            pos_hint: {"right": .99, "center_y": .5}
            on_release: root.trigger_right_btn_function()
'''


class IconBtn(MDIconButton):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super(IconBtn, self).__init__(**kwargs)
        self.search_open_ico_anim = Animation(angle = -180, duration=.2)
        self.search_open_ico_anim.bind(on_complete=self.on_complete_open_anim)
        self.search_close_ico_anim = Animation(angle = 180, duration=.2)
        self.search_close_ico_anim.bind(on_complete=self.on_complete_close_anim)
        self._left_icon = ""

    def on_complete_open_anim(self, *kwargs):
        self.angle = 0
        self.icon = "arrow-left"

    def on_complete_close_anim(self, *kwargs):
        self.angle = 0
        self.icon = self._left_icon

    def open_start_animation(self):
        self.search_open_ico_anim.start(self)
    
    def close_start_animation(self):
        self.search_close_ico_anim.start(self)

class SearchBar(MDFloatLayout, EventDispatcher):
    default_search_size_hint = ListProperty([1, 1])
    default_search_size = ListProperty(["300dp", "60dp"])
    search_text_field_size = ListProperty(["300dp", "60dp"])
    open_search_size_hint = ListProperty([1, 1])
    default_radius = VariableListProperty(default_value= "15dp", length=4)
    open_radius = VariableListProperty(default_value= "15dp", length=4)
    search_bar_color = ColorProperty([.8,.8,.8,1])
    search_view_color = ColorProperty([.8,.8,.8,1])
    border_color = ColorProperty([1,1,1,0])
    separator_color = ColorProperty([.5,.5,.5,1])
    left_icon_color = ColorProperty([0,0,0,1])
    right_icon_color = ColorProperty([0,0,0,1])
    left_icon = StringProperty("menu")
    right_icon = StringProperty("microphone")
    text = StringProperty("")
    search_function = ObjectProperty(None)

    def trigger_search(self):
        # Dispatch the on_search event
        self.dispatch('on_search')

    def trigger_left_btn_function(self):
        # Dispatch the on_search event
        self.dispatch('on_left_btn_press')

    def trigger_right_btn_function(self):
        # Dispatch the on_search event
        self.dispatch('on_right_btn_press')

    def __init__(self, **kwargs):
        super(SearchBar, self).__init__(**kwargs)
        # Register the on_search event, which can be overridden in KV
        self.register_event_type('on_search')
        self.register_event_type('on_left_btn_press')
        self.register_event_type('on_right_btn_press')
        self.open = False
        self.touch_count = 0


    def on_search(self, *args):
        pass  # Will be overridden in KV

    def on_left_btn_press(self, *args):
        pass  # Will be overridden in KV

    def on_right_btn_press(self, *args):
        pass  # Will be overridden in KV

    def on_right_icon_color(self, *args):
        self.children[-1].children[-1].icon_color= self.right_icon_color

    def on_input_focus(self, input_field):

        if self.touch_count == 0:

            self.parent_size = self.parent.size

            self.default_search_size = [dp(float(x[:-2])) if isinstance(x, str) and x.endswith('dp') else x for x in self.default_search_size]
            
            if self.size_hint_x != None:
                self.open_anime_x = Animation(size_hint_x=self.open_search_size_hint[0], duration=.2)
            else:
                self.open_anime_x = Animation(width=self.parent_size[0], duration=.2)

            if self.size_hint_y != None:
                self.open_anime_y = Animation(size_hint_x=self.open_search_size_hint[1], duration=.2)
            else:
                self.open_anime_y = Animation(height=self.parent_size[1], duration=.2)
            

            self._border_color = self.border_color
            self._pos_hint = self.pos_hint
            icon = self.children[-1].children[-1]
            if self.size_hint_y == self.default_search_size_hint[1] != None:
                self.children[-1].size_hint_y = None
                self.children[-1].size = self.search_text_field_size
                self.pos_hint = {"center_x": .5, "top": 1}
                self.open_anime_x.start(self)
                self.open_anime_y.start(self)
                self.radius = self.open_radius
                self.border_color = [0,0,0,0]
                self.icon_angle = 60
                self._separator_color = self.separator_color
                self.children[-1].pos_hint = {"center_x": .5, "top": 1}
                icon.open_start_animation()

            elif self.size_hint_y == self.default_search_size_hint[1] == None:
                if self.height == self.default_search_size[1]:
                    self.children[-1].size_hint_y = None
                    self.children[-1].size = self.search_text_field_size
                    self.pos_hint = {"center_x": .5, "top": 1}
                    self.open_anime_x.start(self)
                    self.open_anime_y.start(self)
                    self.radius = self.open_radius
                    self.border_color = [0,0,0,0]
                    self.icon_angle = 60
                    self._separator_color = self.separator_color
                    self.children[-1].pos_hint = {"center_x": .5, "top": 1}
                    icon.open_start_animation()


    def searched(self, *args):
        self.close_search_view()
        self.trigger_search()


    def close_search_view(self):
        if self.size_hint_y != self.default_search_size_hint[1]:

            if self.default_search_size_hint[0] != None:
                self.close_anime_x = Animation(size_hint_x=self.default_search_size_hint[0], duration=.2)
            else:
                self.close_anime_x = Animation(width=self.default_search_size[0], duration=.2)

            if self.default_search_size_hint[1] != None:
                self.close_anime_y = Animation(size_hint_x=self.default_search_size_hint[1], duration=.2)
            else:
                self.close_anime_y = Animation(height=self.default_search_size[1], duration=.2)
                self.close_anime_y.bind(on_complete = self.on_complete_close_anim_y)

            self.close_anime_x.start(self)
            self.close_anime_y.start(self)
            self.radius = self.default_radius
            self.pos_hint = self._pos_hint
            self._separator_color = [0,0,0,0]
            self.children[-1].pos_hint = {"center_x": .5, "center_y": .5}
            self.children[-1].children[-1].close_start_animation()
            self.children[-1].children[-1].search_open_ico_anim.cancel(self.children[-1].children[-1])
            
        else:
            if self.size_hint_y == self.default_search_size_hint[1] == None:
                if self.height != self.default_search_size[1]:

                    if self.default_search_size_hint[0] != None:
                        self.close_anime_x = Animation(size_hint_x=self.default_search_size_hint[0], duration=.2)
                    else:
                        self.close_anime_x = Animation(width=self.default_search_size[0], duration=.2)

                    if self.default_search_size_hint[1] != None:
                        self.close_anime_y = Animation(size_hint_x=self.default_search_size_hint[1], duration=.2)
                    else:
                        self.close_anime_y = Animation(height=self.default_search_size[1], duration=.2)
                        self.close_anime_y.bind(on_complete = self.on_complete_close_anim_y)

                    self.close_anime_x.start(self)
                    self.close_anime_y.start(self)
                    self.radius = self.default_radius
                    self.pos_hint = self._pos_hint
                    self._separator_color = [0,0,0,0]
                    self.children[-1].children[-1].close_start_animation()
                    self.children[-1].children[-1].search_open_ico_anim.cancel(self.children[-1].children[-1])

    def on_complete_close_anim_y(self, *args):
        self.children[-1].size_hint_y = 1
        self.children[-1].pos_hint = {"center_x": .5, "center_y": .5}
        self.border_color = self._border_color


Builder.load_string(kv)