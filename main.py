# -*- coding: utf-8 -*-
import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
import json
import os
import random
import time
import datetime

if platform not in ('android', 'ios'):
    Window.size = (450, 800)

# ============================================================
#  ДАННЫЕ
# ============================================================
RARITY = {
    'trash':      {'name': 'Хлам',         'color': (0.62, 0.62, 0.62, 1), 'tier': 0, 'base': 60,    'shard': 0},
    'common':     {'name': 'Обычный',      'color': (0.85, 0.85, 0.85, 1), 'tier': 1, 'base': 30,    'shard': 0},
    'uncommon':   {'name': 'Необычный',    'color': (0.30, 0.69, 0.31, 1), 'tier': 2, 'base': 8,     'shard': 0},
    'rare':       {'name': 'Редкий',       'color': (0.13, 0.59, 0.95, 1), 'tier': 3, 'base': 1.5,   'shard': 0},
    'epic':       {'name': 'Эпический',    'color': (0.61, 0.15, 0.69, 1), 'tier': 4, 'base': 0.4,   'shard': 1},
    'legendary':  {'name': 'Легендарный',  'color': (1.00, 0.60, 0.00, 1), 'tier': 5, 'base': 0.08,  'shard': 1},
    'mythic':     {'name': 'Мифический',   'color': (0.96, 0.26, 0.21, 1), 'tier': 6, 'base': 0.015, 'shard': 2},
    'divine':     {'name': 'Божественный', 'color': (1.00, 0.84, 0.00, 1), 'tier': 7, 'base': 0.004, 'shard': 0},
    'primordial': {'name': 'Первородный',  'color': (1.00, 0.20, 0.80, 1), 'tier': 8, 'base': 0.001, 'shard': 0},
}

TIERS_ORDER = ['trash', 'common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic', 'divine', 'primordial']

CHESTS = {
    'free':       {'name': 'Бесплатный',   'color': (0.00, 0.80, 0.80, 1), 'min': 1,  'max': 2,  'quality': 0.8, 'cost': 0,   'cur': 'coins',    'req': 0},
    'common':     {'name': 'Обычный',      'color': (0.62, 0.62, 0.62, 1), 'min': 3,  'max': 6,  'quality': 1.0, 'cost': 50,  'cur': 'coins',    'req': 0},
    'uncommon':   {'name': 'Необычный',    'color': (0.30, 0.69, 0.31, 1), 'min': 6,  'max': 10, 'quality': 1.3, 'cost': 200, 'cur': 'coins',    'req': 5},
    'rare':       {'name': 'Редкий',       'color': (0.13, 0.59, 0.95, 1), 'min': 10, 'max': 15, 'quality': 1.6, 'cost': 600, 'cur': 'coins',    'req': 15},
    'epic':       {'name': 'Эпический',    'color': (0.61, 0.15, 0.69, 1), 'min': 15, 'max': 25, 'quality': 2.0, 'cost': 2000,'cur': 'coins',    'req': 40},
    'legendary':  {'name': 'Легендарный',  'color': (1.00, 0.60, 0.00, 1), 'min': 25, 'max': 35, 'quality': 2.5, 'cost': 2,   'cur': 'crystals', 'req': 80},
    'mythic':     {'name': 'Мифический',   'color': (0.96, 0.26, 0.21, 1), 'min': 35, 'max': 50, 'quality': 3.5, 'cost': 5,   'cur': 'crystals', 'req': 150},
    'divine':     {'name': 'Божественный', 'color': (1.00, 0.84, 0.00, 1), 'min': 50, 'max': 70, 'quality': 5.0, 'cost': 20,  'cur': 'crystals', 'req': 300},
    'primordial': {'name': 'Первородный',  'color': (1.00, 0.20, 0.80, 1), 'min': 70, 'max': 100,'quality': 7.0, 'cost': 100, 'cur': 'crystals', 'req': 500},
}

