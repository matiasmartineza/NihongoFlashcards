import os
import json
import random
from typing import Dict
from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
STATS_FILE = os.path.join(BASE_DIR, "stats.json")

DATA_FILES = {
    "verbo": "verbos.json",
    "adjetivo": "adjetivos.json",
    "adverbio": "adverbios.json",
    "jlpt": "verbosN5.json",
}


def load_cards(category: str):
    fname = DATA_FILES.get(category)
    if not fname:
        abort(400, description="Categoría desconocida")
    with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
        return json.load(f)


def load_stats() -> Dict[str, Dict[str, int]]:
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_stats(stats: Dict[str, Dict[str, int]]):
    tmp = STATS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATS_FILE)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tarjetas")
def api_tarjetas():
    categoria = request.args.get("categoria")
    modo = request.args.get("modo", "normal")
    try:
        n = int(request.args.get("n", "10"))
    except ValueError:
        n = 10

    cards = load_cards(categoria)
    stats = load_stats()

    if modo == "smart":
        def metric(card):
            stat = stats.get(card.get("id"), {"shown": 0, "correct": 0})
            shown = stat["shown"]
            acc = stat["correct"] / shown if shown > 0 else 0
            return (acc, -shown)
        ordered = sorted(cards, key=metric)
        selected = ordered[:n]
    elif modo == "all":
        selected = cards[:]
        random.shuffle(selected)
    else:
        if n > len(cards):
            n = len(cards)
        selected = random.sample(cards, n)

    return jsonify(selected)


@app.route("/api/stats", methods=["POST"])
def api_stats():
    data = request.get_json(force=True)
    cid = data.get("id")
    if not cid:
        abort(400)
    shown_delta = int(data.get("shownDelta", 0))
    correct_delta = int(data.get("correctDelta", 0))

    stats = load_stats()
    stats.setdefault(cid, {"shown": 0, "correct": 0})
    stats[cid]["shown"] += shown_delta
    stats[cid]["correct"] += correct_delta
    save_stats(stats)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
