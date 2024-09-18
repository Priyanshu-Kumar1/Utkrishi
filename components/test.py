from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.label import Label

from kivy.core.window import Window
Window.size = (380, 600)


# Define the KV string
kv_string = """
#:import SearchBar SearchBar.SearchBar

MDFloatLayout:
    
    SearchBar:
        default_search_size_hint: .9, None
        default_search_size: 300, "40dp"
        open_search_size_hint: 1, 1
        default_radius: "10dp"
        left_icon: "magnify"
        border_color: 0,0,0,1
        pos_hint: {'center_x': .5, 'top': .8}
        on_search: app.search_function(self.text)
"""

class HelloWorldApp(MDApp):
    
    def build(self):
        # Load the KV string
        return Builder.load_string(kv_string)
    
    def search_function(self, text):
        print(f"Searching for {text}")
        return

if __name__ == '__main__':
    HelloWorldApp().run()