ITEMS_DATA = [
    ('rusty_nail', 'Ржавый гвоздь', 'trash', 2, 0), ('broken_spoon', 'Сломанная ложка', 'trash', 2, 0),
    ('holey_sock', 'Дырявый носок', 'trash', 1, 0), ('road_pebble', 'Камешек с дороги', 'trash', 1, 0),
    ('empty_bottle', 'Пустая бутылка', 'trash', 3, 0), ('apple_core', 'Огрызок яблока', 'trash', 1, 0),
    ('bent_coin', 'Согнутая монета', 'trash', 2, 0), ('rope_piece', 'Кусок верёвки', 'trash', 2, 0),
    ('cracked_pot', 'Треснувший горшок', 'trash', 3, 0), ('old_newspaper', 'Старая газета', 'trash', 1, 0),
    ('rusted_key', 'Ржавый ключ', 'trash', 2, 0), ('pickaxe_fragment', 'Обломок кирки', 'trash', 3, 0),
    ('crow_feather', 'Пёрышко вороны', 'trash', 1, 0), ('fish_bone', 'Рыбья косточка', 'trash', 1, 0),
    ('stale_bread', 'Засохшая краюха', 'trash', 2, 0), ('jar_lid', 'Крышка от банки', 'trash', 1, 0),
    ('glass_shard', 'Стеклянный осколок', 'trash', 2, 0), ('worn_belt', 'Изношенный ремень', 'trash', 3, 0),
    ('burnt_candle', 'Прогоревшая свеча', 'trash', 2, 0), ('dust_bag', 'Мешочек с пылью', 'trash', 1, 0),
    ('crumpled_draft', 'Скомканный черновик', 'trash', 1, 0), ('shirt_button', 'Пуговица от рубахи', 'trash', 1, 0),
    ('rusty_horseshoe', 'Ржавая подкова', 'trash', 3, 0), ('hairy_soap', 'Мыло с волосками', 'trash', 1, 0),
    ('deflated_ball', 'Сдутый мяч', 'trash', 2, 0),
    ('wooden_spoon', 'Деревянная ложка', 'common', 5, 0), ('copper_key', 'Медный ключ', 'common', 8, 0),
    ('leather_belt', 'Кожаный ремень', 'common', 7, 0), ('candle', 'Свеча', 'common', 6, 0),
    ('coal_piece', 'Кусок угля', 'common', 5, 0), ('iron_nail', 'Железный гвоздь', 'common', 6, 0),
    ('rope', 'Верёвка', 'common', 8, 0), ('clay_mug', 'Глиняная кружка', 'common', 7, 0),
    ('fabric_scrap', 'Лоскут ткани', 'common', 5, 0), ('flint', 'Огниво', 'common', 9, 0),
    ('luck_coin', 'Монета удачи', 'common', 10, 0), ('fish_hook', 'Рыболовный крючок', 'common', 7, 0),
    ('small_knife', 'Маленький нож', 'common', 9, 0), ('salt_bag', 'Мешочек соли', 'common', 6, 0),
    ('compass', 'Компас', 'common', 10, 0), ('lantern', 'Фонарь', 'common', 9, 0),
    ('pocket_knife', 'Перочинный ножик', 'common', 8, 0), ('cheese_piece', 'Кусок сыра', 'common', 5, 0),
    ('water_flask', 'Походная фляга', 'common', 8, 0), ('bandage', 'Бинт', 'common', 6, 0),
    ('pencil', 'Карандаш', 'common', 5, 0), ('thread_spool', 'Моток ниток', 'common', 6, 0),
    ('steel_knife', 'Стальной нож', 'uncommon', 30, 0), ('silver_key', 'Серебряный ключ', 'uncommon', 40, 0),
    ('luck_ring', 'Кольцо удачи', 'uncommon', 45, 0), ('evil_eye_amulet', 'Амулет от сглаза', 'uncommon', 40, 0),
    ('fire_flint', 'Огненный кремень', 'uncommon', 35, 0), ('pathfinder_compass', 'Компас следопыта', 'uncommon', 50, 0),
    ('small_heal_potion', 'Зелье малого лечения', 'uncommon', 30, 0), ('gem_bag', 'Мешочек с самоцветами', 'uncommon', 45, 0),
    ('spark_scroll', 'Свиток искры', 'uncommon', 40, 0), ('iron_shield', 'Железный щит', 'uncommon', 45, 0),
    ('leather_boots', 'Кожаные сапоги', 'uncommon', 35, 0), ('hunter_bow', 'Лук охотника', 'uncommon', 50, 0),
    ('silver_coin', 'Серебряная монета', 'uncommon', 30, 0), ('eternal_lantern', 'Фонарь вечного огня', 'uncommon', 45, 0),
    ('dungeon_map', 'Карта подземелья', 'uncommon', 40, 0), ('strength_potion', 'Зелье силы', 'uncommon', 35, 0),
    ('wanderer_cloak', 'Плащ странника', 'uncommon', 45, 0), ('poison_dagger', 'Кинжал отравителя', 'uncommon', 50, 0),
    ('gold_key', 'Золотой ключ', 'rare', 150, 0), ('guard_sword', 'Меч стражи', 'rare', 180, 0),
    ('protection_ring', 'Кольцо защиты', 'rare', 160, 0), ('fire_wand', 'Жезл огня', 'rare', 170, 0),
    ('big_heal_potion', 'Зелье большого лечения', 'rare', 120, 0), ('teleport_scroll', 'Свиток телепорта', 'rare', 200, 0),
    ('mana_crystal', 'Кристалл маны', 'rare', 190, 0), ('knight_shield', 'Щит рыцаря', 'rare', 170, 0),
    ('wisdom_amulet', 'Амулет мудрости', 'rare', 160, 0), ('shadow_cloak', 'Плащ теней', 'rare', 180, 0),
    ('crossbow', 'Арбалет', 'rare', 175, 0), ('speed_boots', 'Сапоги скорости', 'rare', 155, 0),
    ('strength_glove', 'Перчатка силы', 'rare', 165, 0),
    ('flame_sword', 'Меч пламени', 'epic', 800, 1), ('storm_staff', 'Посох бури', 'epic', 900, 1),
    ('overlord_ring', 'Кольцо повелителя', 'epic', 850, 1), ('dragon_scale_armor', 'Доспех драконьей чешуи', 'epic', 1000, 1),
    ('weak_immortality', 'Амулет бессмертия', 'epic', 950, 1), ('soul_crystal', 'Кристалл душ', 'epic', 700, 1),
    ('void_cloak', 'Плащ пустоты', 'epic', 850, 1), ('moonlight_bow', 'Лук лунного света', 'epic', 800, 1),
    ('darkness_dagger', 'Кинжал тьмы', 'epic', 900, 1),
    ('dawn_blade', 'Клинок рассвета', 'legendary', 3000, 5), ('world_tree_staff', 'Посох мирового древа', 'legendary', 3000, 5),
    ('kings_crown', 'Корона королей', 'legendary', 3200, 5), ('abyss_ring', 'Перстень бездны', 'legendary', 2800, 5),
    ('titan_armor', 'Доспех титана', 'legendary', 3100, 5), ('star_hunter_bow', 'Лук звёздного охотника', 'legendary', 3000, 5),
    ('end_times_sword', 'Меч конца времён', 'mythic', 10000, 20), ('dragon_heart', 'Сердце дракона', 'mythic', 11000, 20),
    ('seer_eye', 'Око провидца', 'mythic', 10500, 20), ('gods_cloak', 'Плащ богов', 'mythic', 12000, 20),
    ('creator_hammer', 'Молот Творца', 'divine', 0, 100), ('goddess_tear', 'Слеза богини', 'divine', 0, 100),
    ('first_light_shard', 'Осколок Первого Света', 'primordial', 0, 0),
]

ITEMS = {row[0]: {'name': row[1], 'rarity': row[2], 'sellCoins': row[3], 'sellCrystals': row[4]} for row in ITEMS_DATA}

# ============================================================
#  ЛОГИКА
# ============================================================
class SaveData:
    def __init__(self):
        self.version = 5
        self.coins = 0
        self.crystals = 0
        self.inventory = {}
        self.stats = {'chests': 0, 'sold': 0, 'coins_earned': 0}
        self.discovered = []
        self.pity = 0
        self.last_free_chest = 0
        self.upgrades = {
            'greed': 0, 'luck': 0, 'autosell': False, 
            'discount': 0, 'timer_master': 0, 'pity_master': 0
        }
        self.last_quest_date = ""
        self.quests = []

    def to_dict(self):
        return {'version': self.version, 'coins': self.coins, 'crystals': self.crystals, 
                'inventory': self.inventory, 'stats': self.stats, 'discovered': self.discovered, 
                'pity': self.pity, 'last_free_chest': self.last_free_chest, 'upgrades': self.upgrades,
                'last_quest_date': self.last_quest_date, 'quests': self.quests}

    @classmethod
    def from_dict(cls, d):
        if d.get('version', 1) < 5: return cls()
        s = cls()
        s.coins = d.get('coins', 0)
        s.crystals = d.get('crystals', 0)
        s.inventory = d.get('inventory', {})
        s.stats = d.get('stats', {'chests': 0, 'sold': 0, 'coins_earned': 0})
        if 'coins_earned' not in s.stats: s.stats['coins_earned'] = 0
        s.discovered = d.get('discovered', [])
        s.pity = d.get('pity', 0)
        s.last_free_chest = d.get('last_free_chest', 0)
        s.upgrades = d.get('upgrades', {})
        for k, v in cls().upgrades.items():
            if k not in s.upgrades: s.upgrades[k] = v
        s.last_quest_date = d.get('last_quest_date', "")
        s.quests = d.get('quests', [])
        return s

