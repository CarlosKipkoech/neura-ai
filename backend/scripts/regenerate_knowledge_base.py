"""
Generate the complete Neura AI synthetic enterprise knowledge base.

Produces 24 PDF + 24 JSON files under backend/knowledge_base/.
PDFs are text-based (FlateDecode), UTF-8-safe via latin-1 subset, and compatible
with the custom extractor in src/ingest.py.
"""

from __future__ import annotations

import json
import textwrap
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

BASE_DIR = Path(__file__).resolve().parents[1] / "knowledge_base"

COMPANY = "Neura AI"
FISCAL_YEAR = "2026"
CREATED_DATE = "2026-03-31"

# Shared corporate facts referenced across departments
CORPORATE = {
    "employees": 847,
    "revenue_fy2025": "$142.3M ARR",
    "revenue_forecast_fy2026": "$198.7M",
    "ebitda_margin": "18.4%",
    "headquarters": "San Francisco, CA",
    "ceo": "Dr. Elena Vasquez",
    "cfo": "Marcus Chen",
    "cto": "James Okonkwo",
    "chro": "Sarah Mitchell",
    "cmo": "Priya Sharma",
    "coo": "David Park",
    "engineering_headcount": 312,
    "marketing_budget_fy2026": "$14.2M",
    "it_budget_fy2026": "$22.8M",
    "open_incidents_q1": 3,
    "nps_score": 62,
    "customer_count": 1240,
}


@dataclass
class DocumentSpec:
    title: str
    document_type: str
    classification: str
    access_roles: list[str]
    version: str
    content_builder: Callable[[], list[str]]


def wrap(text: str, width: int = 92) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        stripped = paragraph.strip()
        if not stripped:
            lines.append("")
            continue
        if stripped.startswith("- ") or stripped.startswith("* "):
            wrapped = textwrap.wrap(stripped, width=width, subsequent_indent="  ")
            lines.extend(wrapped)
        elif stripped.startswith("|"):
            lines.append(stripped)
        else:
            lines.extend(textwrap.wrap(stripped, width=width))
    return lines


def section(title: str, body: str) -> list[str]:
    return [title, "-" * len(title), *wrap(body), ""]


def bullet_section(title: str, items: list[str]) -> list[str]:
    lines = [title, "-" * len(title)]
    for item in items:
        lines.extend(wrap(f"- {item}"))
    lines.append("")
    return lines


def table_section(title: str, headers: list[str], rows: list[list[str]]) -> list[str]:
    col_widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(len(headers))]
    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    sep_line = "|-" + "-|-".join("-" * w for w in col_widths) + "-|"
    lines = [title, "-" * len(title), header_line, sep_line]
    for row in rows:
        lines.append("| " + " | ".join(row[i].ljust(col_widths[i]) for i in range(len(headers))) + " |")
    lines.append("")
    return lines


def paginate(lines: list[str], lines_per_page: int = 44) -> list[list[str]]:
    pages: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if len(current) >= lines_per_page:
            pages.append(current)
            current = []
        current.append(line)
    if current:
        pages.append(current)
    return pages


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_pdf_page_content(lines: list[str]) -> bytes:
    text_lines = ["BT", "/F1 11 Tf", "50 760 Td", "14 TL"]
    for i, line in enumerate(lines):
        if i == 0:
            text_lines.append(f"({escape_pdf_text(line or ' ')}) Tj")
        else:
            text_lines.append("T*")
            text_lines.append(f"({escape_pdf_text(line or ' ')}) Tj")
    text_lines.append("ET")
    return "\n".join(text_lines).encode("latin-1", errors="replace")


def write_pdf(path: Path, pages: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    font_obj = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    content_objs = []
    for page_lines in pages:
        content = build_pdf_page_content(page_lines)
        compressed = zlib.compress(content)
        content_stream = b"<< /Filter /FlateDecode /Length %d >>\nstream\n%s\nendstream" % (
            len(compressed),
            compressed,
        )
        content_objs.append(content_stream)

    page_objs = []
    for idx in range(len(pages)):
        content_obj_num = 4 + idx
        page_obj = (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 3 0 R >> >> "
            b"/Contents %d 0 R >>" % content_obj_num
        )
        page_objs.append(page_obj)

    kids = b"[" + b" ".join(f"{4 + len(pages) + idx} 0 R".encode("ascii") for idx in range(len(page_objs))) + b"]"
    pages_tree = b"<< /Type /Pages /Kids " + kids + b" /Count %d >>" % len(page_objs)
    catalog = b"<< /Type /Catalog /Pages 2 0 R >>"

    objects = [catalog, pages_tree, font_obj] + content_objs + page_objs

    offsets = []
    body = b"%PDF-1.4\n\n"
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(body))
        body += f"{i} 0 obj\n".encode("ascii")
        body += obj + b"\nendobj\n\n"

    xref_pos = len(body)
    body += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for offset in offsets:
        body += f"{offset:010d} 00000 n \n".encode("ascii")
    body += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%EOF\n" % (len(objects) + 1, xref_pos)

    path.write_bytes(body)


def doc_header(title: str, dept: str) -> list[str]:
    return [
        f"{COMPANY} | {dept}",
        title,
        f"Version 1.0 | Classification: Internal | Effective Date: {CREATED_DATE}",
        f"Document Owner: {dept.replace('_', ' ')} Leadership | Review Cycle: Quarterly",
        "",
    ]


def cross_refs(*refs: str) -> list[str]:
    return bullet_section("Cross-References", list(refs))


def definitions(items: dict[str, str]) -> list[str]:
    lines = ["Definitions", "-----------"]
    for term, definition in items.items():
        lines.extend(wrap(f"{term}: {definition}"))
    lines.append("")
    return lines


def approval_workflow(steps: list[str]) -> list[str]:
    return bullet_section("Approval Workflow", steps)


def scenario(title: str, narrative: str) -> list[str]:
    return section(f"Example Scenario: {title}", narrative)


# ---------------------------------------------------------------------------
# Engineering_IT documents
# ---------------------------------------------------------------------------


