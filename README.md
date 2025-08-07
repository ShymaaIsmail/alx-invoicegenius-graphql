# 🧾 InvoiceGenius – Smart Invoice & Receipt Parser (GraphQL Edition)

**ALX ProDev Backend – Project Nexus**  
**Repository:** `alx-invoicegenius-graphql`  
**Author:** [Shymaa M Ismail]  
**Track:** AI, OCR, Django, Celery and GraphQL API Development

---

## 📌 Overview

**InvoiceGenius** is a smart backend system that enables users to upload receipts or invoices in PDF or image format, then intelligently extracts structured fields (like vendor name, date, tax, and total amount) using **OCR** and **OpenAI's GPT**.  

The application exposes a modern, flexible **GraphQL API** using **Graphene-Django**, with background task processing via **Celery** and **Redis**.

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
| 📤 Upload Invoices | Upload PDFs or images via GraphQL mutation |
| 🧠 AI-Powered Parsing | Uses PyMuPDF for text extraction + GPT-3.5 for field classification |
| 🌀 Asynchronous Processing | Tasks handled in background with Celery + Redis |
| 🧩 GraphQL API | Flexible queries and mutations for fetching parsed results |
| 🔐 Authenticated Access | JWT/Token-based authentication via DRF |
| 🛠 Built for Real-World Use | Secure file handling, robust architecture, easy scaling |

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend Framework | Django 4.x, Graphene-Django |
| Auth System | Django REST Framework Tokens |
| OCR | PyMuPDF (fitz) |
| AI Integration | OpenAI GPT-3.5 (via API) |
| Background Tasks | Celery with Redis as broker |
| Storage | Local filesystem (`media/`) |
| Docs & Schema | GraphQL Playground / Google OAuth Background/ Altair (Mutations and Queries Collection) |

---

## 🗃️ ERD & Data Models

📌 [Link to ERD Diagram](https://github.com/ShymaaIsmail/alx-invoicegenius-graphql/tree/main/docs/erd)


- **User**
- **InvoiceFile**: Holds uploaded files and metadata
- **ParsedInvoice**: Stores extracted fields like `vendor`, `date`, `subtotal`, `total`, `tax`

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
📌 For more available queries and mutations, please import  the Altair collection here (https://github.com/ShymaaIsmail/alx-invoicegenius-graphql/blob/main/docs/altair_alx_invoicesgenius_apis_collection.agc)
---

## 🛠 Installation & Setup

```bash
git clone https://github.com/ShymaaIsmail/invoicegenius-graphql.git
cd invoicegenius-graphql

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

## 📚 Best Practices Applied

- Modular Django app structure
- Environment separation using `.env`
- GraphQL schema introspection enabled
- Async task queuing for performance
- Secure file upload & validation
- Token-based authentication
- Field validation and prompt engineering for reliable parsing
- Swagger/Postman setup for non-GraphQL routes (e.g., auth)

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

## 🚧 Challenges & Solutions

📁 [`challenges/`](./challenges) includes:
- Handling mixed-format PDFs
- Mitigating hallucinations from LLM
- Uploading files via GraphQL
- Extracting tabular data reliably

---

## ✨ Future Enhancements

- Real-time notifications (GraphQL subscriptions)
- CSV/Excel export
- Multi-user team billing
- Email-to-receipt forwarding
- Multilingual invoice support

---

## 📜 License

Educational Graduation project for the **ALX ProDev Backend Program**  
© 2025 All rights reserved
