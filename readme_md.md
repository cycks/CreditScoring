# Credit Scoring & Risk Assessment Engine

A modular Python-based Credit Scoring and Risk Assessment platform. This system integrates behavioral and transactional data processing, machine learning model inference for default risk and credit limit determination, corporate registration and approval workflows, user administration, and automated reporting.

## 📋 Table of Contents

- [Overview](#overview)
- [API Endpoints](#api-endpoints)
- [Architecture & Key Modules](#architecture--key-modules)
- [Machine Learning Artifacts](#machine-learning-artifacts)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Database Migrations](#database-migrations)
- [Documentation Build](#documentation-build)
- [License](#license)

---

## 🎯 Overview

The **CreditScoring** platform automates the credit lifecycle for both individual and corporate clients:

- **Corporate Management:** Handles corporate onboarding, registration verification, and administrative approvals.
- **Data Ingestion & Cleaning:** Ingests transaction logs, mobile metadata, and application parameters.
- **Feature Engineering:** Extracts behavioral predictors and risk features for downstream scoring.
- **Model Inference:** Predicts default probability (`saved_default_model.pkl`) and calculates optimal credit limits (`saved_limit_model.pkl`).
- **Approval Workflows:** Manages administrative permissions, user verification, and status tracking.
- **API Dispatch:** Delivers data payloads via internal helpers and external endpoints.

---

## 🌐 API Endpoints

### Corporate Registration & Approvals (`Companies/`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/register_company` | Registers a new corporate entity for credit evaluation. |
| `GET` | `/api/v1/check_company` | Queries company registration status and verification metrics. |
| `POST` | `/api/v1/approve_company` | Admin endpoint to formally approve or reject a corporate applicant. |

---

## 🏗 Architecture & Key Modules

| Module | Description |
| :--- | :--- |
| **`Companies/`** | Manages corporate onboarding, status verification, and approval pipelines (`corporate_approvals.py`). |
| **`ModelBuilding/`** | Processing scripts for transaction data (`processtransdata.py`), mobile data (`processphonedata.py`), feature engineering, and default/limit preparation routines. |
| **`Models/`** | Data layer defining SQLAlchemy/ORM models (`tables.py`), query functions (`model_users.py`), payment tracking (`payments.py`), and approval checks. |
| **`Users/`** | Handles user verification (`admin_checks.py`), admin permissions (`admin_approvals.py`), and application status displays (`show_status.py`). |
| **`SentData/`** | Prepares and dispatches outgoing API payloads (`send_endpoints.py`, `sentdata_helpers.py`). |
| **`Helpers/`** | Common utility functions for input validation, email processing, and data transformation. |

---

## 🤖 Machine Learning Artifacts

The application loads pre-trained serialized model artifacts from the root directory:

* **`saved_default_model.pkl`**: Evaluates borrower credit risk and outputs default probability score.
* **`saved_limit_model.pkl`**: Computes recommended maximum credit limit based on behavioral history.

---

## 📂 Project Structure

```text
CreditScoring/
├── Companies/              # Corporate registration and approval modules
│   ├── __init__.py
│   └── corporate_approvals.py
├── Helpers/                # Validation, email, and data utilities
├── ModelBuilding/          # Preprocessing & feature engineering pipelines
│   ├── Application/        # Application scoring modules
│   └── Behavioural/        # Transaction & phone data feature extractors
├── Models/                 # ORM tables, payment pipelines, database models
├── SentData/               # Outgoing payload formatting and API endpoints
├── Users/                  # User and admin workflows
├── docs/                   # Sphinx documentation source & HTML output
├── migrations/             # Alembic database migration scripts
├── saved_default_model.pkl # Default risk model
├── saved_limit_model.pkl   # Credit limit determination model
└── requirements.txt        # Project dependencies
```

---

## 🚀 Installation & Setup

### Prerequisites

* Python 3.8+
* Virtual environment utility (`venv` or `conda`)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/CreditScoring.git
   cd CreditScoring
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🗄 Database Migrations

Schema migrations are managed via **Alembic**:

* **Run migrations:**
  ```bash
  alembic upgrade head
  ```
* **Create a new migration:**
  ```bash
  alembic revision --autogenerate -m "Migration description"
  ```

---

## 📚 Documentation Build

Documentation is generated using **Sphinx**:

```bash
cd docs
make html  # Windows: make.bat html
```

Access the built documentation at `docs/build/html/index.html`.

---

## 📄 License

This repository is proprietary and confidential. Unauthorized copying or redistribution is strictly prohibited.