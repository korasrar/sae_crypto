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
    client = Client(host="localhost", port=1234)

    #permet de ne pas lancer de fenêtre pygame pendant les tests
    monkeypatch.setattr(client, "init_screen", lambda: None)
    monkeypatch.setattr(client, "update_screen", lambda: None)
    monkeypatch.setattr(client, "board_to_surface", lambda board: None)

    return client


def test_est_mon_tour_blanc(client):
    client.en_partie = True
    client.couleur = "w"
    client.board.reset()
    assert client.board.turn == chess.WHITE
    assert client.est_mon_tour() is True


def test_est_mon_tour_noir(client):
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
    client.envoyer("play a2 a3")
    assert client.fichier.buffer == ["play a2 a3\n"]
    assert client.fichier.flushed is True
    #

def test_recevoir(client):
    client.fichier = FauxFichier()
    assert client.recevoir() == "OK"
    #


def test_traiter_message_ok(client):
    client.attente_reponse = True
    client.traiter_message("OK")
    assert client.derniere_reponse == "OK"
    assert client.attente_reponse is False


def test_traiter_message_err(client):
    client.attente_reponse = True
    client.traiter_message("ERR")
    assert client.derniere_reponse == "ERR "
    assert client.attente_reponse is False


def test_appliquer_coup_adversaire_pushes_legal_move(client, monkeypatch):
    monkeypatch.setattr(client, "affiche_plateau", lambda: None)
    monkeypatch.setattr(client, "afficher_fin_partie", lambda: None)

    client.board.reset()
    client.appliquer_coup_adversaire("e2", "e4")
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


def test_traiter_commande_inconnue(client, capsys):
    client.traiter_commande_jeu("unknowncmd")
    out = capsys.readouterr().out
    assert "Commande inconnue" in out
