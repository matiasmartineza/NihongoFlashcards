window.addEventListener('DOMContentLoaded', () => {
    const selection = document.getElementById('selection');
    const flashcard = document.getElementById('flashcard');
    const startBtn = document.getElementById('start');
    const smartBtn = document.getElementById('start-smart');
    const prevBtn = document.getElementById('prev');
    const flipBtn = document.getElementById('flip');
    const yesBtn = document.getElementById('yes');
    const noBtn = document.getElementById('no');
    const exitBtn = document.getElementById('exit');

    let cards = [];
    let index = 0;
    let flipped = false;

    function updateStats(id, shownDelta, correctDelta) {
        fetch('/api/stats', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id, shownDelta, correctDelta })
        });
    }

    function showCard() {
        const card = cards[index];
        document.getElementById('kanji').textContent = card.adverbio || card.kanji;
        const hira = document.getElementById('hiragana');
        if (card.hiragana) {
            hira.textContent = card.hiragana;
            hira.style.display = 'block';
        } else {
            hira.style.display = 'none';
        }
        document.getElementById('translation').style.display = 'none';
        flipBtn.textContent = 'Mostrar significado';
        flipped = false;
        document.getElementById('counter').textContent = `Tarjeta ${index + 1} de ${cards.length}`;
        if (card.id) {
            updateStats(card.id, 1, 0);
        }
    }

    function fetchCards(mode) {
        const category = document.getElementById('category').value;
        const count = document.getElementById('count').value || 10;
        fetch(`/api/tarjetas?categoria=${category}&modo=${mode}&n=${count}`)
            .then(r => r.json())
            .then(data => {
                cards = data;
                index = 0;
                selection.style.display = 'none';
                flashcard.style.display = 'block';
                showCard();
            });
    }

    startBtn.onclick = () => fetchCards('normal');
    smartBtn.onclick = () => fetchCards('smart');

    prevBtn.onclick = () => {
        if (index <= 0) {
            alert('Esta es la primera tarjeta');
        } else {
            index -= 1;
            showCard();
        }
    };

    flipBtn.onclick = () => {
        const card = cards[index];
        const trans = document.getElementById('translation');
        if (!flipped) {
            let text = '';
            if (card.grupo) {
                text = `${card.español}\nGrupo: ${card.grupo}`;
                if (card.par_transitivo_intransitivo === 'Sí') {
                    text += `\nVersión: ${card.tipo}`;
                }
            } else if (card.tipo && card.español && card.kanji) {
                text = `${card.español}\nTipo: ${card.tipo}`;
            } else {
                const significado = card.español || card.significado || '';
                text = significado ? `${significado}\nCategoría: ${card.categoria}` :
                    `Categoría: ${card.categoria}\n(Traducción no disponible)`;
            }
            trans.textContent = text;
            trans.style.display = 'block';
            flipBtn.textContent = 'Ocultar significado';
            flipped = true;
        } else {
            trans.style.display = 'none';
            flipBtn.textContent = 'Mostrar significado';
            flipped = false;
        }
    };

    function answer(knew) {
        const card = cards[index];
        if (knew && card.id) {
            updateStats(card.id, 0, 1);
        }
        index += 1;
        if (index >= cards.length) {
            alert('Fin de la sesión');
            exit();
        } else {
            showCard();
        }
    }

    yesBtn.onclick = () => answer(true);
    noBtn.onclick = () => answer(false);

    function exit() {
        flashcard.style.display = 'none';
        selection.style.display = 'block';
    }

    exitBtn.onclick = exit;
});
