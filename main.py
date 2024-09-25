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
from kivymd.uix.label import MDLabel, MDIcon
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
from kivy.uix.stencilview import StencilView
from mapview import MapMarker, MapView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.font_definitions import theme_font_styles
from threading import Thread
from functools import partial


from scripts.cordinate_to_address import get_address
from scripts.DistanceCalc import get_distance
from scripts.User import User
from scripts import local_db
from login import login, sign_up
import database as db
from Speechrecognizer import stt
from CloudStorage import upload_file

from kivy.core.window import Window
Window.size = (380, 600)

class LoadingDialogContent(MDFloatLayout):
    pass

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

class CardButton(ButtonBehavior, Card):
    pass

class BoxButtonLayout(ButtonBehavior, MDBoxLayout):
    pass

class ButtonLayout(ButtonBehavior, MDFloatLayout):
    pass

class NavButton(ButtonLayout):
    pass

class ProductCard(ButtonLayout, StencilView):
    product_name = StringProperty()
    product_price = StringProperty()
    image = StringProperty()
    product_selling_unit = StringProperty()
    distance = StringProperty()
    duration = StringProperty()
    item_count = StringProperty()
    list_type = StringProperty()

    def trigger_quantity_changed(self, *args):
        # Dispatch the on_search event
        self.dispatch('on_quantity_changed', *args)

    def __init__(self, **kwargs):
        super(ProductCard, self).__init__(**kwargs)
        self.register_event_type('on_quantity_changed')

    def on_item_count(self, *args):
        if self.item_count == "0":
            self.ids.item_count_layout.opacity = 0
            self.ids.item_count_layout.width = 0
            if self.list_type == "cart":
                self.ids.cart_btn.size_hint_x = 1
                self.ids.pickup_btn.size_hint_x = 1
                self.ids.pickup_btn.opacity = 1
        self.trigger_quantity_changed(self.item_count)

    def on_quantity_changed(self, *args):
        pass


    def add_to_cart(self, cart_btn, pickup_btn):
        self.list_type = "cart"
        self.ids.item_count_layout.opacity = 1
        self.ids.item_count_layout.width = dp(100)
        self.ids.item_count_lb.text = "1"
        cart_btn.size_hint_x = None
        cart_btn.width = self.width - dp(130)
        pickup_btn.size_hint_x = None
        pickup_btn.width = "0dp"
        pickup_btn.opacity = 0

