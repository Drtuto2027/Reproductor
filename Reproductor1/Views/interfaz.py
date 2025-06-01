from tkinter import *
import os
from tkinter import font
from Reproductor.Tooltip import Tooltip
from controlador.reproductor_controller import ReproductorController

class Reproductor():
    def __init__(self):
        self.controlador = ReproductorController(self)

        self.ventana = Tk()
        self.ventana.title("Reproductor")
        self.ventana.resizable(0, 0)
        self.ventana.geometry("400x600")

        # Iconos
        self.iconoPlay = PhotoImage(file=r"icons\control_play_blue.png")
        self.iconoPause = PhotoImage(file=r"icons\control_pause_blue.png")
        self.iconoStop = PhotoImage(file=r"icons\control_stop_blue.png")
        self.iconoNext = PhotoImage(file=r"icons\control_fastforward_blue.png")
        self.iconoAtras = PhotoImage(file=r"icons\control_rewind_blue.png")
        self.iconoAdelantar10 = PhotoImage(file=r"icons\arrow_right.png")
        self.iconoRetroceder10 = PhotoImage(file=r"icons\arrow_left.png")

        # Lienzo
        self.lienzo = Canvas(self.ventana, width=580, height=400, bg="yellow")
        self.lienzo.place(relx=0.5, rely=0.45, anchor="center")

        # Botones
        self.btnStop = Button(self.ventana, image=self.iconoStop, command=self.controlador.detener, bg="blue", fg="white")
        self.btnStop.place(x=105, y=520, width=25, height=25)
        Tooltip(self.btnStop, "Presione para detener la reproducción")

        self.btnPlay = Button(self.ventana, image=self.iconoPlay, command=self.controlador.toggleReproduccion, bg="blue", fg="blue")
        self.btnPlay.place(x=130, y=520, width=25, height=25)
        Tooltip(self.btnPlay, "Presione para iniciar/pausar la reproducción")

        self.btnNext = Button(self.ventana, image=self.iconoNext, command=self.controlador.siguiente, bg="blue", fg="blue")
        self.btnNext.place(x=270, y=520, width=25, height=25)
        Tooltip(self.btnNext, "Siguiente canción")

        self.btnAnterior = Button(self.ventana, image=self.iconoAtras, command=self.controlador.anterior, bg="blue", fg="white")
        self.btnAnterior.place(x=245, y=520, width=25, height=25)
        Tooltip(self.btnAnterior, "Canción anterior")

        self.btnAdelantar = Button(self.ventana, image=self.iconoAdelantar10, command=self.controlador.adelantar10, bg="blue", fg="white")
        self.btnAdelantar.place(x=290, y=520, width=25, height=25)
        Tooltip(self.btnAdelantar, "Adelantar 10 segundos")

        self.btnRetroceder = Button(self.ventana, image=self.iconoRetroceder10, command=self.controlador.retroceder10, bg="blue", fg="white")
        self.btnRetroceder.place(x=80, y=520, width=25, height=25)
        Tooltip(self.btnRetroceder, "Retroceder 10 segundos")

        self.btnCargar = Button(self.ventana, text="Cargar Carpeta", command=self.controlador.seleccionarCarpeta, bg="blue", fg="white")
        self.btnCargar.place(relx=0.5, y=532, anchor="center")
        Tooltip(self.btnCargar, "Seleccionar carpeta con canciones")

        self.barraVolumen = Scale(self.ventana, from_=0, to=100, orient=HORIZONTAL, label='Volumen', command=self.controlador.ajustarVolumen, bg="white", fg="black")
        self.barraVolumen.set(50)
        self.barraVolumen.place(x=100, y=225, width=200)

        # Ecualización con barras más pequeñas
        fuente_pequena = font.Font(size=8)

        self.marcoEcualizador = Frame(self.ventana, bg="yellow")
        self.marcoEcualizador.place(x=100, y=283, width=200, height=190)

        self.barraBajos = Scale(self.marcoEcualizador, from_=0, to=200, orient=HORIZONTAL, label='Bajos',
                                command=self.controlador.ajustarBajos, sliderlength=10, length=180, font=fuente_pequena)
        self.barraBajos.set(100)
        self.barraBajos.pack(fill=X, pady=0)

        self.barraMedios = Scale(self.marcoEcualizador, from_=0, to=200, orient=HORIZONTAL, label='Medios',
                                 command=self.controlador.ajustarMedios, sliderlength=10, length=180, font=fuente_pequena)
        self.barraMedios.set(100)
        self.barraMedios.pack(fill=X, pady=0)

        self.barraAgudos = Scale(self.marcoEcualizador, from_=0, to=200, orient=HORIZONTAL, label='Agudos',
                                 command=self.controlador.ajustarAgudos, sliderlength=10, length=180, font=fuente_pequena)
        self.barraAgudos.set(100)
        self.barraAgudos.pack(fill=X, pady=0)

        self.etiquetaDuracion = Label(self.ventana, text="Duración: 00:00", background="white", fg="black")
        self.etiquetaDuracion.place(relx=0.5, y=110, anchor="center")

        self.etiquetaEstado = Label(self.ventana, text="Listo para reproducir", bg="white", fg="black")
        self.etiquetaEstado.place(relx=0.5, y=85, anchor="center")

        self.listaReproduccion = Listbox(self.ventana, bg="white", fg="black")
        self.listaReproduccion.place(x=100, y=140, width=200, height=87)

        self.barraProgreso = Scale(self.ventana, from_=0, to=100, orient=HORIZONTAL, length=300, showvalue=0, bg="white")
        self.barraProgreso.place(x=100, y=120, width=200, height=20)


        # carga inicial
        if os.path.exists("canciones"):
            self.controlador.cargarCancionesDesdeCarpeta("canciones")

        self.ventana.mainloop()