def build_incident_management_report() -> list[str]:
    lines = doc_header("Incident Management Report", "Engineering_IT")
    lines.extend(
        section(
            "Executive Summary",
            f"This report documents three production incidents affecting {COMPANY} platform services "
            f"during Q1 {FISCAL_YEAR}. Total customer-impacting downtime was 47 minutes across incidents "
            f"INC-2026-0142 (API latency degradation), INC-2026-0187 (authentication service outage), "
            f"and INC-2026-0211 (batch pipeline delay). Mean time to detect (MTTD) averaged 8.2 minutes; "
            f"mean time to resolve (MTTR) averaged 22 minutes. No data loss occurred. Engineering_IT "
            f"has implemented four preventative controls and updated the on-call runbook referenced in "
            f"Operations Standard Operating Procedures.",
        )
    )
    lines.extend(
        table_section(
            "Incident Summary Table",
            ["Incident ID", "Severity", "Duration", "Customers Affected", "Root Cause"],
            [
                ["INC-2026-0142", "SEV-2", "18 min", "340", "Connection pool exhaustion"],
                ["INC-2026-0187", "SEV-1", "12 min", "890", "Bad config deployment"],
                ["INC-2026-0211", "SEV-3", "17 min", "120", "Upstream vendor API timeout"],
            ],
        )
    )
    lines.extend(
        bullet_section(
            "Remediation Actions Completed",
            [
                "Increased API gateway connection pool limits from 200 to 500 (Engineering_IT)",
                "Added canary deployment gate requiring 5-minute soak test (Engineering_IT)",
                "Implemented circuit breaker for vendor integration Neura Connect (Engineering_IT)",
                "Updated incident communication templates per Operations Compliance Framework",
            ],
        )
    )
    lines.extend(
        scenario(
            "SEV-1 Authentication Outage (INC-2026-0187)",
            "On March 12, 2026 at 09:14 PST, the authentication microservice began returning HTTP 503 "
            "errors after a configuration change removed a required TLS certificate reference. PagerDuty "
            "alert fired at 09:17. On-call engineer James Okonkwo's team rolled back the deployment "
            "within 9 minutes. Customer Success notified 890 affected enterprise accounts per the "
            "Executive crisis communication protocol. Post-incident review assigned action items to "
            "Finance (vendor SLA credit verification) and Human_Resources (on-call compensation review).",
        )
    )
    lines.extend(
        definitions(
            {
                "SEV-1": "Critical incident with complete service unavailability or data integrity risk.",
                "MTTR": "Mean Time to Resolve: elapsed time from detection to service restoration.",
                "PIR": "Post-Incident Review: structured analysis conducted within 5 business days.",
                "War Room": "Cross-functional bridge for SEV-1 incidents including Engineering, Operations, and Executive.",
            }
        )
    )
    lines.extend(
        approval_workflow(
            [
                "Incident Commander documents timeline within 24 hours",
                "Engineering Manager reviews and signs off within 48 hours",
                "CTO approves final PIR and action item owners",
                "Operations receives copy for Compliance Framework audit trail",
            ]
        )
    )
    lines.extend(
        cross_refs(
            "Operations/Standard Operating Procedures.pdf - incident escalation steps",
            "Engineering_IT/Information Security Policy.pdf - breach notification criteria",
            "Executive/Enterprise Risk Assessment.pdf - technology risk register entry",
            "Finance/Annual Financial Report 2026.pdf - SLA penalty provisions",
        )
    )
    lines.extend(
        section(
            "Metrics and Targets",
            f"Q1 {FISCAL_YEAR} incident metrics: {CORPORATE['open_incidents_q1']} open incidents at quarter end, "
            "99.97% platform uptime (target 99.95%), 0 security breaches. Q2 targets: MTTD under 5 minutes, "
            "MTTR under 15 minutes for SEV-1, 100% PIR completion within SLA.",
        )
    )
    return lines


def build_information_security_policy() -> list[str]:
    lines = doc_header("Information Security Policy", "Engineering_IT")
    lines.extend(
        section(
            "Executive Summary",
            f"This policy establishes information security requirements for all {COMPANY} employees, "
            "contractors, and third parties handling corporate or customer data. It aligns with SOC 2 Type II, "
            "ISO 27001, and GDPR obligations referenced in Operations/Compliance Framework.pdf. "
            "Violations may result in disciplinary action per Human_Resources/Employee Handbook.pdf.",
        )
    )
    lines.extend(
        bullet_section(
            "Policy Statements",
            [
                "All production systems must enforce multi-factor authentication (MFA)",
                "Customer data must be encrypted at rest (AES-256) and in transit (TLS 1.3)",
                "Access reviews conducted quarterly for all privileged accounts",
                "Security incidents must be reported within 1 hour to security@neura.ai",
                "Personal devices require MDM enrollment before accessing corporate resources",
                "Password minimum length: 14 characters with complexity requirements",
            ],
        )
    )
    lines.extend(
        table_section(
            "Data Classification Levels",
            ["Level", "Examples", "Handling Requirements", "Approval for External Share"],
            [
                ["Public", "Marketing materials, press releases", "No restrictions", "CMO approval"],
                ["Internal", "Org charts, internal memos", "Employee access only", "Manager approval"],
                ["Confidential", "Financial reports, customer contracts", "Role-based access", "VP approval"],
                ["Restricted", "PII, encryption keys, M&A data", "Need-to-know, logged access", "CISO + Legal"],
            ],
        )
    )
    lines.extend(
        scenario(
            "Phishing Attempt Response",
            "An employee receives a suspicious email impersonating Finance requesting wire transfer details. "
            "The employee reports via the Phish Alert button. Security Operations isolates the message, "
            "blocks the sender domain, and scans affected mailboxes within 30 minutes. Human_Resources "
            "sends company-wide awareness reminder. No credentials were compromised.",
        )
    )
    lines.extend(
        approval_workflow(
            [
                "Policy draft by CISO (Engineering_IT)",
                "Legal and Compliance review (Operations)",
                "CFO approval for financial data handling sections",
                "CEO sign-off for Restricted classification procedures",
                "Annual review by Audit Committee (Executive/Board Performance Report)",
            ]
        )
    )
    lines.extend(cross_refs("Operations/Compliance Framework.pdf", "Human_Resources/Employee Handbook.pdf"))
    return lines


def build_software_development_standards() -> list[str]:
    lines = doc_header("Software Development Standards", "Engineering_IT")
    lines.extend(
        section(
            "Executive Summary",
            f"These standards govern software development across {COMPANY}'s {CORPORATE['engineering_headcount']} "
            "engineers building the Neura Platform, Neura Insights, and Neura Connect products. "
            "Compliance is mandatory for all code merged to main branches.",
        )
    )
    lines.extend(
        bullet_section(
            "Coding Standards",
            [
                "Python: PEP 8, type hints required, 80% unit test coverage minimum",
                "TypeScript: ESLint strict mode, no any types in production code",
                "All APIs must follow OpenAPI 3.0 specification with versioning",
                "Database migrations require DBA review for tables exceeding 10M rows",
                "Feature flags required for all user-facing changes",
                "Dependency updates: critical CVE patches within 72 hours",
            ],
        )
    )
    lines.extend(
        table_section(
            "CI/CD Quality Gates",
            ["Gate", "Requirement", "Tool", "Blocking"],
            [
                ["Unit Tests", ">= 80% coverage", "pytest / vitest", "Yes"],
                ["SAST Scan", "Zero critical findings", "Semgrep", "Yes"],
                ["Integration Tests", "All pass", "GitHub Actions", "Yes"],
                ["Performance", "p95 < 200ms", "k6", "SEV-1 features only"],
                ["Security Review", "Threat model for new services", "Manual", "Yes"],
            ],
        )
    )
    lines.extend(
        scenario(
            "Production Hotfix Process",
            "A critical bug in the billing module requires emergency patch. Engineer creates hotfix branch, "
            "obtains Engineering Manager approval, runs abbreviated CI pipeline, deploys via canary to 5% "
            "traffic, monitors for 15 minutes, then promotes. Finance notified if billing calculations affected.",
        )
    )
    lines.extend(
        definitions(
            {
                "Trunk-Based Development": "Short-lived feature branches merged to main at least daily.",
                "Definition of Done": "Code reviewed, tested, documented, deployed, and monitored.",
                "ADR": "Architecture Decision Record documenting significant technical choices.",
            }
        )
    )
    lines.extend(cross_refs("Engineering_IT/System Architecture Documentation.pdf", "Finance/Budget Allocation Policy.pdf"))
    return lines


