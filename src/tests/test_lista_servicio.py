import unittest
from unittest.mock import MagicMock
from servicios.lista_servicio import ListaServicio

class TestListaServicio(unittest.TestCase):
    def setUp(self):
        self.lista_repo = MagicMock()
        self.paciente_repo = MagicMock()
        self.servicio = ListaServicio(self.lista_repo, self.paciente_repo)

    def test_generar_fechas_recurrencia_diaria(self):
        fecha_inicio = "2026-05-22 10:00"
        patron = "Diaria"
        repeticiones = 3

        resultado = self.servicio.generar_fechas_recurrencia(fecha_inicio, patron, repeticiones)

        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado[0], "2026-05-22 10:00")
        self.assertEqual(resultado[1], "2026-05-23 10:00")
        self.assertEqual(resultado[2], "2026-05-24 10:00")

    def test_generar_fechas_recurrencia_semanal(self):
        fecha_inicio = "2026-05-22 14:30"
        patron = "Semanal"
        repeticiones = 2

        resultado = self.servicio.generar_fechas_recurrencia(fecha_inicio, patron, repeticiones)

        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0], "2026-05-22 14:30")
        self.assertEqual(resultado[1], "2026-05-29 14:30")

    def test_generar_fechas_recurrencia_fecha_invalida(self):
        fecha_inicio = "2026/05/22 14:30"  # Formato incorrecto
        patron = "Diaria"
        repeticiones = 3

        with self.assertRaises(ValueError) as context:
            self.servicio.generar_fechas_recurrencia(fecha_inicio, patron, repeticiones)
        self.assertIn("La fecha inicial debe estar en formato YYYY-MM-DD HH:MM", str(context.exception))

    def test_generar_fechas_recurrencia_repeticiones_invalidas(self):
        fecha_inicio = "2026-05-22 10:00"
        patron = "Diaria"
        repeticiones = 0  # < 1

        with self.assertRaises(ValueError) as context:
            self.servicio.generar_fechas_recurrencia(fecha_inicio, patron, repeticiones)
        self.assertIn("El número de repeticiones debe ser un entero mayor o igual a 1.", str(context.exception))

if __name__ == "__main__":
    unittest.main()
