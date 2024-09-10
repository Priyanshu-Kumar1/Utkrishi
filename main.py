from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import NoTransition
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as C
from plyer import filechooser, gps
from kivy.clock import mainthread
from kivy.animation import Animation


from login import sign_up
import database as db
from CloudStorage import upload_file

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class Card(CommonElevationBehavior, MDFloatLayout):
    pass

class ButtonLayout(ButtonBehavior, MDFloatLayout):
    pass

class NavButton(ButtonLayout):
    pass

class User():
    def __init__(self, username=None, email=None, type=None):
        self.username = username
        self.email = email
        self.type = type

class LanguageSelectionScreen(MDScreen):
    def change_screen(self):
        self.manager.current = "main"

class MainScreen(MDScreen):
    def change_screen(self):
        if user.type == None:
            self.manager.current = "login"

        elif user.type == "Seller":
            self.manager.current = "addproducts"
        
    def show_layout(self, layout):
        layout.pos_hint= {'x': 0}
        for i in self.ids.main_layout.children:
            if(i != layout):
                i.pos_hint= {'x': 1}
            else:
                i.pos_hint= {'x': 0}

    def on_enter(self, *args):
        try:
            self.add_products()
        except Exception as e:
            print(e)

    def add_products(self):
        products= db.get_data('/products/')
        
        self.add(products)

    def add(self, product_list):
        product_layout = sm.get_screen('main').ids.main_product_layout
        product_row_container = MDBoxLayout(
                                size_hint=[.9, None],
                                size= [0, "200dp"],
                                spacing= "20dp",
                                pos_hint= {'center_x': .5},
                            )

        if product_list is not None:
            for k, v in product_list.items():
                for seller, item in v.items():
                    for product, product_details in item.items():
                        if product_details["id"] not in self.ids.keys():
                            if len(product_row_container.children) < 2:
                                print(len(product_row_container.children))
                            else:
                                print(len(product_row_container.children))
                                product_row_container = MDBoxLayout(
                                    size_hint=[.9, None],
                                    size= [0, "200dp"],
                                    spacing= "20dp",
                                    pos_hint= {'center_x': .5},
                                )
                            product_card = Card(
                                size_hint= [.4, 1],
                                elevation= 1,
                                md_bg_color= [1,1,1,1],
                                radius= "10dp",
                            )
                            product_img = AsyncImage(
                                source= product_details["url"],
                                size_hint= [.5, .5],
                                pos_hint= {'center_x': .5, 'top': 1},
                            )
                            product_name_lb = MDLabel(
                                text= product,
                                halign = "center",
                                pos_hint={'center_x': .5, 'center_y': .4}
                            )
                            product_price_lb = MDLabel(
                                text= "₹"+product_details["price"]+product_details["unit_type"],
                                font_size= 24,
                                halign = "center",
                                pos_hint={'center_x': .5, 'center_y': .1}
                            )
                            product_card.add_widget(product_img)
                            product_card.add_widget(product_name_lb)
                            product_card.add_widget(product_price_lb)
                            product_row_container.add_widget(product_card)
                            try:
                                product_layout.add_widget(product_row_container)
                            except:
                                pass
                            self.ids[product_details["id"]] = product_card
            product_layout.add_widget(Widget(
                size_hint_y= None,
                height= "60dp"
            ))

    def scroll_touch_down(self, touch_point_x, touch_point_y, search_bar, nav_bar):
        if not (search_bar.collide_point(touch_point_x, touch_point_y) or nav_bar.collide_point(touch_point_x, touch_point_y)):
            self.touched_down_x = touch_point_x
            self.touched_down_y = touch_point_y
        
    def scroll_touch_up(self, touch_point_x, touch_point_y, navbar):
        if self.touched_down_y < touch_point_y:
            self.nabar_up_anim = Animation(y=navbar.parent.height, duration=.1)
            self.nabar_up_anim.start(navbar)

        if self.touched_down_y > touch_point_y:
            self.nabar_down_anim = Animation(y=navbar.parent.height-navbar.height, duration=.1)
            self.nabar_down_anim.start(navbar)
                
        
class LoginScreen(MDScreen):
    
    def change_screen(self):
        self.manager.current = "main"
    
    def login(self, email=None, password=None):
        email = "rprem058@gmail.com"
        password = "test"
        loggeduser = sign_up(email, password)
        user.username = email.split("@")[0]
        user.email = email
        user.uid = loggeduser.uid
        if user.type == "Buyer":
            sm.get_screen('main').ids.login_btn.icon = "cart"
            sm.get_screen('main').ids.login_btn.text = "Cart"
        else:
            sm.get_screen('main').ids.login_btn.icon = "plus"
            sm.get_screen('main').ids.login_btn.text = "ADD"
            
        self.manager.current = "main"
        
class AddProductsScreen(MDScreen):
    def change_screen(self):
        self.manager.current = "main"

class FormScreen(MDScreen):
    pass

sm = ScreenManager(transition=NoTransition())
user = User()

