"""Motor de sesión: estado de una partida (RF03 a RF09, RF11 a RF14)."""


class Sesion:
    def __init__(self, historia):
        self._historia = historia
        self._escenas = {e["id"]: e for e in historia["escenas"]}
        self.escena_id = None
        self.variables = {}
        self._anterior = None
        self.reiniciar()

    def reiniciar(self):
        """Restaura escena y variables iniciales y elimina el historial (RF09)."""
        self.escena_id = self._historia["inicio"]
        self.variables = dict(self._historia["variables"])
        self._anterior = None

    @property
    def escena(self):
        return self._escenas[self.escena_id]

    @property
    def es_final(self):
        return self.escena["final"]

    @property
    def puede_deshacer(self):
        """Hay una elección válida que se pueda revertir (RF13)."""
        return self._anterior is not None

    def _habilitada(self, opcion):
        return all(self.variables.get(var) == valor
                   for var, valor in opcion["condiciones"].items())

    def opciones_habilitadas(self):
        """Opciones cuyas condiciones se cumplen (RF04)."""
        if self.es_final:
            return []
        return [o for o in self.escena["opciones"] if self._habilitada(o)]

    @property
    def bloqueada(self):
        """Escena no final sin opciones habilitadas (RF11)."""
        return not self.es_final and not self.opciones_habilitadas()

    def elegir(self, opcion_id):
        """Aplica una opción habilitada. Devuelve True si avanzó, False si no.

        Una opción inexistente o no habilitada no modifica el estado ni el
        historial de la última elección válida (RF06, RF14).
        """
        for op in self.opciones_habilitadas():
            if op["id"] == opcion_id:
                self._anterior = (self.escena_id, dict(self.variables))
                self.variables.update(op["efectos"])
                self.escena_id = op["destino"]
                return True
        return False

    def deshacer(self):
        """Revierte la última elección válida. Un solo nivel (RF12, RF13).

        Devuelve True si restauró el estado anterior, False si no había
        nada que deshacer (en ese caso el estado no cambia).
        """
        if self._anterior is None:
            return False
        self.escena_id, self.variables = self._anterior
        self._anterior = None
        return True