def build_system_architecture_documentation() -> list[str]:
    lines = doc_header("System Architecture Documentation", "Engineering_IT")
    lines.extend(
        section(
            "Executive Summary",
            f"{COMPANY} platform architecture supports {CORPORATE['customer_count']} enterprise customers "
            f"processing 2.4M API requests daily with 99.97% uptime. The system runs on AWS us-west-2 "
            "primary with us-east-1 disaster recovery failover (RTO: 15 minutes, RPO: 5 minutes).",
        )
    )
    lines.extend(
        bullet_section(
            "Core Components",
            [
                "API Gateway (Kong): Rate limiting, authentication, request routing",
                "Neura Core Service (Python/FastAPI): RAG pipeline, LLM orchestration",
                "Vector Store (Qdrant): Document embeddings, semantic search",
                "Document Processor: PDF/text ingestion, chunking (600 tokens, 120 overlap)",
                "Auth Service (OAuth 2.0/OIDC): RBAC with department-level access control",
                "Analytics Pipeline (Kafka + Spark): Usage metrics, billing events",
            ],
        )
    )
    lines.extend(
        table_section(
            "Service Inventory",
            ["Service", "Language", "Replicas", "CPU/Memory", "Owner Team"],
            [
                ["neura-api", "Python", "12", "2 vCPU / 4GB", "Platform"],
                ["neura-ingest", "Python", "4", "4 vCPU / 8GB", "Platform"],
                ["neura-auth", "Go", "6", "1 vCPU / 2GB", "Security"],
                ["neura-web", "TypeScript", "8", "1 vCPU / 2GB", "Frontend"],
                ["neura-analytics", "Scala", "3", "4 vCPU / 16GB", "Data"],
            ],
        )
    )
    lines.extend(
        section(
            "Data Flow",
            "User query -> API Gateway -> Auth Service (role validation) -> Neura Core Service -> "
            "Qdrant (filtered vector search by allowed_roles) -> LLM (Gemini) -> Response with source citations. "
            "Document upload -> Document Processor -> chunking -> embedding (all-MiniLM-L6-v2) -> Qdrant indexing.",
        )
    )
    lines.extend(cross_refs("Engineering_IT/Information Security Policy.pdf", "Marketing/Brand Guidelines.pdf"))
    return lines


# ---------------------------------------------------------------------------
# Executive documents
# ---------------------------------------------------------------------------


def build_board_performance_report() -> list[str]:
    lines = doc_header("Board Performance Report", "Executive")
    lines.extend(
        section(
            "Executive Summary",
            f"The {COMPANY} Board of Directors held 4 meetings in Q1 {FISCAL_YEAR}. Key outcomes include "
            f"approval of the ${CORPORATE['revenue_forecast_fy2026']} revenue target, authorization of a "
            f"${CORPORATE['marketing_budget_fy2026']} marketing investment, and appointment of two "
            "independent directors. Board attendance averaged 96%. All governance obligations met.",
        )
    )
    lines.extend(
        table_section(
            "Board KPI Dashboard",
            ["Metric", "Q1 Actual", "Q1 Target", "FY2026 Target", "Trend"],
            [
                ["Revenue (ARR)", "$36.2M", "$34.0M", "$198.7M", "Above"],
                ["Net Revenue Retention", "118%", "115%", "120%", "Above"],
                ["Gross Margin", "72.1%", "70.0%", "73.0%", "Above"],
                ["Employee Engagement", "82%", "80%", "85%", "On Track"],
                ["Customer NPS", "62", "60", "65", "On Track"],
            ],
        )
    )
    lines.extend(
        bullet_section(
            "Board Resolutions Q1 2026",
            [
                "RES-2026-001: Approved FY2026 operating budget ($168.4M total expenditure)",
                "RES-2026-002: Authorized Series C extension ($45M) for international expansion",
                "RES-2026-003: Ratified executive compensation per HR Performance Management Framework",
                "RES-2026-004: Approved acquisition diligence budget for AI startup target",
            ],
        )
    )
    lines.extend(cross_refs("Finance/Annual Financial Report 2026.pdf", "Executive/Corporate Strategy 2026.pdf"))
    return lines


def build_corporate_strategy_2026() -> list[str]:
    lines = doc_header("Corporate Strategy 2026", "Executive")
    lines.extend(
        section(
            "Executive Summary",
            f"{COMPANY}'s 2026 strategy focuses on three pillars: Enterprise AI Leadership, "
            f"International Expansion, and Platform Ecosystem Growth. Target: ${CORPORATE['revenue_forecast_fy2026']} "
            f"ARR with {CORPORATE['ebitda_margin']} EBITDA margin by year-end.",
        )
    )
    lines.extend(
        bullet_section(
            "Strategic Pillars",
            [
                "Pillar 1 - Enterprise AI Leadership: Launch Neura Agent Studio for custom AI workflows",
                "Pillar 2 - International Expansion: Enter UK, DACH, and APAC markets (3 new offices)",
                "Pillar 3 - Platform Ecosystem: 50+ integration partners via Neura Connect marketplace",
                "Cross-cutting: Achieve SOC 2 Type II and ISO 27001 certification",
                "Talent: Grow headcount from 847 to 1,100 while maintaining culture scores above 80%",
            ],
        )
    )
    lines.extend(
        table_section(
            "Strategic Initiative Portfolio",
            ["Initiative", "Investment", "Expected ROI", "Owner", "Status"],
            [
                ["Neura Agent Studio", "$8.2M", "3.2x", "CTO", "In Progress"],
                ["EMEA Go-to-Market", "$6.5M", "2.8x", "CMO", "Planning"],
                ["Connect Marketplace", "$3.1M", "4.1x", "COO", "In Progress"],
                ["Enterprise Security+", "$2.4M", "Risk Reduction", "CISO", "In Progress"],
            ],
        )
    )
    lines.extend(cross_refs("Marketing/Marketing Strategy 2026.pdf", "Executive/Five Year Business Roadmap.pdf"))
    return lines


def build_enterprise_risk_assessment() -> list[str]:
    lines = doc_header("Enterprise Risk Assessment", "Executive")
    lines.extend(
        section(
            "Executive Summary",
            f"This assessment identifies 24 enterprise risks across {COMPANY}'s operations. "
            "4 risks rated High, 12 Medium, 8 Low. Top risks: AI regulatory changes, key talent retention, "
            "competitive pressure from hyperscaler AI offerings, and third-party vendor concentration.",
        )
    )
    lines.extend(
        table_section(
            "Top Enterprise Risks",
            ["Risk ID", "Category", "Likelihood", "Impact", "Rating", "Mitigation Owner"],
            [
                ["ER-001", "Regulatory", "Medium", "High", "High", "General Counsel"],
                ["ER-002", "Talent", "High", "Medium", "High", "CHRO"],
                ["ER-003", "Competitive", "High", "High", "High", "CEO"],
                ["ER-004", "Vendor", "Medium", "High", "High", "COO"],
                ["ER-005", "Cybersecurity", "Low", "High", "Medium", "CISO"],
            ],
        )
    )
    lines.extend(
        scenario(
            "AI Regulation Scenario",
            "EU AI Act enforcement requires Neura Platform classification review. Legal assesses product "
            "as 'limited risk' system. Engineering implements transparency disclosures. Marketing updates "
            "customer communications. Estimated compliance cost: $420K.",
        )
    )
    lines.extend(cross_refs("Operations/Risk Management Register.pdf", "Engineering_IT/Information Security Policy.pdf"))
    return lines


