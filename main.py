import os
import re
import threading
import time
import random
import logging
from datetime import datetime
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.utils import platform

# Importar o carregador GGUF customizado
from gguf_loader import GGUFModelWrapper

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Detectar se está no Android
IS_ANDROID = platform == 'android'

# Configurações de cores
WINDOW_BG = (0, 0, 0, 1)  # Preto
INPUT_BG = (0.07, 0.07, 0.07, 1)  # Cinza escuro
BUTTON_BG = (0.02, 0.39, 0.62, 1)  # Azul
MIC_ACTIVE_COLOR = (1, 0, 0, 1)  # Vermelho
TEXT_COLOR = (1, 1, 1, 1)  # Branco
HIGHLIGHT_COLOR = (0, 1, 1, 1)  # Ciano

# Configurar caminho do modelo (adaptado para Android)
if IS_ANDROID:
    try:
        from android.storage import primary_external_storage_path

        MODEL_PATH = Path(
            primary_external_storage_path()) / "TerlineT" / "modelo" / "DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf"
    except ImportError:
        logger.warning("Módulo android.storage não disponível")
        MODEL_PATH = Path(
            "/storage/emulated/0/TerlineT/modelo/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf")
else:
    MODEL_PATH = Path("K:/FLUTTER/TerlineT_Kivy/modelo/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf")

# Configurar permissões Android
if IS_ANDROID:
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.RECORD_AUDIO,
            Permission.INTERNET
        ])
    except ImportError:
        logger.warning("Módulo android.permissions não disponível")
        pass


class VoiceSynthesizer:
    def __init__(self):
        self.is_speaking = False

    def speak(self, text, callback):
        if not text or self.is_speaking:
            callback()
            return
        
        self.is_speaking = True
        logger.info(f"Falando: {text}")
        # Simula o tempo de fala (reduzido para Android)
        sleep_time = len(text.split()) * (0.1 if IS_ANDROID else 0.2)
        time.sleep(sleep_time)
        self.is_speaking = False
        callback()


class VoiceRecognizer:
    def __init__(self):
        self.listening = False
        self.recording = False
        self.confirmation_phrase = "Sim, estou ouvindo! Como posso ajudar?"

    def start_listening(self):
        self.listening = True
        logger.info("Reconhecimento de voz simulado ativado")

    def stop_listening(self):
        self.listening = False
        self.recording = False

    def record_command(self, callback):
        """Simula o reconhecimento de voz"""
        if not self.listening:
            callback("")
            return
            
        self.recording = True
        logger.info("Simulando gravação de comando")
        time.sleep(1.5 if IS_ANDROID else 2)  # Tempo reduzido para Android
        self.recording = False
        callback("comando de voz simulado")


# Widget com fundo colorido
class ColoredBoxLayout(BoxLayout):
    bg_color = (0, 0, 0, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect)
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_bg_color(self, color):
        self.bg_color = color
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)


# Botão de microfone animado
class AnimatedMicButton(Button):
    mic_active = BooleanProperty(False)
    mic_level = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation = None
        self.bind(mic_active=self.update_animation)

    def update_animation(self, instance, value):
        if value:
            # Inicia animação de pulso
            self.animation = Animation(mic_level=1, duration=0.5) + Animation(mic_level=0, duration=0.5)
            self.animation.repeat = True
            self.animation.start(self)
        elif self.animation:
            self.animation.cancel(self)
            self.mic_level = 0


