import unittest
from unittest.mock import MagicMock
from servicios.paciente_servicio import PacienteServicio

class TestPacienteServicio(unittest.TestCase):
    def setUp(self):
        # Creamos mocks de los repositorios
        self.paciente_repo = MagicMock()
        self.tension_repo = MagicMock()
        self.servicio = PacienteServicio(self.paciente_repo, self.tension_repo)

    def test_obtener_paciente_con_tensiones_sin_tensiones(self):
        # Configurar el mock
        self.paciente_repo.obtener_por_id.return_value = {
            "_id": "paciente123",
            "nombre": "Juan",
            "apellido": "Pérez"
        }
        self.tension_repo.obtener_todos.return_value = []

        # Ejecutar el método
        resultado = self.servicio.obtener_paciente_con_tensiones("paciente123")

        # Verificaciones
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["nombre"], "Juan")
        self.assertEqual(resultado["tensiones_asociadas"], [])
        self.assertEqual(resultado["total_tensiones"], 0)
        self.assertNotIn("promedio_sistolica", resultado)
        self.assertNotIn("promedio_diastolica", resultado)

    def test_obtener_paciente_con_tensiones_con_varias_tensiones(self):
        self.paciente_repo.obtener_por_id.return_value = {
            "_id": "paciente123",
            "nombre": "Maria",
            "apellido": "López"
        }
        self.tension_repo.obtener_todos.return_value = [
            {"valores": {"sistolica": 120, "diastolica": 80}},
            {"valores": {"sistolica": 130, "diastolica": 85}},
            {"valores": {"sistolica": 140, "diastolica": 90}}
        ]

        resultado = self.servicio.obtener_paciente_con_tensiones("paciente123")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["total_tensiones"], 3)
        # Promedio sistólica: (120+130+140)/3 = 130.0
        self.assertEqual(resultado["promedio_sistolica"], 130.0)
        # Promedio diastólica: (80+85+90)/3 = 85.0
        self.assertEqual(resultado["promedio_diastolica"], 85.0)

    def test_eliminar_paciente_en_cascada(self):
        # Configurar mocks
        self.tension_repo.eliminar_por_paciente.return_value = True
        self.paciente_repo.eliminar.return_value = True

        # Ejecutar
        resultado = self.servicio.eliminar_paciente_en_cascada("paciente123")

        # Verificar llamadas
        self.tension_repo.eliminar_por_paciente.assert_called_once_with("paciente123")
        self.paciente_repo.eliminar.assert_called_once_with("paciente123")
        self.assertTrue(resultado)

if __name__ == "__main__":
    unittest.main()