def build_five_year_business_roadmap() -> list[str]:
    lines = doc_header("Five Year Business Roadmap", "Executive")
    lines.extend(
        section(
            "Executive Summary",
            f"This roadmap outlines {COMPANY}'s growth trajectory from FY2026 (${CORPORATE['revenue_forecast_fy2026']} "
            "ARR) to FY2030 ($850M ARR target). The plan assumes continued enterprise AI adoption, "
            "successful international expansion, and maintenance of net revenue retention above 115%.",
        )
    )
    lines.extend(
        table_section(
            "Five-Year Milestones",
            ["Year", "ARR Target", "Headcount", "Markets", "Key Milestone"],
            [
                ["2026", "$198.7M", "1,100", "US, UK", "Agent Studio launch"],
                ["2027", "$310M", "1,600", "+ DACH", "ISO 27001 certified"],
                ["2028", "$450M", "2,200", "+ APAC", "IPO readiness assessment"],
                ["2029", "$620M", "2,800", "Global", "Platform marketplace 200+ partners"],
                ["2030", "$850M", "3,500", "Global", "Category leader in enterprise AI"],
            ],
        )
    )
    lines.extend(cross_refs("Executive/Corporate Strategy 2026.pdf", "Finance/Revenue Forecast Report.pdf"))
    return lines


# ---------------------------------------------------------------------------
# Finance documents
# ---------------------------------------------------------------------------


def build_annual_financial_report() -> list[str]:
    lines = doc_header("Annual Financial Report 2026", "Finance")
    lines.extend(
        section(
            "Executive Summary",
            f"{COMPANY} delivered strong financial performance in FY2025 with {CORPORATE['revenue_fy2025']} ARR, "
            f"representing 39% year-over-year growth. Gross margin improved to 72.1%. Operating cash flow "
            f"was $18.7M. FY2026 guidance: {CORPORATE['revenue_forecast_fy2026']} ARR with {CORPORATE['ebitda_margin']} EBITDA margin.",
        )
    )
    lines.extend(
        table_section(
            "Income Statement Summary (USD millions)",
            ["Line Item", "FY2024", "FY2025", "FY2026 Forecast", "YoY Growth"],
            [
                ["Total Revenue", "$102.4", "$142.3", "$198.7", "+39.6%"],
                ["Cost of Revenue", "$32.8", "$39.7", "$53.6", "+19.1%"],
                ["Gross Profit", "$69.6", "$102.6", "$145.1", "+47.4%"],
                ["Operating Expenses", "$78.2", "$96.4", "$128.9", "+23.4%"],
                ["EBITDA", "$12.1", "$26.2", "$36.6", "+39.7%"],
                ["Net Income", "$4.8", "$14.1", "$22.4", "+58.9%"],
            ],
        )
    )
    lines.extend(
        table_section(
            "Revenue by Segment",
            ["Segment", "FY2025 Revenue", "% of Total", "Growth Rate"],
            [
                ["Neura Platform (SaaS)", "$98.6M", "69.3%", "+42%"],
                ["Neura Insights (Analytics)", "$28.4M", "20.0%", "+35%"],
                ["Neura Connect (Integrations)", "$15.3M", "10.7%", "+28%"],
            ],
        )
    )
    lines.extend(cross_refs("Finance/Revenue Forecast Report.pdf", "Finance/Budget Allocation Policy.pdf"))
    return lines


def build_budget_allocation_policy() -> list[str]:
    lines = doc_header("Budget Allocation Policy", "Finance")
    lines.extend(
        section(
            "Executive Summary",
            "This policy defines how Neura AI allocates, approves, and monitors departmental budgets. "
            f"Total FY2026 operating budget: $168.4M. Engineering_IT receives the largest allocation "
            f"at ${CORPORATE['it_budget_fy2026']} (13.5%), followed by Sales & Marketing at $28.6M (17.0%).",
        )
    )
    lines.extend(
        table_section(
            "FY2026 Department Budget Allocation",
            ["Department", "Budget (USD)", "% of Total", "Headcount", "Budget per FTE"],
            [
                ["Engineering_IT", "$22.8M", "13.5%", "312", "$73,077"],
                ["Sales & Marketing", "$28.6M", "17.0%", "186", "$153,763"],
                ["Operations", "$12.4M", "7.4%", "98", "$126,531"],
                ["Human_Resources", "$6.2M", "3.7%", "42", "$147,619"],
                ["Finance", "$4.8M", "2.8%", "38", "$126,316"],
                ["Executive/G&A", "$8.6M", "5.1%", "24", "$358,333"],
                ["R&D (Capitalized)", "$14.2M", "8.4%", "N/A", "N/A"],
                ["Infrastructure/COGS", "$70.8M", "42.0%", "N/A", "N/A"],
            ],
        )
    )
    lines.extend(
        approval_workflow(
            [
                "Department heads submit annual budget requests by October 1",
                "Finance consolidates and models scenarios by November 1",
                "CFO presents to Executive Leadership Team by November 15",
                "Board approves final budget at December meeting",
                "Quarterly reforecasts due 15th of Jan, Apr, Jul, Oct",
            ]
        )
    )
    lines.extend(cross_refs("Finance/Expense Management Policy.pdf", "Executive/Board Performance Report.pdf"))
    return lines


def build_expense_management_policy() -> list[str]:
    lines = doc_header("Expense Management Policy", "Finance")
    lines.extend(
        section(
            "Executive Summary",
            "This policy governs employee business expenses, reimbursement procedures, and spending limits "
            "for all Neura AI personnel. Effective immediately. Non-compliance may result in delayed reimbursement "
            "or disciplinary action per Human_Resources/Employee Handbook.pdf.",
        )
    )
    lines.extend(
        table_section(
            "Expense Limits and Approval Thresholds",
            ["Category", "Daily Limit", "Requires Pre-Approval", "Approver"],
            [
                ["Domestic Travel", "$350/day", "Trips > $2,000", "Direct Manager"],
                ["International Travel", "$500/day", "All trips", "Director + Finance"],
                ["Client Entertainment", "$150/person", "Events > $500", "VP + Finance"],
                ["Software/Tools", "$200/month", "Subscriptions > $200/mo", "Manager"],
                ["Office Supplies", "$100/purchase", "Purchases > $500", "Office Manager"],
                ["Training/Conferences", "$3,000/event", "All external events", "Manager + HR"],
            ],
        )
    )
    lines.extend(
        bullet_section(
            "Reimbursement Procedures",
            [
                "Submit expenses within 30 days via ExpensePro system",
                "Attach itemized receipts for all expenses over $25",
                "Use corporate card for purchases over $100 when available",
                "Finance processes reimbursements within 10 business days",
                "Audit sampling: 15% of submissions reviewed monthly",
            ],
        )
    )
    lines.extend(
        scenario(
            "Conference Travel Expense",
            "Engineering manager attends AI Summit 2026 in New York. Pre-approval obtained for $2,800 "
            "(registration $1,200, flight $900, hotel $700). Submits ExpensePro report with receipts "
            "within 14 days. Finance approves in 3 business days. Amount coded to Engineering_IT budget.",
        )
    )
    lines.extend(cross_refs("Human_Resources/Payroll and Benefits Policy.pdf", "Finance/Budget Allocation Policy.pdf"))
    return lines


