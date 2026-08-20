import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
import time

class AplicacaoEfeitoRevelacaoDinamica:
    def __init__(self, master, lista_pares_imagens, duracao_ciclo=6):
        self.master = master
        self.master.title("Efeito de Revelação Dinâmica - Versão Automática")
        self.lista_pares = lista_pares_imagens
        self.duracao_ciclo_ms = duracao_ciclo * 1000  # segundos → milissegundos
        self.indice_atual = 0

        # Parâmetros de efeito
        self.raio = 60
        self.suavizacao = 30
        self.automatico = False
        self.x_auto, self.y_auto = 0, 0
        self.direcao_x = 5

        # --- Atributos de controle de animação ---
        # CORREÇÃO 1: Inicializa o atributo 'ultimo_tempo_troca' que causava o erro
        self.ultimo_tempo_troca = time.time()
        self.id_after_animacao = None
        self.id_after_ciclo = None

        # --- Carregamento inicial (apenas para obter o tamanho) ---
        # REATORAÇÃO: Carrega as imagens em memória primeiro para definir o tamanho da tela
        try:
            self.img_inferior_original = Image.open(self.lista_pares[self.indice_atual][0])
            self.img_superior_original = Image.open(self.lista_pares[self.indice_atual][1])
            self.size = self.img_inferior_original.size
            self.img_superior_original = self.img_superior_original.resize(
                self.size, Image.Resampling.LANCZOS
            )
        except Exception as e:
            print(f"⚠️ Erro fatal ao carregar imagens iniciais: {e}")
            self.master.destroy()
            return

        # --- Canvas principal ---
        # CORREÇÃO 2: O Canvas agora é criado ANTES de qualquer função que o utilize
        self.tela = tk.Canvas(master, width=self.size[0], height=self.size[1])
        self.tela.pack()
        
        # Centraliza a posição Y da animação automática para um efeito melhor
        self.y_auto = self.size[1] // 2

        self.tk_img_base = ImageTk.PhotoImage(self.img_inferior_original)
        self.img_canvas = self.tela.create_image(0, 0, anchor=tk.NW, image=self.tk_img_base)

        # --- Controles de interface ---
        frame_controle = ttk.Frame(master)
        frame_controle.pack(pady=10)

        ttk.Label(frame_controle, text="Tamanho da Revelação:").pack(side=tk.LEFT, padx=5)
        self.slider_raio = ttk.Scale(
            frame_controle, from_=10, to=200, orient="horizontal",
            command=self.atualizar_raio
        )
        self.slider_raio.set(self.raio)
        self.slider_raio.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_controle, text="Suavização:").pack(side=tk.LEFT, padx=5)
        self.slider_suave = ttk.Scale(
            frame_controle, from_=0, to=100, orient="horizontal",
            command=self.atualizar_suavizacao
        )
        self.slider_suave.set(self.suavizacao)
        self.slider_suave.pack(side=tk.LEFT, padx=5)

        self.botao_modo = ttk.Button(
            master, text="▶️ Ativar Modo Automático", command=self.toggle_automatico
        )
        self.botao_modo.pack(pady=8)

        self.tela.bind("<Motion>", self.movimento_mouse)

        print("✅ Sistema inicializado com sucesso!")
        print("Passe o mouse ou ative o modo automático para iniciar.")

    def carregar_imagens(self, par):
        """Carrega as imagens de um par (inferior, superior) e redimensiona"""
        inf, sup = par
        try:
            self.img_inferior_original = Image.open(inf)
            self.img_superior_original = Image.open(sup)

            # Garante que a imagem superior tenha o mesmo tamanho da inferior
            self.img_superior_original = self.img_superior_original.resize(
                self.img_inferior_original.size, Image.Resampling.LANCZOS
            )
            self.size = self.img_inferior_original.size
            
            # Atualiza o canvas com a nova imagem de base
            self.tk_img_base = ImageTk.PhotoImage(self.img_inferior_original)
            self.tela.itemconfig(self.img_canvas, image=self.tk_img_base)
            self.tela.config(width=self.size[0], height=self.size[1])

            print(f"🖼️ Par carregado: {inf} + {sup}")

        except FileNotFoundError:
            print(f"❌ Arquivos não encontrados: {inf}, {sup}")
        except Exception as e:
            print(f"⚠️ Erro ao carregar imagens: {e}")

    def atualizar_raio(self, valor):
        self.raio = int(float(valor))

    def atualizar_suavizacao(self, valor):
        self.suavizacao = int(float(valor))

    def toggle_automatico(self):
        self.automatico = not self.automatico
        if self.automatico:
            self.botao_modo.config(text="⏸️ Parar Modo Automático")
            self.animar()
            self.ciclo_troca_imagem() # REATORAÇÃO: Inicia o ciclo de troca de imagem
        else:
            self.botao_modo.config(text="▶️ Ativar Modo Automático")
            # REATORAÇÃO: Cancela os 'afters' para parar completamente a automação
            if self.id_after_animacao:
                self.master.after_cancel(self.id_after_animacao)
            if self.id_after_ciclo:
                self.master.after_cancel(self.id_after_ciclo)
            self.id_after_animacao = None
            self.id_after_ciclo = None


    def proximo_par(self):
        """Troca para o próximo par de imagens"""
        self.indice_atual = (self.indice_atual + 1) % len(self.lista_pares)
        novo_par = self.lista_pares[self.indice_atual]
        self.carregar_imagens(novo_par)
    
    # REATORAÇÃO: Lógica de troca de imagem movida para uma função dedicada
    def ciclo_troca_imagem(self):
        """Função que gerencia a troca periódica de imagens no modo automático."""
        if not self.automatico:
            return
        self.proximo_par()
        self.id_after_ciclo = self.master.after(self.duracao_ciclo_ms, self.ciclo_troca_imagem)

    def animar(self):
        """Movimento automático do efeito de revelação"""
        if not self.automatico:
            return

        # Movimento horizontal do círculo
        self.x_auto += self.direcao_x
        if self.x_auto > self.size[0] + self.raio or self.x_auto < -self.raio:
            self.direcao_x *= -1

        # Atualiza a imagem composta no modo automático
        self.atualizar_imagem(self.x_auto, self.y_auto)

        # REATORAÇÃO: Removida a lógica de troca de tempo daqui
        
        # Continua a animação
        self.id_after_animacao = self.master.after(30, self.animar)

    def movimento_mouse(self, evento):
        if not self.automatico:
            self.atualizar_imagem(evento.x, evento.y)

    def atualizar_imagem(self, x, y):
        r = self.raio
        mascara = Image.new("L", self.img_inferior_original.size, 0)
        draw = ImageDraw.Draw(mascara)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=255)

        if self.suavizacao > 0:
            mascara = mascara.filter(ImageFilter.GaussianBlur(self.suavizacao))

        imagem_composta = Image.composite(
            self.img_superior_original, self.img_inferior_original, mascara
        )

        self.tk_imagem_com_mascara = ImageTk.PhotoImage(imagem_composta)
        self.tela.itemconfig(self.img_canvas, image=self.tk_imagem_com_mascara)


# --- Execução principal ---
if __name__ == "__main__":
    root = tk.Tk()

    # 🔹 Adicione aqui os pares de imagens (inferior, superior)
    # Certifique-se que estas imagens existem na mesma pasta do script
    pares = [
        ("imagem1_inferior.jpg", "imagem1_superior.jpg"),
        ("imagem2_inferior.jpg", "imagem2_superior.jpg"),
        ("imagem3_inferior.jpg", "imagem3_superior.jpg"),
        ("imagem4_inferior.jpg", "imagem4_superior.jpg")
    ]

    # Verifica se os diretórios e arquivos existem antes de iniciar
    if not all(os.path.exists(p[0]) and os.path.exists(p[1]) for p in pares):
        print("❌ ERRO: Uma ou mais imagens não foram encontradas. Verifique os nomes e os caminhos dos arquivos.")
    else:
        app = AplicacaoEfeitoRevelacaoDinamica(root, pares, duracao_ciclo=6)
        root.mainloop()