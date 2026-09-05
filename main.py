import os
os.environ["KIVY_AUDIO"] = "sdl2"
os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, FallOutTransition, RiseInTransition, SwapTransition
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random
from kivy.lang import Builder
Builder.load_file('clicker.kv')

class MenuScreen(Screen):
    bg_image = StringProperty("assets/image/bg.jpg")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.images = ["assets/image/bg.jpg", "assets/image/town.jpg", "assets/image/city.jpg"]
        self.current_image_index = 0

    def on_enter(self):
        Clock.schedule_interval(self.change_background, 3.0)

    def on_leave(self):
        Clock.unschedule(self.change_background)

    def change_background(self, dt):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.bg_image = self.images[self.current_image_index]

    def go_game(self):
        self.manager.transition = RiseInTransition(duration=0.5)
        self.manager.current = 'game'

    def go_settings(self):
        self.manager.transition = SwapTransition(duration=0.5)
        self.manager.current = 'settings'

    def exit_app(self):
        App.get_running_app().stop()

class TargetButton(ButtonBehavior, Widget):
    hp = NumericProperty(6)
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_death')

    def on_press(self):
        if self.parent and self.parent.parent.is_animating:
            return
        if self.hp > 0:
            self.hp -= 1
            if self.hp == 0:
                self.dispatch('on_death')

    def on_death(self):
        pass

class GameScreen(Screen):
    points = NumericProperty(0)
    click_power = NumericProperty(1)
    passive_income = NumericProperty(0)
    current_level = NumericProperty(1)
    game_bg = StringProperty("assets/image/pizzeria.jpg")
    target_img = StringProperty("assets/image/pizza.png")
    is_animating = BooleanProperty(False)

    def on_enter(self):
        self.is_animating = False
        Clock.schedule_once(lambda dt: self.spawn_new_pizza(), 0)
        Clock.schedule_interval(self.generate_passive_income, 1.0)

    def on_leave(self):
        Clock.unschedule(self.generate_passive_income)

    def on_pizza_click(self):
        if not self.is_animating and self.ids.target_button.hp > 0:
            self.points += self.click_power
            App.get_running_app().play_click_sound_eat()

    def generate_passive_income(self, dt):
        if self.passive_income > 0:
            self.points += self.passive_income

    def spawn_new_pizza(self):
        self.is_animating = True
        pizza = self.ids.target_button
        pizza.hp = 6
        pizza.opacity = 1  
        pizza.angle = 0
        
        Animation.cancel_all(pizza)
        
        if self.current_level == 1:
            pizza.pos_hint = {"center_x": -0.3, "center_y": 0.4}
            anim = Animation(pos_hint={"center_x": 0.5, "center_y": 0.4}, angle=-360, duration=0.8, t='out_quad')
            anim.bind(on_complete=self.finish_spawn_animation)
            anim.start(pizza)
        else:
            pizza.pos_hint = {"center_x": 0.5, "center_y": 1.5}
            anim_fall = Animation(pos_hint={"center_x": 0.5, "center_y": 0.4}, duration=0.4, t='in_quad')
            anim_bounce1 = Animation(pos_hint={"center_x": 0.5, "center_y": 0.46}, duration=0.15, t='out_quad')
            anim_fall1 = Animation(pos_hint={"center_x": 0.5, "center_y": 0.4}, duration=0.12, t='in_quad')
            anim_bounce2 = Animation(pos_hint={"center_x": 0.5, "center_y": 0.42}, duration=0.08, t='out_quad')
            anim_fall2 = Animation(pos_hint={"center_x": 0.5, "center_y": 0.4}, duration=0.07, t='in_quad')
            
            full_anim = anim_fall + anim_bounce1 + anim_fall1 + anim_bounce2 + anim_fall2
            full_anim.bind(on_complete=self.finish_spawn_animation)
            full_anim.start(pizza)

    def finish_spawn_animation(self, *args):
        self.is_animating = False

    def level_complete(self):
        self.is_animating = True
        pizza = self.ids.target_button
        Animation.cancel_all(pizza)
        
        if self.current_level == 1:
            anim_out = Animation(pos_hint={"center_x": 1.3, "center_y": 0.4}, angle=-720, duration=0.8, t='in_quad')
            anim_out.bind(on_complete=lambda *args: self.spawn_new_pizza())
            anim_out.start(pizza)
        else:
            anim_out = Animation(pos_hint={"center_x": 0.5, "center_y": -0.5}, duration=0.5, t='in_quad')
            anim_out.bind(on_complete=lambda *args: self.spawn_new_pizza())
            anim_out.start(pizza)

    def go_menu(self):
        self.manager.transition = FallOutTransition(duration=0.5)
        self.manager.current = 'menu'

    def go_shop(self):
        self.manager.transition = WipeTransition(duration=0.5)
        self.manager.current = 'shop'

