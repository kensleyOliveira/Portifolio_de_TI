import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class MissionPlannerGUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Caminho da imagem
        image_path = os.path.join("images", "Image", "spaceTravel.png")

        # Canvas para imagem de fundo
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Carregamento e redimensionamento da imagem
        try:
            self.original_img = Image.open(image_path)
            self.photo = ImageTk.PhotoImage(self.original_img)
            self.bg = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

            # Vincula o redimensionamento da janela para adaptar a imagem
            self.bind("<Configure>", self._resize_image)
        except Exception as e:
            print(f"[Erro ao carregar imagem]: {e}")

    def _resize_image(self, event):
        """Redimensiona a imagem para preencher toda a aba"""
        if hasattr(self, "original_img"):
            new_width = event.width
            new_height = event.height
            resized = self.original_img.resize((new_width, new_height), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized)
            self.canvas.itemconfig(self.bg, image=self.photo)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("AstroSim - Planejamento de Missões")
    root.geometry("800x600")  # Tamanho inicial sugerido
    app = MissionPlannerGUI(root)
    root.mainloop()