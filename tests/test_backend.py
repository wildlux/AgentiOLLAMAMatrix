#!/usr/bin/env python3
"""
Test per il backend dell'Assistente AI
"""

import unittest
import requests
import json
import time

class TestBackend(unittest.TestCase):
    """Test per le API del backend"""
    
    @classmethod
    def setUpClass(cls):
        """Setup prima dei test"""
        print("🧪 Setup test backend...")
        
    def test_health_endpoint(self):
        """Test dell'endpoint /api/health"""
        response = requests.get(
            'http://localhost:54324/api/health',
            headers={'X-API-Key': 'demo_key_123'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
        print("✅ Test /api/health passato")
    
    def test_chat_endpoint(self):
        """Test dell'endpoint /api/chat"""
        payload = {
            'text': 'Ciao',
            'mode': 'general'
        }
        response = requests.post(
            'http://localhost:54324/api/chat',
            headers={
                'Content-Type': 'application/json',
                'X-API-Key': 'demo_key_123'
            },
            data=json.dumps(payload)
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertIn('mode', data)
        print("✅ Test /api/chat passato")
    
    def test_api_key_required(self):
        """Test che l'API key è richiesta"""
        response = requests.get('http://localhost:54324/api/health')
        self.assertEqual(response.status_code, 401)
        print("✅ Test API key richiesta passato")
    
    def test_invalid_api_key(self):
        """Test con API key non valida"""
        response = requests.get(
            'http://localhost:54324/api/health',
            headers={'X-API-Key': 'invalid_key'}
        )
        self.assertEqual(response.status_code, 401)
        print("✅ Test API key non valida passato")

if __name__ == '__main__':
    unittest.main()