def build_revenue_forecast_report() -> list[str]:
    lines = doc_header("Revenue Forecast Report", "Finance")
    lines.extend(
        section(
            "Executive Summary",
            f"Finance projects {COMPANY} FY2026 revenue at {CORPORATE['revenue_forecast_fy2026']} ARR "
            "(baseline scenario), with upside of $215M (+8.2%) and downside of $178M (-10.4%). "
            "Key drivers: new logo acquisition (target 280), net revenue retention (118%), and average "
            "contract value increase (8%).",
        )
    )
    lines.extend(
        table_section(
            "Quarterly Revenue Forecast (USD millions)",
            ["Quarter", "Baseline", "Upside", "Downside", "New Logos", "Churn Rate"],
            [
                ["Q1 2026", "$36.2", "$38.1", "$33.8", "58", "2.1%"],
                ["Q2 2026", "$44.8", "$47.2", "$41.5", "72", "2.0%"],
                ["Q3 2026", "$52.1", "$55.4", "$47.9", "78", "1.9%"],
                ["Q4 2026", "$65.6", "$74.3", "$54.8", "72", "1.8%"],
            ],
        )
    )
    lines.extend(cross_refs("Marketing/Campaign Performance Report.pdf", "Executive/Corporate Strategy 2026.pdf"))
    return lines


# ---------------------------------------------------------------------------
# Human_Resources documents
# ---------------------------------------------------------------------------


def build_employee_handbook() -> list[str]:
    lines = doc_header("Employee Handbook", "Human_Resources")
    lines.extend(
        section(
            "Executive Summary",
            f"Welcome to {COMPANY}. This handbook outlines workplace policies, benefits, and expectations "
            f"for all {CORPORATE['employees']} employees. It supplements your employment agreement and "
            "should be read in conjunction with department-specific policies.",
        )
    )
    lines.extend(
        bullet_section(
            "Core Values",
            [
                "Innovation with Integrity: Push boundaries responsibly",
                "Customer Obsession: Every decision starts with customer impact",
                "Inclusive Excellence: Diverse teams build better AI",
                "Transparent Communication: Default to open, document decisions",
                "Continuous Learning: Invest in growth at every level",
            ],
        )
    )
    lines.extend(
        table_section(
            "Leave Entitlements",
            ["Leave Type", "Full-Time", "Part-Time (>= 20hr)", "Notes"],
            [
                ["PTO", "20 days/year", "Pro-rated", "Accrues monthly"],
                ["Sick Leave", "10 days/year", "Pro-rated", "No doctor note required < 3 days"],
                ["Parental Leave", "16 weeks paid", "16 weeks paid", "All parents eligible"],
                ["Bereavement", "5 days", "5 days", "Extended for immediate family"],
                ["Volunteer Day", "2 days/year", "1 day/year", "Approved nonprofits only"],
            ],
        )
    )
    lines.extend(cross_refs("Human_Resources/Payroll and Benefits Policy.pdf", "Engineering_IT/Information Security Policy.pdf"))
    return lines


def build_payroll_benefits_policy() -> list[str]:
    lines = doc_header("Payroll and Benefits Policy", "Human_Resources")
    lines.extend(
        section(
            "Executive Summary",
            f"This policy describes compensation, payroll schedules, and benefit programs for {COMPANY} "
            "employees. Total compensation philosophy: market 75th percentile base + equity + benefits. "
            "Annual compensation review cycle aligned with Performance Management Framework.",
        )
    )
    lines.extend(
        table_section(
            "Benefits Summary",
            ["Benefit", "Employee Cost", "Company Contribution", "Eligibility"],
            [
                ["Medical (PPO/HMO)", "$180/month", "85% of premium", "Day 1"],
                ["Dental", "$25/month", "100% employee", "Day 1"],
                ["Vision", "$10/month", "100% employee", "Day 1"],
                ["401(k) Match", "N/A", "4% match", "After 90 days"],
                ["Life Insurance", "N/A", "2x salary", "Day 1"],
                ["Equity (RSU)", "N/A", "Varies by level", "Offer letter"],
            ],
        )
    )
    lines.extend(
        bullet_section(
            "Payroll Schedule",
            [
                "Bi-weekly pay periods (26 per year)",
                "Direct deposit required for all employees",
                "Pay dates: every other Friday",
                "Expense reimbursements processed separately within 10 business days",
                "W-2 available by January 31 annually",
            ],
        )
    )
    lines.extend(cross_refs("Finance/Expense Management Policy.pdf", "Human_Resources/Performance Management Framework.pdf"))
    return lines


def build_performance_management_framework() -> list[str]:
    lines = doc_header("Performance Management Framework", "Human_Resources")
    lines.extend(
        section(
            "Executive Summary",
            "Neura AI's performance management framework ensures fair, consistent evaluation and development "
            "of all employees. Cycle: annual goal setting (January), mid-year check-in (July), year-end review "
            "(December). Calibration sessions ensure rating consistency across departments.",
        )
    )
    lines.extend(
        table_section(
            "Performance Rating Scale",
            ["Rating", "Label", "Description", "Compensation Impact"],
            [
                ["5", "Exceptional", "Consistently exceeds all expectations", "150-200% target bonus"],
                ["4", "Exceeds", "Regularly exceeds most expectations", "125-150% target bonus"],
                ["3", "Meets", "Consistently meets expectations", "100% target bonus"],
                ["2", "Developing", "Partially meets expectations", "0-50% target bonus + PIP"],
                ["1", "Unsatisfactory", "Does not meet expectations", "PIP or separation"],
            ],
        )
    )
    lines.extend(
        scenario(
            "Mid-Year Performance Check-In",
            "Engineering IC receives mid-year feedback from manager. Goals: deliver Agent Studio MVP (70% complete), "
            "mentor 2 junior engineers (on track), improve test coverage to 85% (currently 78%). "
            "Manager documents feedback in Workday. Employee updates development plan with training goals.",
        )
    )
    lines.extend(cross_refs("Human_Resources/Recruitment Guidelines.pdf", "Executive/Board Performance Report.pdf"))
    return lines