class CartProductCard(ButtonLayout, StencilView):
    card_id = StringProperty()
    product_name = StringProperty()
    product_price = StringProperty()
    image = StringProperty()
    product_selling_unit = StringProperty()
    distance = StringProperty()
    duration = StringProperty()
    item_count = StringProperty("0")
    list_type = StringProperty()

    def on_item_count(self, *args):
        if self.item_count == "0":
            self.delete_card()

    def delete_card(self):
        if self.parent:
            self.parent.ids[self.card_id] = None
            self.parent.remove_widget(self)
            app.cart.pop(self.card_id)


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
    def on_enter(self):
        self.loading_dialog = MDDialog(
            type="custom",
            content_cls=LoadingDialogContent(),
            auto_dismiss=False,
            height = dp(55),
        )

        self.auto_login()


    def auto_login(self):
        login_data = local_db.get_auto_login_data()
        if login_data:
            Clock.schedule_once(lambda x: self.loading_dialog.open(), 1)
            app.user.email = login_data["email"]
            app.user.name = login_data["name"]
            app.user.phone = login_data["phone"]
            app.user.type = login_data["type"]
            app.user.uid = login_data["uid"]
            app.user.address = login_data.get("address")
            if app.user.address:
                address_data = login_data["address"]
                app.user.address = address_data['address_name']
                app.user.latitude = address_data['latitude']
                app.user.longitude = address_data['longitude']
                app.user.state = address_data['state']
                app.user.city = address_data['city']
                app.user.pincode = address_data['pincode']
            login_thread = Thread(target=self.login_thread, args=(login_data["email"], login_data["password"]))
            login_thread.start()

    def login_thread(self, email, password):
        loggeduser = login(email, password)
        if loggeduser:
            Clock.schedule_once(lambda x: self.loading_dialog.dismiss(), 1)
            self.change_screen()
        else:
            self.auto_login_change_screen("SignUpScreen")

    @mainthread
    def change_screen(self):
        self.manager.current = "main"

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self._initial_touch_y = None
        self._initial_layout_y = None

    def change_screen(self, screen="main"):
        self.manager.current = screen

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
        navbar = self.ids.navbar
        for i in self.ids.main_layout.children:
            if(i != layout):
                i.pos_hint= {'x': 1}
            else:
                if i == self.ids.shopping_layout:
                    self.navbar_up_anim = Animation(y=navbar.parent.height, duration=.1)
                    self.navbar_up_anim.start(navbar)

                if i == self.ids.shopping_layout:
                    self.search_bar_bg_down_anim = Animation(y=self.height-self.ids.search_bar_bg.height, duration=.1)
                    self.search_bar_bg_down_anim.start(self.ids.search_bar_bg)

                elif i == self.ids.home_layout:
                    self.search_bar_bg_down_anim = Animation(y=navbar.y-self.ids.search_bar_bg.height, duration=.1)
                    self.search_bar_bg_down_anim.start(self.ids.search_bar_bg)
        
                if i in [self.ids.cart_layout, self.ids.my_order_layout, self.ids.account_layout]:
                    self.navbar_down_anim = Animation(y=self.height-self.ids.navbar.height, duration=.1)
                    self.navbar_down_anim.start(navbar)

                if i == self.ids.cart_layout:
                    search_bar_up_anim = Animation(y=self.height, duration=.1)
                    search_bar_up_anim.start(self.ids.search_bar_bg)

                elif i == self.ids.my_order_layout:
                    search_bar_up_anim = Animation(y=self.height, duration=.1)
                    search_bar_up_anim.start(self.ids.search_bar_bg)
                
                elif i == self.ids.account_layout:
                    search_bar_up_anim = Animation(y=self.height, duration=.1)
                    search_bar_up_anim.start(self.ids.search_bar_bg)
            
    def search_focus(self, *args):
        navbar = self.ids.navbar
        if args[-1][-1]:
            navbar.opacity = 0
        else:
            navbar.opacity = 1
        print("search_focus")

    def on_enter(self, *args):
        self.loading_dialog = MDDialog(
            type="custom",
            content_cls=LoadingDialogContent(),
            auto_dismiss=False,
            height = dp(55),
        )
        if app.user.name:
            self.ids.user_name_lb.text = app.user.name.split(" ")[0]
        self.ids.user_address_lb.text = str(app.user.address)
        try:
            my_location_marker = MapMarker(lat=app.geo_cordinates[0], lon=app.geo_cordinates[1], source='assets/my_location.png', size_hint=[None,None], size=["50dp", "50dp"])
            self.ids.shopping_map.add_marker(my_location_marker)

            if app.user.uid == None and self.ids.get("login_card") == None:
                login_card = CardButton(
                    size_hint=[1, 1],
                    md_bg_color=[0, 0, 0, .7],
                    radius= "15dp",
                    pos_hint= {'center_x': .5, 'center_y': .5},
                )
                login_lb = MDLabel(
                    text= "Login",
                    halign = "center",
                    bold= True,
                    pos_hint={'center_x': .5, 'center_y': .5}
                )
                login_icon = MDIcon(
                    icon= "lock",
                    pos_hint={'center_x': .4, 'center_y': .5},
                )
                login_icon.color = C("#ffffff")
                login_lb.color = C("#ffffff")
                login_card.add_widget(login_icon)
                login_card.add_widget(login_lb)
                login_card.bind(on_press= lambda x: self.change_screen("login"))
                user_info_layout = self.ids.user_info_layout
                user_info_layout.add_widget(login_card)
                self.ids['login_card'] = login_card
                
            elif app.user.uid != None:
                if self.ids.get("login_card") != None:
                    self.ids.user_info_layout.remove_widget(self.ids.login_card)

            self.product_list_layout = self.ids.product_list_layout
            self.product_list_layout.y = 0-self.product_list_layout.height
            #self.add_products()
        except Exception as e:
            print("error: ", e)

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
        self.loading_dialog.open()
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
                    self.add_product_to_list(product["id"])
                    self.add_product_pin(mapview, prod_lat, prod_lon, product)
    
    @mainthread
    def add_product_pin(self, mapview, prod_lat, prod_lon, product):
        marker = MapMarker(lat = prod_lat, lon = prod_lon, source='assets/marker.png')
        mapview.ids[product["id"]] = marker
        func = partial(self.show_product_card, product["id"])
        marker.bind(on_press=func)
        mapview.add_marker(marker)

    def show_product_card(self, product_id, *args):
        widget = self.ids[product_id]
        product_list_scroll = self.ids.product_list_scroll
        product_list_boxlayout = self.ids.product_list_boxlayout
        self.product_list_layout.y = self.ids.search_bar_bg.y - self.product_list_layout.height
        scroll_pos = 1 - (widget.y / (product_list_boxlayout.height - product_list_scroll.height))
        print(scroll_pos)
        anim = Animation(scroll_y = scroll_pos, duration=.1)
        anim.start(product_list_scroll)

                    
    @mainthread
    def add_product_to_list(self, product_id, *args):
        self.product_list_layout = self.ids.product_list_layout
        self.product_list_boxlayout = self.ids.product_list_boxlayout
        product = self.product_details[product_id]
        product_card = ProductCard(
            image= product["url"],
            product_name= product["product name"],
            product_price= product["price"],
            product_selling_unit= f"[size={round(dp(10))}]{product["unit_type"]}[/size]",
            distance= product["distance"],
            duration= product["duration"],
            size_hint= [None, None],
            size= [self.parent.width - dp(40), "150dp"],
        )
        product_card.bind(on_release= lambda x: self.open_prod_menu(product_id, product_card))
        product_card.bind(on_quantity_changed= lambda *args: self.update_cart(product_id, *args))
        self.product_list_boxlayout.add_widget(product_card)
        self.ids[product_id] = product_card
        self.loading_dialog.dismiss()

    def open_prod_menu(self, product_id, product_card):
        product_card.height = "200dp"

    def update_cart(self, product_id, *args):
        product_dict = self.product_details[product_id]
        product_price = int(product_dict['price'])
        quantity = int(args[-1])
        price_for_quantity = product_price * quantity
        app.cart[product_id] = {
            "product_details": product_dict,
            "quantity": quantity,
            "price_for_quantity": price_for_quantity,
            }
        
        self.add_product_to_cart_layout(product_id)
        
    #cart layout functions

    def add_product_to_cart_layout(self, product_id):
        product_dict = app.cart[product_id]
        product_details_dict = product_dict["product_details"]
        self.cart_layout_product_list = self.ids.cart_list
        if self.cart_layout_product_list.ids.get(product_id) == None:
            cart_product_card = CartProductCard(
                card_id= product_id,
                image= product_details_dict["url"],
                product_name= product_details_dict["product name"],
                product_price= product_details_dict["price"],
                product_selling_unit= f"[size={round(dp(10))}]{product_details_dict["unit_type"]}[/size]",
                item_count = str(product_dict["quantity"]),
                size_hint= [None, None],
                distance= product_details_dict["distance"],
                duration= product_details_dict["duration"],
                size= [self.parent.width - dp(40), "200dp"],
            )
            self.cart_layout_product_list.add_widget(cart_product_card)
            self.cart_layout_product_list.ids[product_id] = cart_product_card

        else:
            self.update_product_details(product_id)

    def update_product_details(self, product_id, *args):
        product_dict = app.cart[product_id]
        procuct_card = self.cart_layout_product_list.ids.get(product_id)
        procuct_card.item_count = str(product_dict["quantity"])
        
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
        app.user.latitude = touch_geo_cordinates[0]
        app.user.longitude = touch_geo_cordinates[1]
        app.user.country = adderess["country"]
        app.user.state = adderess["state"]
        app.user.city = adderess["city"]
        app.user.pincode = adderess["pincode"]

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

    def on_enter(self):
        self.loading_dialog = MDDialog(
            type="custom",
            content_cls=LoadingDialogContent(),
            auto_dismiss=False,
            height = dp(55),
        )
    
    def change_screen(self):
        self.manager.current = "main"
    
    def login(self, email=None, password=None):
        app.user.email = email
        app.user.password = password
        loggeduser = login(email, password)

        if loggeduser:
            userdata = db.get_data(f'users/{loggeduser.uid}')
            app.user.name = userdata["name"]
            app.user.phone = userdata["phone"]
            app.user.type = userdata["type"]
            app.user.uid = loggeduser.uid
            local_login_data = {
                "email": email,
                "password": password,
                "name": userdata["name"],
                "phone": userdata["phone"],
                "type": userdata["type"],
                "uid": loggeduser.uid,
                "address": userdata.get("address")
            }
            local_db.store_login(local_login_data)
            if userdata.get("address"):
                address_data = userdata["address"]
                app.user.address = address_data['address_name']
                app.user.latitude = address_data['latitude']
                app.user.longitude = address_data['longitude']
                app.user.state = address_data['state']
                app.user.city = address_data['city']
                app.user.pincode = address_data['pincode']

        else:
            self.manager.current = "SignUpScreen"
        
