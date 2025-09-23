import httpx
import os
from dotenv import load_dotenv

load_dotenv()

KENJA_AI_URL = os.environ.get("KENJA_AI_URL")
KENJA_AI_SECRET = os.getenv("KENJA_AI_SECRET")
KENJA_CORPUS_ID = os.getenv("KENJA_CORPUS_ID")
KENJA_CONVERSATION_ID = os.getenv("KENJA_CONVERSATION_ID")


async def get_esg_report(payload:dict):

    headers = {
        "Authorization": f"Bearer {KENJA_AI_SECRET}",
        "Content-Type": "application/json",
    }
    ai_prompt = f"""Create a professional ESG (Environmental, Social, Governance) report for a Carbon Capture and Storage (CCS) facility.
                 Generate a complete ESG (Environmental, Social, Governance) report in Markdown style. 

        Now generate the ESG report based on the following data: 
                 The facility has the following operational output data:
                 Facility name: {payload['facility_name']},
                 Total CO₂ emissions: {payload['total_annual_emissions']} tons,
                 Mean capture efficiency: {payload['mean_capture_efficiency']}%,
                 Mean storage efficiency: {payload['mean_storage_integrity']}%,
                 Minimum capture efficiency: {payload['minimum_capture_efficiency']}%,
                 Minimum storage efficiency: {payload['minimum_storage_integrity']}%,
                 Please generate a structured report that includes the following sections:
                 Executive Summary: Brief overview of the facility’s ESG performance.
                 Environmental Performance: Compare the capture and storage efficiencies, 
                 and total CO₂ emissions, against governmental or international benchmarks
                  (e.g., EU CCS Directive, IEA, IPCC). Highlight areas of excellence and areas needing improvement.
                Social Impact: Discuss how the facility’s operations affect local communities, public health, and stakeholder value.
                Governance & Compliance: Evaluate regulatory alignment, risk management, and transparency.
                Recommendations & Improvement Measures: Suggest operational improvements, emissions reduction strategies, and ESG best practices to enhance performance.
                Conclusion: Summarize the ESG performance and potential next steps for the facility.
                The report should be professional, data-driven, and actionable, with comparisons to accepted standards."""


    request_body = {
         "content": ai_prompt,
         "corpus_id": KENJA_CORPUS_ID,
         "include_reference_objects": [],
         "factuality_mode": "grounded",
         "answer_mode": "permissive",
         "accuracy_mode": "speed",
         "temperature": 0.8,
         "pipeline_id": "default_rag",
         "llm_inference_provider_id": "openai",
         "llm_model_id": "openai.gpt-4.1-mini"
    }
    time_out = httpx.Timeout(60.0, connect=10.0)
    max_attempts = 3
    backoff = 1.0
    url = f"{KENJA_AI_URL}chatbot/conversations/{KENJA_CONVERSATION_ID}/messages"
    async with httpx.AsyncClient(timeout=time_out) as client:
        response = await client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        esg_output = response.json()
        return esg_output["response"]["content"]