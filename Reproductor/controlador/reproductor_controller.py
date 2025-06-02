import pygame.mixer as mx
import os

class ReproductorController:
    def __init__(self, vista):
        mx.init(frequency=44100, size=-16, channels=2, buffer=4096)

        self.vista = vista
        self.playlist = []
        self.inicio = 0
        self.playing = False
        self.paused = False

        self.nivelBajos = 1.0
        self.nivelMedios = 1.0
        self.nivelAgudos = 1.0

    def ajustarBajos(self, valor):
        self.nivelBajos = float(valor)/100
        self.aplicarEcualizacion()

    def ajustarMedios(self, valor):
        self.nivelMedios = float(valor)/100
        self.aplicarEcualizacion()

    def ajustarAgudos(self, valor):
        self.nivelAgudos = float(valor)/100
        self.aplicarEcualizacion()

    def aplicarEcualizacion(self):
        if not self.playing:
            return
        try:
            balance = (self.nivelBajos * 0.4 + self.nivelMedios * 0.3 + self.nivelAgudos * 0.3)
            mx.music.set_volume(balance * (self.vista.barraVolumen.get()/100))
        except:
            pass

    def ajustarVolumen(self, valor):
        volumen = float(valor)/100
        mx.music.set_volume(volumen)

    def seleccionarCarpeta(self):
        from tkinter import filedialog
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de canciones")
        if carpeta:
            self.cargarCancionesDesdeCarpeta(carpeta)

    def cargarCancionesDesdeCarpeta(self, rutaCarpeta):
        try:
            archivos = os.listdir(rutaCarpeta)
            extensionesValidas = ('.mp3', '.wav', '.ogg')
            cancionesEncontradas = [os.path.join(rutaCarpeta, f) for f in archivos if f.lower().endswith(extensionesValidas)]
            if cancionesEncontradas:
                self.playlist = cancionesEncontradas
                self.vista.listaReproduccion.delete(0, 'end')
                for cancion in cancionesEncontradas:
                    self.vista.listaReproduccion.insert('end', os.path.basename(cancion))
                self.inicio = 0
                self.vista.etiquetaEstado.config(text=f"Cargadas {len(cancionesEncontradas)} canciones")
            else:
                self.vista.etiquetaEstado.config(text="No se encontraron canciones válidas")
        except Exception as error:
            self.vista.etiquetaEstado.config(text=f"Error: {str(error)}")

    def reproducir(self):
        if not self.playlist:
            self.vista.etiquetaEstado.config(text="No hay canciones disponibles")
            return
        try:
            self.cancionActual = self.playlist[self.inicio]
            mx.music.load(self.cancionActual)
            mx.music.play()
            self.playing = True
            self.paused = False
            nombre = os.path.basename(self.cancionActual)
            self.vista.etiquetaEstado.config(text=f"Reproduciendo: {nombre}")
            mx.music.set_volume(self.vista.barraVolumen.get()/100)

            sound = mx.Sound(self.cancionActual)
            self.duracionTotal = sound.get_length()
            minutos, segundos = divmod(int(self.duracionTotal), 60)
            self.vista.etiquetaDuracion.config(text=f"Duración: {minutos:02}:{segundos:02}")

            self.actualizarProgreso()
        except Exception as e:
            self.vista.etiquetaEstado.config(text=f"Error: {str(e)}")
            self.playing = False

    def actualizarProgreso(self):
     if self.playing and not self.paused:
        try:
            posicionActual = mx.music.get_pos() / 1000
            progreso = (posicionActual / self.duracionTotal) * 100
            self.vista.barraProgreso.set(min(100, max(0, progreso)))
            minutos_transcurridos, segundos_transcurridos = divmod(int(posicionActual), 60)
            minutos_totales, segundos_totales = divmod(int(self.duracionTotal), 60)

            self.vista.etiquetaDuracion.config(
                text=f"{minutos_transcurridos:02}:{segundos_transcurridos:02} / {minutos_totales:02}:{segundos_totales:02}"
            )

            self.vista.ventana.after(1000, self.actualizarProgreso) 
        except:
            pass

    def toggleReproduccion(self):
        if not self.playlist:
            self.vista.etiquetaEstado.config(text="No hay canciones disponibles")
            return
        if self.playing and not self.paused:
            self.pausar()
        else:
            self.reproducir()

    def detener(self):
        mx.music.stop()
        self.playing = False
        self.paused = False
        self.vista.barraProgreso.set(0)
        self.vista.etiquetaEstado.config(text="Reproducción detenida")

    def pausar(self):
        if self.playing:
            mx.music.pause()
            self.paused = True
            self.playing = False
            self.vista.etiquetaEstado.config(text="Reproducción pausada")

    def siguiente(self):
        if not self.playlist:
            return
        self.detener()
        self.inicio = (self.inicio + 1) % len(self.playlist)
        self.reproducir()

    def anterior(self):
        if not self.playlist:
            return
        self.detener()
        self.inicio = (self.inicio - 1) % len(self.playlist)
        self.reproducir()

    def adelantar10(self):
        if self.playing and not self.paused:
            try:
                posicionActual = mx.music.get_pos() / 1000
                nuevaPosicion = min(posicionActual + 10, self.duracionTotal)
                mx.music.set_pos(nuevaPosicion)
                self.vista.etiquetaEstado.config(text="Adelantando 10 segundos...")
            except:
                self.vista.etiquetaEstado.config(text="Error al adelantar")

    def retroceder10(self):
        if self.playing and not self.paused:
            try:
                posicionActual = mx.music.get_pos() / 1000
                nuevaPosicion = max(0, posicionActual - 10)
                mx.music.set_pos(nuevaPosicion)
                self.vista.etiquetaEstado.config(text="Retrocediendo 10 segundos...")
            except:
                self.vista.etiquetaEstado.config(text="Error al retroceder")
