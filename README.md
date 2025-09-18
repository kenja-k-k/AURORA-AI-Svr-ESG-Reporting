# AURORA AI Service – ESG Reporting

This repository contains the **ESG Reporting AI Service**, part of the broader **AURORA Project**, focused on verifiable carbon monitoring and reporting using **AI**, **blockchain**, and **IoT** technologies.

The service demonstrates how simulated IoT data from Carbon Capture and Storage (CCS) facilities can be analyzed for **immediate trends, ESG goal alignment, and natural language reporting**, providing actionable insights, alerts, and simple LLM-based responses to improve operational performance and sustainability outcomes.

---

## 1. High-Level Architecture

The AURORA system integrates **SingularityNET**, AI Services, blockchain-based verification, and IoT data streams into a cohesive decentralized platform.
All three services are independent of each other and can therefore be used individually. However, they are hosted on the same server.

### System Overview
![Aurora component diagram](https://github.com/kenja-k-k/AURORA-AI-Svr-ESG-Reporting/blob/main/Aurora%20component%20diagram.jpg)

### Key Components
- **SingularityNET Integration**
  - Users and admins access the **Marketplace** and **Publisher Portal** to test and deploy AI services.
  - The ESG Reporting service is published to the marketplace for discovery and consumption.
  - The main way to use the service is as a component to be integrated into an external/pre-existing system, by said system calling the service's exposed endpoint(s) through the daemon. Frontend display and further processing of this or other services' outputs are up to the aforementioned system. By making these kinds of integratable components (services) available, SingularityNET simplifies AI application development.

- **Virtual Machine / Backend**
  - Each AI service is intended to be run inside **isolated containers**:
    - **Service 1 (CO₂ Analytics)** – Operational performance and anomaly detection.
    - **Service 2 (CO₂ Predictive Analytics)** – Seasonal trends and forecasting.
    - **Service 3 (ESG Reporting)** – Implemented in this repository.
  - Blockchain hashing (placeholder in Poc) ensures secure and tamper-proof records through creating cyptographic fingerprints.
  - IoT data streams (simulated in PoC) feed into the analytics service for processing.

- **Daemon**
  - This acts as your trusted **gateway** between SingularityNET and your chosen service.
  - You interact with the daemon using the standard SingularityNET tools (SDKs, CLI).
  - The daemon exposes the standard SingularityNET API endpoint. It takes care of **authentication** and payment **verification** automatically, so only valid, authorized requests reach the AI service.
  - It ensures requests are properly formatted and reliably delivered, while also handling responses back to your application.
  - This design means your application connects to our service in a secure, predictable, and marketplace-compliant way, without needing to worry about the internal details of our infrastructure.

- **Frontend (Optional)**  
  - A dashboard visualizes ESG metrics, immediate performance trends, and alerts.  
  - Mostly for demo purposes, there is a dedicated simple frontend available, to visualize the services' generated outputs. It is connected to the service backend through the daemon in the same way as intended in the original way of use. Direct access to the frontend code deployment (on the VM) is neded for this setup.

- **Database Container**  
  - Stores processed data and enables querying for ESG reporting. 

**Components interact as follows**
![Aurora sequence diagram](https://github.com/kenja-k-k/AURORA-AI-Svr-ESG-Reporting/blob/main/Aurora%20sequence%20diagram.png)

---

## 2. Role of This Service

This repository specifically implements **Service 3 Backend (ESG Reporting)** highlighted in **Container 3** of the architecture.

- **Input:** Simulated IoT data streams mimicking CCS facility operations (CO₂ emissions, capture efficiency, storage conditions, etc.).  
- **Output:** ESG metrics, live performance trends, benchmark comparisons, and simple natural-language ESG reports.  
- **Insights Generation:** You can check the `insights.py` file to see the code for generating the insights. This code file includes highly detailed comments explaining the steps taken, understandable also for non-developers.
- **Blockchain Integration:** Hashes analytics data to the **internal Blockchain Hashing Service** for verifiable storage (separate from SingularityNET’s Ethereum metering).  

This service extends the AURORA platform by focusing on **ESG goal alignment and explainability**, helping operators and stakeholders interpret the operational data in business and sustainability terms.

### Choice of Models (LightGBM + LLM)
- **LightGBM**: An ensemble model trained on multiple variables (facility type, region, season) to classify whether performance meets ESG goals.  
- **Lightweight LLM (Phi-3-mini-128k)**: Used for natural language responses to ESG-related queries. The LLM uses a **RAG pipeline** combining structured data (CSV) and unstructured guidance (guidelines.txt).    

### Choice of Frameworks
For this service, we align with two complementary ESG reporting frameworks. GRI establishes a reliable baseline for emissions reporting, while TCFD enables more strategic, risk-oriented disclosure.
- **Global Reporting Initiative (GRI)**: A widely used framework that provides transparent reporting on environmental impacts such as emissions and capture efficiency. It was selected because it is relatively straightforward to implement with the data already collected (e.g., CO₂ emitted, CO₂ captured, efficiency percentages). It allows us to present transparent facility-level metrics and compare them against benchmarks.
- **Task Force on Climate-related Financial Disclosures (TCFD)**: A forward-looking framework emphasizing scenario analysis and climate risk disclosure. This was chosen because it aligns well with the predictive capabilities of our service. Using models such as LightGBM, we generate forecasts of future capture efficiency and emissions. This supports TCFD’s emphasis on climate scenario analysis and resilience planning, extending our ESG reporting beyond historical tracking into forward-looking insights.

**Future Considerations**: As the service evolves from Proof of Concept (POC) to Minimum Viable Product (MVP) and eventually to production, the chosen framework(s) can be re-evaluated. Key considerations for switching or expanding frameworks include:
- Availability of financial data (enabling SASB alignment).
- Client requirements for compliance with CSRD/ESRS or other regional regulations.
- Expansion of tracked variables (e.g., environmental, social, and governance metrics beyond emissions).
For now, GRI + TCFD provide the most practical and justifiable combination given our dataset and the service’s current purpose: delivering live, actionable ESG insights.

---

## 3. PoC Features and Requirements

The **Proof of Concept (PoC)** demonstrates three primary features using simulated IoT data, as specified in the *ESG Reporting Specification*:

| Feature ID | Feature Name              | Description                                                                 |
|------------|---------------------------|-----------------------------------------------------------------------------|
| **3.1**    | Immediate Trend Detection | Detects short-term trends (“Rising”, “Falling”, “Stable”) in CCS performance metrics. |
| **3.2**    | ESG Goal Alignment        | Compares facility performance to global benchmarks and flags deviations.    |
| **3.3** *(planned)*    | Natural Language Reports  | Generates simple ESG-focused summaries using a lightweight LLM and RAG pipeline. |

**Summary of PoC Objectives:**
- Demonstrate ESG analytics using **simulated IoT data**.  
- Highlight **short-term trends** and **global benchmark alignment**.  
- Showcase **LLM-generated ESG reports and query responses**.  

---

## 4. Repository Structure

The repository is structured to reflect the modular design of the ESG Reporting service.  
Core components include analytics modules, LLM/RAG pipelines, sample datasets, and deployment files.  

| Path / File                          | Description                                                                                       | Related Features |
|--------------------------------------|---------------------------------------------------------------------------------------------------|------------------|
| **`protos/`**                        | Protocol Buffers definitions for gRPC communication.                                              | Deployment |
| **`saved_models/`**                  | Directory for storing trained LightGBM models per facility.                                       | 3.2 |
| **`.env.example`**                   | Example environment variables for configuring the service (API keys, paths, etc.).                | Deployment |
| **`.gitignore`**                     | Rules to exclude Python/IDE/cache files from git.                                                 | Housekeeping |
| **`Aurora component diagram.jpg, Aurora sequence diagram.png, Aurora service 1 insights generation flow.jpg`**   | Diagrams of the Aurora project and ESG Reporting service.                                         | Documentation |
| **`README.md`**                      | Project overview, installation, and usage instructions (this file).                               | Documentation |
| **`bench.csv`**                      | Benchmark dataset for comparing facility metrics to global/regional standards.                     | 3.2 |
| **`data.csv`**                       | Example dataset with CCS facility performance data.                                               | Demo |
| **`get_annual_stats response.json`** | Example output for annual ESG metrics.                                                            | Demo |
| **`get_esg response example.json`**  | Example output for ESG query.                                                                     | Demo |
| **`grpc_server.py`**                 | gRPC server implementation to allow remote calls to ESG endpoints.                                | Deployment |
| **`guidelines.txt`**                 | ESG guidelines document used in the RAG pipeline.                                                 | 3.3 |
| **`insights.py`**                    | Analytics logic: trend detection, percent change calculations, ESG benchmarking.                  | 3.1, 3.2 |
| **`kenjaAI.py`**                     | gRPC service handler integrating business logic with the server.                                  | Deployment |
| **`llm response example.json`**      | Example response from LLM query.                                                                  | Demo |
| **`models.py`**                      | LightGBM model implementation and training for ESG goal checks.                                   | 3.2 |
| **`rag.py`**                         | Retrieval-Augmented Generation logic for LLM queries.                                             | 3.3 |
| **`requirements.txt`**               | Python dependencies for the service (FastAPI, pandas, scikit-learn, LightGBM, etc.).              | Deployment |
| **`service.py`**                     | FastAPI entry point exposing endpoints: `get_esg`, `get_trend`, `get_graph`, `get_annual_stats`.   | 3.1, 3.2, 3.3 |

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
2. **Build and run the container:**
  The first one will build the three images specified in the docker-compose.yml file (the service, the ETCD store and the daemon).
The second one will start the containers based on the built images. There is no need to specify ports and names of containers, as everything is specified in the docker-compose.yml file.
   ```bash
   docker compose build
   docker compose up -d
3. **Access the service:**
    Backend API: http://localhost:7000
    Optional frontend dashboard: http://localhost:3000
4. **Publish to SingularityNet testnet (optional)**
      Configure daemon files in /backend/daemon/.
      Use the SingularityNET Publisher Portal

## 6. Deployment Instructions for True Integration

Our service is available on the **SingularityNET Marketplace**. You can integrate it into your application in just a few steps.
- You don’t interact with our infrastructure directly.
- You just use the SingularityNET CLI or SDK.
- The daemon + marketplace handle authentication, payments, and routing to our AI service.

### 1. Create a SingularityNET Account
1. Go to the [SingularityNET Marketplace] (https://beta.singularitynet.io/).  
2. Create an account.
3. Link your **Metamask (or compatible wallet)**
4. Fund your wallet with **AGIX tokens** (required for service usage).

### 2. Install the SingularityNET CLI or SDK
**Prerequisites**
- **Python 3.8+** for CLI and Python SDK  
- **Node.js (LTS)** if using the JavaScript SDK

**Steps**
1. Install the CLI with pip
   ```bash
   pip install snet-cli
3. (Optional) Install SDKs for integration (Python or JavaScript SDK)

### 3. Open a Payment Channel
**Prerequisites**
- SNET CLI installed and configured
- AGIX tokens available in your wallet

**Steps**
1. Deposit AGIX into your account
   ```bash
   snet account deposit 100
3. Open a payment channel for the service
   ```bash
   snet channel open <org_id> <service_id> 10 1

Where:
- `<org_id>` → the organization ID on the marketplace
- `<service_id>` → the identifier of our AI service
- `10` → amount of AGIX tokens allocated
- `1` → channel expiration in blocks

### 4. Call the Service
**Prerequisites**
- Open payment channel to our service
- Service method name (from marketplace metadata)

**Steps**
1. Call the service via CLI
   ```bash
   snet call <org_id> <service_id> <service_method> \
   -y '{"input": "Your request here"}'
2. Or call the service via Python SDK
   ```bash
   from snet import sdk
   snet_sdk = sdk.SnetSDK(config_path="~/.snet/config")
   client = snet_sdk.create_service_client(
       org_id="<org_id>",
       service_id="<service_id>",
       group_name="default_group"
   )
   response = client.call_rpc("service_method", {"input": "Your request here"})
   print(response)

### 5. Integrate Into Your Application
**Prerequisites**
- Working backend (Python, Node.js, or other supported runtime)
- Access to the SNET SDK or CLI

**Steps**
1. Wrap the SDK call into your backend service or workflow.
2. Pass inputs from your application into the request.
3. Handle the responses just like any other API result.
4. Rely on the daemon to ensure authentication, payments, and secure execution.

### 6. Monitor & Manage Usage
**Prerequisites**
- SNET CLI configured
- Active payment channels

**Steps**
1. Check channel balance
   ```bash
   snet channel balance
3. Extend or open new channels as needed
   ```bash
   net channel extend-add-for-service <org_id> <service_id> 10 10000
4. Monitor logs and metrics through your SingularityNET account dashboard.
