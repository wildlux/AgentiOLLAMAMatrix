import pytest
from backend.app import create_app

@pytest.fixture
def client():
    """Fixture per test client Flask"""
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test endpoint health"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'checks' in data

def test_agents_endpoint(client):
    """Test lista agenti"""
    response = client.get('/api/agents', headers={'X-API-Key': 'demo_key_123'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'agents' in data
    assert isinstance(data['agents'], list)

def test_chat_validation(client):
    """Test validazione chat"""
    # Messaggio vuoto
    response = client.post('/api/chat', json={
        'message': '',
        'agent': 'general'
    }, headers={'X-API-Key': 'demo_key_123'})
    assert response.status_code == 400

    # Messaggio valido
    response = client.post('/api/chat', json={
        'message': 'Ciao',
        'agent': 'general'
    }, headers={'X-API-Key': 'demo_key_123'})
    assert response.status_code == 200

def test_rate_limiting(client):
    """Test rate limiting (disabilitato in test)"""
    # In configurazione testing, rate limiting è disabilitato
    pass

def test_cors_headers(client):
    """Test CORS headers"""
    response = client.get('/api/health')
    assert 'Access-Control-Allow-Origin' in response.headers