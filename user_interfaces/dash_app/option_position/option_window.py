class OptionWindow:
    def __init__(self, app: dash.Dash, **kwargs):
        self.app = app
        self.window = self.create_window()
        self.layout = self.create_layout()
        self.window.layout = self.layout

    def create_window(self):
        window = Window(title='Option Position')
        return window

    def create_layout(self):
        layout = GridLayout(rows=3, columns=2)
        layout.add_widget(Label(text='Option Symbol'))
        layout.add_widget(TextInput())
        layout.add_widget(Label(text='Option Type'))
        layout.add_widget(TextInput())
        layout.add_widget(Label(text='Option Strike'))
        layout.add_widget(TextInput())
        return layout