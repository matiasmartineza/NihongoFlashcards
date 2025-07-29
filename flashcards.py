import json
import random
import tkinter as tk
from tkinter import messagebox
import os
from typing import Dict

class FlashcardApp:
    def __init__(self, master):
        self.master = master
        master.title("Flashcards de Japonés")
        master.geometry("600x500")
        # Evita que el tamaño de la ventana cambie y los botones se oculten
        master.resizable(True, True)
        
        # Variables generales
        self.all_cards = []
        self.session_cards = []
        self.session_total = 0
        self.index = 0
        self.flipped = False
        # Las categorías posibles son: "verbo", "adjetivo", "adverbio", "jlpt"
        self.card_category = None

        base_dir = os.path.dirname(__file__)
        self.stats_file = os.path.join(base_dir, "stats.json")

        self.stats: Dict[str, Dict[str, int]] = {}
        self.load_stats()
        
        # Pantalla de selección inicial
        self.create_initial_selection_frame()

    def load_stats(self):
        """Carga o crea el archivo de estadísticas."""
        base_dir = os.path.dirname(__file__)
        vocab_files = ["verbos.json", "adjetivos.json", "adverbios.json", "verbosN5.json"]
        all_ids = []
        for fname in vocab_files:
            try:
                with open(os.path.join(base_dir, fname), "r", encoding="utf-8") as f:
                    data = json.load(f)
                for card in data:
                    if "id" in card:
                        all_ids.append(card["id"])
            except Exception:
                continue

        try:
            with open(self.stats_file, "r", encoding="utf-8") as f:
                self.stats = json.load(f)
        except Exception:
            self.stats = {}

        ids_set = set(all_ids)
        for cid in ids_set:
            self.stats.setdefault(cid, {"shown": 0, "correct": 0})
        for cid in list(self.stats.keys()):
            if cid not in ids_set:
                del self.stats[cid]
        self.save_stats()

    def save_stats(self):
        tmp = self.stats_file + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.stats_file)
        except Exception:
            pass

    def reset_stats(self):
        for cid in self.stats:
            self.stats[cid]["shown"] = 0
            self.stats[cid]["correct"] = 0
        self.save_stats()
        messagebox.showinfo("Estadísticas", "Se han reiniciado las estadísticas.")

    def record_shown(self, cid: str):
        self.stats.setdefault(cid, {"shown": 0, "correct": 0})
        self.stats[cid]["shown"] += 1
        self.save_stats()

    def record_correct(self, cid: str):
        self.stats.setdefault(cid, {"shown": 0, "correct": 0})
        self.stats[cid]["correct"] += 1
        self.save_stats()

    def back_to_selection(self):
        """Vuelve a la pantalla de selección inicial."""
        if hasattr(self, 'flashcard_frame') and self.flashcard_frame.winfo_exists():
            self.flashcard_frame.destroy()
        if hasattr(self, 'config_frame') and self.config_frame.winfo_exists():
            self.config_frame.destroy()
        self.create_initial_selection_frame()
        
    def create_initial_selection_frame(self):
        """Pantalla inicial para seleccionar entre Verbos, Adjetivos, Adverbios o JLPT N5."""
        self.selection_frame = tk.Frame(self.master, padx=20, pady=20)
        self.selection_frame.pack(expand=True)
        
        label = tk.Label(self.selection_frame, text="¿Qué tarjetas deseas repasar?", font=("Helvetica", 16))
        label.pack(pady=10)
        
        button_frame = tk.Frame(self.selection_frame)
        button_frame.pack(pady=20)
        
        verbos_button = tk.Button(button_frame, text="Verbos", command=lambda: self.load_cards("verbo"), width=20)
        verbos_button.pack(side=tk.LEFT, padx=10)

        adjetivos_button = tk.Button(button_frame, text="Adjetivos", command=lambda: self.load_cards("adjetivo"), width=20)
        adjetivos_button.pack(side=tk.LEFT, padx=10)

        adverbios_button = tk.Button(button_frame, text="Adverbios", command=lambda: self.load_cards("adverbio"), width=20)
        adverbios_button.pack(side=tk.LEFT, padx=10)

        jlpt_button = tk.Button(button_frame, text="JLPT N5", command=lambda: self.load_cards("jlpt"), width=20)
        jlpt_button.pack(side=tk.LEFT, padx=10)

        reset_button = tk.Button(self.selection_frame, text="Reiniciar estadísticas", command=self.reset_stats, width=20)
        reset_button.pack(pady=10)
    
    def load_cards(self, category):
        """Carga el JSON correspondiente según la categoría elegida."""
        self.card_category = category
        if category == "verbo":
            filename = "verbos.json"
        elif category == "adjetivo":
            filename = "adjetivos.json"
        elif category == "adverbio":
            filename = "adverbios.json"
        elif category == "jlpt":
            filename = "verbosN5.json"
        else:
            messagebox.showerror("Error", "Categoría desconocida.")
            self.master.destroy()
            return
        
        try:
            base_dir = os.path.dirname(__file__)
            filepath = os.path.join(base_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                self.all_cards = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar '{filename}': {e}")
            self.master.destroy()
            return
        
        if not self.all_cards:
            messagebox.showerror("Error", f"El archivo '{filename}' está vacío.")
            self.master.destroy()
            return
        
        self.total_available = len(self.all_cards)
        self.selection_frame.destroy()
        self.create_config_frame()
    
    def create_config_frame(self):
        """Pantalla de configuración para seleccionar cuántas tarjetas se quieren practicar."""
        self.config_frame = tk.Frame(self.master, padx=20, pady=20)
        self.config_frame.pack(expand=True)
        
        total_label = tk.Label(self.config_frame, text=f"Tienes {self.total_available} tarjetas disponibles.", font=("Helvetica", 16))
        total_label.pack(pady=10)
        
        prompt_label = tk.Label(self.config_frame, text="¿Cuántas tarjetas quieres practicar hoy?", font=("Helvetica", 14))
        prompt_label.pack(pady=10)
        
        self.num_entry = tk.Entry(self.config_frame, font=("Helvetica", 14), justify='center')
        self.num_entry.pack(pady=5)
        
        button_frame = tk.Frame(self.config_frame)
        button_frame.pack(pady=20)
        
        iniciar_button = tk.Button(button_frame, text="Iniciar", command=self.start_session, width=20)
        iniciar_button.pack(side=tk.LEFT, padx=10)
        
        iniciar_todas_button = tk.Button(button_frame, text="Iniciar todas las tarjetas", command=self.start_all_session, width=20)
        iniciar_todas_button.pack(side=tk.LEFT, padx=10)

        inteligente_button = tk.Button(button_frame, text="Modo inteligente", command=self.start_smart_session, width=20)
        inteligente_button.pack(side=tk.LEFT, padx=10)

        regresar_button = tk.Button(button_frame, text="Regresar", command=self.back_to_selection, width=20)
        regresar_button.pack(side=tk.LEFT, padx=10)
    
    def start_session(self):
        """Inicia la sesión con la cantidad de tarjetas especificada."""
        num_str = self.num_entry.get()
        try:
            num = int(num_str)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido.")
            return
        
        if num <= 0 or num > self.total_available:
            messagebox.showerror("Error", f"Ingresa un número entre 1 y {self.total_available}.")
            return
        
        self.session_total = num
        # Selecciona aleatoriamente 'num' tarjetas sin repetir
        self.session_cards = random.sample(self.all_cards, self.session_total)
        self.config_frame.destroy()
        self.create_flashcard_frame()
    
    def start_all_session(self):
        """Inicia la sesión con todas las tarjetas disponibles."""
        self.session_total = self.total_available
        self.session_cards = self.all_cards[:]  # Copia de todas las tarjetas
        random.shuffle(self.session_cards)
        self.config_frame.destroy()
        self.create_flashcard_frame()

    def start_smart_session(self):
        """Inicia la sesión priorizando tarjetas con menor precisión."""
        num_str = self.num_entry.get()
        if num_str:
            try:
                num = int(num_str)
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa un número válido.")
                return
            if num <= 0 or num > self.total_available:
                messagebox.showerror("Error", f"Ingresa un número entre 1 y {self.total_available}.")
                return
        else:
            num = self.total_available

        def metric(card):
            stat = self.stats.get(card.get("id"), {"shown": 0, "correct": 0})
            shown = stat["shown"]
            acc = stat["correct"] / shown if shown > 0 else 0
            return (acc, shown)

        ordered = sorted(self.all_cards, key=metric)
        self.session_cards = ordered[:num]
        self.session_total = len(self.session_cards)
        self.config_frame.destroy()
        self.create_flashcard_frame()
    
    def create_flashcard_frame(self):
        """Crea la interfaz de flashcards y muestra la primera tarjeta."""
        self.index = 0
        self.flipped = False
        self.correct_answers = 0

        self.flashcard_frame = tk.Frame(self.master, padx=20, pady=20)
        self.flashcard_frame.pack(expand=True)
        
        # Contador de tarjetas
        self.counter_label = tk.Label(self.flashcard_frame, text=f"Tarjeta 1 de {self.session_total}", font=("Helvetica", 14))
        self.counter_label.pack(pady=5)
        
        # Marco para la tarjeta
        self.card_frame = tk.Frame(self.flashcard_frame, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        self.card_frame.pack(expand=True, fill=tk.BOTH)
        
        self.kanji_label = tk.Label(self.card_frame, text="", font=("Helvetica", 48))
        self.kanji_label.pack(pady=(20,10))
        self.hiragana_label = tk.Label(self.card_frame, text="", font=("Helvetica", 24))
        self.hiragana_label.pack(pady=(0,20))
        
        # Inicialmente sin mostrar la traducción ni la info extra
        self.translation_label = tk.Label(self.card_frame, text="", font=("Helvetica", 24), fg="blue")
        self.translation_label.pack()
        
        # Botones: Anterior, Mostrar/Ocultar, No lo sabía y Lo sabía
        self.button_frame = tk.Frame(self.flashcard_frame)
        self.button_frame.pack(pady=20)

        self.prev_button = tk.Button(self.button_frame, text="Anterior", command=self.prev_card, width=20)
        self.prev_button.pack(side=tk.LEFT, padx=10)
        
        self.flip_button = tk.Button(self.button_frame, text="Mostrar significado", command=self.flip_card, width=20)
        self.flip_button.pack(side=tk.LEFT, padx=10)
        
        self.no_button = tk.Button(self.button_frame, text="No lo sabía", command=lambda: self.answer(False), width=20)
        self.no_button.pack(side=tk.LEFT, padx=10)

        self.yes_button = tk.Button(self.button_frame, text="Lo sabía", command=lambda: self.answer(True), width=20)
        self.yes_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.button_frame, text="Regresar", command=self.back_to_selection, width=20)
        self.exit_button.pack(side=tk.LEFT, padx=10)

        self.show_current_card()

    def show_current_card(self):
        self.current_card = self.session_cards[self.index]
        if self.card_category == "adverbio":
            self.kanji_label.config(text=self.current_card["adverbio"])
            self.hiragana_label.config(text="")
            self.hiragana_label.pack_forget()
        else:
            self.kanji_label.config(text=self.current_card["kanji"])
            self.hiragana_label.config(text=self.current_card["hiragana"])
            self.hiragana_label.pack(pady=(0,20))
        self.translation_label.config(text="")
        self.flip_button.config(text="Mostrar significado")
        self.flipped = False
        self.counter_label.config(text=f"Tarjeta {self.index + 1} de {self.session_total}")
        if "id" in self.current_card:
            self.record_shown(self.current_card["id"])

    def flip_card(self):
        """Muestra u oculta el significado y la información extra.
           Para verbos y JLPT N5: se muestra el español, el grupo y, si "par_transitivo_intransitivo" es "Sí", la versión (valor en "tipo").
           Para adjetivos: se muestra el español y el tipo (por ejemplo, い o な).
        """
        if not self.flipped:
            if self.card_category in ["verbo", "jlpt"]:
                info = f"{self.current_card['español']}\nGrupo: {self.current_card['grupo']}"
                if self.current_card.get('par_transitivo_intransitivo', 'No') == "Sí":
                    info += f"\nVersión: {self.current_card['tipo']}"
            elif self.card_category == "adjetivo":
                info = f"{self.current_card['español']}\nTipo: {self.current_card['tipo']}"
            else:  # adverbio
                significado = self.current_card.get('español') or self.current_card.get('significado')
                if significado:
                    info = f"{significado}\nCategoría: {self.current_card['categoria']}"
                else:
                    info = f"Categoría: {self.current_card['categoria']}\n(Traducción no disponible)"
            self.translation_label.config(text=info)
            self.flip_button.config(text="Ocultar significado")
            self.flipped = True
        else:
            self.translation_label.config(text="")
            self.flip_button.config(text="Mostrar significado")
            self.flipped = False
    
    def answer(self, knew: bool):
        card_id = self.current_card.get("id")
        if knew and card_id:
            self.record_correct(card_id)
            self.correct_answers += 1
        self.next_card()

    def next_card(self):
        """Avanza a la siguiente tarjeta y actualiza el contador.
           Si se completan todas, finaliza la sesión.
        """
        self.index += 1
        if self.index >= self.session_total:
            accuracy = (self.correct_answers / self.session_total) * 100 if self.session_total else 0
            messagebox.showinfo("Fin de la sesión", f"Has repasado {self.session_total} tarjetas, con {self.correct_answers} aciertos ({accuracy:.1f}% de media).")
            self.back_to_selection()
            return

        self.show_current_card()

    def prev_card(self):
        """Retrocede a la tarjeta anterior (si existe) y actualiza el contador."""
        if self.index <= 0:
            messagebox.showinfo("Información", "Esta es la primera tarjeta, no hay una anterior.")
            return
        self.index -= 1
        self.show_current_card()


if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
