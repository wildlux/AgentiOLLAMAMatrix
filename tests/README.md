# 🧪 Test del Progetto

## 🎯 Organizzazione dei Test

La cartella `tests/` contiene test automatici per verificare il funzionamento del progetto.

## 📁 Struttura

```
tests/
├── test_backend.py    # Test per il backend
├── README.md          # Documentazione
└── (altri test futuri)
```

## 🚀 Come Eseguire i Test

### 1. Avviare il backend
```bash
cd backend
./start_stable.sh
```

### 2. Eseguire i test
```bash
cd tests
python3 test_backend.py
```

### 3. Risultato atteso
```
🧪 Setup test backend...
✅ Test /api/health passato
✅ Test /api/chat passato
✅ Test API key richiesta passato
✅ Test API key non valida passato

Ran 4 tests in X.XXXs
OK
```

## 📋 Test Implementati

### 1. `test_backend.py`
- ✅ Test endpoint `/api/health`
- ✅ Test endpoint `/api/chat`
- ✅ Test API key richiesta
- ✅ Test API key non valida

### 2. Test Futuri (da implementare)
- Test endpoint `/api/chart3d`
- Test endpoint `/api/code/execute`
- Test endpoint `/api/news`
- Test di carico
- Test di sicurezza

## 🎯 Best Practices

1. **Test isolati**: Ogni test è indipendente
2. **Assert chiari**: Verifica specifiche
3. **Documentazione**: Commenti chiari
4. **Copertura**: Test per tutte le funzionalità

## 📊 Vantaggi

1. **Qualità**: Verifica automatica
2. **Manutenibilità**: Facile da aggiornare
3. **Documentazione**: Esempi di utilizzo
4. **Sicurezza**: Test di autenticazione

## 🛠️ Come Aggiungere Test

### 1. Crea un nuovo file
```bash
touch tests/test_nuovo.py
```

### 2. Aggiungi il test
```python
import unittest

class TestNuovo(unittest.TestCase):
    def test_funzione(self):
        # Codice del test
        self.assertEqual(result, expected)
```

### 3. Esegui
```bash
python3 -m unittest tests.test_nuovo
```

## 📋 Checklist

- [x] Creata cartella `tests/`
- [x] Aggiunto `test_backend.py`
- [x] Documentazione creata
- [ ] Aggiungere altri test
- [ ] Integrare in CI/CD

---

🎯 **Test pronti per l'uso!** 🎯

*Data: 13 Dicembre 2024*
*Test: 4 implementati*
*Copertura: In crescita*

---

*"I test sono la base della qualità."* 🧪✨