# Todo API - Python Projekt

Detta är ett Python-projekt där du ska bygga en REST API för att hantera todos (att-göra-listor) med FastAPI.

## 📋 Innehåll

- [Installation](#installation)
- [Projektstruktur](#projektstruktur)
- [Uppgifter att implementera](#uppgifter-att-implementera)
- [Testning](#testning)
- [Kör projektet](#kör-projektet)

## 🚀 Installation

### Steg 1: Skapa ett virtuellt miljö (venv)

Ett virtuellt miljö hjälper dig att isolera projektets beroenden från andra Python-projekt på din dator.

```bash
# Skapa ett nytt virtuellt miljö
python3 -m venv venv

# Aktivera det virtuella miljön
# På macOS/Linux:
source venv/bin/activate

# På Windows:
# venv\Scripts\activate
```

När det virtuella miljön är aktiverat ser du `(venv)` i början av din terminalrad.

### Steg 2: Installera beroenden

När du har aktiverat det virtuella miljön, installera alla paket som projektet behöver:

```bash
pip install -r requirements.txt
```

Detta installerar:
- `fastapi` - Web-ramverk för att bygga API:er
- `uvicorn` - Server för att köra FastAPI-applikationer
- `pydantic` - För datavalidering
- `pytest` - För att skriva och köra tester

### Steg 3: Verifiera installationen

Kontrollera att allt fungerar genom att köra servern:

```bash
uvicorn app.main:app --reload
```

Öppna din webbläsare och gå till `http://localhost:8000`. Du bör se ett meddelande som säger "Hello, World!".

Du kan också se API-dokumentationen på:
- `http://localhost:8000/docs` (Swagger UI)
- `http://localhost:8000/redoc` (ReDoc)

## 📁 Projektstruktur

```
jensen_todo/
├── app/
│   ├── main.py              # Huvudapplikationen och FastAPI-instans
│   ├── routers/
│   │   └── todos.py         # API-endpoints för todos
│   ├── schemas/
│   │   └── todo.py          # Datamodell för Todo
│   ├── services/
│   │   └── file_service.py  # Funktioner för att läsa/skriva till JSON-fil
│   └── data/
│       └── db.json          # Databasfil (skapas automatiskt) - HÄR sparas dina todos!
├── tests/
│   └── test_todos.py        # Tester för API:et
├── requirements.txt          # Projektets beroenden
└── README.md                 # Denna fil
```

## ✅ Uppgifter att implementera

Projektet har redan grundläggande funktionalitet implementerad, men du behöver slutföra följande endpoints:

### Uppgift 1: Hämta en specifik todo (GET /todos/{id})

**Mål:** Implementera en endpoint som hämtar en specifik todo baserat på dess ID.

**Steg:**
1. Öppna `app/routers/todos.py`
2. Lägg till en ny endpoint med `@router.get("/todos/{todo_id}")`
3. Funktionen ska:
   - Ta emot `todo_id` som parameter
   - Läsa alla todos från databasen med `read_db()`
   - Hitta todo med matchande ID
   - Returnera todo om den finns, annars returnera 404-fel

**Tips:**
- Använd `HTTPException` från FastAPI för att returnera felmeddelanden
- Statuskod 404 används när något inte hittas

**Exempel på förväntat beteende:**
```python
GET /todos/1  → Returnerar todo med id=1
GET /todos/999  → Returnerar 404 Not Found
```

### Uppgift 2: Uppdatera en todo (PUT /todos/{id})

**Mål:** Implementera en endpoint som uppdaterar en befintlig todo.

**Steg:**
1. Lägg till en ny endpoint med `@router.put("/todos/{todo_id}")`
2. Funktionen ska:
   - Ta emot `todo_id` som parameter
   - Ta emot en `Todo`-objekt i request body
   - Hitta todo med matchande ID
   - Uppdatera todo med nya värden
   - Spara ändringarna till databasen med `write_db()`
   - Returnera den uppdaterade todo
   - Returnera 404 om todo inte finns

**Tips:**
- Använd `model_dump()` för att konvertera Pydantic-modellen till dict
- Kom ihåg att behålla det ursprungliga ID:t

**Exempel på förväntat beteende:**
```python
PUT /todos/1
Body: {"title": "Ny titel", "description": "Ny beskrivning", "completed": true}
→ Returnerar uppdaterad todo med id=1
```

### Uppgift 3: Ta bort en todo (DELETE /todos/{id})

**Mål:** Implementera en endpoint som tar bort en todo från databasen.

**Steg:**
1. Lägg till en ny endpoint med `@router.delete("/todos/{todo_id}")`
2. Funktionen ska:
   - Ta emot `todo_id` som parameter
   - Läsa alla todos från databasen
   - Hitta och ta bort todo med matchande ID
   - Spara den uppdaterade listan till databasen
   - Returnera ett bekräftelsemeddelande
   - Returnera 404 om todo inte finns

**Tips:**
- Använd list comprehension eller `filter()` för att ta bort elementet
- Du kan returnera en enkel dict med ett meddelande

**Exempel på förväntat beteende:**
```python
DELETE /todos/1  → Tar bort todo med id=1 och returnerar bekräftelse
DELETE /todos/999  → Returnerar 404 Not Found
```

### Uppgift 4: Förbättra POST /todos

**Mål:** Förbättra den befintliga create-funktionen för att hantera ID:t bättre.

**Nuvarande problem:** 
- Nuvarande implementation använder `len(todos) + 1` för ID, vilket kan leda till problem om todos tas bort.

**Steg:**
1. Förbättra ID-genereringen så att den alltid använder det högsta befintliga ID:t + 1
2. Om listan är tom, börja med ID 1

**Tips:**
- Använd `max()` funktionen för att hitta det högsta ID:t
- Hantera fallet när listan är tom

## 🧪 Testning

### Skriva tester

Öppna `tests/test_todos.py` och skriv tester för alla endpoints. Här är några exempel:

**Exempel på tester att skriva:**

```python
def test_create_todo():
    """Test att skapa en ny todo"""
    # Test-kod här

def test_get_todo_by_id():
    """Test att hämta en specifik todo"""
    # Test-kod här

def test_get_nonexistent_todo():
    """Test att hämta en todo som inte finns"""
    # Test-kod här

def test_update_todo():
    """Test att uppdatera en todo"""
    # Test-kod här

def test_delete_todo():
    """Test att ta bort en todo"""
    # Test-kod här
```

### Köra tester

Kör alla tester med:

```bash
pytest
```

För mer detaljerad output:

```bash
pytest -v
```

För att se print-statements i tester:

```bash
pytest -v -s
```

### Testa API:et manuellt

Du kan testa API:et på flera sätt:

1. **Swagger UI** (Rekommenderat för nybörjare):
   - Kör servern: `uvicorn app.main:app --reload`
   - Öppna `http://localhost:8000/docs` i webbläsaren
   - Testa endpoints direkt i webbläsaren

2. **curl** (kommandorad):
   ```bash
   # Hämta alla todos
   curl http://localhost:8000/todos
   
   # Skapa ny todo
   curl -X POST http://localhost:8000/todos \
     -H "Content-Type: application/json" \
     -d '{"title": "Lära mig Python", "description": "Studera FastAPI", "completed": false}'
   ```

3. **Python requests**:
   ```python
   import requests
   
   # Hämta alla todos
   response = requests.get("http://localhost:8000/todos")
   print(response.json())
   ```

## 🏃 Kör projektet

### Starta utvecklingsservern

```bash
uvicorn app.main:app --reload
```

Flaggan `--reload` gör att servern automatiskt startar om när du ändrar kod, vilket är praktiskt under utveckling.

### Stoppa servern

Tryck `Ctrl + C` i terminalen där servern körs.

### Deaktivera virtuellt miljö

När du är klar med arbetet kan du deaktivera det virtuella miljön:

```bash
deactivate
```

## 📚 Lärresurser

- [FastAPI Dokumentation](https://fastapi.tiangolo.com/)
- [Pydantic Dokumentation](https://docs.pydantic.dev/)
- [Pytest Dokumentation](https://docs.pytest.org/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 🐛 Felsökning

### Problem: "ModuleNotFoundError"

**Lösning:** Kontrollera att:
1. Du har aktiverat det virtuella miljön (`(venv)` ska synas i terminalen)
2. Du har installerat alla beroenden: `pip install -r requirements.txt`

### Problem: "Port already in use"

**Lösning:** Någon annan process använder port 8000. Antingen:
- Stoppa den andra processen
- Eller använd en annan port: `uvicorn app.main:app --reload --port 8001`

### Problem: "db.json not found"

**Lösning:** Detta är normalt! Filen skapas automatiskt första gången du skapar en todo.

### Problem: "Mina todos syns inte i db.json i repot"

**Lösning:** 
- Kontrollera att du tittar på rätt fil: `app/data/db.json` (INTE `app/db.json`)
- Filen `app/data/db.json` är den som faktiskt används av applikationen

## ✅ Checklista

När du är klar, kontrollera att du har:

- [ ] Implementerat GET /todos/{id}
- [ ] Implementerat PUT /todos/{id}
- [ ] Implementerat DELETE /todos/{id}
- [ ] Förbättrat POST /todos ID-generering
- [ ] Skrivit tester för alla endpoints
- [ ] Alla tester passerar
- [ ] Testat API:et manuellt i Swagger UI

## 🎓 Ytterligare utmaningar (Valfritt)

Om du vill gå längre kan du implementera:

1. **Validering**: Lägg till mer validering (t.ex. att titel inte får vara tom)
2. **Sökfunktion**: Lägg till en endpoint för att söka todos
3. **Filtrering**: Filtrera todos baserat på om de är klara eller inte
4. **Paginering**: Lägg till paginering för att hämta todos i sidor
5. **Datum**: Lägg till skapad- och uppdaterad-datum till Todo-modellen

Lycka till med projektet! 🚀