class SettingsScreen(Screen):
    playlist = ListProperty([
        {"name": "Fu", "path": "assets/sounds/f.mp3"},
        {"name": "Id", "path": "assets/sounds/i.mp3"},
        {"name": "TuNe", "path": "assets/sounds/tnep.mp3"},
        {"name": "Vu", "path": "assets/sounds/v.mp3"},
        {"name": "Td", "path": "assets/sounds/td.mp3"}
    ])
    
    current_track_index = NumericProperty(0) 
    current_track_name = StringProperty("None")
    music_volume = NumericProperty(50)
    sounds_volume = NumericProperty(50)  

    def update_music_state(self):
        app = App.get_running_app()
        
        if self.current_track_index == 0:
            self.current_track_name = "None"
            if app.bg_music:
                app.bg_music.stop()
        else:
            track_data = self.playlist[self.current_track_index - 1]
            self.current_track_name = track_data["name"]
            
            if app.bg_music:
                app.bg_music.stop()
                
            app.bg_music = SoundLoader.load(track_data["path"])
            if app.bg_music:
                app.bg_music.loop = True
                app.bg_music.volume = self.music_volume / 100.0
                app.bg_music.play()

    def change_volume(self, value):
        self.music_volume = int(value)
        app = App.get_running_app()
        if app.bg_music:
            app.bg_music.volume = self.music_volume / 100.0

    def change_sounds_volume(self, value):
        self.sounds_volume = int(value)
        app = App.get_running_app()
        if app.click_sound_eat:
            app.click_sound_eat.volume = self.sounds_volume / 100.0
        if app.shop_sound_coin:
            app.shop_sound_coin.volume = self.sounds_volume / 100.0

    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % 6
        self.update_music_state()

    def prev_track(self):
        self.current_track_index = (self.current_track_index - 1) % 6
        self.update_music_state()

    def go_menu(self):
        self.manager.transition = SwapTransition(duration=0.5)
        self.manager.current = 'menu'   

class ShopScreen(Screen):
    price_item_1 = NumericProperty(15)
    price_item_2 = NumericProperty(150)
    price_level = NumericProperty(100000)
    level_text = StringProperty("Level 2")
    player_coins = NumericProperty(0)

    def on_enter(self):
        game_screen = self.manager.get_screen('game')
        self.player_coins = game_screen.points

    def buy_item_1(self):
        game_screen = self.manager.get_screen('game')
        if game_screen.points >= self.price_item_1:
            game_screen.points -= self.price_item_1
            self.player_coins = game_screen.points
            
            if game_screen.current_level == 1:
                self.price_item_1 *= 3
            else:
                self.price_item_1 *= 4
                
            game_screen.click_power *= 2
            App.get_running_app().play_shop_sound_coin()

    def buy_item_2(self):
        game_screen = self.manager.get_screen('game')
        if game_screen.points >= self.price_item_2:
            game_screen.points -= self.price_item_2
            self.player_coins = game_screen.points
            
            if game_screen.current_level == 1:
                self.price_item_2 *= 2
            else:
                self.price_item_2 *= 3
                
            if game_screen.passive_income == 0:
                game_screen.passive_income = 1
            else:
                game_screen.passive_income *= 2
            App.get_running_app().play_shop_sound_coin()

    def buy_level(self):
        if self.level_text == "The End":
            self.show_end_game_overlay()
            return

        game_screen = self.manager.get_screen('game')
        if game_screen.points >= self.price_level:
            game_screen.points = 0
            game_screen.click_power = 1
            game_screen.passive_income = 0
            game_screen.current_level = 2
            game_screen.game_bg = "assets/image/sushibar.jpg"
            game_screen.target_img = "assets/image/sushi.png"
            
            app = App.get_running_app()
            app.game_font = "assets/fonts/YanoneKaffeesatz-Regular.ttf"
            
            self.price_item_1 = 15
            self.price_item_2 = 150
            self.player_coins = 0
            
            self.level_text = "The End"
            self.price_level = 1000000
            App.get_running_app().play_shop_sound_coin()

    def show_end_game_overlay(self):
        self.ids.end_overlay.size_hint = (1, 1)
        self.ids.end_overlay.opacity = 1
        self.ids.end_overlay.disabled = False
        Clock.schedule_interval(self.spawn_falling_object, 0.1)

    def spawn_falling_object(self, dt):
        img_type = random.choice(["assets/image/pizza.png", "assets/image/sushi.png"])
        falling_img = Image(
            source=img_type,
            size_hint=(None, None),
            size=("180dp", "180dp"),
            pos_hint={"center_x": random.uniform(0.0, 1.0), "center_y": 1.2}
        )
        self.ids.end_overlay.add_widget(falling_img, index=0)
        
        anim = Animation(pos_hint={"center_y": -0.2}, duration=random.uniform(2.0, 3.5))
        anim.bind(on_complete=lambda a, w: self.ids.end_overlay.remove_widget(w))
        anim.start(falling_img)

    def exit_app(self):
        App.get_running_app().stop()

    def go_game(self):
        self.manager.current = 'game'       

class ClickerApp(App):
    game_font = StringProperty("assets/fonts/SpicyPizza.ttf")

    def build(self):
        self.bg_music = None
        self.click_sound_eat = None 
        self.shop_sound_coin = None

        sm = ScreenManager(transition=WipeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ShopScreen(name='shop'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm
    
    def on_start(self):
        settings = self.root.get_screen('settings')
        
        self.click_sound_eat = SoundLoader.load('assets/sounds/eat.wav')
        if self.click_sound_eat:
            self.click_sound_eat.volume = settings.sounds_volume / 100.0
            
        self.shop_sound_coin = SoundLoader.load('assets/sounds/coinse.wav')
        if self.shop_sound_coin:
            self.shop_sound_coin.volume = settings.sounds_volume / 100.0
    
    def play_click_sound_eat(self):
        if self.click_sound_eat:
            self.click_sound_eat.stop() 
            self.click_sound_eat.play()

    def play_shop_sound_coin(self):
        if self.shop_sound_coin:
            self.shop_sound_coin.stop()
            self.shop_sound_coin.play()

if __name__ == '__main__':
    ClickerApp().run()
