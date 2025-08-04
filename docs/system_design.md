# System Design – InvoiceGenius

## 1. Overview

InvoiceGenius is designed to allow users to upload invoice or receipt documents (PDFs/images), extract structured information using OCR and AI parsing, and retrieve that data in a reliable, performant, and secure way. The system leverages asynchronous processing with Celery and serves a GraphQL API for efficient querying and mutation.

---

## 2. Objectives

* Handle file uploads securely and efficiently
* Extract text using OCR tools
* Parse extracted text using AI models to detect invoice fields
* Store and serve structured data back to authenticated users
* Enable scalability and fault tolerance using asynchronous architecture

---

## 3. High-Level Architecture

```
+---------------------+     GraphQL     +------------------+
|  Frontend Client    | <-------------> |   Django Backend |
| (Web or Mobile)     |                 |  (Graphene API)  |
+---------------------+                 +--------+---------+
                                                  |
                                                  | (File Saved + Task Triggered)
                                                  v
                                     +------------+-----------+
                                     |    Celery Task Queue   |
                                     |   (Redis as Broker)    |
                                     +------------+-----------+
                                                  |
                                                  | (Async Parsing)
                                                  v
                       +----------------+      +------------------+
                       |   OCR Engine   | ---> |     AI Parser     |
                       | (PyMuPDF/Tess) |      | (OpenAI/LayoutLM) |
                       +----------------+      +------------------+
                                                  |
                                                  | (Structured Data)
                                                  v
                                       +----------+-----------+
                                       |   PostgreSQL DB      |
                                       +----------------------+
```

---

## 4. Components Breakdown

### 4.1 Frontend (Optional)

* Upload invoices
* View parsed results
* Authenticate via JWT (handled by backend)

### 4.2 Django Backend (GraphQL API)

* Handles:

  * User registration/login
  * File uploads (mutation)
  * Parsed invoice retrieval (query)
* Uses Graphene + Django ORM
* Secured with JWT

### 4.3 Celery + Redis

* Background task execution
* Triggered immediately after file upload
* Capable of retry, logging, and fault isolation

### 4.4 OCR Layer

* Extracts raw text from PDFs/images
* Tools: PyMuPDF or Tesseract

### 4.5 AI Parser

* Takes extracted text and infers structured fields (vendor, date, amount, tax, etc.)
* Tools: OpenAI GPT / LayoutLM
* Fine-tuned prompts for consistency

### 4.6 PostgreSQL

* Stores:

  * User accounts
  * Invoice file metadata
  * Parsed invoice fields

---

## 5. Key Design Decisions

* **GraphQL API**: Chosen for flexibility, schema enforcement, and rich query capability.
* **Async Processing**: Invoices can take time to process; Celery ensures the app remains responsive.
* **AI + OCR Split**: Clean separation of OCR (text extraction) and LLM (field understanding).
* **Scalability**: Each component (web, worker, DB, AI API) can scale independently.
* **Security**: JWT auth, file validation, strict media MIME checks.

---

## 6. Performance Considerations

* **Queue Offloading**: Prevents request timeouts and keeps frontend snappy.
* **Redis Broker**: Fast and reliable task handling
* **Database Indexes**: On user\_id and invoice\_file\_id for optimized queries
* **AI Cost Optimization**: Minimal prompt sizes, use of fine-tuned small models where possible

---

## 7. Reliability

* **Retry Policy**: Celery retries failed OCR/LLM tasks
* **Logging**: Centralized logging of parsing attempts
* **Storage Redundancy**: Cloud media storage recommended (e.g., S3)

---

## 8. Future Enhancements

* Multi-language invoice support
* Bulk upload and zip file processing
* Fine-tuned LayoutLM with domain-specific datasets
* Admin analytics dashboard
* Role-based access control (RBAC)

---

## 9. External Services

* Google Authentication
* OpenAI API for AI parsing
* Redis (task broker)

---

## 10. Security Measures

* JWT-based auth for all endpoints
* Strict file type/size validation
* Limited OCR/AI API usage per user quota
* Obfuscated file storage paths

---

This system design supports scalability, performance, and real-world application needs, positioning InvoiceGenius as a professional-grade solution for smart document parsing.
