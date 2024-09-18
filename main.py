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
from kivymd.uix.fitimage import FitImage
from kivymd.utils.set_bars_colors import set_bars_colors
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import NoTransition
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.metrics import dp
from kivy.utils import get_color_from_hex as C
from plyer import filechooser, gps
from kivy.clock import mainthread, Clock
from kivy.animation import Animation
from kivy.garden.mapview import MapMarker, MapView
from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.textfield import MDTextField
from kivymd.font_definitions import theme_font_styles
from threading import Thread
from functools import partial


from scripts.cordinate_to_address import get_address
from scripts.DistanceCalc import get_distance
from scripts.User import User
from login import sign_up
import database as db
from Speechrecognizer.facades import stt
from CloudStorage import upload_file


class ShoppingMap(MapView):
    def on_touch_down(self, touch):
        # Check if the touch is colliding with the overlay layout
        if self.parent.children[0].collide_point(*touch.pos):
            # If touch happens in overlay, don't handle map scroll
            return False
        # Otherwise, allow the map to scroll
        return super(ShoppingMap, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        # Same logic for moving: if touching overlay, don't allow map to move
        if self.parent.children[0].collide_point(*touch.pos):
            print(self.parent)
            return False
        return super(ShoppingMap, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.parent.children[0].collide_point(*touch.pos):
            return False
        return super(ShoppingMap, self).on_touch_up(touch)

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class Card(CommonElevationBehavior, MDFloatLayout):
    shadow_color = [0,0,0,.2]

class ButtonLayout(ButtonBehavior, MDFloatLayout):
    pass

class NavButton(ButtonLayout):
    pass

class ProductCard(ButtonLayout):
    product_name = StringProperty()
    product_price = StringProperty()
    image = StringProperty()
    product_selling_unit = StringProperty()
    distance = StringProperty()
    duration = StringProperty()

class SectionProgressBar(ButtonLayout, MDFloatLayout):
    current_section = None
    def section_color(self, section):
        if self.current_section == section:
            self.current_section.children[0].color = [1,1,1,1]
            return C("#4CC955")
        else:
            self.current_section.children[0].color = C("#4CC955")
            return C("#dbf1db")

class CirclarProgress(CommonElevationBehavior, MDFloatLayout):
    def spin(self):
        spin_anim = Animation(angle=360, duration=1)
        spin_anim.bind(on_complete=self.restart_anim)
        spin_anim.start(self)
    
    def restart_anim(self, *args):
        self.angle = 0
        self.spin()

class LanguageSelectionScreen(MDScreen):
    def change_screen(self):
        self.manager.current = "main"

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self._initial_touch_y = None
        self._initial_layout_y = None

    def change_screen(self):
        if user.type == None:
            self.manager.current = "login"

        elif user.type == "Seller":
            self.manager.current = "addproducts"

    def on_touch_down(self, touch):
        if self.ids.drag_handler.collide_point(*touch.pos):
            self.dragable_layout_touch_down(touch)
            return True
        
        return super(MainScreen, self).on_touch_down(touch)
    
    def dragable_layout_touch_down(self, touch):
        self._initial_touch_y = touch.y
        self._initial_layout_y = self.ids.product_list_layout.y
    
    def on_touch_move(self, touch):
        if self._initial_touch_y is not None:
            delta_y = touch.y - self._initial_touch_y
            new_y = self._initial_layout_y + delta_y
            drag_high_limit = self.ids.search_bar_bg.y
            drag_low_limit = 0-(self.height/2)-(self.height/4.5)

            if not ((new_y+self.ids.product_list_layout.height) > drag_high_limit) and not (new_y < drag_low_limit):
                self.ids.product_list_layout.y = new_y

    def on_touch_up(self, touch):
        self._initial_touch_y = None
        self._initial_layout_y = None

    def show_layout(self, layout):
        layout.pos_hint= {'x': 0}
        for i in self.ids.main_layout.children:
            if(i != layout):
                i.pos_hint= {'x': 1}
            else:
                if i == self.ids.shopping_layout:
                    self.nabar_up_anim = Animation(y=self.ids.navbar.parent.height, duration=.1)
                    self.nabar_up_anim.start(self.ids.navbar)
                i.pos_hint= {'x': 0}

    def on_enter(self, *args):
        try:
            my_location_marker = MapMarker(lat=app.geo_cordinates[0], lon=app.geo_cordinates[1], source='assets/my_location.png', size_hint=[None,None], size=["50dp", "50dp"])
            self.ids.shopping_map.add_marker(my_location_marker)
            self.product_list_layout = self.ids.product_list_layout
            self.product_list_layout.y = 0-self.product_list_layout.height
            #self.add_products()
        except Exception as e:
            print(e)

    def add_products(self):
        products= db.get_data('/products/')
        print(products)
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

    def scroll_touch_down(self, touch_point_x, touch_point_y, search_bar, nav_bar, horizontal_scroll):
        if not (search_bar.collide_point(touch_point_x, touch_point_y) or nav_bar.collide_point(touch_point_x, touch_point_y)):
            self.scroll_view_touched = True
            self.touched_down_x = touch_point_x
            self.touched_down_y = touch_point_y

    def move_test(self, touch_point_x, touch_point_y, navbar):
        try:
            if (self.touched_down_y < touch_point_y):
                self.nabar_up_anim = Animation(y=navbar.parent.height, duration=.1)
                self.nabar_up_anim.start(navbar)
                self.is_product_layout_scrolled = False
                self.ids.drag_handler.set_drag_limit(self.ids.search_bar_bg.y)

            if (self.touched_down_y > touch_point_y):
                self.nabar_down_anim = Animation(y=navbar.parent.height-navbar.height, duration=.1)
                self.nabar_down_anim.start(navbar)
                self.is_product_layout_scrolled = False
                self.ids.drag_handler.set_drag_limit(self.ids.search_bar_bg.y)
        except:
            pass

    def search_product(self, shopping_layout, search_text):
        self.product_list_layout = self.ids.product_list_layout
        self.ids.product_list_boxlayout.clear_widgets()
        anim = Animation(y = (0-(self.height/2)), duration=.1)
        anim.start(self.product_list_layout)
        Thread1 = Thread(target=self.get_products, args=(search_text, shopping_layout))
        Thread1.start()

    def get_products(self, search_text, shopping_layout):
        self.show_layout(shopping_layout)
        products= db.get_data('/products/')
        self.product_details = {}

        for product_name, product_list in products.items():
            if search_text.upper() in product_name.upper():
                for product_id, product in product_list.items():
                    prod_lat = product["location"]['latitude']
                    prod_lon = product["location"]['longitude']

                    distance, duration = get_distance(app.geo_cordinates, [prod_lat, prod_lon])
                    print(distance, duration)
                    mapview = self.ids.shopping_map
                    product["product name"] = product_name
                    product["distance"] = distance
                    product["duration"] = duration
                    self.product_details[product["id"]] = product
                    self.show_product_details(product["id"])
                    self.add_product_pin(mapview, prod_lat, prod_lon, product)
    @mainthread
    def add_product_pin(self, mapview, prod_lat, prod_lon, product):
        marker = MapMarker(lat = prod_lat, lon = prod_lon, source='assets/marker.png')
        mapview.ids[product["id"]] = marker
        func = partial(self.show_product_details, product["id"])
        marker.bind(on_press=func)
        mapview.add_marker(marker)
                    
    @mainthread
    def show_product_details(self, product_id, *args):
        self.product_list_layout = self.ids.product_list_layout
        self.product_list_boxlayout = self.ids.product_list_boxlayout
        product = self.product_details[product_id]
        product_card = ProductCard(
            image= product["url"],
            product_name= product["product name"],
            product_price= product["price"],
            product_selling_unit= product["unit_type"],
            distance= product["distance"],
            duration= product["duration"],
            size_hint= [None, None],
            size= [self.parent.width - dp(40), "150dp"],
        )
        product_card.bind(on_press= lambda x: self.open_prod_menu(product_id, product_card))
        self.product_list_boxlayout.add_widget(product_card)

    def open_prod_menu(self, product_id, product_card):
        product = self.product_details[product_id]
        product_card.height = "200dp"
        

touch_count = 0

class AddAddressScreen(MDScreen):
    marker_exists = False
    touch_moved = False
    is_processing = False

    def change_screen(self):
        self.manager.current = app.previous_screen

    def on_enter(self):
        try:
            test = theme_font_styles
            print("test" , test)
        except Exception as e:
            print("error: ", e)

    def on_touch_move(self, touch):
        self.touch_moved = True

    def add_pin(self, touch_cordinates_x, touch_cordinates_y):
        global touch_count
        touch_count += 1

        if touch_count == 2:
            touch_count = 0

        if touch_count == 0:
            if not (self.ids.navbar.collide_point(touch_cordinates_x, touch_cordinates_y) or self.ids.address_layout.collide_point(touch_cordinates_x, touch_cordinates_y)):
                if not self.touch_moved:
                    map_view = self.ids.my_address_map
                    components_cordinate_y = touch_cordinates_y - map_view.y
                    touch_geo_cordinates = map_view.get_latlon_at(touch_cordinates_x, components_cordinate_y)
                    my_location_marker = MapMarker(lat=touch_geo_cordinates[0], lon=touch_geo_cordinates[1], source='assets/marker.png')
                    
                    if self.marker_exists:
                        map_view.remove_marker(map_view.ids.touched_marker)
                        map_view.ids["touched_marker"] = my_location_marker
                        map_view.add_marker(my_location_marker)
                        self.marker_exists = True
                    else:
                        map_view.ids["touched_marker"] = my_location_marker
                        map_view.add_marker(my_location_marker)
                        self.marker_exists = True

                    processing_layout_in_anim = Animation(md_bg_color = [0, 0, 0, .8], duration=.1)
                    processing_layout_in_anim.start(self.ids.processing_layout)
                    self.ids.title_bar_address_lb.text = "Fill Address"
                    self.ids.processing_layout.add_widget(ButtonLayout())
                    self.ids.circlarprogress.progress_bar_color = C('#ffffff')
                    self.ids.circlarprogress.spin()

                    auto_fill_thread = Thread(target=self.fetch_address, args=(touch_geo_cordinates,))
                    auto_fill_thread.start()

                else:
                    self.touch_moved = False

    def fetch_address(self, touch_geo_cordinates):
        adderess = get_address(touch_geo_cordinates[0], touch_geo_cordinates[1])
        self.auto_fill_address(adderess)
        user.latitude = touch_geo_cordinates[0]
        user.longitude = touch_geo_cordinates[1]
        user.country = adderess["country"]
        user.state = adderess["state"]
        user.city = adderess["city"]
        user.pincode = adderess["pincode"]

    @mainthread
    def auto_fill_address(self, adderess):
        self.ids.house_input.text = adderess["housenumber"]
        self.ids.street_input.text = adderess["street"]
        self.ids.state_input.text = adderess["state"]
        self.ids.city_input.text = adderess["city"]
        self.ids.pincode_input.text = adderess["pincode"]
        self.touch_moved = False
        form_up_anim = Animation(y=0, duration=.1)
        form_up_anim.start(self.ids.address_layout)

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
        self.manager.current = "main"
        
class AddProductsScreen(MDScreen):
    def change_screen(self):
        self.manager.current = "main"

class OrderSummeryScreen(MDScreen):
    pass

sm = ScreenManager(transition=NoTransition())
user = User()

class Utkrishi(MDApp):
    previous_screen = "main"
    def build(self):
        self.geo_cordinates = (12.8168653, 80.0396097)
        Builder.load_file("Utkrishi.kv")
        self.loggedin = False
        self.language = "English"
        sm.add_widget(LanguageSelectionScreen(name = 'LanguageSelectionScreen'))
        sm.add_widget(MainScreen(name = 'main'))
        sm.add_widget(LoginScreen(name = 'login'))
        sm.add_widget(AddAddressScreen(name = 'AddAddressScreen'))
        sm.add_widget(OrderSummeryScreen(name = 'OrderSummeryScreen'))
        sm.add_widget(AddProductsScreen(name = 'addproducts'))
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
            set_bars_colors(C('#ffffff'), C('#ffffff'))

            request_permissions([
                Permission.CAMERA,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION,
                Permission.RECORD_AUDIO,
            ])
            
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start()
        else:
            lat = 12.816868178227127
            lon = 80.03963143159984
            get_city_thread = Thread(target=self.get_city_name, args=(lat, lon))
            get_city_thread.start()

            print("Location is not available for ", platform, " system.")
        
        return sm
    
    def get_city_name(self, lat, lon):
        city = get_address(lat, lon)["city"]
        self.set_city_name(city)
    
    @mainthread
    def set_city_name(self, city):
        sm.get_screen('main').ids.location_btn.text = city
    
    @mainthread
    def on_location(self, **kwargs):
        self.geo_cordinates = (kwargs['lat'], kwargs['lon'])
        city = get_address(kwargs['lat'], kwargs['lon'])["city"]
        sm.get_screen('main').ids.location_btn.text = city
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
        filechooser.open_file(on_selection=self.file_handle_selection, filters=[("Comma-separated Values", "*.png","*.jpeg","*.jpg",)])

    def file_handle_selection(self, selection):
        self.selection = selection[0]
        sm.get_screen('addproducts').ids.product_img.source = selection[0]

    def on_selection(self, *a, **k):
        
        sm.get_screen('addproducts').ids.product_img.source = str(self.selection)
        
    def addproducts(self, product_img, product_name, product_price, unit_type, category):
        print(product_name, product_price, product_img, app.item_type)
        if user.address != None:
            product_url= upload_file(product_img, f'{user.username}/products/{category}/{product_name}') 
            existing_data = db.get_data(f'products/{category}/{user.country}/{user.state}/{user.city}/{user.username}/{product_name}')
            in_stalk = 0
            if existing_data:
                if existing_data["in_stalk"] != '0':
                    in_stalk = int(existing_data["in_stalk"]) + 0
            product= {
                "id": product_name+"@"+user.uid,
                "Seller Name": user.username,
                "category": category,
                "url": product_url,
                "price": product_price,
                "unit_type": unit_type,
                "location": {
                    "latitude": user.latitude,
                    "longitude": user.longitude,
                    "country": user.country,
                    "state": user.state,
                    "city": user.city,
                    "pincode": user.pincode,
                },
                "in_stalk": str(in_stalk),
                }
            db.push(product, f'products/{product_name}')

        else:
            self.previous_screen = sm.current
            sm.current = "AddAddressScreen"
    
    def saveaddress(self, name, house, street, city, state, pincode):
        user.address = {
            "name": name,
            "email": user.email,
            "acctype": user.type,
            "address": {
                "house": house,
                "street": street,
                "city": city,
                "state": state,
                "pincode": pincode,
                "latitude": user.latitude,
                "longitude": user.longitude,
            }}
        db.store(user.address, f'{user.username}/address')

    def start_listening(self, search_bar):
        self.search_bar = search_bar
        self.search_bar.right_icon_color = "red"
        try:
            if stt.listening:
                self.stop_listening()
                return


            self.speech_rec_results = []

            stt.start()

            Clock.schedule_interval(self.check_state, 1 / 5)

        except Exception as e:
            print(e)

    def stop_listening(self):
        self.search_bar.right_icon_color = "black"

        stt.stop()
        self.update()

        Clock.unschedule(self.check_state)

    def check_state(self, dt):
        # if the recognizer service stops, change UI
        if not stt.listening:
            self.stop_listening()

    def update(self):
        self.speech_rec_results = stt.results[0]

app = Utkrishi()

if __name__=="__main__":
    app.run()