def build_recruitment_guidelines() -> list[str]:
    lines = doc_header("Recruitment Guidelines", "Human_Resources")
    lines.extend(
        section(
            "Executive Summary",
            f"These guidelines govern hiring practices at {COMPANY}. FY2026 hiring plan: 253 net new "
            f"positions across all departments. Time-to-fill target: 45 days. Diversity target: 40% "
            "underrepresented candidates in final interview panels.",
        )
    )
    lines.extend(
        table_section(
            "Hiring Approval Matrix",
            ["Level", "Comp Range", "Approver 1", "Approver 2", "Approver 3"],
            [
                ["IC1-IC3", "$80K-$140K", "Hiring Manager", "Director", "HR Business Partner"],
                ["IC4-IC5", "$140K-$220K", "Director", "VP", "CHRO"],
                ["Manager", "$160K-$250K", "VP", "CHRO", "CEO (if VP+)"],
                ["Director+", "$200K-$350K", "CHRO", "CEO", "Board Comp Committee"],
            ],
        )
    )
    lines.extend(cross_refs("Human_Resources/Employee Handbook.pdf", "Finance/Budget Allocation Policy.pdf"))
    return lines


# ---------------------------------------------------------------------------
# Marketing documents
# ---------------------------------------------------------------------------


def build_brand_guidelines() -> list[str]:
    lines = doc_header("Brand Guidelines", "Marketing")
    lines.extend(
        section(
            "Executive Summary",
            f"This document defines the {COMPANY} brand identity including visual standards, messaging "
            "framework, and tone of voice. All internal and external communications must comply. "
            "Questions: brand@neura.ai.",
        )
    )
    lines.extend(
        bullet_section(
            "Brand Identity",
            [
                "Primary Color: Neura Blue (#2563EB) - trust, intelligence, reliability",
                "Secondary Color: Neural Purple (#7C3AED) - innovation, creativity",
                "Accent Color: Synapse Green (#10B981) - growth, success",
                "Primary Font: Inter (headings and body)",
                "Logo: Neura wordmark with neural network icon - minimum clear space: 1x icon height",
                "Tagline: 'Intelligence, Amplified.'",
            ],
        )
    )
    lines.extend(
        table_section(
            "Tone of Voice by Audience",
            ["Audience", "Tone", "Example", "Avoid"],
            [
                ["Enterprise Buyers", "Authoritative, ROI-focused", "Reduce costs 40% with AI", "Hype, jargon"],
                ["Developers", "Technical, precise", "API-first RAG pipeline", "Marketing fluff"],
                ["Executives", "Strategic, concise", "Board-ready AI governance", "Feature lists"],
                ["General Public", "Accessible, inspiring", "AI that works for everyone", "Fear-based messaging"],
            ],
        )
    )
    lines.extend(cross_refs("Marketing/Marketing Strategy 2026.pdf", "Executive/Corporate Strategy 2026.pdf"))
    return lines


def build_campaign_performance_report() -> list[str]:
    lines = doc_header("Campaign Performance Report", "Marketing")
    lines.extend(
        section(
            "Executive Summary",
            "Q1 2026 'AI Transformation Summit' campaign results: $1.2M spend, 2,840 MQLs generated, "
            "142 SQLs, 38 closed-won deals ($4.8M pipeline influenced). Campaign ROI: 4.0x. "
            "Best performing channel: LinkedIn (42% of MQLs). Recommendation: increase LinkedIn budget 25% for Q2.",
        )
    )
    lines.extend(
        table_section(
            "Channel Performance",
            ["Channel", "Spend", "Impressions", "CTR", "MQLs", "CPL", "ROI"],
            [
                ["LinkedIn", "$480K", "2.4M", "2.8%", "1,193", "$402", "5.2x"],
                ["Google Ads", "$320K", "1.8M", "3.1%", "852", "$375", "3.8x"],
                ["Events", "$280K", "N/A", "N/A", "485", "$577", "3.2x"],
                ["Content/SEO", "$120K", "890K", "4.2%", "310", "$387", "4.5x"],
            ],
        )
    )
    lines.extend(cross_refs("Marketing/Marketing Strategy 2026.pdf", "Finance/Revenue Forecast Report.pdf"))
    return lines


def build_customer_insights_report() -> list[str]:
    lines = doc_header("Customer Insights Report", "Marketing")
    lines.extend(
        section(
            "Executive Summary",
            f"Based on Q1 2026 research (n=450 customer interviews, NPS survey n=1,240), {COMPANY} "
            f"customers value accuracy (89%), integration ease (82%), and security (78%) most highly. "
            f"NPS score: {CORPORATE['nps_score']} (industry benchmark: 45). Primary churn driver: "
            "insufficient onboarding support (34% of churned accounts).",
        )
    )
    lines.extend(
        table_section(
            "Customer Segments",
            ["Segment", "Count", "Avg ACV", "NPS", "Top Need", "Growth Potential"],
            [
                ["Enterprise (>1000 emp)", "186", "$285K", "68", "Custom integrations", "High"],
                ["Mid-Market (200-1000)", "524", "$72K", "61", "Ease of deployment", "High"],
                ["SMB (<200 emp)", "530", "$18K", "55", "Affordable pricing", "Medium"],
            ],
        )
    )
    lines.extend(cross_refs("Marketing/Marketing Strategy 2026.pdf", "Operations/Standard Operating Procedures.pdf"))
    return lines


def build_marketing_strategy_2026() -> list[str]:
    lines = doc_header("Marketing Strategy 2026", "Marketing")
    lines.extend(
        section(
            "Executive Summary",
            f"{COMPANY} Marketing FY2026 strategy targets 280 new logos and ${CORPORATE['revenue_forecast_fy2026']} "
            f"pipeline contribution. Total budget: {CORPORATE['marketing_budget_fy2026']}. "
            "Focus areas: enterprise ABM, developer community, international launch support.",
        )
    )
    lines.extend(
        table_section(
            "Marketing Budget Allocation",
            ["Category", "Budget", "% of Total", "KPI Target"],
            [
                ["Digital Advertising", "$4.8M", "33.8%", "3,500 MQLs"],
                ["Events & Conferences", "$3.2M", "22.5%", "48 events, 2,400 leads"],
                ["Content & SEO", "$2.1M", "14.8%", "Organic traffic +40%"],
                ["Brand & Creative", "$1.6M", "11.3%", "Brand awareness +15%"],
                ["ABM Platform", "$1.4M", "9.9%", "120 enterprise targets"],
                ["International Launch", "$1.1M", "7.7%", "UK market entry"],
            ],
        )
    )
    lines.extend(cross_refs("Executive/Corporate Strategy 2026.pdf", "Marketing/Campaign Performance Report.pdf"))
    return lines


# ---------------------------------------------------------------------------
# Operations documents
# ---------------------------------------------------------------------------