class Game:
    def __init__(self, save):
        self.save = save
        self.check_daily_quests()

    def check_daily_quests(self):
        today = datetime.date.today().isoformat()
        if self.save.last_quest_date != today:
            self.save.last_quest_date = today
            self.generate_quests()

    def generate_quests(self):
        self.save.quests = []
        q_types = [
            {'type': 'open_chests', 'target': random.choice([10, 15, 20]), 'name': 'Открой сундуки'},
            {'type': 'sell_items',  'target': random.choice([30, 50, 80]), 'name': 'Продай предметы'},
            {'type': 'earn_coins',  'target': random.choice([500, 1000, 2000]), 'name': 'Заработай монет'}
        ]
        random.shuffle(q_types)
        
        for i in range(3):
            qt = q_types[i]
            self.save.quests.append({
                'id': i, 'type': qt['type'], 'name': qt['name'], 'target': qt['target'],
                'current': 0, 'reward_c': qt['target'] * 5, 
                'reward_cr': 1 if i == 0 else (2 if i == 1 else 3), 'claimed': False
            })

    def add_progress(self, q_type, amount):
        for q in self.save.quests:
            if q['type'] == q_type and not q['claimed'] and q['current'] < q['target']:
                q['current'] = min(q['target'], q['current'] + amount)

    def claim_quest(self, index):
        q = self.save.quests[index]
        if q['current'] >= q['target'] and not q['claimed']:
            q['claimed'] = True
            self.save.coins += q['reward_c']
            self.save.crystals += q['reward_cr']
            return True
        return False

    def get_pity_threshold(self):
        lvl = self.save.upgrades.get('pity_master', 0)
        return max(10, 40 - (lvl * 5))

    def get_chest_cost(self, chest_id):
        base_cost = CHESTS[chest_id]['cost']
        if base_cost == 0: return 0
        lvl = self.save.upgrades.get('discount', 0)
        return int(base_cost * (1 - (lvl * 0.1)))

    def roll_chest_items(self, chest_id, is_free=False):
        cfg = CHESTS[chest_id]
        n = random.randint(cfg['min'], cfg['max'])
        result = []
        force_epic = False
        if self.save.pity >= self.get_pity_threshold():
            force_epic = True
            self.save.pity = 0
            
        for _ in range(n):
            r = self._roll_item_rarity(cfg['quality'], force_epic)
            if RARITY[r]['tier'] >= 4: self.save.pity = 0
            pool = [k for k, v in ITEMS.items() if v['rarity'] == r]
            if pool: result.append(random.choice(pool))
                
        if not force_epic: self.save.pity += 1
        if chest_id != 'free' and not is_free: 
            self.save.stats['chests'] += 1
            self.add_progress('open_chests', 1)
        return result

    def _roll_item_rarity(self, quality, force_epic=False):
        if force_epic: return 'epic'
        weights = {}
        luck = 1.0 + (self.save.upgrades.get('luck', 0) * 0.1)
        for r, cfg in RARITY.items():
            w = cfg['base'] * (1 + (quality - 1) * cfg['tier'] * 0.1)
            if cfg['tier'] >= 3: w *= luck
            weights[r] = w
        total = sum(weights.values())
        roll = random.uniform(0, total)
        acc = 0
        for r, w in weights.items():
            acc += w
            if roll <= acc: return r
        return 'trash'

    def buy_chest(self, chest_id):
        cfg = CHESTS[chest_id]
        if self.save.stats['chests'] < cfg['req']: return False
        cost = self.get_chest_cost(chest_id)
        if cfg['cur'] == 'coins' and self.save.coins < cost: return False
        if cfg['cur'] == 'crystals' and self.save.crystals < cost: return False
        if cfg['cur'] == 'coins': self.save.coins -= cost
        else: self.save.crystals -= cost
        return True

    def add_item(self, item_id):
        item = ITEMS[item_id]
        if self.save.upgrades.get('autosell', False) and item['rarity'] in ('trash', 'common'):
            mult = 1.0 + (self.save.upgrades.get('greed', 0) * 0.1)
            earned = int(item['sellCoins'] * mult)
            self.save.coins += earned
            self.save.stats['coins_earned'] += earned
            self.add_progress('earn_coins', earned)
            return False
            
        self.save.inventory[item_id] = self.save.inventory.get(item_id, 0) + 1
        if item_id not in self.save.discovered: self.save.discovered.append(item_id)
        return True

    def sell_item(self, item_id, count=1):
        if item_id not in self.save.inventory: return
        item = ITEMS[item_id]
        if item['rarity'] == 'primordial': return
        count = min(count, self.save.inventory[item_id])
        mult = 1.0 + (self.save.upgrades.get('greed', 0) * 0.1)
        earned_c = int(item['sellCoins'] * count * mult)
        earned_cr = item['sellCrystals'] * count
        self.save.coins += earned_c
        self.save.crystals += earned_cr
        self.save.inventory[item_id] -= count
        if self.save.inventory[item_id] <= 0: del self.save.inventory[item_id]
        self.save.stats['sold'] += count
        self.save.stats['coins_earned'] += earned_c
        self.add_progress('sell_items', count)
        self.add_progress('earn_coins', earned_c)

    def craft_item(self, item_id):
        if item_id not in self.save.inventory or self.save.inventory[item_id] < 5: return False
        item = ITEMS[item_id]
        current_tier_idx = TIERS_ORDER.index(item['rarity'])
        if current_tier_idx >= len(TIERS_ORDER) - 1: return False
        self.save.inventory[item_id] -= 5
        if self.save.inventory[item_id] <= 0: del self.save.inventory[item_id]
        next_tier = TIERS_ORDER[current_tier_idx + 1]
        pool = [k for k, v in ITEMS.items() if v['rarity'] == next_tier]
        if pool:
            new_item_id = random.choice(pool)
            self.add_item(new_item_id)
            return new_item_id
        return False

    def get_upgrade_cost(self, upg_id):
        lvl = self.save.upgrades.get(upg_id, 0)
        if upg_id == 'greed': return (lvl + 1) * 1000, 'coins'
        elif upg_id == 'luck': return (lvl + 1) * 5, 'crystals'
        elif upg_id == 'autosell': return 20, 'crystals'
        elif upg_id == 'discount': return (lvl + 1) * 10, 'crystals'
        elif upg_id == 'timer_master': return (lvl + 1) * 8, 'crystals'
        elif upg_id == 'pity_master': return (lvl + 1) * 15, 'crystals'
        return 0, 'coins'

    def buy_upgrade(self, upg_id):
        cost, cur = self.get_upgrade_cost(upg_id)
        if upg_id == 'autosell' and self.save.upgrades.get('autosell'): return False
        if upg_id == 'discount' and self.save.upgrades.get('discount', 0) >= 5: return False
        if cur == 'coins' and self.save.coins >= cost: self.save.coins -= cost
        elif cur == 'crystals' and self.save.crystals >= cost: self.save.crystals -= cost
        else: return False
        if upg_id == 'autosell': self.save.upgrades['autosell'] = True
        else: self.save.upgrades[upg_id] += 1
        return True

    def get_free_chest_status(self):
        lvl = self.save.upgrades.get('timer_master', 0)
        cooldown = max(600, (4 * 3600) - (lvl * 900))
        elapsed = time.time() - self.save.last_free_chest
        if elapsed >= cooldown: return True, 0
        return False, int(cooldown - elapsed)

