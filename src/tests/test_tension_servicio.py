import unittest
from unittest.mock import MagicMock
from servicios.tension_servicio import TensionServicio

class TestTensionServicio(unittest.TestCase):
    def setUp(self):
        self.tension_repo = MagicMock()
        self.servicio = TensionServicio(self.tension_repo)

    def test_verificar_rango_optimo(self):
        # Sistólica < 140 y Diastólica < 90 es óptimo (True)
        self.assertTrue(self.servicio.verificar_rango(120, 80))
        self.assertTrue(self.servicio.verificar_rango(139, 89))
        
        # Al menos uno en el límite o mayor es no óptimo (False)
        self.assertFalse(self.servicio.verificar_rango(140, 80))
        self.assertFalse(self.servicio.verificar_rango(120, 90))
        self.assertFalse(self.servicio.verificar_rango(140, 90))
        self.assertFalse(self.servicio.verificar_rango(150, 95))

    def test_crear_toma_actualiza_rango_en_toma_automatica(self):
        # Toma con valores óptimos
        toma_input_optima = MagicMock()
        toma_input_optima.valores.sistolica = 120
        toma_input_optima.valores.diastolica = 80
        toma_input_optima.model_dump.return_value = {
            "valores": {"sistolica": 120, "diastolica": 80},
            "valor_en_rango": True
        }

        self.servicio.crear_toma(toma_input_optima)
        
        # Verificar que el atributo valor_en_rango se estableció en True
        self.assertTrue(toma_input_optima.valor_en_rango)
        self.tension_repo.crear.assert_called_once()

        # Toma con valores altos
        toma_input_alta = MagicMock()
        toma_input_alta.valores.sistolica = 150
        toma_input_alta.valores.diastolica = 95
        toma_input_alta.model_dump.return_value = {
            "valores": {"sistolica": 150, "diastolica": 95},
            "valor_en_rango": False
        }

        self.servicio.crear_toma(toma_input_alta)
        
        # Verificar que se estableció en False
        self.assertFalse(toma_input_alta.valor_en_rango)

if __name__ == "__main__":
    unittest.main()
