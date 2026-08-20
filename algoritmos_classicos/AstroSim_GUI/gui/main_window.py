import ttkbootstrap as tb
from ttkbootstrap.constants import LEFT, RIGHT, TOP, BOTTOM  # Exemplo, ajuste conforme necessário
from gui.mission_planner_gui import MissionPlannerGUI
from gui.inventory_gui import InventoryGUI
from gui.data_transmission_gui import DataTransmissionGUI
from gui.space_map_gui import SpaceMapGUI
from gui.resource_manager_gui import ResourceManagerGUI


class MainWindow(tb.Window):
    
    """Classe que representa a janela principal da aplicação AstroSim."""
    def __init__(self):
        super().__init__(themename="superhero")  # Aplica o tema direto aqui
        self.title("AstroSim - Simulador de Missões Espaciais") # Título da janela
        self.geometry("1324x1324") # Tamanho inicial da janela

        self.create_widgets() # Cria os widgets da janela principal

    def create_widgets(self): # Método para criar os widgets da janela principal
        menu = tb.Notebook(self, bootstyle="primary") # Cria um notebook para organizar as abas em estilo primary(azul)
        menu.pack(fill="both", expand=True, padx=10, pady=10) # Preenche o notebook com as abas

        menu.add(MissionPlannerGUI(menu), text="Planejamento de Missão") # Adiciona a aba de planejamento de missão
        menu.add(InventoryGUI(menu), text="Inventário de Componentes") # Adiciona a aba de inventário de componentes
        menu.add(DataTransmissionGUI(menu), text="Transmissão de Dados") # Adiciona a aba de transmissão de dados
        menu.add(SpaceMapGUI(menu), text="Mapa Espacial") # Adiciona a aba de mapa espacial
        menu.add(ResourceManagerGUI(menu), text="Gerenciamento de Recursos") # Adiciona a aba de gerenciamento de recurso
