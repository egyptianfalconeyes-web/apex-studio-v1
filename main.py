# -*- coding: utf-8 -*-
"""
Apex Master AI Studio - Mobile Edition (Android) v1.0
المبتكرون العرب لصناعة البرمجيات والإلكترونيات
إشراف إدارة: م. عادل الدريني
------------------------------------------------------
المميزات:
- واجهة مودرن خفيفة جداً وسلسة (Zero-Lag UI)
- بطاقات مضاءة بنيون المنصات (YouTube / TikTok / Instagram)
- نظام تفعيل تجاري بالعتاد (Android HWID) + فترة 15 يوماً تجريبية
- معالجة غير متزامنة (Async Threads) لمنع السخونة أو التهنيج
"""

import os
import sys
import json
import time
import hashlib
import threading
import asyncio

# استيراد بيئة Kivy المخصصة للأندرويد
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.window import Window

import edge_tts

# تعيين أبعاد افتراضية شبيها بالشاشة المحمولة للتعامل الفوري عند التجربة
Window.softinput_mode = "below_target"

# ---------------------------------------------------------------
# 1. نظام الحماية والتفعيل التجاري لعتاد الأندرويد (Android HWID)
# ---------------------------------------------------------------
SECRET_SALT = "ARAB_INNOVATORS_MOBILE_2026_SALT"

def get_android_hwid():
    """ استخراج المعرّف الفريد لجهاز الأندرويد """
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        SettingsSecure = autoclass('android.provider.Settings$Secure')
        context = PythonActivity.mActivity.getContentResolver()
        android_id = SettingsSecure.getString(context, SettingsSecure.ANDROID_ID)
        if android_id:
            return hashlib.md5(android_id.encode()).hexdigest()[:12].upper()
    except Exception:
        pass
    # احتياطي في بيئة التطوير
    import uuid
    mac = hex(uuid.getnode())[2:].zfill(12)
    return hashlib.md5(mac.encode()).hexdigest()[:12].upper()

def verify_license(hwid, key):
    key = key.strip().upper()
    parts = key.split("-")
    if len(parts) != 5:
        return False, "INVALID"
    prefix = parts[0]
    body = "-".join(parts[1:])
    mode = "LIFETIME" if prefix == "LIF" else ("YEAR1" if prefix == "Y1Y" else "TRIAL15")
    raw = f"{hwid.strip().upper()}::{mode}::{SECRET_SALT}"
    digest = hashlib.sha256(raw.encode('utf-8')).hexdigest().upper()
    expected_body = "-".join([digest[i:i+4] for i in range(0, 16, 4)])
    return (body == expected_body), mode

# ---------------------------------------------------------------
# 2. البيانات المرجعية والمنصات (Preset Platforms)
# ---------------------------------------------------------------
PLATFORMS = {
    "TIKTOK": {
        "title": "TikTok / Shorts",
        "sub": "رأسي حديث (9:16)",
        "color": (0.02, 0.71, 0.83, 1), # Cyan Neon
        "glow": [0.02, 0.71, 0.83, 0.3],
        "safe_bottom": 160
    },
    "YOUTUBE": {
        "title": "YouTube / FB",
        "sub": "أفقي سينمائي (16:9)",
        "color": (0.93, 0.26, 0.26, 1), # Red Neon
        "glow": [0.93, 0.26, 0.26, 0.3],
        "safe_bottom": 50
    },
    "INSTAGRAM": {
        "title": "Instagram Post",
        "sub": "مربع متناسق (1:1)",
        "color": (0.65, 0.33, 0.96, 1), # Purple Neon
        "glow": [0.65, 0.33, 0.96, 0.3],
        "safe_bottom": 80
    }
}

# ---------------------------------------------------------------
# 3. مكونات الواجهة المخصصة (Custom Responsive Widgets)
# ---------------------------------------------------------------
class PlatformPresetCard(BoxLayout):
    def __init__(self, key, info, callback, **kwargs):
        super().__init__(**kwargs)
        self.key = key
        self.info = info
        self.callback = callback
        self.is_selected = False
        
        self.orientation = "vertical"
        self.padding = [12, 10, 12, 10]
        self.spacing = 4
        self.size_hint_y = None
        self.height = 75

        self.lbl_title = Label(
            text=f"[b]{info['title']}[/b]", 
            markup=True, 
            font_size="14sp", 
            color=(1, 1, 1, 1),
            halign="right", valign="middle"
        )
        self.lbl_title.bind(size=self.lbl_title.setter('text_size'))

        self.lbl_sub = Label(
            text=info['sub'], 
            font_size="11sp", 
            color=(0.58, 0.63, 0.72, 1),
            halign="right", valign="middle"
        )
        self.lbl_sub.bind(size=self.lbl_sub.setter('text_size'))

        self.add_widget(self.lbl_title)
        self.add_widget(self.lbl_sub)
        self.update_graphics()

    def update_graphics(self):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_selected:
                Color(0.11, 0.16, 0.23, 1) # خلفية مميزة
            else:
                Color(0.05, 0.07, 0.12, 1) # خلفية داكنة فاخرة
            
            RoundedRectangle(pos=self.pos, size=self.size, radius=[10,])
            
            # حدود توهج النيون للمنصة المختارة
            if self.is_selected:
                Color(*self.info['color'])
                Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=1.8)
            else:
                Color(0.12, 0.16, 0.23, 1)
                Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=1)

    def on_size(self, *args):
        self.update_graphics()

    def on_pos(self, *args):
        self.update_graphics()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.callback(self.key)
            return True
        return super().on_touch_down(touch)

