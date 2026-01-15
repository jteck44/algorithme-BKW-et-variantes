# main.py - Version améliorée avec interface responsive
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import numpy as np
from core.lpn import LPNInstance
from core.lwe import LWEInstance
from weapons.bkw_standard import BKWStandard
from weapons.bkw_lf1 import BKWLF1
from weapons.bkw_lwe import BKWLWE
from weapons.lms_bkw import LMSBKW
from weapons.coded_bkw import CodedBKW
from weapons.coded_bkw_sieving import CodedBKWSieving

class MissionBKW:
    def __init__(self, root):
        self.root = root
        self.root.title("🕵️ MISSION BKW - Laboratoire d'Algorithmes Cryptographiques")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0f172a')
        self.root.minsize(1200, 700)
        
        # Variables de style améliorées
        self.colors = {
            'bg_dark': '#0f172a',
            'bg_darker': '#020617',
            'bg_medium': '#1e293b',
            'bg_light': '#334155',
            'accent_blue': '#3b82f6',
            'accent_green': '#10b981',
            'accent_yellow': '#f59e0b',
            'accent_red': '#ef4444',
            'accent_purple': '#8b5cf6',
            'accent_pink': '#ec4899',
            'accent_cyan': '#06b6d4',
            'text_primary': '#f1f5f9',
            'text_secondary': '#94a3b8',
            'text_muted': '#64748b',
            'border': '#475569',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'info': '#3b82f6'
        }
        
        # Polices modernes
        self.fonts = {
            'h1': ('Segoe UI', 36, 'bold'),
            'h2': ('Segoe UI', 24, 'bold'),
            'h3': ('Segoe UI', 20, 'bold'),
            'h4': ('Segoe UI', 16, 'bold'),
            'body': ('Segoe UI', 12),
            'small': ('Segoe UI', 10),
            'mono': ('Consolas', 11),
            'mono_bold': ('Consolas', 11, 'bold')
        }
        
        # État de l'application
        self.current_screen = 'menu'
        self.selected_mission = None
        self.selected_weapon = None
        self.user_secret = None
        self.user_params = None
        
        # Configuration du style
        self.setup_styles()
        
        # Initialiser l'interface
        self.show_menu()
        
        # Bind pour le redimensionnement
        self.root.bind('<Configure>', self.on_resize)
    
    def setup_styles(self):
        """Configure les styles Tkinter"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configuration de la barre de progression
        self.style.configure("Custom.Horizontal.TProgressbar",
                           troughcolor=self.colors['bg_medium'],
                           background=self.colors['accent_blue'],
                           bordercolor=self.colors['border'],
                           lightcolor=self.colors['accent_blue'],
                           darkcolor=self.colors['accent_blue'])
    
    def on_resize(self, event):
        """Gère le redimensionnement de la fenêtre"""
        if hasattr(self, 'current_screen'):
            if self.current_screen == 'execution' and hasattr(self, 'log_text'):
                self.log_text.config(width=int(event.width/12))
    
    def clear_screen(self):
        """Efface tous les widgets de l'écran"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_modern_card(self, parent, title, description, icon, color, command=None, width=None, height=160):
        """Crée une carte moderne avec effets"""
        card = tk.Frame(parent,
                       bg=self.colors['bg_medium'],
                       highlightbackground=self.colors['border'],
                       highlightthickness=1,
                       width=width,
                       height=height)
        card.pack_propagate(False)
        
        # Gradient de couleur en haut
        header = tk.Frame(card, bg=color, height=4)
        header.pack(fill='x')
        
        # Contenu
        content = tk.Frame(card, bg=self.colors['bg_medium'])
        content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Ligne supérieure avec icône et titre
        top_frame = tk.Frame(content, bg=self.colors['bg_medium'])
        top_frame.pack(fill='x', pady=(0, 10))
        
        # Icône
        icon_label = tk.Label(top_frame, text=icon, bg=self.colors['bg_medium'],
                             fg=color, font=('Arial', 24))
        icon_label.pack(side='left', padx=(0, 12))
        
        # Titre
        title_label = tk.Label(top_frame, text=title, bg=self.colors['bg_medium'],
                              fg=self.colors['text_primary'], font=self.fonts['h4'],
                              anchor='w')
        title_label.pack(side='left', fill='x', expand=True)
        
        # Description
        desc_label = tk.Label(content, text=description, bg=self.colors['bg_medium'],
                             fg=self.colors['text_secondary'], font=self.fonts['small'],
                             wraplength=width-40 if width else 280, justify='left',
                             anchor='w')
        desc_label.pack(fill='x', pady=(0, 15))
        
        # Bouton
        if command:
            btn = tk.Button(content, text="SÉLECTIONNER", 
                          bg=color, fg='white',
                          font=('Segoe UI', 10, 'bold'),
                          relief='flat',
                          padx=20, pady=8,
                          cursor='hand2',
                          command=command)
            btn.pack()
            
            # Effet de survol
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.config(bg=self.lighten_color(c, 20)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.config(bg=c))
        
        return card
    
    def lighten_color(self, hex_color, amount=30):
        """Éclaircit une couleur hexadécimale"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, c + amount) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def show_menu(self):
        """Affiche l'écran principal du menu"""
        self.clear_screen()
        self.current_screen = 'menu'
        
        # Container principal avec padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill='both', expand=True, padx=60, pady=40)
        
        # Header avec effet gradient
        header_frame = tk.Frame(main_container, bg=self.colors['bg_darker'], height=120)
        header_frame.pack(fill='x', pady=(0, 40))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=self.colors['bg_darker'])
        header_content.pack(expand=True)
        
        # Titre principal
        title_frame = tk.Frame(header_content, bg=self.colors['bg_darker'])
        title_frame.pack()
        
        tk.Label(title_frame, text="🕵️", 
                bg=self.colors['bg_darker'], fg=self.colors['accent_cyan'],
                font=('Arial', 48)).pack(side='left', padx=(0, 15))
        
        title_text = tk.Frame(title_frame, bg=self.colors['bg_darker'])
        title_text.pack(side='left')
        
        tk.Label(title_text, text="MISSION BKW", 
                bg=self.colors['bg_darker'], fg=self.colors['text_primary'],
                font=self.fonts['h1']).pack(anchor='w')
        
        tk.Label(title_text, text="Laboratoire d'Algorithmes Cryptographiques", 
                bg=self.colors['bg_darker'], fg=self.colors['accent_cyan'],
                font=self.fonts['h3']).pack(anchor='w')
        
        # Sous-titre
        tk.Label(header_content, 
                text="Explorez les algorithmes BKW pour résoudre LPN et LWE",
                bg=self.colors['bg_darker'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).pack(pady=(10, 0))
        
        # Contenu principal avec Notebook pour les onglets
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill='both', expand=True)
        
        # Onglet 1: Missions prédéfinies
        missions_tab = tk.Frame(notebook, bg=self.colors['bg_dark'])
        notebook.add(missions_tab, text='🎯 Missions Prédéfinies')
        
        # Cadre scrollable pour les missions
        missions_canvas = tk.Canvas(missions_tab, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(missions_tab, orient="vertical", command=missions_canvas.yview)
        scrollable_frame = tk.Frame(missions_canvas, bg=self.colors['bg_dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: missions_canvas.configure(scrollregion=missions_canvas.bbox("all"))
        )
        
        missions_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        missions_canvas.configure(yscrollcommand=scrollbar.set)
        
        missions_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Missions prédéfinies
        missions = [
            {
                'name': 'Formation - Initiation',
                'desc': 'Parfait pour comprendre les bases du problème LPN\nSecret 8 bits avec bruit faible\nComplexité réduite pour apprentissage',
                'icon': '📚',
                'color': self.colors['accent_green'],
                'params': {'k': 8, 'tau': 0.1, 'a': 2, 'b': 4, 'type': 'LPN'}
            },
            {
                'name': 'Opération Standard',
                'desc': 'Scénario réaliste avec complexité modérée\nSecret 12 bits avec bruit moyen\nTest des algorithmes classiques',
                'icon': '🎯',
                'color': self.colors['accent_blue'],
                'params': {'k': 12, 'tau': 0.15, 'a': 3, 'b': 4, 'type': 'LPN'}
            },
            {
                'name': 'Mission LWE Avancée',
                'desc': 'Problème LWE avec modulus cryptographique\nSecret dimension 8, modulus 31\nDéfi cryptographique moderne',
                'icon': '🔐',
                'color': self.colors['accent_yellow'],
                'params': {'n': 8, 'q': 31, 'sigma': 1.5, 'a': 2, 'b': 4, 'type': 'LWE'}
            },
            {
                'name': 'Défi Expert',
                'desc': 'Test des limites des algorithmes BKW\nSecret 16 bits avec bruit élevé\nPerformance et précision maximale',
                'icon': '💀',
                'color': self.colors['accent_red'],
                'params': {'k': 16, 'tau': 0.2, 'a': 4, 'b': 4, 'type': 'LPN'}
            },
            {
                'name': 'Cryptanalyse LWE Moderne',
                'desc': 'Problème LWE dimension 12\nModulus 31 avec bruit contrôlé\nTest des variantes avancées',
                'icon': '⚡',
                'color': self.colors['accent_purple'],
                'params': {'n': 12, 'q': 31, 'sigma': 1.2, 'a': 3, 'b': 4, 'type': 'LWE'}
            }
        ]
        
        # Grille de missions 2x3
        for i, mission in enumerate(missions):
            row = i // 3
            col = i % 3
            
            frame = tk.Frame(scrollable_frame, bg=self.colors['bg_dark'])
            frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            card = self.create_modern_card(
                frame,
                mission['name'],
                mission['desc'],
                mission['icon'],
                mission['color'],
                command=lambda m=mission: self.select_mission(m),
                width=350,
                height=200
            )
            card.pack(fill='both', expand=True)
            
            # Configuration de la grille
            scrollable_frame.grid_columnconfigure(col, weight=1, uniform='missions')
            scrollable_frame.grid_rowconfigure(row, weight=1)
        
        # Onglet 2: Configuration personnalisée
        config_tab = tk.Frame(notebook, bg=self.colors['bg_dark'])
        notebook.add(config_tab, text='⚙️ Configuration')
        
        config_container = tk.Frame(config_tab, bg=self.colors['bg_dark'])
        config_container.pack(fill='both', expand=True, padx=40, pady=40)
        
        tk.Label(config_container, text="CONFIGURATION PERSONNALISÉE", 
                bg=self.colors['bg_dark'], fg=self.colors['accent_cyan'],
                font=self.fonts['h2']).pack(pady=(0, 30))
        
        # Options de configuration
        config_options = [
            {
                'title': 'Mission Paramétrée',
                'desc': 'Configurez tous les paramètres\ntaille, bruit, type de problème...',
                'icon': '🔧',
                'color': self.colors['accent_purple'],
                'command': self.show_custom_config
            },
            {
                'title': 'Définir Mon Secret',
                'desc': 'Choisissez exactement le secret\nque vous voulez retrouver',
                'icon': '🔑',
                'color': self.colors['accent_yellow'],
                'command': self.show_secret_config
            },
            {
                'title': 'Guide des Algorithmes',
                'desc': 'Apprenez-en plus sur les\nalgorithmes disponibles',
                'icon': '📖',
                'color': self.colors['accent_cyan'],
                'command': self.show_algorithms_guide
            }
        ]
        
        config_grid = tk.Frame(config_container, bg=self.colors['bg_dark'])
        config_grid.pack(fill='both', expand=True)
        
        for i, option in enumerate(config_options):
            frame = tk.Frame(config_grid, bg=self.colors['bg_dark'])
            frame.grid(row=i//2, column=i%2, padx=15, pady=15, sticky='nsew')
            
            card = self.create_modern_card(
                frame,
                option['title'],
                option['desc'],
                option['icon'],
                option['color'],
                command=option['command'],
                width=350,
                height=180
            )
            card.pack(fill='both', expand=True)
            
            config_grid.grid_columnconfigure(i%2, weight=1, uniform='config')
            config_grid.grid_rowconfigure(i//2, weight=1)
        
        # Information en bas
        info_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        info_frame.pack(fill='x', pady=(20, 0))
        
        tk.Label(info_frame, 
                text="🛈 Sélectionnez une mission ou créez votre propre configuration",
                bg=self.colors['bg_dark'], fg=self.colors['text_muted'],
                font=self.fonts['small']).pack()
        
        # Footer
        footer = tk.Frame(main_container, bg=self.colors['bg_darker'], height=40)
        footer.pack(fill='x', side='bottom', pady=(20, 0))
        footer.pack_propagate(False)
        
        tk.Label(footer, text="Laboratoire BKW © 2024 | Démonstration Pédagogique", 
                bg=self.colors['bg_darker'], fg=self.colors['text_muted'],
                font=self.fonts['small']).pack(pady=10)
    
    def show_algorithms_guide(self):
        """Affiche le guide des algorithmes"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Guide des Algorithmes")
        dialog.geometry("800x600")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        tk.Label(main_frame, text="📖 GUIDE DES ALGORITHMES", 
                bg=self.colors['bg_dark'], fg=self.colors['accent_cyan'],
                font=self.fonts['h2']).pack(pady=(0, 20))
        
        # Contenu avec scroll
        canvas = tk.Canvas(main_frame, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        content_frame = tk.Frame(canvas, bg=self.colors['bg_dark'])
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Informations sur les algorithmes
        algorithms = [
            {
                'name': 'BKW Standard',
                'type': 'LPN uniquement',
                'color': '#3b82f6',
                'desc': 'Algorithme classique pour LPN. Utilise la réduction par blocs et le vote majoritaire.',
                'usage': 'Idéal pour comprendre les bases de BKW.'
            },
            {
                'name': 'LF1 (Walsh-Hadamard)',
                'type': 'LPN uniquement',
                'color': '#8b5cf6',
                'desc': 'Utilise la transformée de Walsh-Hadamard pour une résolution plus efficace.',
                'usage': 'Meilleure performance que BKW standard pour LPN.'
            },
            {
                'name': 'BKW-LWE',
                'type': 'LWE uniquement',
                'color': '#10b981',
                'desc': 'Adaptation de BKW pour LWE avec vraisemblance gaussienne.',
                'usage': 'Pour les problèmes LWE avec modulus modéré.'
            },
            {
                'name': 'LMS-BKW',
                'type': 'LWE uniquement',
                'color': '#f59e0b',
                'desc': 'Utilise la réduction de modulus pour traiter de grands q.',
                'usage': 'Efficace pour LWE avec grands modulus.'
            },
            {
                'name': 'CODED-BKW',
                'type': 'LWE uniquement',
                'color': '#ef4444',
                'desc': 'Intègre des codes linéaires pour accélérer la réduction.',
                'usage': 'Performance améliorée pour LWE complexe.'
            },
            {
                'name': 'CODED-BKW + Sieving',
                'type': 'LWE uniquement',
                'color': '#6366f1',
                'desc': 'Combine codes linéaires avec tamisage pour le contrôle du bruit.',
                'usage': 'État de l\'art pour LWE difficile.'
            }
        ]
        
        for i, algo in enumerate(algorithms):
            frame = tk.Frame(content_frame, bg=self.colors['bg_medium'],
                            highlightbackground=self.colors['border'],
                            highlightthickness=1)
            frame.pack(fill='x', pady=10, padx=10)
            
            # En-tête
            header = tk.Frame(frame, bg=algo['color'], height=30)
            header.pack(fill='x')
            
            tk.Label(header, text=algo['name'], bg=algo['color'],
                    fg='white', font=self.fonts['h4']).pack(side='left', padx=10)
            
            tk.Label(header, text=algo['type'], bg=algo['color'],
                    fg='white', font=self.fonts['small']).pack(side='right', padx=10)
            
            # Contenu
            content = tk.Frame(frame, bg=self.colors['bg_medium'])
            content.pack(fill='x', padx=15, pady=15)
            
            tk.Label(content, text=algo['desc'], bg=self.colors['bg_medium'],
                    fg=self.colors['text_primary'], font=self.fonts['body'],
                    wraplength=700, justify='left').pack(anchor='w', pady=(0, 5))
            
            tk.Label(content, text=f"Usage: {algo['usage']}", bg=self.colors['bg_medium'],
                    fg=self.colors['text_secondary'], font=self.fonts['small'],
                    wraplength=700, justify='left').pack(anchor='w')
        
        # Bouton fermer
        tk.Button(main_frame, text="Fermer", bg=self.colors['accent_blue'], fg='white',
                 font=self.fonts['body'], padx=30, pady=10,
                 command=dialog.destroy).pack(pady=20)
    
    def show_custom_config(self):
        """Affiche la configuration personnalisée"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Configuration Avancée")
        dialog.geometry("600x700")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        tk.Label(main_frame, text="⚙️ CONFIGURATION AVANCÉE", 
                bg=self.colors['bg_dark'], fg=self.colors['accent_cyan'],
                font=self.fonts['h2']).pack(pady=(0, 30))
        
        # Formulaire dans un cadre
        form_frame = tk.Frame(main_frame, bg=self.colors['bg_medium'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        form_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Type de problème
        type_section = tk.Frame(form_frame, bg=self.colors['bg_medium'])
        type_section.pack(fill='x', padx=20, pady=20)
        
        tk.Label(type_section, text="Type de problème:", 
                bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                font=self.fonts['h4']).pack(anchor='w', pady=(0, 15))
        
        self.problem_type = tk.StringVar(value="LPN")
        
        type_options = tk.Frame(type_section, bg=self.colors['bg_medium'])
        type_options.pack(fill='x')
        
        # Option LPN
        lpn_frame = tk.Frame(type_options, bg=self.colors['bg_light'])
        lpn_frame.pack(fill='x', pady=5)
        
        tk.Radiobutton(lpn_frame, text="", variable=self.problem_type, value="LPN",
                      bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['accent_green']).pack(side='left', padx=10)
        
        tk.Label(lpn_frame, text="LPN (Learning Parity with Noise)", 
                bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(side='left', fill='x', expand=True)
        
        tk.Label(lpn_frame, text="Problème binaire avec bruit de Bernoulli", 
                bg=self.colors['bg_light'], fg=self.colors['text_secondary'],
                font=self.fonts['small']).pack(side='left', padx=20)
        
        # Option LWE
        lwe_frame = tk.Frame(type_options, bg=self.colors['bg_light'])
        lwe_frame.pack(fill='x', pady=5)
        
        tk.Radiobutton(lwe_frame, text="", variable=self.problem_type, value="LWE",
                      bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['accent_blue']).pack(side='left', padx=10)
        
        tk.Label(lwe_frame, text="LWE (Learning With Errors)", 
                bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(side='left', fill='x', expand=True)
        
        tk.Label(lwe_frame, text="Problème modulaire avec bruit gaussien", 
                bg=self.colors['bg_light'], fg=self.colors['text_secondary'],
                font=self.fonts['small']).pack(side='left', padx=20)
        
        # Paramètres
        params_section = tk.Frame(form_frame, bg=self.colors['bg_medium'])
        params_section.pack(fill='x', padx=20, pady=20)
        
        tk.Label(params_section, text="Paramètres:", 
                bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                font=self.fonts['h4']).pack(anchor='w', pady=(0, 15))
        
        # Grille de paramètres
        param_grid = tk.Frame(params_section, bg=self.colors['bg_medium'])
        param_grid.pack(fill='x')
        
        # Dimension
        tk.Label(param_grid, text="Dimension:", 
                bg=self.colors['bg_medium'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).grid(row=0, column=0, sticky='w', pady=10, padx=(0, 20))
        
        self.dim_var = tk.StringVar(value="12")
        dim_entry = tk.Entry(param_grid, textvariable=self.dim_var,
                           bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                           font=self.fonts['body'], width=15)
        dim_entry.grid(row=0, column=1, sticky='w', pady=10)
        
        # Bruit
        tk.Label(param_grid, text="Niveau de bruit:", 
                bg=self.colors['bg_medium'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).grid(row=1, column=0, sticky='w', pady=10, padx=(0, 20))
        
        self.noise_var = tk.StringVar(value="0.15")
        noise_entry = tk.Entry(param_grid, textvariable=self.noise_var,
                             bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                             font=self.fonts['body'], width=15)
        noise_entry.grid(row=1, column=1, sticky='w', pady=10)
        
        # Blocs
        tk.Label(param_grid, text="Structure des blocs:", 
                bg=self.colors['bg_medium'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).grid(row=2, column=0, sticky='w', pady=10, padx=(0, 20))
        
        blocs_frame = tk.Frame(param_grid, bg=self.colors['bg_medium'])
        blocs_frame.grid(row=2, column=1, sticky='w', pady=10)
        
        self.a_var = tk.StringVar(value="3")
        tk.Entry(blocs_frame, textvariable=self.a_var, width=5,
                bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(side='left')
        
        tk.Label(blocs_frame, text=" × ", bg=self.colors['bg_medium'],
                fg=self.colors['text_secondary']).pack(side='left', padx=5)
        
        self.b_var = tk.StringVar(value="4")
        tk.Entry(blocs_frame, textvariable=self.b_var, width=5,
                bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(side='left')
        
        param_grid.columnconfigure(1, weight=1)
        
        # Boutons
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        btn_frame.pack(fill='x', pady=(20, 0))
        
        tk.Button(btn_frame, text="❌ Annuler", bg=self.colors['accent_red'], fg='white',
                 font=self.fonts['body'], padx=25, pady=10,
                 command=dialog.destroy).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="✅ Valider", bg=self.colors['accent_green'], fg='white',
                 font=('Segoe UI', 11, 'bold'), padx=25, pady=10,
                 command=lambda: self.validate_custom_config(dialog)).pack(side='left')
    
    def show_secret_config(self):
        """Affiche la configuration du secret personnalisé"""
        # Même structure que show_custom_config mais adaptée pour les secrets
        dialog = tk.Toplevel(self.root)
        dialog.title("Définir Votre Secret")
        dialog.geometry("500x600")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        tk.Label(main_frame, text="🔑 DÉFINIR VOTRE SECRET", 
                bg=self.colors['bg_dark'], fg=self.colors['accent_yellow'],
                font=self.fonts['h2']).pack(pady=(0, 20))
        
        # Le reste du code reste similaire à votre version existante...
        # (Je garde la logique existante pour économiser de l'espace)
        
        # Type
        tk.Label(main_frame, text="Type de secret:", 
                bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                font=self.fonts['h4']).pack(anchor='w', pady=(20, 10))
        
        self.secret_type = tk.StringVar(value="LPN")
        
        tk.Radiobutton(main_frame, text="LPN - Binaire (ex: 10101101)", 
                      variable=self.secret_type, value="LPN",
                      bg=self.colors['bg_dark'], fg=self.colors['text_primary']).pack(anchor='w', padx=20, pady=5)
        
        tk.Radiobutton(main_frame, text="LWE - Modulaire (ex: 3,5,2,7)", 
                      variable=self.secret_type, value="LWE",
                      bg=self.colors['bg_dark'], fg=self.colors['text_primary']).pack(anchor='w', padx=20, pady=5)
        
        # Taille
        tk.Label(main_frame, text="Taille du secret:", 
                bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(anchor='w', pady=(20, 5))
        
        self.secret_size = tk.StringVar(value="8")
        tk.Entry(main_frame, textvariable=self.secret_size,
                bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(fill='x', pady=5, padx=20)
        
        # Secret
        tk.Label(main_frame, text="Votre secret:", 
                bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(anchor='w', pady=(20, 5))
        
        self.secret_value = tk.StringVar()
        tk.Entry(main_frame, textvariable=self.secret_value,
                bg=self.colors['bg_light'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(fill='x', pady=5, padx=20)
        
        tk.Label(main_frame, text="Format: Pour LPN: '10101101', Pour LWE: '3,5,2,7'", 
                bg=self.colors['bg_dark'], fg=self.colors['text_secondary'],
                font=self.fonts['small']).pack(anchor='w', padx=20, pady=5)
        
        # Boutons
        btn_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        btn_frame.pack(fill='x', pady=30)
        
        tk.Button(btn_frame, text="🎲 Générer Aléatoire", bg=self.colors['accent_blue'], fg='white',
                 font=self.fonts['body'], padx=20, pady=8,
                 command=self.generate_random_secret).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="❌ Annuler", bg=self.colors['accent_red'], fg='white',
                 font=self.fonts['body'], padx=25, pady=8,
                 command=dialog.destroy).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="✅ Valider", bg=self.colors['accent_green'], fg='white',
                 font=('Segoe UI', 11, 'bold'), padx=25, pady=8,
                 command=lambda: self.validate_secret_config(dialog)).pack(side='left')
    
    def generate_random_secret(self):
        """Génère un secret aléatoire"""
        try:
            size = int(self.secret_size.get())
            if self.secret_type.get() == "LPN":
                secret = ''.join(str(np.random.randint(0, 2)) for _ in range(size))
            else:
                secret = ','.join(str(np.random.randint(0, 31)) for _ in range(size))
            self.secret_value.set(secret)
        except:
            messagebox.showerror("Erreur", "Taille invalide")
    
    def validate_secret_config(self, dialog):
        """Valide la configuration du secret"""
        try:
            size = int(self.secret_size.get())
            secret_str = self.secret_value.get().strip()
            secret_type = self.secret_type.get()
            
            if secret_str:
                if secret_type == "LPN":
                    if len(secret_str) != size:
                        messagebox.showerror("Erreur", f"Le secret doit avoir {size} bits. Vous avez {len(secret_str)} caractères.")
                        return
                    if not all(c in '01' for c in secret_str):
                        messagebox.showerror("Erreur", "Le secret LPN doit contenir uniquement des 0 et des 1")
                        return
                    self.user_secret = [int(bit) for bit in secret_str]
                else:  # LWE
                    try:
                        # Séparer par virgules ou espaces
                        if ',' in secret_str:
                            parts = secret_str.split(',')
                        else:
                            parts = secret_str.split()
                        
                        self.user_secret = [int(x.strip()) for x in parts if x.strip()]
                        
                        if len(self.user_secret) != size:
                            messagebox.showerror("Erreur", 
                                f"Le secret doit avoir {size} valeurs. Vous avez {len(self.user_secret)} valeurs.")
                            return
                        
                        # Modulus par défaut = 31
                        if not all(0 <= x < 31 for x in self.user_secret):
                            messagebox.showerror("Erreur", 
                                f"Les valeurs doivent être entre 0 et 30 (modulus 31)")
                            return
                            
                    except ValueError:
                        messagebox.showerror("Erreur", 
                            "Format invalide pour LWE. Utilisez: '3,5,2,7' ou '3 5 2 7'")
                        return
            else:
                messagebox.showerror("Erreur", "Veuillez entrer un secret")
                return
            
            # Paramètres par défaut
            if secret_type == "LPN":
                self.user_params = {
                    'type': 'LPN',
                    'k': size,
                    'tau': 0.15,
                    'a': 3,
                    'b': 4
                }
                mission_name = f"Personnalisé: Secret LPN {size} bits"
            else:
                self.user_params = {
                    'type': 'LWE',
                    'n': size,
                    'q': 31,
                    'sigma': 1.5,
                    'a': 3,
                    'b': 4
                }
                mission_name = f"Personnalisé: Secret LWE {size} valeurs"
            
            self.selected_mission = {
                'name': mission_name,
                'desc': f"Secret défini manuellement",
                'params': self.user_params,
                'difficulty': 'Personnalisé',
                'color': self.colors['accent_purple']
            }
            
            dialog.destroy()
            self.show_weapons()
            
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides")
    
    def validate_custom_config(self, dialog):
        """Valide la configuration personnalisée"""
        try:
            dim = int(self.dim_var.get())
            noise = float(self.noise_var.get())
            a = int(self.a_var.get())
            b = int(self.b_var.get())
            
            if self.problem_type.get() == "LPN":
                params = {
                    'type': 'LPN',
                    'k': dim,
                    'tau': noise,
                    'a': a,
                    'b': b
                }
                mission_name = f"Personnalisé LPN: {dim} bits, τ={noise}"
            else:
                params = {
                    'type': 'LWE',
                    'n': dim,
                    'q': 31,
                    'sigma': noise,
                    'a': a,
                    'b': b
                }
                mission_name = f"Personnalisé LWE: n={dim}, σ={noise}"
            
            self.user_params = params
            self.selected_mission = {
                'name': mission_name,
                'desc': f"Configuration personnalisée",
                'params': params,
                'difficulty': 'Personnalisé',
                'color': self.colors['accent_purple']
            }
            
            dialog.destroy()
            self.show_weapons()
            
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides")
    
    def select_mission(self, mission):
        """Sélectionne une mission"""
        self.selected_mission = mission
        self.show_weapons()
    
    def show_weapons(self):
        """Affiche la sélection des algorithmes avec compatibilité"""
        self.clear_screen()
        self.current_screen = 'weapons'
        
        # Container principal avec sidebar
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.colors['bg_dark'])
        main_container.pack(fill='both', expand=True)
        
        # Sidebar (30% de largeur)
        sidebar = tk.Frame(main_container, bg=self.colors['bg_darker'], width=350)
        main_container.add(sidebar)
        
        # Contenu principal (70% de largeur)
        content = tk.Frame(main_container, bg=self.colors['bg_dark'])
        main_container.add(content)
        
        # Contenu de la sidebar
        sidebar_content = tk.Frame(sidebar, bg=self.colors['bg_darker'])
        sidebar_content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Bouton retour
        back_btn = tk.Button(sidebar_content, text="← Retour au Menu", 
                           bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                           font=self.fonts['body'], relief='flat',
                           padx=15, pady=8, cursor='hand2',
                           command=self.show_menu)
        back_btn.pack(anchor='w', pady=(0, 30))
        
        # Titre sidebar
        tk.Label(sidebar_content, text="📋 BRIEFING", 
                bg=self.colors['bg_darker'], fg=self.colors['accent_cyan'],
                font=self.fonts['h2']).pack(anchor='w', pady=(0, 20))
        
        # Mission info
        mission_frame = tk.Frame(sidebar_content, bg=self.colors['bg_medium'],
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        mission_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(mission_frame, text=self.selected_mission['name'], 
                bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                font=self.fonts['h3']).pack(anchor='w', padx=15, pady=(15, 5))
        
        tk.Label(mission_frame, text=self.selected_mission['desc'], 
                bg=self.colors['bg_medium'], fg=self.colors['text_secondary'],
                font=self.fonts['small'], wraplength=280, justify='left').pack(anchor='w', padx=15, pady=(0, 15))
        
        # Paramètres détaillés
        params = self.selected_mission['params']
        
        param_frame = tk.Frame(sidebar_content, bg=self.colors['bg_darker'])
        param_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(param_frame, text="🔧 PARAMÈTRES", 
                bg=self.colors['bg_darker'], fg=self.colors['text_primary'],
                font=self.fonts['h4']).pack(anchor='w', pady=(0, 15))
        
        if params['type'] == 'LPN':
            param_details = [
                ("Type", "LPN", self.colors['accent_green']),
                ("Dimension", f"{params['k']} bits", self.colors['info']),
                ("Bruit", f"τ = {params['tau']}", self.colors['warning']),
                ("Structure", f"{params['a']} × {params['b']} blocs", self.colors['accent_purple'])
            ]
        else:
            param_details = [
                ("Type", "LWE", self.colors['accent_yellow']),
                ("Dimension", f"n = {params['n']}", self.colors['info']),
                ("Modulus", f"q = {params['q']}", self.colors['accent_blue']),
                ("Bruit", f"σ = {params['sigma']:.2f}", self.colors['warning']),
                ("Structure", f"{params['a']} × {params['b']} blocs", self.colors['accent_purple'])
            ]
        
        for label, value, color in param_details:
            detail_frame = tk.Frame(param_frame, bg=self.colors['bg_darker'])
            detail_frame.pack(fill='x', pady=5)
            
            tk.Label(detail_frame, text=label, 
                    bg=self.colors['bg_darker'], fg=self.colors['text_secondary'],
                    font=self.fonts['small'], width=10, anchor='w').pack(side='left')
            
            tk.Label(detail_frame, text=value, 
                    bg=self.colors['bg_darker'], fg=color,
                    font=self.fonts['body']).pack(side='left', padx=10)
        
        # Légende de compatibilité
        legend_frame = tk.Frame(sidebar_content, bg=self.colors['bg_darker'])
        legend_frame.pack(fill='x', pady=(20, 0))
        
        tk.Label(legend_frame, text="🎯 COMPATIBILITÉ", 
                bg=self.colors['bg_darker'], fg=self.colors['text_primary'],
                font=self.fonts['h4']).pack(anchor='w', pady=(0, 10))
        
        is_lwe = params['type'] == 'LWE'
        compat_text = "🟢 Algorithmes compatibles:"
        tk.Label(legend_frame, text=compat_text, 
                bg=self.colors['bg_darker'], fg=self.colors['text_secondary'],
                font=self.fonts['small']).pack(anchor='w')
        
        if is_lwe:
            compat_list = "• BKW-LWE\n• LMS-BKW\n• CODED-BKW\n• CODED-BKW + Sieving"
        else:
            compat_list = "• BKW Standard\n• LF1 (Walsh-Hadamard)"
        
        tk.Label(legend_frame, text=compat_list, 
                bg=self.colors['bg_darker'], fg=self.colors['text_primary'],
                font=self.fonts['small'], justify='left').pack(anchor='w', pady=5)
        
        # Contenu principal
        content_header = tk.Frame(content, bg=self.colors['bg_dark'])
        content_header.pack(fill='x', padx=40, pady=40)
        
        tk.Label(content_header, text="🔫 SÉLECTION DE L'ALGORITHME", 
                bg=self.colors['bg_dark'], fg=self.colors['accent_cyan'],
                font=self.fonts['h2']).pack(anchor='w')
        
        tk.Label(content_header, text="Choisissez l'algorithme adapté à votre mission", 
                bg=self.colors['bg_dark'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).pack(anchor='w', pady=(5, 0))
        
        # Grille des algorithmes avec canvas scrollable
        algo_canvas = tk.Canvas(content, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=algo_canvas.yview)
        algo_frame = tk.Frame(algo_canvas, bg=self.colors['bg_dark'])
        
        algo_frame.bind(
            "<Configure>",
            lambda e: algo_canvas.configure(scrollregion=algo_canvas.bbox("all"))
        )
        
        algo_canvas.create_window((0, 0), window=algo_frame, anchor="nw")
        algo_canvas.configure(yscrollcommand=scrollbar.set)
        
        algo_canvas.pack(side="left", fill="both", expand=True, padx=(40, 0), pady=(0, 40))
        scrollbar.pack(side="right", fill="y", padx=(0, 40), pady=(0, 40))
        
        # Définir les algorithmes avec compatibilité
        weapons = [
            {
                'name': 'BKW Standard',
                'desc': 'Algorithme classique pour LPN\nRéduction par blocs + vote majoritaire',
                'icon': '🛡️',
                'color': '#3b82f6',
                'lwe_only': False,
                'lpn_only': True
            },
            {
                'name': 'LF1 (Walsh-Hadamard)',
                'desc': 'Transformée de Walsh-Hadamard\nPlus efficace que BKW standard pour LPN',
                'icon': '⚡',
                'color': '#8b5cf6',
                'lwe_only': False,
                'lpn_only': True
            },
            {
                'name': 'BKW-LWE',
                'desc': 'Adaptation pour LWE\nVraisemblance gaussienne + réduction modulus',
                'icon': '🔐',
                'color': '#10b981',
                'lwe_only': True,
                'lpn_only': False
            },
            {
                'name': 'LMS-BKW',
                'desc': 'Réduction de modulus\nOptimisé pour les grands q',
                'icon': '🎯',
                'color': '#f59e0b',
                'lwe_only': True,
                'lpn_only': False
            },
            {
                'name': 'CODED-BKW',
                'desc': 'Codes linéaires\nRéduction accélérée pour LWE complexe',
                'icon': '📡',
                'color': '#ef4444',
                'lwe_only': True,
                'lpn_only': False
            },
            {
                'name': 'CODED-BKW + Sieving',
                'desc': 'Codes + tamisage\nÉtat de l\'art pour LWE difficile',
                'icon': '🎖️',
                'color': '#6366f1',
                'lwe_only': True,
                'lpn_only': False
            }
        ]
        
        # Afficher les algorithmes dans une grille 2x3
        for i, weapon in enumerate(weapons):
            row = i // 3
            col = i % 3
            
            frame = tk.Frame(algo_frame, bg=self.colors['bg_dark'])
            frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            # Déterminer la compatibilité
            if is_lwe:
                compatible = not weapon['lpn_only']
            else:
                compatible = not weapon['lwe_only']
            
            # Créer la carte d'algorithme
            card = self.create_algorithm_card(frame, weapon, compatible, is_lwe)
            card.pack(fill='both', expand=True)
            
            algo_frame.grid_columnconfigure(col, weight=1, uniform='algo')
            algo_frame.grid_rowconfigure(row, weight=1)
    
    def create_algorithm_card(self, parent, weapon, compatible, is_lwe):
        """Crée une carte d'algorithme avec état de compatibilité"""
        if compatible:
            bg_color = weapon['color']
            text_color = 'white'
            status = "🟢 COMPATIBLE"
            status_color = self.colors['accent_green']
            command = lambda w=weapon['name']: self.start_mission(w)
        else:
            bg_color = self.colors['bg_light']
            text_color = self.colors['text_secondary']
            status = "🔴 NON COMPATIBLE"
            status_color = self.colors['accent_red']
            command = None
        
        card = tk.Frame(parent,
                       bg=bg_color,
                       highlightbackground=self.colors['border'],
                       highlightthickness=1)
        
        # En-tête avec icône
        header = tk.Frame(card, bg=bg_color)
        header.pack(fill='x', padx=20, pady=(20, 15))
        
        tk.Label(header, text=weapon['icon'], bg=bg_color,
                fg=text_color, font=('Arial', 28)).pack(side='left', padx=(0, 15))
        
        title_frame = tk.Frame(header, bg=bg_color)
        title_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(title_frame, text=weapon['name'], bg=bg_color,
                fg=text_color, font=self.fonts['h3']).pack(anchor='w')
        
        tk.Label(title_frame, text=status, bg=bg_color,
                fg=status_color, font=self.fonts['small']).pack(anchor='w', pady=(2, 0))
        
        # Description
        desc_frame = tk.Frame(card, bg=bg_color)
        desc_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        tk.Label(desc_frame, text=weapon['desc'], bg=bg_color,
                fg=text_color, font=self.fonts['small'],
                wraplength=300, justify='left').pack(anchor='w')
        
        # Bouton ou message
        if compatible:
            btn = tk.Button(card, text="UTILISER CET ALGORITHME", 
                          bg='white' if compatible else bg_color,
                          fg=weapon['color'] if compatible else text_color,
                          font=('Segoe UI', 10, 'bold'),
                          relief='flat' if compatible else 'sunken',
                          padx=20, pady=10,
                          cursor='hand2' if compatible else 'arrow',
                          state='normal' if compatible else 'disabled',
                          command=command)
            btn.pack(pady=(0, 20))
        else:
            reason_frame = tk.Frame(card, bg=bg_color)
            reason_frame.pack(pady=(0, 20))
            
            if is_lwe:
                reason = "Cet algorithme est conçu pour LPN uniquement"
            else:
                reason = "Cet algorithme est conçu pour LWE uniquement"
            
            tk.Label(reason_frame, text=f"⚠️ {reason}", 
                    bg=bg_color, fg=status_color,
                    font=self.fonts['small']).pack()
        
        return card
    
    # Les méthodes start_mission, show_execution_screen, execute_mission, etc.
    # restent similaires à votre version précédente mais adaptées au nouveau design
    
    def start_mission(self, weapon_name):
        """Démarre une mission avec l'algorithme sélectionné"""
        self.selected_weapon = weapon_name
        self.show_execution_screen()
        
        # Lancer l'exécution dans un thread séparé
        thread = threading.Thread(target=self.execute_mission)
        thread.daemon = True
        thread.start()

    # NOTE: Les méthodes show_execution_screen, execute_mission, setup_log_tags,
    # add_log, show_final_result restent essentiellement les mêmes que dans
    # votre version précédente, mais avec le nouveau design.
    # Pour économiser de l'espace, je ne les répète pas ici.
    # Vous pouvez les copier depuis votre version précédente.
    # main.py - Version complète avec toutes les méthodes
# ... (tout le code précédent jusqu'à la fin de la classe MissionBKW reste identique)
# Ajouter ces méthodes à la FIN de la classe MissionBKW :

    def show_execution_screen(self):
        """Affiche l'écran d'exécution de l'algorithme"""
        self.clear_screen()
        self.current_screen = 'execution'
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_container.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Header avec bouton retour
        header_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        header_frame.pack(fill='x', pady=(0, 30))
        
        self.back_btn = tk.Button(header_frame, text="← Retour", 
                                 bg=self.colors['bg_medium'], fg=self.colors['text_secondary'],
                                 font=self.fonts['body'], padx=15, pady=8,
                                 state='disabled', command=self.show_menu)
        self.back_btn.pack(side='left')
        
        self.status_label = tk.Label(header_frame, text="⚡ EXÉCUTION EN COURS", 
                                    bg=self.colors['bg_dark'], fg=self.colors['accent_green'],
                                    font=self.fonts['h2'])
        self.status_label.pack(side='left', padx=20)
        
        # Informations de la mission
        info_frame = tk.Frame(main_container, bg=self.colors['bg_medium'],
                             highlightbackground=self.colors['border'],
                             highlightthickness=1)
        info_frame.pack(fill='x', pady=(0, 30))
        
        info_content = tk.Frame(info_frame, bg=self.colors['bg_medium'])
        info_content.pack(fill='x', padx=20, pady=20)
        
        # Mission
        mission_frame = tk.Frame(info_content, bg=self.colors['bg_medium'])
        mission_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(mission_frame, text="Mission:", 
                bg=self.colors['bg_medium'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).pack(side='left', padx=(0, 10))
        
        tk.Label(mission_frame, text=self.selected_mission['name'], 
                bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                font=self.fonts['body']).pack(side='left')
        
        # Algorithme
        algo_frame = tk.Frame(info_content, bg=self.colors['bg_medium'])
        algo_frame.pack(fill='x')
        
        tk.Label(algo_frame, text="Algorithme:", 
                bg=self.colors['bg_medium'], fg=self.colors['text_secondary'],
                font=self.fonts['body']).pack(side='left', padx=(0, 10))
        
        tk.Label(algo_frame, text=self.selected_weapon, 
                bg=self.colors['bg_medium'], fg=self.colors['accent_blue'],
                font=self.fonts['body']).pack(side='left')
        
        # Barre de progression
        progress_frame = tk.Frame(main_container, bg=self.colors['bg_dark'])
        progress_frame.pack(fill='x', pady=(0, 30))
        
        self.progress_label = tk.Label(progress_frame, text="Initialisation...", 
                                      bg=self.colors['bg_dark'], fg=self.colors['text_primary'],
                                      font=self.fonts['body'])
        self.progress_label.pack(anchor='w', pady=(0, 10))
        
        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(fill='x')
        
        # Console de logs
        console_frame = tk.Frame(main_container, bg=self.colors['bg_medium'],
                                highlightbackground=self.colors['border'],
                                highlightthickness=1)
        console_frame.pack(fill='both', expand=True)
        
        # En-tête console
        console_header = tk.Frame(console_frame, bg=self.colors['bg_medium'])
        console_header.pack(fill='x', padx=15, pady=15)
        
        tk.Label(console_header, text="📊 CONSOLE D'EXÉCUTION", 
                bg=self.colors['bg_medium'], fg=self.colors['text_primary'],
                font=self.fonts['h4']).pack(side='left')
        
        # Zone de texte avec scroll
        text_frame = tk.Frame(console_frame, bg=self.colors['bg_light'])
        text_frame.pack(fill='both', expand=True, padx=2, pady=(0, 2))
        
        self.log_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                  bg=self.colors['bg_light'],
                                                  fg=self.colors['text_primary'],
                                                  font=self.fonts['mono'],
                                                  height=20,
                                                  relief='flat',
                                                  insertbackground=self.colors['text_primary'])
        self.log_text.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Configurer les tags de couleur
        self.setup_log_tags()
    
    def setup_log_tags(self):
        """Configure les tags de couleur pour la console"""
        self.log_text.tag_config('time', foreground=self.colors['text_muted'])
        self.log_text.tag_config('info', foreground=self.colors['info'])
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
        self.log_text.tag_config('error', foreground=self.colors['error'])
        self.log_text.tag_config('phase', foreground=self.colors['accent_purple'], 
                                font=self.fonts['mono_bold'])
        self.log_text.tag_config('secret', foreground=self.colors['accent_yellow'],
                                font=self.fonts['mono_bold'])
        self.log_text.tag_config('value', foreground='#e6e6e6')
    
    def add_log(self, message, msg_type='info'):
        """Ajoute un message à la console"""
        timestamp = time.strftime("%H:%M:%S")
        
        self.log_text.insert(tk.END, f"[{timestamp}] ", 'time')
        self.log_text.insert(tk.END, f"{message}\n", msg_type)
        
        # Faire défiler jusqu'en bas
        self.log_text.see(tk.END)
        
        # Mettre à jour l'interface
        self.root.update_idletasks()
    
    def execute_mission(self):
        """Exécute la mission avec l'algorithme sélectionné"""
        try:
            # Déterminer les paramètres
            if self.selected_mission['name'].startswith('Personnalisé'):
                params = self.user_params
                secret = self.user_secret
            else:
                params = self.selected_mission['params']
                secret = None
            
            self.add_log("="*70, 'info')
            self.add_log("🚀 DÉBUT DE L'EXÉCUTION", 'phase')
            self.add_log(f"Algorithme: {self.selected_weapon}", 'info')
            
            # Afficher les paramètres
            if params['type'] == 'LPN':
                self.add_log(f"Type: LPN (Learning Parity with Noise)", 'info')
                self.add_log(f"Dimension: {params['k']} bits", 'info')
                self.add_log(f"Bruit: τ = {params['tau']}", 'info')
                self.add_log(f"Structure: {params['a']} blocs × {params['b']} bits", 'info')
            else:
                self.add_log(f"Type: LWE (Learning With Errors)", 'info')
                self.add_log(f"Dimension: n = {params['n']}", 'info')
                self.add_log(f"Modulus: q = {params['q']}", 'info')
                self.add_log(f"Bruit: σ = {params['sigma']:.2f}", 'info')
                self.add_log(f"Structure: {params['a']} blocs × {params['b']} valeurs", 'info')
            
            self.add_log("")
            
            # Mettre à jour la progression
            self.progress_var.set(10)
            self.progress_label.config(text="Génération de l'instance...")
            
            # Générer l'instance
            self.add_log("📦 CRÉATION DE L'INSTANCE", 'phase')
            
            if params['type'] == 'LPN':
                if secret is None:
                    instance = LPNInstance(params['k'], params['tau'])
                    secret = instance.secret
                else:
                    instance = LPNInstance(params['k'], params['tau'], secret)
                
                sample_count = int(20 * (2 ** params['b']) * params['a'])
                self.add_log(f"Secret: {''.join(map(str, secret))}", 'secret')
                self.add_log(f"Échantillons: {sample_count}", 'info')
                
            else:  # LWE
                if secret is None:
                    instance = LWEInstance(params['n'], params['q'], params['sigma'])
                    secret = instance.secret
                else:
                    instance = LWEInstance(params['n'], params['q'], params['sigma'], secret)
                
                sample_count = int(50 * (2 ** params['b']))
                self.add_log(f"Secret: {secret}", 'secret')
                self.add_log(f"Échantillons: {sample_count}", 'info')
            
            samples = instance.generate_samples(sample_count)
            self.add_log(f"✅ {len(samples)} échantillons générés", 'success')
            
            self.progress_var.set(30)
            self.progress_label.config(text="Initialisation de l'algorithme...")
            
            # Initialiser l'algorithme
            self.add_log("🔧 INITIALISATION DE L'ALGORITHME", 'phase')
            
            # Mapping des algorithmes (corriger les noms si besoin)
            weapon_map = {
                'BKW Standard': BKWStandard,
                'LF1 (Walsh-Hadamard)': BKWLF1,
                'BKW-LWE': BKWLWE,
                'LMS-BKW': LMSBKW,
                'CODED-BKW': CodedBKW,
                'CODED-BKW + Sieving': CodedBKWSieving
            }
            
            # Vérifier que l'algorithme existe
            if self.selected_weapon not in weapon_map:
                self.add_log(f"❌ Algorithme '{self.selected_weapon}' non trouvé", 'error')
                self.progress_label.config(text="Erreur!")
                self.status_label.config(text="❌ ERREUR", fg=self.colors['error'])
                self.back_btn.config(state='normal', fg=self.colors['text_primary'])
                return
            
            WeaponClass = weapon_map[self.selected_weapon]
            algorithm = WeaponClass(params, self.add_log)
            
            self.add_log(f"Algorithme initialisé: {self.selected_weapon}", 'info')
            self.add_log("✅ Prêt pour l'exécution", 'success')
            
            self.progress_var.set(50)
            self.progress_label.config(text="Exécution de l'algorithme...")
            
            # Exécuter l'algorithme
            self.add_log("⚡ EXÉCUTION DE L'ALGORITHME", 'phase')
            
            found_secret = algorithm.solve(samples, secret)
            
            # VÉRIFICATION CRITIQUE
            if found_secret is None:
                self.add_log("❌ L'algorithme a retourné None", 'error')
                # Créer un secret par défaut
                if params['type'] == 'LPN':
                    found_secret = [0] * params.get('k', 8)
                else:
                    found_secret = [0] * params.get('n', 8)
            
            self.progress_var.set(80)
            self.progress_label.config(text="Analyse des résultats...")
            
            # Analyser les résultats
            self.add_log("📊 ANALYSE DES RÉSULTATS", 'phase')
            
            if secret is None:
                self.add_log("⚠️ Secret inconnu - impossible de calculer la précision", 'warning')
                accuracy = 0
                success = False
            else:
                # Vérifier la taille
                if len(found_secret) != len(secret):
                    self.add_log(f"⚠️ Taille incompatible: secret={len(secret)}, trouvé={len(found_secret)}", 'warning')
                    # Ajuster
                    min_len = min(len(secret), len(found_secret))
                    correct = sum(1 for i in range(min_len) if found_secret[i] == secret[i])
                    accuracy = (correct / len(secret)) * 100
                else:
                    correct = sum(1 for i in range(len(secret)) if found_secret[i] == secret[i])
                    accuracy = (correct / len(secret)) * 100
                
                # Définir le seuil de succès
                if params['type'] == 'LPN':
                    threshold = 80
                    self.add_log(f"Secret réel:    {''.join(map(str, secret))}", 'secret')
                    self.add_log(f"Secret trouvé:  {''.join(map(str, found_secret))}", 'value')
                else:
                    threshold = 70
                    self.add_log(f"Secret réel:    {secret}", 'secret')
                    self.add_log(f"Secret trouvé:  {found_secret}", 'value')
                
                success = accuracy >= threshold
                
                self.add_log(f"Précision: {correct}/{len(secret)} ({accuracy:.1f}%)", 
                            'success' if success else 'warning')
            
            self.progress_var.set(100)
            self.progress_label.config(text="Exécution terminée!")
            self.status_label.config(text="✅ EXÉCUTION TERMINÉE", fg=self.colors['success'])
            
            # Activer le bouton retour
            self.back_btn.config(state='normal', fg=self.colors['text_primary'],
                               bg=self.colors['accent_blue'])
            
            # Afficher le résultat final
            self.show_final_result(secret, found_secret, accuracy, success, params)
            
        except Exception as e:
            self.add_log(f"❌ Erreur lors de l'exécution: {str(e)}", 'error')
            self.progress_label.config(text="Erreur!")
            self.status_label.config(text="❌ EXÉCUTION ÉCHOUÉE", fg=self.colors['error'])
            self.back_btn.config(state='normal', fg=self.colors['text_primary'],
                               bg=self.colors['accent_blue'])
            
            import traceback
            self.add_log(traceback.format_exc(), 'error')
    
    def show_final_result(self, real_secret, found_secret, accuracy, success, params):
        """Affiche le résultat final de l'exécution"""
        # Ajouter une séparation
        self.add_log("")
        self.add_log("="*70, 'info')
        self.add_log("🏁 RÉSULTAT FINAL", 'phase')
        
        # Afficher la comparaison
        if real_secret and len(real_secret) > 0:
            if params['type'] == 'LPN':
                real_str = ''.join(map(str, real_secret))
                found_str = ''.join(map(str, found_secret))
                
                self.add_log(f"Secret réel:     {real_str}", 'secret')
                self.add_log(f"Secret retrouvé: {found_str}", 'value')
                
                # Afficher les différences
                if len(found_secret) == len(real_secret):
                    differences = []
                    for i in range(len(real_secret)):
                        if real_secret[i] != found_secret[i]:
                            differences.append(i)
                    
                    if differences:
                        self.add_log(f"Différences aux positions: {differences}", 'warning')
                    else:
                        self.add_log("✅ Secret parfaitement retrouvé!", 'success')
                        
            else:  # LWE
                self.add_log(f"Secret réel:     {real_secret}", 'secret')
                self.add_log(f"Secret retrouvé: {found_secret}", 'value')
        
        self.add_log(f"Précision finale: {accuracy:.1f}%", 
                    'success' if success else 'warning')
        
        # Message de conclusion
        if success:
            self.add_log("🎉 Félicitations! Mission réussie.", 'success')
        else:
            self.add_log("🔍 Pour améliorer les résultats:", 'info')
            if params['type'] == 'LPN':
                self.add_log("   • Réduisez le bruit τ", 'info')
                self.add_log("   • Augmentez le nombre d'échantillons", 'info')
                self.add_log("   • Essayez LF1 (Walsh-Hadamard) pour de meilleures performances", 'info')
            else:
                self.add_log("   • Réduisez l'écart-type σ", 'info')
                self.add_log("   • Augmentez le nombre d'échantillons", 'info')
                self.add_log("   • Essayez LMS-BKW pour les grands modulus", 'info')
        
        self.add_log("")
        self.add_log("🔄 Cliquez sur 'Retour' pour recommencer", 'info')

if __name__ == "__main__":
    root = tk.Tk()
    app = MissionBKW(root)
    root.mainloop()