from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.behaviors import CommonElevationBehavior, CircularElevationBehavior, RectangularRippleBehavior, CircularRippleBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as C
from plyer import filechooser, gps

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
    pass

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
            product_layout = sm.get_screen('main').ids.main_product_layout
            self.add_products(product_layout, "")
        except Exception as e:
            print(e)

    def add_products(self, Layout, product_card):
        self.Layout = Layout
        self.product_card = product_card
        
        
        products= db.get_data('/products/')
        
        def add(*args):
            global MainApp
                
            pair_list = self.make_pair(productlist)
                
            for i in pair_list:
                    
                layout= MDBoxLayout(md_bg_color= [0,0,0,1],
                        spacing= "10dp",
                        padding= "10dp",
                        adaptive_height= True)
                    
                for j in i:
                    card= ProductCard(size_hint= [.2, None],
                            size= self.product_card.size,
                                md_bg_color= [1,1,1,1],
                                elevation= 2,
                                radius= [10])
                    img= products[j]['url']
                    img = img.replace('https://storage.googleapis.com/icon-7623d.appspot.com/products/', '')
                    img = f"https://firebasestorage.googleapis.com/v0/b/icon-7623d.appspot.com/o/products%2F{img}?alt=media&token=18409308-326b-4ac7-b866-52105f2cef3f"
                    price = products[j]['price']
                    image= AsyncImage(source= img,
                                    size_hint= [.75, .75],
                                    pos_hint= {'center_x': .5, 'center_y': .55})
                    label= MDLabel(text= f'Rs. {price}', pos_hint= {'center_x': .53, 'center_y': .12}, bold= True,)
                    btn_layout= ButtonLayout(size_hint= [1, 1], pos_hint= {"center_x": .5, "center_y": .5})
                    btn_fun = partial(MainApp().change_screen, "Edit Product", "ChangeScreen", {"title": j, "price": products[j]['price'], "img_url": img}) if user.teacher else partial(self.buy_request, j)
                    btn_layout.bind(on_release= btn_fun)
                    card.add_widget(image)
                    card.add_widget(label)
                    card.add_widget(btn_layout)
                    layout.add_widget(card)
                        
                    
                        
                self.Layout.add_widget(layout)
                self.dialog.dismiss()
        
        if (products != None and self.Layout.children == []):
            productlist = []
            for k, v in products.items():
                productlist += [k]
                
            '''self.dialog= MDDialog(text= "Loading...",)
            self.dialog.open()
            Clock.schedule_once(add, 0.5) '''
        
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

    def search_bar_up_anim(self, **kwargs):
        print(kwargs)
                
        
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

sm = ScreenManager()
user = User()

class Utkrishi(MDApp):
    def build(self):
        Builder.load_file("Utkrishi.kv")
        self.loggedin = False
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

            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
            ])
            
            gps.configure(on_location=self.gps_on_location)
            gps.start()
        else:
            print("Location is not available for ", platform, " system.")
        
        return sm
    
    def gps_on_location(self, **kwargs):
        sm.get_screen('login').ids.test_lb.text = kwargs
        print("python_location: ", kwargs)
        
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
