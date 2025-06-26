import os
import threading
import time
import random
from datetime import datetime
from pathlib import Path

# Configuração do Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

# Configurações de cores
WINDOW_BG = (0, 0, 0, 1)  # Preto
INPUT_BG = (0.07, 0.07, 0.07, 1)  # Cinza escuro
BUTTON_BG = (0.02, 0.39, 0.62, 1)  # Azul
TEXT_COLOR = (1, 1, 1, 1)  # Branco
HIGHLIGHT_COLOR = (0, 1, 1, 1)  # Ciano


# Modelo simulado simples
class SimpleModel:
    def __init__(self):
        self.responses = [
            "Olá! Como posso ajudar você hoje?",
            "Interessante! Me conte mais sobre isso.",
            "Entendo. Posso ajudar com mais alguma coisa?",
            "Ótima pergunta! Deixe-me pensar...",
            "Claro! Fico feliz em ajudar.",
            "Isso é muito legal! Obrigada por compartilhar.",
            "Hmm, preciso pensar mais sobre isso.",
            "Você tem razão! É uma boa observação.",
            "Posso tentar te ajudar com isso.",
            "Que interessante! Nunca havia pensado nisso."
        ]

    def generate(self, message):
        # Respostas simples baseadas em palavras-chave
        message_lower = message.lower()

        if any(word in message_lower for word in ['olá', 'oi', 'boa', 'dia', 'tarde', 'noite']):
            return "Olá! Como posso ajudar você hoje?"
        elif any(word in message_lower for word in ['nome', 'quem']):
            return "Meu nome é TerlineT! Sou uma assistente virtual."
        elif any(word in message_lower for word in ['como', 'vai', 'tudo']):
            return "Estou bem, obrigada por perguntar! E você?"
        elif any(word in message_lower for word in ['obrigado', 'obrigada', 'valeu']):
            return "De nada! Fico feliz em ajudar."
        elif any(word in message_lower for word in ['tchau', 'até', 'falou']):
            return "Até mais! Foi um prazer conversar com você."
        else:
            return random.choice(self.responses)


# Widget com fundo colorido
class ColoredBoxLayout(BoxLayout):
    def __init__(self, bg_color=(0, 0, 0, 1), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.bind(pos=self.update_rect, size=self.update_rect)
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


# Interface principal
class ChatScreen(ColoredBoxLayout):
    chat_log = StringProperty("")
    status_text = StringProperty("Pronto para conversar!")
    input_text = StringProperty("")
    send_enabled = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(bg_color=WINDOW_BG, **kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10

        # Título
        title = Label(
            text='TERLINET - Versão Simples',
            font_size=25,
            bold=True,
            color=HIGHLIGHT_COLOR,
            size_hint_y=None,
            height=40
        )

        # Status
        status = Label(
            text=self.status_text,
            font_size=12,
            color=HIGHLIGHT_COLOR,
            size_hint_y=None,
            height=25
        )
        self.bind(status_text=status.setter('text'))

        # Área de chat
        scroll_view = ScrollView(size_hint=(1, 0.7))
        self.chat_label = Label(
            text=self.chat_log,
            font_size=14,
            color=TEXT_COLOR,
            size_hint_y=None,
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        self.chat_label.bind(texture_size=self.chat_label.setter('size'))
        self.bind(chat_log=self.chat_label.setter('text'))
        scroll_view.add_widget(self.chat_label)

        # Área de entrada
        input_box = BoxLayout(
            size_hint_y=None,
            height=50,
            spacing=10
        )

        self.input_field = TextInput(
            text=self.input_text,
            hint_text='Digite sua mensagem...',
            font_size=14,
            background_color=INPUT_BG,
            foreground_color=TEXT_COLOR,
            multiline=False,
            size_hint_x=0.8
        )
        self.input_field.bind(text=self.setter('input_text'))
        self.input_field.bind(on_text_validate=self.send_message)

        self.send_btn = Button(
            text='ENVIAR',
            font_size=14,
            bold=True,
            background_color=BUTTON_BG,
            size_hint_x=0.2
        )
        self.send_btn.bind(on_press=self.send_message)

        input_box.add_widget(self.input_field)
        input_box.add_widget(self.send_btn)

        # Monta a interface
        self.add_widget(title)
        self.add_widget(status)
        self.add_widget(scroll_view)
        self.add_widget(input_box)

        # Inicializa o modelo simples
        self.model = SimpleModel()

        # Mensagem inicial
        self.add_message("TerlineT", "Olá! Sou a TerlineT. Como posso ajudar você hoje?")

    def add_message(self, sender, message):
        timestamp = datetime.now().strftime("%H:%M")
        formatted = f"[{timestamp}] {sender}: {message}\n\n"
        self.chat_log += formatted

        # Atualiza o tamanho do label de chat
        Clock.schedule_once(self.update_chat_size, 0.1)

    def update_chat_size(self, dt):
        self.chat_label.text_size = (Window.width - 40, None)
        self.chat_label.texture_update()

    def send_message(self, instance):
        message = self.input_text.strip()
        if not message:
            return

        # Adiciona a mensagem do usuário
        self.add_message("Você", message)
        self.input_text = ""
        self.input_field.text = ""
        self.status_text = "Pensando..."

        # Processa a resposta em outra thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def process_message(self, message):
        try:
            # Simula tempo de processamento
            time.sleep(0.5)
            response = self.model.generate(message)

            # Atualiza a UI na thread principal
            Clock.schedule_once(lambda dt: self.add_message("TerlineT", response))
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            Clock.schedule_once(lambda dt: self.add_message("Sistema", error_msg))
        finally:
            Clock.schedule_once(lambda dt: setattr(self, 'status_text', "Pronto para conversar!"))


# App principal
class TerlineTApp(App):
    def build(self):
        Window.clearcolor = WINDOW_BG
        return ChatScreen()


if __name__ == '__main__':
    TerlineTApp().run()
