from dataclasses import dataclass
from model.rifugio import Rifugio


@dataclass
class Connessione:
    r1 : Rifugio
    r2 : Rifugio
    distanza : int
    difficolta : str