import io
import types
import chess
import pytest

from client.client import Client


class FauxFichier:
    def __init__(self):
        self.buffer = []
        self.flushed = False

    def write(self, s: str):
        self.buffer.append(s)

    def flush(self):
        self.flushed = True

    def readline(self):
        return "OK\n"


@pytest.fixture()
def client(monkeypatch):
    client = Client(host="example.com", port=1234)

    # Avoid opening a real pygame window during tests
    monkeypatch.setattr(client, "init_screen", lambda: None)
    monkeypatch.setattr(client, "update_screen", lambda: None)
    monkeypatch.setattr(client, "board_to_surface", lambda board: None)

    return client


def test_est_mon_tour_false_when_not_in_game(client):
    client.en_partie = False
    client.couleur = "w"
    assert client.est_mon_tour() is False


def test_est_mon_tour_white(client):
    client.en_partie = True
    client.couleur = "w"
    client.board.reset()
    assert client.board.turn == chess.WHITE
    assert client.est_mon_tour() is True


def test_est_mon_tour_black(client):
    client.en_partie = True
    client.couleur = "b"
    client.board.reset()
    # start position: white to move
    assert client.est_mon_tour() is False
    # make a legal move so it becomes black to move
    client.board.push_san("e4")
    assert client.board.turn == chess.BLACK
    assert client.est_mon_tour() is True


def test_envoyer_writes_and_flushes(client):
    client.fichier = FauxFichier()
    client.envoyer("hello")
    assert client.fichier.buffer == ["hello\n"]
    assert client.fichier.flushed is True


def test_recevoir_strips_line(client):
    client.fichier = FauxFichier()
    assert client.recevoir() == "OK"


def test_traiter_message_ok(client):
    client.attente_reponse = True
    client.traiter_message("OK")
    assert client.derniere_reponse == "OK"
    assert client.attente_reponse is False


def test_traiter_message_err(client, capsys):
    client.attente_reponse = True
    client.traiter_message("ERR bad stuff")
    assert client.derniere_reponse == "ERR bad stuff"
    assert client.attente_reponse is False
    out = capsys.readouterr().out
    assert "bad stuff" in out


def test_traiter_message_start_sets_state_and_resets_board(client, monkeypatch):
    called = {"plateau": 0}

    def fake_affiche():
        called["plateau"] += 1

    monkeypatch.setattr(client, "affiche_plateau", fake_affiche)

    client.board.push_san("e4")
    client.traiter_message("start w")

    assert client.couleur == "w"
    assert client.en_partie is True
    assert client.partie_trouvee is True
    assert client.board.fen() == chess.Board().fen()
    assert called["plateau"] == 1


def test_traiter_message_play_calls_appliquer(client, monkeypatch):
    called = {}

    def fake_apply(src, dst):
        called["src"] = src
        called["dst"] = dst

    monkeypatch.setattr(client, "appliquer_coup_adversaire", fake_apply)
    client.traiter_message("play e2 e4")
    assert called == {"src": "e2", "dst": "e4"}


def test_appliquer_coup_adversaire_pushes_legal_move(client, monkeypatch):
    monkeypatch.setattr(client, "affiche_plateau", lambda: None)
    monkeypatch.setattr(client, "afficher_fin_partie", lambda: None)

    client.board.reset()
    client.appliquer_coup_adversaire("e2", "e4")
    assert client.board.peek().uci() == "e2e4"


def test_jouer_coup_rejects_illegal_move_without_sending(client, monkeypatch):
    sent = []
    monkeypatch.setattr(client, "envoyer", lambda msg: sent.append(msg))

    client.board.reset()
    ok = client.jouer_coup("e2", "e5")
    assert ok is False
    assert sent == []


def test_jouer_coup_sends_and_pushes_on_ok(client, monkeypatch):
    sent = []
    monkeypatch.setattr(client, "envoyer", lambda msg: sent.append(msg))
    monkeypatch.setattr(client, "attendre_reponse", lambda timeout=5: "OK")
    monkeypatch.setattr(client, "affiche_plateau", lambda: None)
    monkeypatch.setattr(client, "afficher_fin_partie", lambda: None)

    client.board.reset()
    ok = client.jouer_coup("e2", "e4")

    assert ok is True
    assert sent == ["play e2 e4"]
    assert client.board.peek().uci() == "e2e4"


def test_traiter_commande_move_compact_format_calls_jouer_coup(client, monkeypatch):
    called = {}

    def fake_jouer(src, dst):
        called["src"] = src
        called["dst"] = dst

    monkeypatch.setattr(client, "jouer_coup", fake_jouer)
    client.traiter_commande_jeu("move e2e4")
    assert called == {"src": "e2", "dst": "e4"}


def test_traiter_commande_move_split_format_calls_jouer_coup(client, monkeypatch):
    called = {}

    def fake_jouer(src, dst):
        called["src"] = src
        called["dst"] = dst

    monkeypatch.setattr(client, "jouer_coup", fake_jouer)
    client.traiter_commande_jeu("move e2 e4")
    assert called == {"src": "e2", "dst": "e4"}


def test_traiter_commande_legal_calls_afficher_coups_legaux(client, monkeypatch):
    hit = {"n": 0}
    monkeypatch.setattr(client, "afficher_coups_legaux", lambda: hit.__setitem__("n", hit["n"] + 1))
    client.traiter_commande_jeu("legal")
    assert hit["n"] == 1


def test_traiter_commande_unknown_prints_help(client, capsys):
    client.traiter_commande_jeu("unknowncmd")
    out = capsys.readouterr().out
    assert "Commande inconnue" in out
