# AURORA AI Service – ESG Reporting

This repository contains the **ESG Reporting AI Service**, part of the broader **AURORA Project**, focused on verifiable carbon monitoring and reporting using **AI**, **blockchain**, and **IoT** technologies.

The service demonstrates how simulated IoT data from Carbon Capture and Storage (CCS) facilities can be analyzed for **immediate trends, ESG goal alignment, and natural language reporting**, providing actionable insights, alerts, and simple LLM-based responses to improve operational performance and sustainability outcomes.

---

## 1. High-Level Architecture

The AURORA system integrates **SingularityNET**, AI Services, blockchain-based verification, and IoT data streams into a cohesive decentralized platform.

### System Overview
![Aurora component diagram](https://github.com/kenja-k-k/AURORA-AI-Svr-ESG-Reporting/blob/main/Aurora%20component%20diagram.jpg)

### Key Components
- **SingularityNET Integration**
  - Users and admins access the **Marketplace** and **Publisher Portal** to test and deploy AI services.
  - The ESG Reporting service will be published to the marketplace for discovery and consumption.

- **Virtual Machine / Backend**
  - Each AI service is intended to be run inside **isolated containers**:
    - **Service 1 (CO₂ Analytics)** – Operational performance and anomaly detection.
    - **Service 2 (CO₂ Predictive Analytics)** – Seasonal trends and forecasting.
    - **Service 3 (ESG Reporting)** – Implemented in this repository (under development).
  - Blockchain hashing ensures secure and tamper-proof records.
  - IoT data streams (simulated in PoC) feed into the analytics service for processing.

- **Frontend (Optional)**  
  - A dashboard visualizes ESG metrics, immediate performance trends, and alerts.  
  - [PLACEHOLDER: Final integration of frontend components pending.]  

- **Database Container**  
  - Stores processed data and enables querying for ESG reporting.  
  - [PLACEHOLDER: Database schema and integration not finalized.]  

---

## 2. Role of This Service

This repository specifically implements **Service 3 Backend (ESG Reporting)** highlighted in **Container 1** of the architecture.

- **Input:** Simulated IoT data streams mimicking CCS facility operations (CO₂ emissions, capture efficiency, storage conditions, etc.).  
- **Output:** ESG metrics, live performance trends, benchmark comparisons, and simple natural-language ESG reports.  
- **Blockchain Integration:** Hashes analytics data to the **internal Blockchain Hashing Service** for verifiable storage (separate from SingularityNET’s Ethereum metering).  

This service extends the AURORA platform by focusing on **ESG goal alignment and explainability**, helping operators and stakeholders interpret the operational data in business and sustainability terms.

### Choice of Models (LightGBM + LLM)
- **LightGBM**: An ensemble model trained on multiple variables (facility type, region, season) to classify whether performance meets ESG goals.  
- **Lightweight LLM (Phi-3-mini-128k)**: Used for natural language responses to ESG-related queries. The LLM uses a **RAG pipeline** combining structured data (CSV) and unstructured guidance (guidelines.txt).  
- [PLACEHOLDER: Model hyperparameters, training dataset size, and benchmarking results to be finalized.]  

---

## 3. PoC Features and Requirements

The **Proof of Concept (PoC)** demonstrates three primary features using simulated IoT data, as specified in the *ESG Reporting Specification*:
[PLACEHOLDER: All features to be confirmed and finalized.]

| Feature ID | Feature Name              | Description                                                                 |
|------------|---------------------------|-----------------------------------------------------------------------------|
| **3.1**    | Immediate Trend Detection | Detects short-term trends (“Rising”, “Falling”, “Stable”) in CCS performance metrics. |
| **3.2**    | ESG Goal Alignment        | Compares facility performance to global benchmarks and flags deviations.    |
| **3.3**    | Natural Language Reports  | Generates simple ESG-focused summaries using a lightweight LLM and RAG pipeline. |

**Summary of PoC Objectives:**
- Demonstrate ESG analytics using **simulated IoT data**.  
- Highlight **short-term trends** and **global benchmark alignment**.  
- Showcase **LLM-generated ESG reports and query responses**.  

---

## 4. Repository Structure

The repository is structured to reflect the modular design of the ESG Reporting service.  
Core components include analytics modules, LLM/RAG pipelines, sample datasets, and deployment files.  
[PLACEHOLDER: Structure may change as development continues.]

| Path / File                | Description                                                                                       | Related Features |
|-----------------------------|---------------------------------------------------------------------------------------------------|------------------|
| **`.gitignore`**            | Rules to exclude Python/IDE/cache files from git.                                                 | Housekeeping |
| **`data.csv`**              | Example dataset with CCS facility performance data.                                               | Demo |
| **`dataset_file.csv`**      | Sample dataset for ESG metrics analysis.                                                          | Demo |
| **`get_annual_stats response.json`** | Example output for annual ESG metrics.                                                     | Demo |
| **`get_esg response example.json`**  | Example output for ESG query.                                                              | Demo |
| **`llm response example.json`**      | Example response from LLM query.                                                           | Demo |
| **`guidelines.txt`**        | ESG guidelines document used in the RAG pipeline.                                                 | 3.3 |
| **`insights.py`**           | Analytics logic: trend detection, percent change calculations, ESG benchmarking.                  | 3.1, 3.2 |
| **`models.py`**             | LightGBM model implementation for ESG goal checks.                                                | 3.2 |
| **`rag.py`**                | Retrieval-Augmented Generation logic for LLM queries.                                             | 3.3 |
| **`requirements.txt`**      | Python dependencies for the service (FastAPI, pandas, scikit-learn, LightGBM, etc.).              | Deployment |
| **`service.py`**            | FastAPI entry point exposing endpoints: `get_esg`, `get_trend`, `get_graph`, `get_annual_stats`.   | 3.1, 3.2, 3.3 |
| **`README.md`**             | Project overview, installation, and usage instructions (this file).                               | Documentation |

---

## 5. Deployment Instructions

### Prerequisites
- **Docker** for containerized deployment.  
- **Python 3.10+** for running locally.  
- **SingularityNET CLI** for publishing to the marketplace (optional).  
- **Metamask Wallet (TestNet Account)** for blockchain testnet interactions (optional).  

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kenja-k-k/AURORA-AI-Svr-ESG-Reporting.git
   cd AURORA-AI-Svr-ESG-Reporting