# Interface principal
class ChatScreen(ColoredBoxLayout):
    chat_log = StringProperty("")
    status_text = StringProperty("Carregando...")
    input_text = StringProperty("")
    send_enabled = BooleanProperty(False)
    mic_active = BooleanProperty(False)
    mic_level = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = WINDOW_BG
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10

        # Título
        title = Label(
            text='🤖 TERLINET - ASSISTENTE VIRTUAL',
            font_size=16 if IS_ANDROID else 20,
            bold=True,
            color=HIGHLIGHT_COLOR,
            size_hint_y=None,
            height=35 if IS_ANDROID else 40
        )

        # Status
        status = Label(
            text=self.status_text,
            font_size=10 if IS_ANDROID else 11,
            color=HIGHLIGHT_COLOR,
            size_hint_y=None,
            height=20
        )
        self.bind(status_text=status.setter('text'))

        # Área de chat
        scroll_view = ScrollView(size_hint=(1, 0.7))
        self.chat_label = Label(
            text=self.chat_log,
            font_size=12 if IS_ANDROID else 14,
            color=TEXT_COLOR,
            size_hint_y=None,
            text_size=(Window.width - 20, None),
            halign='left',
            valign='top'
        )
        self.chat_label.bind(texture_size=self.chat_label.setter('size'))
        self.bind(chat_log=self.chat_label.setter('text'))
        scroll_view.add_widget(self.chat_label)

        # Área de entrada
        input_box = BoxLayout(
            size_hint_y=None,
            height=50 if IS_ANDROID else 40,
            spacing=10
        )

        self.input_field = TextInput(
            text=self.input_text,
            hint_text='Digite sua mensagem...',
            font_size=12 if IS_ANDROID else 14,
            background_color=INPUT_BG,
            foreground_color=TEXT_COLOR,
            multiline=False,
            size_hint_x=0.6
        )
        self.input_field.bind(text=self.setter('input_text'))
        self.input_field.bind(on_text_validate=self.send_message)

        self.send_btn = Button(
            text='ENVIAR',
            font_size=12 if IS_ANDROID else 14,
            bold=True,
            background_color=BUTTON_BG if self.send_enabled else (0.5, 0.5, 0.5, 1),
            disabled=not self.send_enabled,
            size_hint_x=0.2
        )
        self.send_btn.bind(on_press=self.send_message)
        self.bind(send_enabled=self.update_send_button)

        # Botão de microfone
        self.mic_btn = AnimatedMicButton(
            text='🎤',
            font_size=18 if IS_ANDROID else 20,
            background_color=MIC_ACTIVE_COLOR if self.mic_active else BUTTON_BG,
            size_hint_x=0.2
        )
        self.mic_btn.bind(on_press=self.toggle_microphone)
        self.bind(mic_active=self.mic_btn.setter('mic_active'))
        self.bind(mic_level=self.mic_btn.setter('mic_level'))

        input_box.add_widget(self.input_field)
        input_box.add_widget(self.send_btn)
        input_box.add_widget(self.mic_btn)

        # Monta a interface
        self.add_widget(title)
        self.add_widget(status)
        self.add_widget(scroll_view)
        self.add_widget(input_box)

        # Inicializa componentes
        self.model = GGUFModelWrapper()
        self.voice = VoiceSynthesizer()
        self.voice_recognizer = VoiceRecognizer()

        # Mensagem inicial
        platform_msg = "🤖 Android" if IS_ANDROID else "💻 Desktop"
        self.add_message("Sistema", f"TerlineT iniciando... Plataforma: {platform_msg}")
        self.status_text = "Carregando modelo GGUF..."

        # Carrega o modelo
        self.model.load_model(str(MODEL_PATH), self.model_loaded_callback)

    def on_start(self):
        """Inicia o reconhecimento de voz automaticamente"""
        self.start_voice_recognition()

    def update_send_button(self, instance, value):
        self.send_btn.disabled = not value
        self.send_btn.background_color = BUTTON_BG if value else (0.5, 0.5, 0.5, 1)

    def model_loaded_callback(self, success, error=None):
        """Callback chamado quando o modelo é carregado"""
        if success:
            if error and "simulado" in error.lower():
                self.status_text = "Modo simulado inteligente ativo"
                self.add_message("TerlineT",
                                 f"Olá! Estou funcionando em modo simulado inteligente. {error}")
            else:
                self.status_text = "Modelo GGUF carregado - Pronto!"
                self.add_message("TerlineT",
                                 "Olá! Modelo GGUF carregado com sucesso! Como posso ajudar?")

            if IS_ANDROID:
                self.add_message("TerlineT",
                                 f"📱 Funcionando perfeitamente no Android! Modelo localizado em: {MODEL_PATH}")

            self.send_enabled = True
            self.speak("Olá! Estou pronta para ajudar você!")
        else:
            self.status_text = f"Erro: {error}" if error else "Erro ao carregar"
            self.add_message("Sistema",
                             f"❌ Falha ao carregar modelo: {error or 'Erro desconhecido'}")
            self.send_enabled = True  # Permite uso mesmo com erro

    def add_message(self, sender, message):
        timestamp = datetime.now().strftime("%H:%M")
        formatted = f"[{timestamp}] {sender}: {message}\n\n"
        self.chat_log += formatted

        # Atualiza o tamanho do label de chat
        self.chat_label.texture_update()
        self.chat_label.height = max(self.chat_label.texture_size[1], 40)

    def speak(self, text):
        def callback():
            self.send_enabled = True

        self.send_enabled = False
        threading.Thread(target=self.voice.speak, args=(text, callback), daemon=True).start()

    def send_message(self, instance):
        message = self.input_text.strip()
        if not message or not self.send_enabled:
            return

        # Adiciona a mensagem do usuário
        self.add_message("Você", message)
        self.input_text = ""
        self.input_field.text = ""
        self.send_enabled = False
        self.status_text = "Processando..."

        # Processa a resposta em outra thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def process_message(self, message):
        try:
            # Gera resposta usando o modelo GGUF
            response = self.model.generate(message)

            if response:
                # Atualiza a UI na thread principal
                Clock.schedule_once(lambda dt: self.add_message("TerlineT", response))
                Clock.schedule_once(lambda dt: self.speak(response))
            else:
                raise RuntimeError("Resposta vazia do modelo")

        except Exception as e:
            error_msg = f"Erro ao processar: {str(e)}"
            Clock.schedule_once(lambda dt: self.add_message("Sistema", error_msg))
            logger.error(f"Erro no processamento: {e}")
        finally:
            Clock.schedule_once(
                lambda dt: setattr(self, 'status_text', "Pronto para nova mensagem"))
            Clock.schedule_once(lambda dt: setattr(self, 'send_enabled', True))

    def toggle_microphone(self, instance):
        """Ativa/desativa o microfone manualmente"""
        if self.mic_active:
            self.stop_voice_recognition()
        else:
            self.start_voice_recognition()

    def start_voice_recognition(self):
        """Inicia o reconhecimento de voz"""
        self.mic_active = True
        self.status_text = "🎤 Ouvindo... Diga algo!"
        self.voice_recognizer.start_listening()

        # Inicia a verificação de ativação
        Clock.schedule_interval(self.check_voice_activation, 0.5)

    def stop_voice_recognition(self):
        """Para o reconhecimento de voz"""
        self.mic_active = False
        self.status_text = "Pronto para nova mensagem"
        self.voice_recognizer.stop_listening()
        Clock.unschedule(self.check_voice_activation)

    def check_voice_activation(self, dt):
        """Verifica se há comando de voz"""
        if self.voice_recognizer.recording:
            Clock.unschedule(self.check_voice_activation)
            self.status_text = "Gravando comando..."

            # Simula gravação do comando
            self.voice_recognizer.record_command(self.handle_voice_command)

    def handle_voice_command(self, command):
        """Processa o comando de voz reconhecido"""
        if command and command.strip():
            Clock.schedule_once(lambda dt: self.add_message("Você", f"🎤 {command}"))
            Clock.schedule_once(lambda dt: self.process_voice_command(command))
        else:
            self.status_text = "Comando não reconhecido"
            Clock.schedule_once(
                lambda dt: self.add_message("Sistema", "❌ Não consegui entender o comando de voz"))

    def process_voice_command(self, command):
        """Processa o comando de voz como uma mensagem normal"""
        self.input_text = command
        self.input_field.text = command
        self.send_message(None)


# App principal
class TerlineTApp(App):
    def build(self):
        Window.clearcolor = WINDOW_BG
        if IS_ANDROID:
            # Ajustar tamanho para Android
            Window.size = (360, 640)
        return ChatScreen()

    def on_start(self):
        self.root.on_start()

    def on_pause(self):
        # Permite que o app seja pausado no Android
        return True

    def on_resume(self):
        # Permite que o app seja retomado no Android
        pass


if __name__ == '__main__':
    TerlineTApp().run()