def build_compliance_framework() -> list[str]:
    lines = doc_header("Compliance Framework", "Operations")
    lines.extend(
        section(
            "Executive Summary",
            f"{COMPANY} Compliance Framework ensures adherence to regulatory requirements across all "
            "operating jurisdictions. Current certifications: SOC 2 Type II (renewed Jan 2026), GDPR compliant. "
            "In progress: ISO 27001 (target Q3 2026). 12 compliance controls audited quarterly.",
        )
    )
    lines.extend(
        table_section(
            "Compliance Control Status",
            ["Control ID", "Description", "Owner", "Status", "Last Audit", "Next Review"],
            [
                ["CC-001", "Access Control Management", "CISO", "Effective", "2026-01-15", "2026-04-15"],
                ["CC-002", "Data Encryption Standards", "Engineering", "Effective", "2026-01-15", "2026-04-15"],
                ["CC-003", "Vendor Risk Assessment", "Procurement", "Effective", "2026-02-01", "2026-05-01"],
                ["CC-004", "Incident Response Plan", "Operations", "Effective", "2026-01-20", "2026-04-20"],
                ["CC-005", "Employee Training Program", "HR", "Needs Improvement", "2026-02-15", "2026-05-15"],
            ],
        )
    )
    lines.extend(cross_refs("Engineering_IT/Information Security Policy.pdf", "Operations/Risk Management Register.pdf"))
    return lines


def build_risk_management_register() -> list[str]:
    lines = doc_header("Risk Management Register", "Operations")
    lines.extend(
        section(
            "Executive Summary",
            "The Operations Risk Management Register tracks 47 operational risks across supply chain, "
            "vendor, regulatory, process, and technology categories. 3 risks currently rated Critical, "
            "requiring monthly executive review. Last updated: March 2026.",
        )
    )
    lines.extend(
        table_section(
            "Critical Operational Risks",
            ["Risk ID", "Description", "Likelihood", "Impact", "Owner", "Mitigation Status"],
            [
                ["OPR-001", "Single cloud provider dependency (AWS)", "Low", "Critical", "CTO", "Multi-cloud POC"],
                ["OPR-002", "Key vendor SLA breach (embedding API)", "Medium", "High", "COO", "Fallback provider"],
                ["OPR-003", "Regulatory audit finding (GDPR)", "Medium", "High", "DPO", "Remediation 80% done"],
                ["OPR-004", "Supply chain disruption (hardware)", "Low", "Medium", "Procurement", "Dual sourcing"],
                ["OPR-005", "Business continuity plan untested", "Medium", "High", "COO", "DR drill Q2 2026"],
            ],
        )
    )
    lines.extend(cross_refs("Executive/Enterprise Risk Assessment.pdf", "Operations/Compliance Framework.pdf"))
    return lines


def build_standard_operating_procedures() -> list[str]:
    lines = doc_header("Standard Operating Procedures", "Operations")
    lines.extend(
        section(
            "Executive Summary",
            "This document contains core Standard Operating Procedures (SOPs) for Neura AI Operations. "
            "All procedures require annual review and version control. Training completion tracked in LMS.",
        )
    )
    lines.extend(
        bullet_section(
            "SOP-001: Incident Escalation",
            [
                "Step 1: On-call engineer acknowledges alert within 5 minutes",
                "Step 2: Assess severity using SEV-1 through SEV-4 matrix",
                "Step 3: SEV-1/2: Open war room bridge, notify Incident Commander",
                "Step 4: SEV-1: Notify CEO, CFO, and Customer Success VP within 15 minutes",
                "Step 5: Document timeline in incident tracker (Jira)",
                "Step 6: Post-incident review within 5 business days",
            ],
        )
    )
    lines.extend(
        bullet_section(
            "SOP-002: Vendor Onboarding",
            [
                "Step 1: Submit vendor request via Procurement portal",
                "Step 2: Complete security questionnaire (InfoSec review)",
                "Step 3: Legal reviews contract terms and DPA",
                "Step 4: Finance validates budget and payment terms",
                "Step 5: Operations adds vendor to approved supplier list",
                "Step 6: Annual vendor performance review",
            ],
        )
    )
    lines.extend(
        scenario(
            "SEV-2 Incident Escalation",
            "Database replication lag exceeds 30 seconds (SEV-2). On-call DBA acknowledges at T+3min, "
            "opens bridge at T+5min, notifies Engineering Manager. Root cause identified at T+18min "
            "(network partition). Failover to replica completed at T+25min. Customer notification sent. "
            "PIR scheduled for next business day.",
        )
    )
    lines.extend(cross_refs("Engineering_IT/Incident Management Report.pdf", "Operations/Supplier Management Policy.pdf"))
    return lines


def build_supplier_management_policy() -> list[str]:
    lines = doc_header("Supplier Management Policy", "Operations")
    lines.extend(
        section(
            "Executive Summary",
            f"This policy governs supplier selection, onboarding, performance management, and offboarding "
            f"for {COMPANY}. Active suppliers: 142. Total supplier spend FY2025: $38.6M. "
            "Strategic suppliers (Tier 1): 18 requiring quarterly business reviews.",
        )
    )
    lines.extend(
        table_section(
            "Supplier Tier Classification",
            ["Tier", "Criteria", "Review Frequency", "Count", "Total Spend"],
            [
                ["Tier 1 - Strategic", "Business-critical, >$1M/yr", "Quarterly", "18", "$28.4M"],
                ["Tier 2 - Important", "Operational need, $100K-$1M", "Semi-annual", "42", "$8.2M"],
                ["Tier 3 - Standard", "Commodity, <$100K", "Annual", "82", "$2.0M"],
            ],
        )
    )
    lines.extend(
        approval_workflow(
            [
                "Requester submits supplier evaluation form",
                "Procurement conducts due diligence (financial, security, references)",
                "Legal reviews contract and data processing agreement",
                "Finance approves budget allocation",
                "COO approves Tier 1 supplier contracts",
                "Vendor added to approved supplier registry",
            ]
        )
    )
    lines.extend(cross_refs("Operations/Compliance Framework.pdf", "Finance/Budget Allocation Policy.pdf"))
    return lines


# ---------------------------------------------------------------------------
# Document registry
# ---------------------------------------------------------------------------