class SignUpScreen(MDScreen):
    @mainthread
    def change_screen(self):
        self.manager.current = "main"

    def on_enter(self):
        self.loading_dialog = MDDialog(
            type="custom",
            content_cls=LoadingDialogContent(),
            auto_dismiss=False,
            height = dp(55),
        )
        if app.user.email:
            self.ids.email_input.text = app.user.email

        if app.user.password:
            self.ids.password_input.text = app.user.password 
    
    def signup(self, name, email, phone, password, acctype):
        
        signup_thread = Thread(target=self.signup_thread_func, args=(name, email, phone, password, acctype))
        signup_thread.start()

    def signup_thread_func(self, name, email, phone, password, acctype):
        signeduser = sign_up(email, password)
        app.user.username = email.split("@")[0]
        app.user.email = email
        app.user.uid = signeduser.uid
        app.user.phone = phone
        app.user.name = name
        app.user.type = acctype
        local_login_data = {
            "email": email,
            "password": password,
            "name": name,
            "phone": phone,
            "type": acctype,
            "uid": signeduser.uid,
        }
        fbdb_login_data = {
            "email": email,
            "name": name,
            "phone": phone,
            "type": acctype,
            "uid": signeduser.uid,
        }
        db.store(fbdb_login_data, f'users/{signeduser.uid}')
        local_db.store_login(local_login_data)

        self.change_screen()

