# Construction Site Management API

## Task hôm nay

- FastAPI modular structure
- Environment configuration
- MySQL + SQLAlchemy
- Models: User, ConstructionSite, SiteMember, WorkItem
- Pydantic Base/Create/Update/Response schemas
- Initial table creation with `Base.metadata.create_all`
- 400/403/404/422 unified error response
- Health-check endpoint

## Chạy project

1. Tạo database MySQL:

```sql
CREATE DATABASE construction_management;
```

2. Copy `.env.example` thành `.env` và sửa `DATABASE_URL`, `SECRET_KEY`.

3. Cài thư viện:

```bash
pip install -r requirements.txt
```

4. Chạy:

```bash
uvicorn app.main:app --reload
```

5. Kiểm tra:

```text
GET /health
GET /docs
```