# ============================================================
#  ВИДЖЕТЫ
# ============================================================
class ChestWidget(Widget):
    def __init__(self, chest_id, on_open, **kwargs):
        super().__init__(**kwargs)
        self.chest_id = chest_id
        self.on_open = on_open
        self.size_hint = (None, None)
        self.size = (dp(250), dp(250))
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        color = CHESTS[chest_id]['color']
        with self.canvas.before:
            Color(*color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(28)])
        self.bind(pos=self._update, size=self._update)
        self.opacity = 0
        Animation(opacity=1, duration=0.35).start(self)

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._shake_and_open()
            return True
        return super().on_touch_down(touch)

    def _shake_and_open(self):
        Animation.cancel_all(self)
        anim = (Animation(opacity=0.3, duration=0.08) + Animation(opacity=1, duration=0.08) +
                Animation(opacity=0.3, duration=0.08) + Animation(opacity=1, duration=0.08) +
                Animation(opacity=0, duration=0.25))
        anim.bind(on_complete=lambda *a: self.on_open())
        anim.start(self)

class CardWidget(Button):
    def __init__(self, item_id, **kwargs):
        super().__init__(**kwargs)
        self.item_id = item_id
        item = ITEMS[item_id]
        rar = RARITY[item['rarity']]
        self.background_normal = ''
        self.background_color = rar['color']
        self.color = (0, 0, 0, 1) if rar['tier'] < 7 else (1, 1, 1, 1)
        self.text = f"{item['name']}\n[{rar['name']}]"
        self.font_size = dp(11)
        self.size_hint_y = None
        self.height = dp(85)
        self.text_size = (self.width - dp(5), self.height - dp(5))
        self.halign = 'center'
        self.valign = 'middle'
        self.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0] - dp(5), val[1] - dp(5))))
        self.opacity = 0
        Animation(opacity=1, duration=0.15).start(self)

