"""Motor de sesión: estado de una partida (RF03 a RF09, RF11)."""


class Sesion:
    def __init__(self, historia):
        self._historia = historia
        self._escenas = {e["id"]: e for e in historia["escenas"]}
        self.escena_id = None
        self.variables = {}
        self.reiniciar()

    def reiniciar(self):
        """Restaura la escena y las variables iniciales (RF09)."""
        self.escena_id = self._historia["inicio"]
        self.variables = dict(self._historia["variables"])

    @property
    def escena(self):
        return self._escenas[self.escena_id]

    @property
    def es_final(self):
        return self.escena["final"]

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

        Una opción inexistente o no habilitada no modifica el estado (RF06).
        """
        for op in self.opciones_habilitadas():
            if op["id"] == opcion_id:
                self.variables.update(op["efectos"])
                self.escena_id = op["destino"]
                return True
        return False