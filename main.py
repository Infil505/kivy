import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from kivy.lang import Builder

class DownloadBoxLayout(BoxLayout):
    def start_download(self, instance):
        self.ids.boton_descarga.disabled = True
        self.ids.message_label.text = "Descargando..."

        video_url = self.ids.videos.text
        if not video_url:
            self.ids.message_label.text = "Error: Por favor, ingresa un enlace válido"
            self.ids.boton_descarga.disabled = False
            return

        download_thread = threading.Thread(target=self.download_video, args=(video_url,))
        download_thread.start()

    def download_video(self, video_url):
        try:
            video = YouTube(video_url, on_progress_callback=self.update_progress)
            stream = video.streams.get_highest_resolution()
            total_size = stream.filesize

            response = stream.download(output_path="Descargas/")
            self.ids.message_label.text = "       Descarga completada: \n            El video se ha \n       descargado con éxito"
        except RegexMatchError:
            self.ids.message_label.text = "Error: No se pudo encontrar el video."
        except Exception as e:
            self.ids.message_label.text = f"Error durante la descarga: {str(e)}"

        Clock.schedule_once(self.reset_view, 5)

    def reset_view(self, dt):
        self.ids.videos.text = ""
        self.ids.progressbar.value = 0
        self.ids.message_label.text = ""
        self.ids.porcentaje_label.text = ""
        self.ids.boton_descarga.disabled = False

    def update_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.ids.progressbar.value = percentage
        self.ids.porcentaje_label.text = f"Progreso: {int(percentage)}%"

    def clean_filename(self, filename):
        invalid_chars = '<>:"/\\|?*'
        return ''.join(c for c in filename if c not in invalid_chars)

    def get_font_size(self):
        return '20sp'

class YouTubeDownloaderApp(App):
    def build(self):
        return Builder.load_file("youtube_downloader.kv")

if __name__ == "__main__":
    YouTubeDownloaderApp().run()