# НОВЫЙ КЛАСС ДЛЯ КАРТОЧКИ КВЕСТА (исправляет "плывущий" фон)
class QuestCard(BoxLayout):
    def __init__(self, quest, index, game, refresh_callback, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=dp(130), 
                         padding=dp(10), spacing=dp(5), **kwargs)
        
        with self.canvas.before:
            Color(0.18, 0.18, 0.22, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        title_text = f"{quest['name']} ({quest['current']}/{quest['target']})"
        self.add_widget(Label(text=title_text, font_size=dp(16), bold=True, color=(1, 1, 1, 1),
                              size_hint_y=None, height=dp(30)))
        
        reward_text = f"Награда: {quest['reward_c']} Монет | {quest['reward_cr']} Кристаллов"
        self.add_widget(Label(text=reward_text, font_size=dp(14), color=(1, 0.8, 0.2, 1),
                              size_hint_y=None, height=dp(25)))
        
        btn = Button(text="", size_hint_y=None, height=dp(45), font_size=dp(16), bold=True)
        if quest['claimed']:
            btn.text = "ПОЛУЧЕНО"
            btn.disabled = True
            btn.background_color = (0.3, 0.3, 0.3, 1)
        elif quest['current'] >= quest['target']:
            btn.text = "ЗАБРАТЬ НАГРАДУ"
            btn.background_color = (0.2, 0.6, 0.2, 1)
            btn.bind(on_release=lambda *_: self._claim(index, game, refresh_callback))
        else:
            btn.text = "В ПРОЦЕССЕ"
            btn.disabled = True
            btn.background_color = (0.4, 0.4, 0.4, 1)
        
        self.add_widget(btn)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _claim(self, index, game, refresh_callback):
        if game.claim_quest(index):
            refresh_callback()

# ============================================================
#  ЭКРАНЫ
# ============================================================
class MainScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.active_chest = None
        self._pending_items = []
        self._reveal_index = 0
        self._reveal_event = None
        self._clear_event = None
        self._build()
        self.bind(on_pre_enter=self._on_pre_enter)

    def _build(self):
        root = BoxLayout(orientation='vertical')

        top_float = FloatLayout(size_hint_y=None, height=dp(60))
        money_box = BoxLayout(size_hint=(None, None), size=(dp(180), dp(40)),
                              pos_hint={'x': 0.02, 'center_y': 0.5}, padding=(dp(10), 0))
        with money_box.canvas.before:
            Color(0.2, 0.2, 0.25, 1)
            self.m_bg = RoundedRectangle(pos=money_box.pos, size=money_box.size, radius=[dp(10)])
        money_box.bind(pos=lambda i, v: setattr(self.m_bg, 'pos', v),
                       size=lambda i, v: setattr(self.m_bg, 'size', v))
        self.money_lbl = Label(text="Монеты: 0 | Крист: 0", font_size=dp(14), bold=True, color=(1, 0.9, 0.3, 1))
        money_box.add_widget(self.money_lbl)
        
        info_btn = Button(text='Шансы', font_size=dp(14), bold=True,
                          size_hint=(None, None), size=(dp(70), dp(40)),
                          pos_hint={'right': 0.98, 'center_y': 0.5},
                          background_color=(0.3, 0.3, 0.3, 1))
        info_btn.bind(on_release=lambda *_: self._show_probabilities())
        
        top_float.add_widget(money_box)
        top_float.add_widget(info_btn)
        root.add_widget(top_float)

        free_chest_box = BoxLayout(size_hint_y=None, height=dp(50), padding=(dp(15), dp(5)))
        self.free_btn = Button(text="[ БЕСПЛАТНЫЙ СУНДУК ]", font_size=dp(15), bold=True, background_color=(0.8, 0.2, 0.8, 1))
        self.free_btn.bind(on_release=lambda *_: self._claim_free())
        free_chest_box.add_widget(self.free_btn)
        root.add_widget(free_chest_box)

        self.chest_area = FloatLayout()
        self.hint = Label(text='Сундук не куплен.\nЗайдите в Магазин.',
                          halign='center', valign='middle', font_size=dp(20),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5}, opacity=0.7)
        self.hint.bind(size=self.hint.setter('text_size'))
        self.chest_area.add_widget(self.hint)
        root.add_widget(self.chest_area)

        scroll = ScrollView(size_hint_y=0.4)
        self.cards_grid = GridLayout(cols=3, size_hint_y=None, spacing=dp(5), padding=dp(5))
        self.cards_grid.bind(minimum_height=self.cards_grid.setter('height'))
        scroll.add_widget(self.cards_grid)
        root.add_widget(scroll)

        bottom_bar = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5), padding=dp(5))
        
        shop_btn = Button(text='Магазин', font_size=dp(12), bold=True, background_color=(0.20, 0.45, 0.85, 1))
        shop_btn.bind(on_release=lambda *_: self._open_shop())
        bottom_bar.add_widget(shop_btn)

        lab_btn = Button(text='Лаборатория', font_size=dp(12), bold=True, background_color=(0.6, 0.4, 0.0, 1))
        lab_btn.bind(on_release=lambda *_: setattr(self.manager, 'current', 'lab'))
        bottom_bar.add_widget(lab_btn)

        quest_btn = Button(text='Задания', font_size=dp(12), bold=True, background_color=(0.2, 0.6, 0.2, 1))
        quest_btn.bind(on_release=lambda *_: setattr(self.manager, 'current', 'quests'))
        bottom_bar.add_widget(quest_btn)

        inv_btn = Button(text='Коллекция', font_size=dp(12), bold=True, background_color=(0.4, 0.4, 0.4, 1))
        inv_btn.bind(on_release=lambda *_: setattr(self.manager, 'current', 'inventory'))
        bottom_bar.add_widget(inv_btn)

        root.add_widget(bottom_bar)
        self.add_widget(root)
        
        Clock.schedule_interval(self._update_free_btn, 1)

    def _show_probabilities(self):
        popup = Popup(title='Вероятности и Гарант', size_hint=(0.9, 0.8), title_size=dp(18))
        scroll = ScrollView()
        box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10), size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        max_pity = self.game.get_pity_threshold()
        pity_text = f"ГАРАНТ (Эпик+)\nПрогресс: {self.game.save.pity} / {max_pity}\n"
        if self.game.save.pity >= max_pity - 1: pity_text += "Следующий сундук даст Эпик!"
        else: pity_text += "Открывайте сундуки, чтобы заполнить шкалу."
            
        pity_lbl = Label(text=pity_text, font_size=dp(16), bold=True, color=(1, 0.8, 0.2, 1), 
                         size_hint_y=None, height=dp(80), halign='center', valign='middle')
        pity_lbl.bind(size=pity_lbl.setter('text_size'))
        box.add_widget(pity_lbl)

        luck = 1.0 + (self.game.save.upgrades.get('luck', 0) * 0.1)
        box.add_widget(Label(text=f"Базовые шансы (с учетом Удачи x{luck:.1f}):", font_size=dp(16), bold=True))

        total_base = sum(cfg['base'] for cfg in RARITY.values())
        for r_id in reversed(TIERS_ORDER):
            cfg = RARITY[r_id]
            w = cfg['base']
            if cfg['tier'] >= 3: w *= luck
            percent = (w / (total_base + w - cfg['base'])) * 100
            p_text = "<0.01%" if percent < 0.01 else f"{percent:.2f}%"
            text = f"{cfg['name']}: {p_text}"
            box.add_widget(Label(text=text, font_size=dp(14), color=cfg['color'], bold=True, size_hint_y=None, height=dp(30)))

        scroll.add_widget(box)
        popup.content = scroll
        popup.open()

    def _update_free_btn(self, dt):
        if self.manager.current != 'main': return
        avail, time_left = self.game.get_free_chest_status()
        if avail:
            self.free_btn.text = "[ БЕСПЛАТНЫЙ СУНДУК ]"
            self.free_btn.background_color = (0.8, 0.2, 0.8, 1)
            self.free_btn.disabled = False
        else:
            h = time_left // 3600
            m = (time_left % 3600) // 60
            s = time_left % 60
            self.free_btn.text = f"Ждите: {h:02d}:{m:02d}:{s:02d}"
            self.free_btn.background_color = (0.3, 0.3, 0.3, 1)
            self.free_btn.disabled = True

    def _claim_free(self):
        if not self.game.get_free_chest_status()[0]: return
        self.game.save.last_free_chest = time.time()
        self.active_chest = 'rare'
        self.cards_grid.clear_widgets()
        if self._clear_event: self._clear_event.cancel()
        self._open_chest('rare', is_free=True)
        self._refresh()
        self._update_free_btn(0)

    def _on_pre_enter(self, *args):
        self.game.check_daily_quests()
        self._refresh()
        self._update_free_btn(0)

    def _refresh(self):
        self.money_lbl.text = f"Монеты: {self.game.save.coins} | Крист: {self.game.save.crystals}"

    def _open_shop(self):
        popup = Popup(title='Магазин сундуков', size_hint=(0.95, 0.8), title_size=dp(18))
        scroll = ScrollView()
        grid = GridLayout(cols=2, size_hint_y=None, spacing=dp(5), padding=dp(5))
        grid.bind(minimum_height=grid.setter('height'))
        
        total_chests = self.game.save.stats['chests']
        for cid, cfg in CHESTS.items():
            is_unlocked = total_chests >= cfg['req']
            cost = self.game.get_chest_cost(cid)
            price = "Бесплатно" if cost == 0 else (f"{cost} Мон." if cfg['cur'] == 'coins' else f"{cost} Крист.")
            
            if is_unlocked:
                text = f"{cfg['name']}\n({cfg['min']}-{cfg['max']} шт.)\n{price}"
                bg_color = cfg['color']
            else:
                text = f"{cfg['name']}\n(Откр. {cfg['req']})\nЗакрыто"
                bg_color = (0.25, 0.25, 0.25, 1)

            btn = Button(text=text, font_size=dp(12), bold=True, size_hint_y=None, height=dp(90),
                         background_color=bg_color, color=(1, 1, 1, 1) if not is_unlocked else (0, 0, 0, 1))
            if is_unlocked: btn.bind(on_release=lambda x, c=cid: self._buy(c, popup))
            else: btn.disabled = True
            grid.add_widget(btn)

        scroll.add_widget(grid)
        popup.content = scroll
        popup.open()

    def _buy(self, chest_id, popup):
        if not self.game.buy_chest(chest_id):
            self._toast('Недостаточно средств!', (1, 0.3, 0.3, 1))
            return
        popup.dismiss()
        self.active_chest = chest_id
        self.cards_grid.clear_widgets()
        if self._clear_event: self._clear_event.cancel()
        self._show_chest(chest_id)
        self._refresh()

    def _show_chest(self, chest_id):
        self.chest_area.clear_widgets()
        chest = ChestWidget(chest_id, on_open=lambda: self._open_chest(chest_id))
        self.chest_area.add_widget(chest)

    def _open_chest(self, chest_id, is_free=False):
        self.chest_area.clear_widgets()
        self.active_chest = None 
        raw_items = self.game.roll_chest_items(chest_id, is_free)
        self._pending_items = [iid for iid in raw_items if self.game.add_item(iid)]

        self._reveal_index = 0
        self._reveal_event = None
        self._reveal_next()
        self._refresh()

    def _reveal_next(self, *args):
        if self._reveal_index < len(self._pending_items):
            iid = self._pending_items[self._reveal_index]
            self._reveal_index += 1
            self.cards_grid.add_widget(CardWidget(iid))
            self._reveal_event = Clock.schedule_once(self._reveal_next, 0.2)
        else:
            self._reveal_event = None
            if not self._pending_items: self._toast("Всё ушло в авто-продажу!", (0.5, 1, 0.5, 1))
            self._clear_event = Clock.schedule_once(self._clear_cards, 5.0)

    def _clear_cards(self, dt):
        self.cards_grid.clear_widgets()

    def on_touch_down(self, touch):
        if self._reveal_event:
            self._reveal_event.cancel()
            while self._reveal_index < len(self._pending_items):
                iid = self._pending_items[self._reveal_index]
                self._reveal_index += 1
                self.cards_grid.add_widget(CardWidget(iid))
            self._reveal_event = None
            if not self._pending_items: self._toast("Всё ушло в авто-продажу!", (0.5, 1, 0.5, 1))
            if self._clear_event: self._clear_event.cancel()
            self._clear_event = Clock.schedule_once(self._clear_cards, 5.0)
            return True
        return super().on_touch_down(touch)

    def _toast(self, msg, color=(1, 1, 0.6, 1)):
        lbl = Label(text=msg, pos_hint={'center_x': 0.5, 'center_y': 0.8}, size_hint=(1, None), height=dp(70), font_size=dp(22), bold=True, color=color)
        self.add_widget(lbl)
        Animation(opacity=0, duration=1.4).start(lbl)
        Clock.schedule_once(lambda dt: self.remove_widget(lbl), 1.5)

class QuestScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self._build()
        self.bind(on_pre_enter=self._on_pre_enter)

    def _build(self):
        root = BoxLayout(orientation='vertical')
        top_bar = BoxLayout(size_hint_y=None, height=dp(60), padding=(dp(15), dp(10)))
        with top_bar.canvas.before:
            Color(0.15, 0.15, 0.2, 1)
            self.top_rect = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(pos=lambda i, v: setattr(self.top_rect, 'pos', v), size=lambda i, v: setattr(self.top_rect, 'size', v))
        self.money_lbl = Label(text="Монеты: 0 | Кристаллы: 0", font_size=dp(18), bold=True, color=(1, 1, 0.5, 1))
        top_bar.add_widget(self.money_lbl)
        root.add_widget(top_bar)

        scroll = ScrollView()
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(10), padding=dp(10))
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        root.add_widget(scroll)

        bottom_bar = BoxLayout(size_hint_y=None, height=dp(70), padding=dp(10))
        with bottom_bar.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            self.bot_rect = Rectangle(pos=bottom_bar.pos, size=bottom_bar.size)
        bottom_bar.bind(pos=lambda i, v: setattr(self.bot_rect, 'pos', v), size=lambda i, v: setattr(self.bot_rect, 'size', v))
        
        back = Button(text='Назад', font_size=dp(16), bold=True, background_color=(0.4, 0.4, 0.4, 1))
        back.bind(on_release=lambda *_: setattr(self.manager, 'current', 'main'))
        bottom_bar.add_widget(back)
        root.add_widget(bottom_bar)
        self.add_widget(root)

    def _on_pre_enter(self, *args):
        self.game.check_daily_quests()
        self._refresh()

    def _refresh(self):
        self.money_lbl.text = f"Монеты: {self.game.save.coins} | Кристаллы: {self.game.save.crystals}"
        self.grid.clear_widgets()
        for i, q in enumerate(self.game.save.quests):
            self.grid.add_widget(QuestCard(q, i, self.game, self._refresh))

class LabScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self._build()
        self.bind(on_pre_enter=self._on_pre_enter)

    def _build(self):
        root = BoxLayout(orientation='vertical')
        top_bar = BoxLayout(size_hint_y=None, height=dp(60), padding=(dp(15), dp(10)))
        with top_bar.canvas.before:
            Color(0.15, 0.15, 0.2, 1)
            self.top_rect = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(pos=lambda i, v: setattr(self.top_rect, 'pos', v), size=lambda i, v: setattr(self.top_rect, 'size', v))
        self.money_lbl = Label(text="Монеты: 0 | Кристаллы: 0", font_size=dp(18), bold=True, color=(1, 1, 0.5, 1))
        top_bar.add_widget(self.money_lbl)
        root.add_widget(top_bar)

        scroll = ScrollView()
        self.grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(10), padding=dp(10))
        self.grid.bind(minimum_height=self.grid.setter('height'))
        scroll.add_widget(self.grid)
        root.add_widget(scroll)

        bottom_bar = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5), padding=dp(5))
        reset_btn = Button(text='Сброс', font_size=dp(12), background_color=(0.6, 0.2, 0.2, 1))
        reset_btn.bind(on_release=lambda *_: self._confirm_reset())
        bottom_bar.add_widget(reset_btn)
        back = Button(text='Назад', font_size=dp(16), bold=True, background_color=(0.4, 0.4, 0.4, 1))
        back.bind(on_release=lambda *_: setattr(self.manager, 'current', 'main'))
        bottom_bar.add_widget(back)
        root.add_widget(bottom_bar)
        self.add_widget(root)

    def _on_pre_enter(self, *args):
        self._refresh()

    def _refresh(self):
        self.money_lbl.text = f"Монеты: {self.game.save.coins} | Кристаллы: {self.game.save.crystals}"
        self.grid.clear_widgets()

        lvl = self.game.save.upgrades.get('greed', 0)
        cost, _ = self.game.get_upgrade_cost('greed')
        self._add_upgrade_ui("Жадность", f"+{lvl*10}% к цене продажи", f"Улучшить: {cost} Монет", 'greed')

        lvl = self.game.save.upgrades.get('luck', 0)
        cost, _ = self.game.get_upgrade_cost('luck')
        self._add_upgrade_ui("Удача", f"+{lvl*10}% к шансу Редких+", f"Улучшить: {cost} Кристаллов", 'luck')

        is_bought = self.game.save.upgrades.get('autosell', False)
        if is_bought:
            self._add_upgrade_ui("Авто-продажа", "Хлам и Обычные продаются сами", "КУПЛЕНО", 'autosell', disabled=True)
        else:
            cost, _ = self.game.get_upgrade_cost('autosell')
            self._add_upgrade_ui("Авто-продажа", "Хлам и Обычные продаются сами", f"Купить: {cost} Кристаллов", 'autosell')

        lvl = self.game.save.upgrades.get('discount', 0)
        cost, _ = self.game.get_upgrade_cost('discount')
        is_max = lvl >= 5
        self._add_upgrade_ui("Скидка", f"-{lvl*10}% к цене сундуков", "МАКС. УРОВЕНЬ" if is_max else f"Улучшить: {cost} Кристаллов", 'discount', disabled=is_max)

        lvl = self.game.save.upgrades.get('timer_master', 0)
        cost, _ = self.game.get_upgrade_cost('timer_master')
        self._add_upgrade_ui("Мастер Таймера", f"-{lvl*15} мин к ожиданию", f"Улучшить: {cost} Кристаллов", 'timer_master')

        lvl = self.game.save.upgrades.get('pity_master', 0)
        cost, _ = self.game.get_upgrade_cost('pity_master')
        self._add_upgrade_ui("Повелитель Гаранта", f"Порог гаранта: {self.game.get_pity_threshold()} сун.", f"Улучшить: {cost} Кристаллов", 'pity_master')

    def _add_upgrade_ui(self, title, desc, btn_text, upg_id, disabled=False):
        box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), padding=dp(10), spacing=dp(5))
        with box.canvas.before:
            Color(0.2, 0.2, 0.25, 1)
            box.rect = Rectangle(pos=box.pos, size=box.size)
        box.bind(pos=lambda i, v: setattr(box.rect, 'pos', v), size=lambda i, v: setattr(box.rect, 'size', v))

        box.add_widget(Label(text=title, font_size=dp(18), bold=True, color=(1, 0.8, 0.2, 1)))
        box.add_widget(Label(text=desc, font_size=dp(14), color=(0.8, 0.8, 0.8, 1)))
        btn = Button(text=btn_text, font_size=dp(16), size_hint_y=None, height=dp(40),
                     background_color=(0.3, 0.6, 0.3, 1) if not disabled else (0.4, 0.4, 0.4, 1))
        if not disabled: btn.bind(on_release=lambda *_: self._do_buy(upg_id))
        else: btn.disabled = True
        box.add_widget(btn)
        self.grid.add_widget(box)

    def _do_buy(self, upg_id):
        if self.game.buy_upgrade(upg_id): self._refresh()
        else: self._toast("Недостаточно средств!")

    def _confirm_reset(self):
        popup = Popup(title='Сброс', size_hint=(0.85, 0.4))
        box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        box.add_widget(Label(text='Вы уверены? ВЕСЬ прогресс будет удален!', halign='center', font_size=dp(16)))
        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        yes = Button(text='Да, сбросить', background_color=(0.6, 0.2, 0.2, 1), font_size=dp(16))
        no = Button(text='Отмена', font_size=dp(16))
        def do_reset(dt):
            self.game.save = SaveData()
            for name in ['main', 'inventory', 'quests']:
                self.manager.get_screen(name).game = self.game
            self._refresh()
            popup.dismiss()
        yes.bind(on_release=do_reset)
        no.bind(on_release=lambda *_: popup.dismiss())
        btns.add_widget(yes)
        btns.add_widget(no)
        box.add_widget(btns)
        popup.content = box
        popup.open()

    def _toast(self, msg):
        lbl = Label(text=msg, pos_hint={'center_x': 0.5, 'center_y': 0.8}, size_hint=(1, None), height=dp(70), font_size=dp(20), bold=True, color=(1, 0.3, 0.3, 1))
        self.add_widget(lbl)
        Animation(opacity=0, duration=1.4).start(lbl)
        Clock.schedule_once(lambda dt: self.remove_widget(lbl), 1.5)

