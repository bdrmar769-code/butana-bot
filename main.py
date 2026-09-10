from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.lang import Builder

Window.clearcolor = (0.89, 0.95, 1, 1)

kb_data = {
    "نسبه الحضور": {"category": "الحضور", "answer": "نسبة الحضور المطلوبة في المقررات النظرية هي ألا تقل عن 75% من إجمالي المحاضرات.\nيؤدي غياب الطالب لأكثر من 25% من المحاضرات إلى حرمان الطالب من الجلوس للامتحان النهائي.", "source": "اللائحة الأكاديمية - بند 1.12.3"},
    "الامتحانات": {"category": "الامتحانات", "answer": "يحدد تاريخ وموعد امتحانات نهاية كل فصل دراسي بما يتفق ولوائح الكلية المعنية، ويجب على الكلية نشر جدول الامتحانات قبل أسبوعين من بدايتها.", "source": "اللائحة الأكاديمية - بند 1.1.9"},
    "التسجيل": {"category": "التسجيل", "answer": "يكون تسجيل الطالب نظامياً إذا كان تسجيله لا يقل عن عشرة ساعات معتمدة.", "source": "اللائحة الأكاديمية - بند 2.1.5"},
    "الرسوم الدراسيه": {"category": "الرسوم", "answer": "لتسجيل الفصل الدراسي، يجب على الطالب تسديد رسوم التسجيل والمصروفات الدراسية المقررة عند بداية الفصل.", "source": "اللائحة الأكاديمية - بند 4.2.5"},
    "العقوبات والمخالفات": {"category": "العقوبات", "answer": "إذا وجد أي طالب في حالة غش تحر مذكرة بحقه ويحق لمجلس الأساتذة فصله نهائياً.", "source": "اللائحة الأكاديمية - بند 20.3.9"},
    "التخرج": {"category": "التخرج", "answer": "الحد الأدنى لمنح الإجازه الجامعية هو الحصول على معدل تراكمي لا يقل عن 2.00 بعد إكمال المنهج.", "source": "اللائحة الأكاديمية - بند 1.10"}
}

kv = '''
ScreenManager:
    MenuScreen:
        name: 'menu'
    ChatScreen:
        name: 'chat'

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        Label:
            text: "جامعة البطانة"
            font_size: 28
            bold: True
            color: 0.05, 0.27, 0.64, 1
            size_hint_y: None
            height: 60
        Label:
            text: "اختر القسم"
            font_size: 18
            color: 0.08, 0.39, 0.75, 1
        GridLayout:
            cols: 1
            spacing: 8
            Button:
                text: "نسبه الحضور"
                on_press: app.open_chat("نسبه الحضور")
            Button:
                text: "الامتحانات"
                on_press: app.open_chat("الامتحانات")
            Button:
                text: "التسجيل"
                on_press: app.open_chat("التسجيل")
            Button:
                text: "الرسوم الدراسيه"
                on_press: app.open_chat("الرسوم الدراسيه")
            Button:
                text: "العقوبات والمخالفات"
                on_press: app.open_chat("العقوبات والمخالفات")
            Button:
                text: "التخرج"
                on_press: app.open_chat("التخرج")

<ChatScreen>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: None
            height: 50
            Button:
                text: '← رجوع'
                size_hint_x: 0.2
                on_press: app.root.current = 'menu'
            Label:
                id: title
                text: 'القسم'
        ScrollView:
            Label:
                id: chat_log
                text_size: self.width, None
                size_hint_y: None
                height: self.texture_size[1]
        BoxLayout:
            size_hint_y: None
            height: 50
            TextInput:
                id: entry
                multiline: False
            Button:
                text: 'ارسال'
                size_hint_x: 0.3
                on_press: root.send_message()
'''

class MenuScreen(Screen): pass
class ChatScreen(Screen):
    category_key = ""
    def send_message(self):
        user_text = self.ids.entry.text
        if not user_text: return
        self.ids.chat_log.text += f"\n\n👤 أنت:\n{user_text}"
        data = kb_data.get(self.category_key)
        response = f"{data['answer']}\n\nالمصدر: {data['source']}" if data else "خطأ"
        self.ids.chat_log.text += f"\n\n🤖:\n{response}"
        self.ids.entry.text = ""

class BotApp(App):
    def build(self):
        return Builder.load_string(kv)
    def open_chat(self, key):
        chat = self.root.get_screen('chat')
        chat.category_key = key
        chat.ids.title.text = f"قسم: {key}"
        chat.ids.chat_log.text = f"🤖 أهلاً بك! اسأل عن {key}"
        self.root.current = 'chat'

if __name__ == "__main__":
    BotApp().run()
