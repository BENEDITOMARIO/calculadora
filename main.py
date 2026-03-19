from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from logic import CalculatorLogic

Window.size = (360, 640)

class CalculatorLayout(BoxLayout):
    display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = CalculatorLogic()
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        pass

    def on_button_press(self, instance):
        text = instance.text
        display_widget = self.display or self.ids.get('display')
        if display_widget is None:
            print("ERRO: ID 'display' não encontrado.")
            return

        if text == '=':
            result = self.logic.calculate()
            display_widget.text = result

        elif text == 'C':
            display_widget.text = self.logic.clear()

        elif text == '←':
            display_widget.text = self.logic.backspace()

        elif text == '√':
            # Se já tem número no display, calcula imediatamente
            # Se display está vazio ou é '0', marca prefixo √ para digitar depois
            current = self.logic.expression
            if current and current not in ('', '0', '√'):
                # Tenta calcular direto se for só número
                try:
                    float(current)
                    display_widget.text = self.logic.sqrt_current()
                except ValueError:
                    # É uma expressão mista, adiciona √ como prefixo de operação
                    display_widget.text = self.logic.add_char('√')
            else:
                # Display vazio: mostra √ e aguarda número
                display_widget.text = self.logic.sqrt_prefix()

        else:
            display_widget.text = self.logic.add_char(text)

class CalculatorApp(App):
    def build(self):
        self.title = "Calculadora Kivy"
        return CalculatorLayout()

if __name__ == '__main__':
    CalculatorApp().run()