class InventoryScreen(Screen):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.view_mode = 'items'
        self._build()
        self.bind(on_pre_enter=self._on_pre_enter)

    def _build(self):
        root = BoxLayout(orientation='vertical')
        top_bar = BoxLayout(size_hint_y=None, height=dp(60), padding=(dp(15), dp(10)))
        with top_bar.canvas.before:
            Color(0.15, 0.15, 0.2, 1)
            self.top_rect = Rectangle(pos=top_bar.pos, size=top_bar.size)
        top_bar.bind(pos=lambda i, v: setattr(self.top_rect, 'pos', v), size=lambda i, v: setattr(self.top_rect, 'size', v))
        self.money_lbl = Label(text="Монеты: 0 | Кристаллы: 0", font_size=dp(18), bold=True, color=(1, 1, 0.5, 1))
        top_bar.add_widget(self.money_lbl)
        root.add_widget(top_bar)

        tabs = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5), padding=dp(5))
        self.tab_items = Button(text='Инвентарь', font_size=dp(15), bold=True, background_color=(0.2, 0.45, 0.85, 1))
        self.tab_items.bind(on_release=lambda *_: self._switch_view('items'))
        self.tab_album = Button(text='Альбом', font_size=dp(15), background_color=(0.3, 0.3, 0.3, 1))
        self.tab_album.bind(on_release=lambda *_: self._switch_view('album'))
        tabs.add_widget(self.tab_items)
        tabs.add_widget(self.tab_album)
        root.add_widget(tabs)

        scroll = ScrollView()
        self.items_grid = GridLayout(cols=3, size_hint_y=None, spacing=dp(5), padding=dp(5))
        self.items_grid.bind(minimum_height=self.items_grid.setter('height'))
        scroll.add_widget(self.items_grid)
        root.add_widget(scroll)

        bottom_bar = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5), padding=dp(5))
        back = Button(text='Назад', font_size=dp(14), bold=True, background_color=(0.4, 0.4, 0.4, 1))
        back.bind(on_release=lambda *_: setattr(self.manager, 'current', 'main'))
        bottom_bar.add_widget(back)
        sell_trash = Button(text='Хлам', font_size=dp(14), background_color=(0.5, 0.3, 0.3, 1))
        sell_trash.bind(on_release=lambda *_: self._sell_trash())
        bottom_bar.add_widget(sell_trash)
        sell_all = Button(text='ВСЁ', font_size=dp(14), background_color=(0.2, 0.6, 0.2, 1))
        sell_all.bind(on_release=lambda *_: self._sell_all_confirm())
        bottom_bar.add_widget(sell_all)
        root.add_widget(bottom_bar)
        self.add_widget(root)

    def _switch_view(self, mode):
        self.view_mode = mode
        if mode == 'items':
            self.tab_items.background_color = (0.2, 0.45, 0.85, 1)
            self.tab_album.background_color = (0.3, 0.3, 0.3, 1)
        else:
            self.tab_items.background_color = (0.3, 0.3, 0.3, 1)
            self.tab_album.background_color = (0.2, 0.45, 0.85, 1)
        self._refresh()

    def _on_pre_enter(self, *args):
        self._refresh()

    def _refresh(self):
        self.money_lbl.text = f"Монеты: {self.game.save.coins} | Кристаллы: {self.game.save.crystals}"
        self.items_grid.clear_widgets()

        if self.view_mode == 'items':
            if not self.game.save.inventory:
                self.items_grid.add_widget(Label(text="Инвентарь пуст", font_size=dp(20), opacity=0.5))
                return
            entries = sorted(self.game.save.inventory.items(), key=lambda kv: (-RARITY[ITEMS[kv[0]]['rarity']]['tier'], -kv[1]))
            for iid, cnt in entries:
                item = ITEMS[iid]
                rar = RARITY[item['rarity']]
                btn = Button(text=f"{item['name']}\nКол-во: {cnt}", size_hint_y=None, height=dp(90),
                             font_size=dp(11), background_color=rar['color'], color=(0, 0, 0, 1) if rar['tier'] < 7 else (1, 1, 1, 1))
                btn.text_size = (dp(100), btn.height - dp(10))
                btn.halign = 'center'
                btn.valign = 'middle'
                btn.bind(on_release=lambda x, i=iid: self._sell_dialog(i))
                self.items_grid.add_widget(btn)
        
        elif self.view_mode == 'album':
            for item_id, item in ITEMS.items():
                rar = RARITY[item['rarity']]
                is_found = item_id in self.game.save.discovered
                if is_found:
                    text = f"{item['name']}\n[{rar['name']}]"
                    bg = rar['color']
                    fg = (0, 0, 0, 1) if rar['tier'] < 7 else (1, 1, 1, 1)
                else:
                    text = "???\n[Не найден]"
                    bg = (0.15, 0.15, 0.15, 1)
                    fg = (0.4, 0.4, 0.4, 1)
                btn = Button(text=text, size_hint_y=None, height=dp(80), font_size=dp(10), background_color=bg, color=fg, disabled=True)
                btn.text_size = (dp(100), btn.height - dp(10))
                btn.halign = 'center'
                btn.valign = 'middle'
                self.items_grid.add_widget(btn)

    def _sell_dialog(self, item_id):
        item = ITEMS[item_id]
        cnt = self.game.save.inventory[item_id]
        rar = RARITY[item['rarity']]
        popup = Popup(title=item['name'], size_hint=(0.9, 0.7))
        box = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        greed = self.game.save.upgrades.get('greed', 0) * 0.1
        final_coins = int(item['sellCoins'] * (1 + greed))
        
        if item['rarity'] == 'primordial':
            info_text = f"{rar['name']}\n\nЭтот предмет уникален.\nОн не может быть продан или обменян."
        else:
            info_text = f"{rar['name']}\nВ наличии: {cnt}\n\nЦена за 1 шт:\n{final_coins} Монет\n{item['sellCrystals']} Кристаллов"
            
        info_lbl = Label(text=info_text, font_size=dp(16), halign='center', valign='middle')
        info_lbl.bind(size=info_lbl.setter('text_size'))
        box.add_widget(info_lbl)

        if cnt >= 5 and item['rarity'] != 'primordial':
            next_tier_name = RARITY[TIERS_ORDER[TIERS_ORDER.index(item['rarity']) + 1]]['name']
            craft_btn = Button(text=f"Скрафтить 5 шт. -> 1 {next_tier_name}", size_hint_y=None, height=dp(50), background_color=(0.6, 0.4, 0.0, 1), font_size=dp(14))
            craft_btn.bind(on_release=lambda *_: (self._do_craft(item_id), popup.dismiss()))
            box.add_widget(craft_btn)

        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        if item['rarity'] == 'primordial':
            close = Button(text='Закрыть', font_size=dp(14))
            close.bind(on_release=lambda *_: popup.dismiss())
            btns.add_widget(close)
        else:
            b1 = Button(text='Продать 1', font_size=dp(14))
            b1.bind(on_release=lambda *_: (self.game.sell_item(item_id, 1), self._refresh(), popup.dismiss()))
            ball = Button(text='Продать ВСЁ', font_size=dp(14), background_color=(0.2, 0.6, 0.2, 1))
            ball.bind(on_release=lambda *_: (self.game.sell_item(item_id, cnt), self._refresh(), popup.dismiss()))
            bc = Button(text='Отмена', font_size=dp(14))
            bc.bind(on_release=lambda *_: popup.dismiss())
            btns.add_widget(b1)
            btns.add_widget(ball)
            btns.add_widget(bc)
        box.add_widget(btns)
        popup.content = box
        popup.open()

    def _do_craft(self, item_id):
        new_item = self.game.craft_item(item_id)
        self._refresh()
        if new_item:
            popup = Popup(title='Успех!', size_hint=(0.8, 0.3))
            rar = RARITY[ITEMS[new_item]['rarity']]
            popup.content = Label(text=f"Вы получили:\n{ITEMS[new_item]['name']}\n[{rar['name']}]", font_size=dp(18), halign='center')
            popup.open()
            Clock.schedule_once(lambda dt: popup.dismiss(), 2.0)

    def _sell_trash(self):
        targets = [i for i in list(self.game.save.inventory) if ITEMS[i]['rarity'] in ('trash', 'common')]
        for i in targets: self.game.sell_item(i, self.game.save.inventory[i])
        self._refresh()

    def _sell_all_confirm(self):
        if not self.game.save.inventory: return
        popup = Popup(title='Внимание', size_hint=(0.85, 0.4))
        box = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        box.add_widget(Label(text='Вы уверены, что хотите продать ВЕСЬ инвентарь?', halign='center', font_size=dp(16)))
        btns = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        yes = Button(text='Да', background_color=(0.2, 0.6, 0.2, 1), font_size=dp(16))
        no = Button(text='Нет', background_color=(0.6, 0.2, 0.2, 1), font_size=dp(16))
        yes.bind(on_release=lambda *_: (self._do_sell_all(), popup.dismiss()))
        no.bind(on_release=lambda *_: popup.dismiss())
        btns.add_widget(yes)
        btns.add_widget(no)
        box.add_widget(btns)
        popup.content = box
        popup.open()

    def _do_sell_all(self):
        targets = [i for i in list(self.game.save.inventory) if ITEMS[i]['rarity'] != 'primordial']
        for i in targets: self.game.sell_item(i, self.game.save.inventory[i])
        self._refresh()

# ============================================================
#  ПРИЛОЖЕНИЕ
# ============================================================
class ChestGameApp(App):
    def build(self):
        self.title = 'Сундучок'
        self.game = Game(self._load())
        sm = ScreenManager()
        sm.add_widget(MainScreen(self.game, name='main'))
        sm.add_widget(LabScreen(self.game, name='lab'))
        sm.add_widget(QuestScreen(self.game, name='quests'))
        sm.add_widget(InventoryScreen(self.game, name='inventory'))
        return sm

    def _path(self):
        return os.path.join(self.user_data_dir, 'save.json')

    def _load(self):
        try:
            p = self._path()
            if os.path.exists(p):
                with open(p, 'r', encoding='utf-8') as f:
                    return SaveData.from_dict(json.load(f))
        except Exception: pass
        return SaveData()

    def save_game(self):
        try:
            os.makedirs(self.user_data_dir, exist_ok=True)
            with open(self._path(), 'w', encoding='utf-8') as f:
                json.dump(self.game.save.to_dict(), f, ensure_ascii=False)
        except Exception: pass

    def on_pause(self):
        self.save_game()
        return True

    def on_stop(self):
        self.save_game()

if __name__ == '__main__':
    ChestGameApp().run()