class AddProductsScreen(MDScreen):
    def on_enter(self):
        self.loading_dialog = MDDialog(
            type="custom",
            content_cls=LoadingDialogContent(),
            auto_dismiss=False,
            height = dp(55),
        )
    def change_screen(self):
        self.manager.current = "main"

class OrderSummeryScreen(MDScreen):
    pass

sm = ScreenManager(transition=NoTransition())


class Utkrishi(MDApp):
    user = User()
    previous_screen = "main"
    cart = {}
    is_auto_loging = False
    def build(self):
        self.geo_cordinates = (12.8168653, 80.0396097)
        Builder.load_file("Utkrishi.kv")
        self.language = "English"
        sm.add_widget(LanguageSelectionScreen(name = 'LanguageSelectionScreen'))
        sm.add_widget(MainScreen(name = 'main'))
        sm.add_widget(LoginScreen(name = 'login'))
        sm.add_widget(SignUpScreen(name = 'SignUpScreen'))
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
                caller=sm.get_screen('SignUpScreen').ids.drop_item,
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
        
        lat_lon_to_city_thread = Thread(target=self.get_city, args=(kwargs))
        lat_lon_to_city_thread.start()
        
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        print("Location is available for ", self.gps_location)
        gps.stop()

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_resume(self, **kwargs):  
        gps.start()

    def get_city(self, **kwargs):
        city = get_address(kwargs['lat'], kwargs['lon'])["city"]
        self.show_city(city)

    @mainthread
    def show_city(self, city):
        sm.get_screen('main').ids.location_btn.text = city

    def auto_login(self):
        login_data = local_db.get_auto_login_data()
        if login_data:
            self.is_auto_loging = True
            self.user.email = login_data["email"]
            self.user.name = login_data["name"]
            self.user.phone = login_data["phone"]
            self.user.type = login_data["type"]
            self.user.uid = login_data["uid"]
            self.user.address = login_data.get("address")
            if self.user.address:
                address_data = login_data["address"]
                self.user.address = address_data['address_name']
                self.user.latitude = address_data['latitude']
                self.user.longitude = address_data['longitude']
                self.user.state = address_data['state']
                self.user.city = address_data['city']
                self.user.pincode = address_data['pincode']
            login_thread = Thread(target=self.login_thread, args=(login_data["email"], login_data["password"]))
            login_thread.start()
        else:
            sm.current = "LanguageSelectionScreen"

    def login_thread(self, email, password):
        loggeduser = login(email, password)
        if loggeduser:
            pass
        else:
            self.auto_login_change_screen("SignUpScreen")

    @mainthread
    def auto_login_change_screen(self, screen):
        sm.get_screen('LanguageSelectionScreen').show_loading_dialog()

    def set_login_item(self, text_item):
        sm.get_screen('SignUpScreen').ids.drop_item.set_item(text_item)
        self.user.type = text_item
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
        if self.user.address != None:
            product_url= upload_file(product_img, f'{self.user.username}/products/{category}/{product_name}') 
            existing_data = db.get_data(f'products/{category}/{self.user.country}/{self.user.state}/{self.user.city}/{self.user.username}/{product_name}')
            in_stalk = 0
            if existing_data:
                if existing_data["in_stalk"] != '0':
                    in_stalk = int(existing_data["in_stalk"]) + 0
            product= {
                "id": product_name+"@"+self.user.uid,
                "Seller Name": self.user.username,
                "category": category,
                "url": product_url,
                "price": product_price,
                "unit_type": unit_type,
                "location": {
                    "latitude": self.user.latitude,
                    "longitude": self.user.longitude,
                    "country": self.user.country,
                    "state": self.user.state,
                    "city": self.user.city,
                    "pincode": self.user.pincode,
                },
                "in_stalk": str(in_stalk),
                }
            db.push(product, f'products/{product_name}')

        else:
            self.previous_screen = sm.current
            sm.current = "AddAddressScreen"
    
    def saveaddress(self, name, house, street, city, state, pincode):
        self.user.address = f"{house}, {street}, {city}, {state}, {pincode}"
        address_json = {
                "house": house,
                "street": street,
                "city": city,
                "state": state,
                "pincode": pincode,
                "latitude": self.user.latitude,
                "longitude": self.user.longitude,
                "address_name": self.user.address
            }
        local_dp_data = {
            "address": address_json
        }
        local_db.store(self.user.uid, local_dp_data)
        db.store(address_json, f'users/{self.user.uid}/address')

    def start_listening(self, search_bar):
        self.search_bar = search_bar
        self.search_bar.text = "Listening..."
        self.search_bar.right_icon_color = [1,0,0,1]
        self.search_bar.left_icon_color= [.1,.1,.1,1]
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
        self.search_bar.text = self.speech_rec_results

app = Utkrishi()

if __name__=="__main__":
    app.run()
