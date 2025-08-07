# 🧾 InvoiceGenius – Smart Invoice & Receipt Parser (GraphQL Edition)
**ALX ProDev Backend – Project Nexus**  
**Repository:** alx-invoicegenius-graphql  
**Author:** `Shymaa Mohamed Ismail`  
**Track:** AI, OCR, Django, Celery , GraphQL API Development, Docker and Render Deployment

---
## 📌 Overview

**InvoiceGenius** is a smart backend system that enables users to upload receipts or invoices in PDF or image format, then intelligently extracts structured fields (like vendor name, date, tax, and total amount) using **OCR** and **OpenAI's GPT**.  
This project showcases real-world backend engineering with asynchronous processing, AI integration, token authentication, and best practices in modern backend development.

---
## 🎯 Project Objectives

- 📊 Automate invoice parsing using OCR + LLMs
- 🌐 Provide GraphQL APIs for interacting with invoice data
- 🧵 Handle long-running tasks using Celery
- 🔒 Secure file upload and user-specific data access
- 💡 Demonstrate professional, production-level backend architecture
---
## 💼 Core Features

| Feature | Description |
|--------|-------------|
| 📤 Upload Invoices | Multi Format Upload PDFs or images via GraphQL mutation (PDF, PNG, JPG) |
| 🧠 OCR Text Extraction | Powered by Tesseract and PyMuPDF|
| 🧠 AI-Powered Parsing |Uses GPT-3.5 for field classification and smart parsing|
| 🌀 Asynchronous Processing | Tasks handled in background with Celery + Redis , it doesn't block the ui |
| 🧩 GraphQL API | Flexible queries and mutations for fetching parsed results |
| 📊 Dynamic Invoice Filtering |  Relay-style pagination in GraphQL utilizes the concept of "connections" and "edges.|
| 🔐 Authenticated Access | JWT/Token-based authentication via Graphene-jwt |
| 🔐 Google Auth Access | using OAuth2.0 |
| 🛠 Built for Real-World Use | Secure file handling, robust architecture, easy scaling |
| ☁️ Amazon S3 | integration for file storage |
| 🧪 Unit & Integration Tests | python3 test suit |

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend Framework | Django 4.x, Graphene-Django, Graphql |
| Auth System | Google OAuth2.0 and Graphene-jwt |
| OCR | PyMuPDF (fitz) |
| AI Integration | OpenAI GPT-3.5 (via API) |
| Background Tasks | Celery with Redis as broker |
| Storage | Amazon S3  |
| Database | Postgresql and Django ORM |
| Docs & Schema | GraphQL Playground / Google OAuth Background/ Altair (Mutations and Queries Collection) |
| Containerization| Docker |
| Deployment | Render, Upstash |

---
### 📁 Why This Project Structure Matters

| Folder / File            | Purpose                                                                 |
|--------------------------|-------------------------------------------------------------------------|
| `ai_parser/`             | Isolates all AI-related parsing logic and OpenAI integrations.         |
| `authentication/`        | Manages user authentication via JWT and Google OAuth.                  |
| `core/`                  | Central project settings including Celery and GraphQL schema.          |
| `docs/`                  | Documentation assets like ERD diagrams and Altair collections.         |
| `invoices/`              | Handles invoice uploads, parsing, and GraphQL API.                     |
| `invoicesgenius/`        | Django app housing configurations, settings, and entry points.         |
| `ocr/`                   | Contains OCR extraction code using tools like PyMuPDF/Tesseract.       |
| `tests/`                 | Centralized location for unit tests.                   |
| `Dockerfile` & `render.yaml` & `start.sh`| Empower containerization, migrations, background processing, and production readiness. |


---
## 🗃️ ERD & Data Models

