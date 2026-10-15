from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class PhotoSyncApp(App):
    def build(self):
        self.folders = ["Screenshots"]

        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
        )

        title = Label(
            text="Photo Sync",
            font_size=28,
            size_hint_y=None,
            height=60,
        )
        root.add_widget(title)

        self.status_label = Label(
            text="Status: Ready",
            size_hint_y=None,
            height=40,
        )
        root.add_widget(self.status_label)

        root.add_widget(
            Label(
                text="Monitored folders",
                size_hint_y=None,
                height=40,
            )
        )

        self.folder_list = BoxLayout(
            orientation="vertical",
            spacing=5,
        )
        root.add_widget(self.folder_list)

        add_button = Button(
            text="Add test folder",
            size_hint_y=None,
            height=50,
        )
        add_button.bind(on_press=self.add_folder)
        root.add_widget(add_button)

        sync_button = Button(
            text="Synchronize now",
            size_hint_y=None,
            height=50,
        )
        sync_button.bind(on_press=self.synchronize)
        root.add_widget(sync_button)

        self.refresh_folder_list()

        return root

    def refresh_folder_list(self):
        self.folder_list.clear_widgets()

        for folder in self.folders:
            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=45,
                spacing=10,
            )

            row.add_widget(Label(text=folder))

            remove_button = Button(
                text="Remove",
                size_hint_x=None,
                width=100,
            )
            remove_button.bind(
                on_press=lambda instance, name=folder:
                self.remove_folder(name)
            )

            row.add_widget(remove_button)
            self.folder_list.add_widget(row)

    def add_folder(self, instance):
        folder_name = "New folder"

        if folder_name not in self.folders:
            self.folders.append(folder_name)
            self.refresh_folder_list()

    def remove_folder(self, folder_name):
        if folder_name in self.folders:
            self.folders.remove(folder_name)
            self.refresh_folder_list()

    def synchronize(self, instance):
        self.status_label.text = (
            "Synchronization is not connected yet"
        )


if __name__ == "__main__":
    PhotoSyncApp().run()

