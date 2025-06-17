# 🎮 FastAPI Videojoc Marketplace

## Descripció 📋
Aquesta és una **API RESTful desenvolupada amb FastAPI** per gestionar un mercat digital de videojocs.  
Els usuaris poden:
- Comprar videojocs.
- Consultar informació sobre elements en venda.
- Afegir etiquetes als videojocs amb un màxim de 5 etiquetes per usuari i videojoc.

## 📦 Estructura Principal
- **Models:** ElementVenda, Videojoc, DLC, Venda, Usuari, Etiqueta, EtiquetaCom.
- **Funcionalitats:** CRUD d’elements, vendes, etiquetes i gestió d’usuaris.

---

## 🚀 Instal·lació

### Requisits previs
- Python 3.9+
- PostgreSQL
- FastAPI
- SQLAlchemy
- Uvicorn

### Clonació del projecte
```bash
git clone https://github.com/el_teu_usuari/fastapi-videojoc-marketplace.git
pip install -r requirements.txt
DATABASE_URL = "postgresql://usuari:contrasenya@localhost:5432/nom_base_de_dades"
uvicorn app.main:app --reload