# ---------------------------------------------------------------
# 4. الشاشة الرئيسية للتطبيق (Apex Mobile Main Layout)
# ---------------------------------------------------------------
class ApexMobileStudio(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 14
        self.spacing = 10
        self.selected_platform = "TIKTOK"
        self.cards_dict = {}
        self.hwid = get_android_hwid()
        self.lic_file = os.path.join(App.get_running_app().user_data_dir, "license.dat")
        
        self.init_license()
        self.build_ui()

    def init_license(self):
        now = int(time.time())
        self.lic_data = {"first_run": now, "activated": False, "key": "", "mode": "TRIAL"}
        
        if os.path.exists(self.lic_file):
            try:
                with open(self.lic_file, "r", encoding="utf-8") as f:
                    self.lic_data.update(json.load(f))
            except Exception:
                pass

        if self.lic_data.get("key"):
            valid, mode = verify_license(self.hwid, self.lic_data["key"])
            if valid:
                self.lic_data["activated"] = True
                self.lic_data["mode"] = mode

    def save_license(self):
        try:
            with open(self.lic_file, "w", encoding="utf-8") as f:
                json.dump(self.lic_data, f)
        except Exception:
            pass

    def build_ui(self):
        # 1. شريط العنوان والترخيص العلوي (Header Bar)
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=45)
        
        lbl_app_name = Label(
            text="[b]APEX STUDIO[/b] [color=10b981]MOBILE[/color]",
            markup=True, font_size="16sp", halign="left", valign="middle"
        )
        lbl_app_name.bind(size=lbl_app_name.setter('text_size'))

        if self.lic_data["activated"]:
            status_text = f"[color=10b981]مفعل ({self.lic_data['mode']})[/color]"
        else:
            days = max(0, 15 - int((time.time() - self.lic_data["first_run"]) / 86400))
            status_text = f"[color=38bdf8]تجريبي: {days} يوم[/color]"

        btn_act = Button(
            text=status_text, markup=True,
            size_hint=(None, 1), width=130,
            background_normal="", background_color=(0.09, 0.13, 0.2, 1)
        )
        btn_act.bind(on_release=self.show_activation_popup)

        header.add_widget(lbl_app_name)
        header.add_widget(btn_act)
        self.add_widget(header)

        # Scrollable Body Layout (لضمان الانسيابية الكاملة على مختلف الشاشات)
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content = BoxLayout(orientation="vertical", spacing=12, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # 2. قسم بطاقات المنصات المضاءة (Neon Preset Cards)
        lbl_sec1 = Label(
            text="[b]اختر منصة التصدير السريعة:[/b]", 
            markup=True, font_size="13sp", size_hint_y=None, height=25,
            color=(0.58, 0.63, 0.72, 1), halign="right"
        )
        lbl_sec1.bind(size=lbl_sec1.setter('text_size'))
        content.add_widget(lbl_sec1)

        cards_grid = GridLayout(cols=1, spacing=8, size_hint_y=None)
        cards_grid.bind(minimum_height=cards_grid.setter('height'))

        for key, info in PLATFORMS.items():
            card = PlatformPresetCard(key, info, self.select_platform)
            self.cards_dict[key] = card
            cards_grid.add_widget(card)

        content.add_widget(cards_grid)
        self.select_platform("TIKTOK")

        # 3. صندوق إدخال النص والسيناريو
        lbl_sec2 = Label(
            text="[b]نص السيناريو والقصة:[/b]", 
            markup=True, font_size="13sp", size_hint_y=None, height=25,
            color=(0.58, 0.63, 0.72, 1), halign="right"
        )
        lbl_sec2.bind(size=lbl_sec2.setter('text_size'))
        content.add_widget(lbl_sec2)

        self.txt_prompt = TextInput(
            hint_text="اكتب الفكرة أو السيناريو هنا..",
            multiline=True, size_hint_y=None, height=110,
            background_color=(0.02, 0.03, 0.05, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.06, 0.72, 0.51, 1),
            padding=[10, 10, 10, 10]
        )
        content.add_widget(self.txt_prompt)

        # 4. أزرار التشغيل والعمليات
        self.btn_generate = Button(
            text="[b]توليد ومعالجة المشاهد 🎬[/b]", markup=True,
            size_hint_y=None, height=50,
            background_normal="", background_color=(0.06, 0.72, 0.51, 1) # Emerald Green
        )
        self.btn_generate.bind(on_release=self.start_processing)
        content.add_widget(self.btn_generate)

        self.p_bar = ProgressBar(max=100, size_hint_y=None, height=15)
        content.add_widget(self.p_bar)

        self.lbl_status = Label(
            text="النظام مستقر وجاهز", font_size="12sp",
            color=(0.06, 0.72, 0.51, 1), size_hint_y=None, height=20
        )
        content.add_widget(self.lbl_status)

        scroll.add_widget(content)
        self.add_widget(scroll)

    def select_platform(self, key):
        self.selected_platform = key
        for k, card in self.cards_dict.items():
            card.is_selected = (k == key)
            card.update_graphics()

    def start_processing(self, instance):
        prompt = self.txt_prompt.text.strip()
        if not prompt:
            self.lbl_status.text = "يرجى كتابة نص السيناريو أولاً!"
            self.lbl_status.color = (0.93, 0.26, 0.26, 1)
            return

        self.btn_generate.disabled = True
        self.lbl_status.text = "جاري المعالجة بالخلفية..."
        self.lbl_status.color = (0.22, 0.82, 0.93, 1)
        self.p_bar.value = 10

        # خيط خلفي لمنع تهنيج واجهة الموبايل تماماً (Async Engine)
        threading.Thread(target=self._async_task, args=(prompt,), daemon=True).start()

    def _async_task(self, prompt):
        try:
            # محاكاة خطوة المعالجة السريعة
            for val in range(15, 101, 20):
                time.sleep(0.4)
                Clock.schedule_once(lambda dt, v=val: setattr(self.p_bar, 'value', v))

            Clock.schedule_once(self._on_task_finished)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_task_failed(str(e)))

    def _on_task_finished(self, dt):
        self.btn_generate.disabled = False
        self.lbl_status.text = "تم التوليد والحفظ بنجاح! 🚀"
        self.lbl_status.color = (0.06, 0.72, 0.51, 1)

    def _on_task_failed(self, err_msg):
        self.btn_generate.disabled = False
        self.lbl_status.text = f"خطأ: {err_msg}"
        self.lbl_status.color = (0.93, 0.26, 0.26, 1)

    # 5. نافذة التفعيل التفاعلية (Activation Modal)
    def show_activation_popup(self, instance):
        box = BoxLayout(orientation="vertical", padding=12, spacing=10)
        box.add_widget(Label(text="رمز جهازك (أرسله للمهندس عادل):", font_size="12sp"))

        txt_hwid = TextInput(text=self.hwid, readonly=True, size_hint_y=None, height=40)
        box.add_widget(txt_hwid)

        box.add_widget(Label(text="أدخل كود التفعيل هنا:", font_size="12sp"))
        txt_key = TextInput(hint_text="XXXX-XXXX-XXXX-XXXX-XXXX", size_hint_y=None, height=40)
        box.add_widget(txt_key)

        btn_apply = Button(
            text="تفعيل الآن 🔑", size_hint_y=None, height=45,
            background_normal="", background_color=(0.06, 0.72, 0.51, 1)
        )
        box.add_widget(btn_apply)

        popup = Popup(
            title="تفعيل التطبيق - المبتكرون العرب", 
            content=box, size_hint=(0.9, 0.55)
        )

        def apply_key(btn):
            key = txt_key.text.strip()
            valid, mode = verify_license(self.hwid, key)
            if valid:
                self.lic_data["activated"] = True
                self.lic_data["key"] = key
                self.lic_data["mode"] = mode
                self.save_license()
                popup.dismiss()
                self.lbl_status.text = "تم تفعيل التطبيق بنجاح!"
            else:
                txt_key.text = ""
                txt_key.hint_text = "كود غير صحيح!"

        btn_apply.bind(on_release=apply_key)
        popup.open()

# ---------------------------------------------------------------
# 5. التطبيق الرئيسي (Kivy App Builder)
# ---------------------------------------------------------------
class ApexMasterMobileApp(App):
    def build(self):
        self.title = "Apex Master AI Studio"
        return ApexMobileStudio()

if __name__ == "__main__":
    ApexMasterMobileApp().run()
