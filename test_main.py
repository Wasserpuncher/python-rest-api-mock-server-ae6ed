import unittest
import threading
import time
import http.client
import json
from main import MockServer, DEFAULT_MOCKS, MockAPIHandler

# Definiert den Host und Port für die Test-Server-Instanz
TEST_HOST = '127.0.0.1'
TEST_PORT = 8001

class TestMockServer(unittest.TestCase):
    """
    Unit-Tests für den MockServer und MockAPIHandler.
    """
    server_thread: threading.Thread
    mock_server_instance: MockServer

    @classmethod
    def setUpClass(cls) -> None:
        """
        Setzt den Mock-Server einmalig vor allen Tests auf.
        Der Server wird in einem separaten Thread gestartet.
        """
        print(f"\n[Test Setup] Starte MockServer auf {TEST_HOST}:{TEST_PORT} für Tests...")
        cls.mock_server_instance = MockServer(host=TEST_HOST, port=TEST_PORT, mocks=DEFAULT_MOCKS)
        cls.server_thread = threading.Thread(target=cls.mock_server_instance.start, daemon=True)
        cls.server_thread.start()
        time.sleep(0.5) # Gibt dem Server Zeit zum Starten.
        print("[Test Setup] MockServer gestartet.")

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Fährt den Mock-Server einmalig nach allen Tests herunter.
        """
        print("\n[Test Teardown] Stoppe MockServer...")
        cls.mock_server_instance.stop()
        cls.server_thread.join(timeout=1) # Wartet kurz, bis der Thread beendet ist.
        print("[Test Teardown] MockServer gestoppt.")

    def setUp(self) -> None:
        """
        Setzt die HTTP-Verbindung für jeden Test neu auf.
        """
        self.conn = http.client.HTTPConnection(TEST_HOST, TEST_PORT)

    def tearDown(self) -> None:
        """
        Schließt die HTTP-Verbindung nach jedem Test.
        """
        self.conn.close()

    def test_get_users_endpoint(self) -> None:
        """
        Testet den GET /api/v1/users Endpunkt.
        """
        print("\n[Test] Teste GET /api/v1/users")
        self.conn.request("GET", "/api/v1/users")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.getheader('Content-Type'), 'application/json')
        data = json.loads(response.read().decode('utf-8'))
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]['name'], 'Alice')

    def test_post_users_endpoint(self) -> None:
        """
        Testet den POST /api/v1/users Endpunkt.
        """
        print("\n[Test] Teste POST /api/v1/users")
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({"name": "Charlie"})
        self.conn.request("POST", "/api/v1/users", body=body, headers=headers)
        response = self.conn.getresponse()
        self.assertEqual(response.status, 201)
        self.assertEqual(response.getheader('Content-Type'), 'application/json')
        data = json.loads(response.read().decode('utf-8'))
        self.assertEqual(data['name'], 'Charlie')
        self.assertEqual(data['message'], 'User created')

    def test_get_product_by_id_endpoint(self) -> None:
        """
        Testet den GET /api/v1/products/1 Endpunkt.
        """
        print("\n[Test] Teste GET /api/v1/products/1")
        self.conn.request("GET", "/api/v1/products/1")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.getheader('Content-Type'), 'application/json')
        data = json.loads(response.read().decode('utf-8'))
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], 'Laptop')

    def test_non_existent_endpoint(self) -> None:
        """
        Testet einen nicht existierenden Endpunkt (erwartet 404).
        """
        print("\n[Test] Teste nicht existierenden Endpunkt /api/v1/nonexistent")
        self.conn.request("GET", "/api/v1/nonexistent")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 404)
        self.assertEqual(response.getheader('Content-Type'), 'text/plain')
        self.assertIn(b'No mock response found', response.read())

    def test_health_endpoint(self) -> None:
        """
        Testet den GET /health Endpunkt.
        """
        print("\n[Test] Teste GET /health")
        self.conn.request("GET", "/health")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.getheader('Content-Type'), 'application/json')
        data = json.loads(response.read().decode('utf-8'))
        self.assertEqual(data['status'], 'UP')

    def test_options_endpoint(self) -> None:
        """
        Testet den OPTIONS-Endpunkt (für CORS-Preflight).
        """
        print("\n[Test] Teste OPTIONS /api/v1/users")
        self.conn.request("OPTIONS", "/api/v1/users")
        response = self.conn.getresponse()
        self.assertEqual(response.status, 200)
        self.assertIn('Access-Control-Allow-Origin', response.headers)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], '*')
        self.assertIn('Access-Control-Allow-Methods', response.headers)
        self.assertIn('GET, POST, PUT, DELETE, OPTIONS', response.headers['Access-Control-Allow-Methods'])

    def test_delay_feature(self) -> None:
        """
        Testet, ob die Verzögerungsfunktion korrekt funktioniert.
        """
        print("\n[Test] Teste Verzögerungsfunktion für POST /api/v1/users")
        # Die POST /api/v1/users hat eine Verzögerung von 0.2 Sekunden im DEFAULT_MOCKS
        start_time = time.time()
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({"name": "DelayedUser"})
        self.conn.request("POST", "/api/v1/users", body=body, headers=headers)
        response = self.conn.getresponse()
        end_time = time.time()
        duration = end_time - start_time
        self.assertEqual(response.status, 201)
        self.assertGreaterEqual(duration, 0.2) # Erwartet eine Dauer von mindestens 0.2 Sekunden.
        self.assertLess(duration, 0.5) # Stellt sicher, dass es nicht zu lange dauert (mit Puffer).


if __name__ == '__main__':
    unittest.main()