DEPARTMENT_DOCS: dict[str, list[DocumentSpec]] = {
    "Engineering_IT": [
        DocumentSpec(
            "Incident Management Report",
            "Incident Report",
            "Internal",
            ["engineering", "employee", "manager", "executive", "operations"],
            "1.0",
            build_incident_management_report,
        ),
        DocumentSpec(
            "Information Security Policy",
            "Policy",
            "Confidential",
            ["engineering", "employee", "manager", "executive", "hr"],
            "2.1",
            build_information_security_policy,
        ),
        DocumentSpec(
            "Software Development Standards",
            "Technical Standard",
            "Internal",
            ["engineering", "employee", "manager"],
            "1.3",
            build_software_development_standards,
        ),
        DocumentSpec(
            "System Architecture Documentation",
            "Technical Documentation",
            "Confidential",
            ["engineering", "manager", "executive"],
            "3.0",
            build_system_architecture_documentation,
        ),
    ],
    "Executive": [
        DocumentSpec(
            "Board Performance Report",
            "Board Report",
            "Restricted",
            ["executive", "finance"],
            "1.0",
            build_board_performance_report,
        ),
        DocumentSpec(
            "Corporate Strategy 2026",
            "Strategy Document",
            "Confidential",
            ["executive", "employee", "manager", "finance", "marketing"],
            "1.0",
            build_corporate_strategy_2026,
        ),
        DocumentSpec(
            "Enterprise Risk Assessment",
            "Risk Assessment",
            "Confidential",
            ["executive", "manager", "finance", "operations"],
            "1.1",
            build_enterprise_risk_assessment,
        ),
        DocumentSpec(
            "Five Year Business Roadmap",
            "Roadmap",
            "Confidential",
            ["executive", "manager", "finance"],
            "1.0",
            build_five_year_business_roadmap,
        ),
    ],
    "Finance": [
        DocumentSpec(
            "Annual Financial Report 2026",
            "Financial Report",
            "Confidential",
            ["finance", "executive", "manager"],
            "1.0",
            build_annual_financial_report,
        ),
        DocumentSpec(
            "Budget Allocation Policy",
            "Policy",
            "Internal",
            ["finance", "employee", "manager", "executive"],
            "1.2",
            build_budget_allocation_policy,
        ),
        DocumentSpec(
            "Expense Management Policy",
            "Policy",
            "Internal",
            ["finance", "employee", "manager"],
            "1.0",
            build_expense_management_policy,
        ),
        DocumentSpec(
            "Revenue Forecast Report",
            "Forecast Report",
            "Confidential",
            ["finance", "executive", "marketing", "manager"],
            "1.0",
            build_revenue_forecast_report,
        ),
    ],
    "Human_Resources": [
        DocumentSpec(
            "Employee Handbook",
            "Handbook",
            "Internal",
            ["hr", "employee", "manager"],
            "4.0",
            build_employee_handbook,
        ),
        DocumentSpec(
            "Payroll and Benefits Policy",
            "Policy",
            "Internal",
            ["hr", "employee", "manager", "finance"],
            "2.0",
            build_payroll_benefits_policy,
        ),
        DocumentSpec(
            "Performance Management Framework",
            "Framework",
            "Internal",
            ["hr", "manager", "executive", "employee"],
            "1.1",
            build_performance_management_framework,
        ),
        DocumentSpec(
            "Recruitment Guidelines",
            "Guidelines",
            "Internal",
            ["hr", "manager", "executive"],
            "1.0",
            build_recruitment_guidelines,
        ),
    ],
    "Marketing": [
        DocumentSpec(
            "Brand Guidelines",
            "Brand Guide",
            "Internal",
            ["marketing", "employee", "manager"],
            "2.0",
            build_brand_guidelines,
        ),
        DocumentSpec(
            "Campaign Performance Report",
            "Performance Report",
            "Internal",
            ["marketing", "executive", "finance", "manager"],
            "1.0",
            build_campaign_performance_report,
        ),
        DocumentSpec(
            "Customer Insights Report",
            "Research Report",
            "Confidential",
            ["marketing", "executive", "manager"],
            "1.0",
            build_customer_insights_report,
        ),
        DocumentSpec(
            "Marketing Strategy 2026",
            "Strategy Document",
            "Internal",
            ["marketing", "executive", "manager", "finance"],
            "1.0",
            build_marketing_strategy_2026,
        ),
    ],
    "Operations": [
        DocumentSpec(
            "Compliance Framework",
            "Compliance Framework",
            "Confidential",
            ["operations", "executive", "manager", "engineering"],
            "1.0",
            build_compliance_framework,
        ),
        DocumentSpec(
            "Risk Management Register",
            "Risk Register",
            "Confidential",
            ["operations", "executive", "manager", "finance"],
            "1.2",
            build_risk_management_register,
        ),
        DocumentSpec(
            "Standard Operating Procedures",
            "SOP",
            "Internal",
            ["operations", "employee", "manager", "engineering"],
            "2.0",
            build_standard_operating_procedures,
        ),
        DocumentSpec(
            "Supplier Management Policy",
            "Policy",
            "Internal",
            ["operations", "manager", "finance", "executive"],
            "1.0",
            build_supplier_management_policy,
        ),
    ],
}


def pad_to_min_pages(lines: list[str], min_pages: int = 5, lines_per_page: int = 44) -> list[str]:
    """Ensure document has at least min_pages by appending structured appendix content."""
    pages = paginate(lines, lines_per_page)
    while len(pages) < min_pages:
        appendix_num = len(pages) - 4  # offset since main content uses ~4 pages
        appendix = [
            f"Appendix {max(1, appendix_num)}: Supplementary Reference Material",
            "-" * 50,
            f"This appendix provides additional context for {COMPANY} enterprise operations.",
            "",
            "Governance and Review:",
            f"- Document reviewed quarterly by department leadership",
            f"- Next scheduled review: Q{(appendix_num % 4) + 1} {FISCAL_YEAR}",
            f"- Compliance alignment verified against Operations/Compliance Framework.pdf",
            "",
            "Related Metrics Snapshot:",
            f"- Total employees: {CORPORATE['employees']}",
            f"- FY2025 revenue: {CORPORATE['revenue_fy2025']}",
            f"- FY2026 forecast: {CORPORATE['revenue_forecast_fy2026']}",
            f"- Customer count: {CORPORATE['customer_count']}",
            f"- Platform NPS: {CORPORATE['nps_score']}",
            "",
            "Department Coordination Notes:",
            "- Engineering_IT: Technical implementation and security controls",
            "- Finance: Budget allocation, expense approval, and financial reporting",
            "- Human_Resources: Policy compliance, training, and employee communications",
            "- Marketing: External communications and brand consistency",
            "- Operations: Process governance, compliance, and vendor management",
            "- Executive: Strategic alignment and board reporting",
            "",
            "Document Control:",
            "- Master copy maintained in corporate document management system",
            "- Previous versions archived for 7 years per retention policy",
            "- Unauthorized distribution of Confidential or Restricted documents is prohibited",
            "",
            f"For questions contact the {COMPANY} document owner listed on page 1.",
        ]
        lines.extend(appendix)
        pages = paginate(lines, lines_per_page)
    return lines


def create_json(path: Path, dept: str, spec: DocumentSpec) -> None:
    dept_display = dept.replace("_", " ")
    access_roles = list(dict.fromkeys([*spec.access_roles, "admin"]))
    data = {
        "department": dept_display,
        "document_type": spec.document_type,
        "access_roles": access_roles,
        "classification": spec.classification,
        "created": CREATED_DATE,
        "title": spec.title,
        "version": spec.version,
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def generate_all() -> list[Path]:
    generated: list[Path] = []
    for dept, specs in DEPARTMENT_DOCS.items():
        for spec in specs:
            pdf_path = BASE_DIR / dept / f"{spec.title}.pdf"
            json_path = BASE_DIR / dept / f"{spec.title}.json"

            content_lines = pad_to_min_pages(spec.content_builder(), min_pages=5)
            pages = paginate(content_lines, lines_per_page=44)

            # Cap at 8 pages
            if len(pages) > 8:
                flat = [line for page in pages[:8] for line in page]
                pages = paginate(flat, lines_per_page=44)

            write_pdf(pdf_path, pages)
            create_json(json_path, dept, spec)
            generated.append(pdf_path)
            print(f"Generated: {pdf_path} ({len(pages)} pages)")
    return generated


def main() -> None:
    paths = generate_all()
    print(f"\nComplete: {len(paths)} PDFs + {len(paths)} JSON files under {BASE_DIR}")


if __name__ == "__main__":
    main()