class Utkrishi(MDApp):
    def build(self):
        Builder.load_file("Utkrishi.kv")
        self.loggedin = False
        self.language = "English"
        sm.add_widget(LanguageSelectionScreen(name = 'LanguageSelectionScreen'))
        sm.add_widget(MainScreen(name = 'main'))
        sm.add_widget(LoginScreen(name = 'login'))
        sm.add_widget(AddProductsScreen(name = 'addproducts'))
        sm.add_widget(FormScreen(name = 'form'))
        try:
            app.item_type = ""
            login_menu_items = [
                {
                    "viewclass": "IconListItem",
                    "text": "Buyer",
                    "height": dp(56),
                    "on_release": lambda x="Buyer": self.set_login_item(x),
                },
                {
                    "viewclass": "IconListItem",
                    "text": "Seller",
                    "height": dp(56),
                    "on_release": lambda x="Seller": self.set_login_item(x),
                }
            ]
            self.menu = MDDropdownMenu(
                caller=sm.get_screen('login').ids.drop_item,
                items=login_menu_items,
                position="center",
                width_mult=4,
            )
            self.menu.bind()
            
            category_menu_items = [
                {
                    "viewclass": "IconListItem",
                    "text": "Veggies & Fruits",
                    "height": dp(56),
                    "on_release": lambda x="Veggies & Fruits": self.set_item_type(x),
                },
                {
                    "viewclass": "IconListItem",
                    "text": "Pharma",
                    "height": dp(56),
                    "on_release": lambda x="Pharma": self.set_item_type(x),
                },
                {
                    "viewclass": "IconListItem",
                    "text": "Dairy",
                    "height": dp(56),
                    "on_release": lambda x="Dairy": self.set_item_type(x),
                },
                {
                    "viewclass": "IconListItem",
                    "text": "Grocery",
                    "height": dp(56),
                    "on_release": lambda x="Grocery": self.set_item_type(x),
                }
            ]
            self.pmenu = MDDropdownMenu(
                caller=sm.get_screen('addproducts').ids.category_drop_item,
                items=category_menu_items,
                position="center",
                width_mult=4,
            )
            self.pmenu.bind()

            unit_type_drop_down_items = [
                {
                    "viewclass": "OneLineListItem",
                    "text": "/Kg",
                    "height": dp(56),
                    "on_release": lambda x="/Kg": self.set_unit_type(x),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "/g",
                    "height": dp(56),
                    "on_release": lambda x="/g": self.set_unit_type(x),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "/Pc",
                    "height": dp(56),
                    "on_release": lambda x="/Pc": self.set_unit_type(x),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "/ml",
                    "height": dp(56),
                    "on_release": lambda x="ml": self.set_unit_type(x),
                },
                {
                    "viewclass": "OneLineListItem",
                    "text": "/l",
                    "height": dp(56),
                    "on_release": lambda x="/l": self.set_unit_type(x),
                },
            ]

            self.unit_type_menu = MDDropdownMenu(
                caller=sm.get_screen('addproducts').ids.unit_type_drop_down,
                items=unit_type_drop_down_items,
                position="center",
                width_mult=4,
            
            )
            self.unit_type_menu.bind()
        except Exception as e:
            print(e)
        
        if ( platform == 'android' ):
            from android.permissions import request_permissions, Permission
            from android.storage import app_storage_path, primary_external_storage_path
            #set_bars_colors(C('#202124'), C('#202124'))

            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
            ])
            
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start()
        else:
            print("Location is not available for ", platform, " system.")
        
        return sm
    
    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        print("Location is available for ", self.gps_location)

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)
        
    def set_login_item(self, text_item):
        sm.get_screen('login').ids.drop_item.set_item(text_item)
        user.type = text_item
        self.menu.dismiss()
        
    def set_item_type(self, text_item):
        sm.get_screen('addproducts').ids.category_drop_item.set_item(text_item)
        app.item_type = text_item
        self.pmenu.dismiss()

    def set_unit_type(self, text_item):
        sm.get_screen('addproducts').ids.unit_type_drop_down.set_item(text_item)
        app.item_type = text_item
        self.pmenu.dismiss()
        
    def file_manager_open(self):
        raw_path = filechooser.open_file(filters=[("Comma-separated Values", "*.png","*.jpeg","*.jpg",)])
        print(raw_path[0])
        sm.get_screen('addproducts').ids.product_img.source = raw_path[0]
        
    def addproducts(self, product_img, product_name, product_price, unit_type, category):
        print(product_name, product_price, product_img, app.item_type)
        product_url= upload_file(product_img, f'{user.username}/products/{category}/{product_name}') 
        existing_data = db.get_data(f'products/{category}/{user.username}/{product_name}')
        in_stalk = 0
        if existing_data:
            if existing_data["in_stalk"] != '0':
                in_stalk = int(existing_data["in_stalk"]) + 0
        product= {
            "id": product_name+"@"+user.uid,
            "url": product_url,
            "price": product_price,
            "unit_type": unit_type,
            "in_stalk": str(in_stalk),
            }
        db.store(product, f'products/{category}/{user.username}/{product_name}')

app = Utkrishi()

if __name__=="__main__":
    app.run()