📌 [Link to ERD Diagram](https://github.com/ShymaaIsmail/alx-invoicegenius-graphql/tree/main/docs/erd)

- **User**
- **InvoiceFile**: Holds uploaded files and metadata
- **ParsedInvoice**: Stores extracted fields like `vendor`, `date`, `subtotal`, `total`, `tax`
- **Celery**: Store TaskResults,...etc
---

## 🚀 Example GraphQL Operations

### Upload an Invoice
```graphql
mutation UploadInvoice($file: Upload!) {
  uploadInvoice(file: $file) {
    message
    success
    invoice {
      id
      originalFile
      processed
      uploadedAt
      processedAt
    }
  }
}
```
### Admin users Authenticate (Token)
```graphql
mutation {
  tokenAuth(username: "user", password: "pass") {
    token
  }
}
```
### Google users Authenticate (Token)
```graphql
mutation {
  googleLogin(idTokenStr: "google_token") {
  email
    firstName
    lastName
    refreshToken
    token
    userId
    username
  }
}
```
📌 For full available GraphQL queries and mutations, please import [Altair collection here](https://github.com/ShymaaIsmail/alx-invoicegenius-graphql/blob/main/docs/altair_alx_invoicesgenius_apis_collection.agc)

---

## 🛠 Installation & Setup

```bash
git clone https://github.com/ShymaaIsmail/alx-invoicegenius-graphql.git
cd alx-invoicegenius-graphql

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add keys: OPENAI_API_KEY, DB_NAME, etc.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# In a new terminal (for background worker)
celery -A invoicegenius worker -l debug

### System Installation Requirement: 
sudo apt install tesseract-ocr

```
---
## 🧑‍💻 Deployment Details
The project is fully deployed using cloud platforms for scalability and availability:
| Component	Platform |	Description|
|--------------------|--------------|
| 🌐 Web App	Render.com	| Deployed Django app|
| 🛢️ Database	Render PostgreSQL |	Production database|
| 🔁 Celery Worker	Render background worker	| Runs async tasks|
| 🧠 AI Parser	OpenAI API	GPT-3.5 | used to extract structured data|
| ☁️ Storage	Amazon S3	| Uploaded invoice files stored securely|
| ⚡ Redis Broker	Upstash Redis	| Used for Celery task queuing|
| 🔐 Google Auth	Google Developer Console	| OAuth2 integration for user login|
| 🎛️ Frontend Tool	GraphQL Playground & Altair	| Testing and documentation of GraphQL APIs|

✅ This multi-service deployment demonstrates real-world scalability, third-party integrations, and cloud-based architecture design.

---
## 📦 Containerization & Production Readiness

InvoiceGenius is built with deployment and scalability in mind:

- **Dockerized Infrastructure**:  
  Uses a multi-stage Docker setup to ensure fast, lean production builds, running Django with Gunicorn and Celery.
- **Startup Automation**:  
  On container launch:
  - Database migrations are run
  - Superuser is auto-created (if not exists)
  - Celery worker starts in background
  - Static files are collected
  - Gunicorn launches the web server
- **Tesseract OCR Support**:  
  System-level dependencies like `tesseract-ocr` are installed directly in the Docker image for parsing text from PDFs and images.
- **Secure and Performant**:  
  - Runs behind Gunicorn (not Django dev server)
  - Proper `.env` support and secrets handling
  - Scales via container orchestration on Render

📌 This container-first architecture ensures **consistent environments**, **fast CI/CD**, and **zero-downtime deploys**.

---
## 📹 Demo Video

🎥 [Watch Demo](https://link-to-your-demo-video)

---
## 🌐 Hosted API

🌍 [Live GraphQL Playground](https://shymaaismail-alx-invoicegenius-graphql.onrender.com/graphql/)  
🔐 Use token header: `Authorization: JWT <your_token>`

🌍 [Live Admin Dashboard](https://shymaaismail-alx-invoicegenius-graphql.onrender.com/admin)  
🔐 User Name and password are available in the presentation slides

---
## 📚 Best Practices Applied

- Modular Django app structure
- Environment separation using `.env`
- GraphQL schema introspection enabled
- Async task queuing for performance using Celery
- Secure file upload & validation
- Token-based authentication
- Field validation and prompt engineering for reliable parsing
- Logs for failed parsing
- Markdown docs and clean commit history
---
## 🚧 Challenges & Solutions

📁 [`challenges/`] includes:
- Integration with external serviceslike openAI,S3, Upstash.
- Deployment on freetier on Render
- Mitigating hallucinations from LLM
- Uploading files via GraphQL
- Extracting tabular data reliably

---

## ✨ Future Enhancements

- Statistics Dashboard
- Real-time notifications (GraphQL subscriptions)
- CSV/Excel export
- Multi-user team billing
- Email-to-receipt forwarding
- Multilingual invoice support

---

## 📜 License

Educational Graduation project for the **ALX ProDev Backend Program**  
© 2025 All rights reserved
