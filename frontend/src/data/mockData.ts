import type {
  Conversation,
  DepartmentUsage,
  SecurityAlert,
  SourceDocument,
  User,
  UserRole,
} from '@/types'

export const DEMO_USERS: User[] = [
  { id: '1', username: 'alice.chen', name: 'Alice Chen', role: 'finance', department: 'Finance' },
  { id: '2', username: 'bob.martinez', name: 'Bob Martinez', role: 'hr', department: 'Human Resources' },
  { id: '3', username: 'carol.williams', name: 'Carol Williams', role: 'marketing', department: 'Marketing' },
  { id: '4', username: 'david.kim', name: 'David Kim', role: 'engineering', department: 'Engineering' },
  { id: '5', username: 'elena.rodriguez', name: 'Elena Rodriguez', role: 'executive', department: 'Executive' },
  { id: '6', username: 'frank.johnson', name: 'Frank Johnson', role: 'employee', department: 'Operations' },
  { id: '7', username: 'admin', name: 'System Admin', role: 'admin', department: 'IT Security' },
]

export const ROLE_OPTIONS: { value: UserRole; label: string }[] = [
  { value: 'finance', label: 'Finance' },
  { value: 'hr', label: 'Human Resources' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'engineering', label: 'Engineering' },
  { value: 'executive', label: 'Executive' },
  { value: 'employee', label: 'Employee' },
  { value: 'admin', label: 'Administrator' },
]

export const MOCK_SOURCES: SourceDocument[] = [
  {
    id: 'src-1',
    title: 'Q4 2025 Financial Compliance Policy',
    department: 'Finance',
    content:
      'All financial transactions exceeding $50,000 require dual authorization from a Finance Manager and VP of Finance. Quarterly compliance audits must be completed within 15 business days of quarter end. SOX controls apply to all revenue recognition processes.',
    confidence: 0.94,
    page: 12,
    lastUpdated: '2026-01-15',
  },
  {
    id: 'src-2',
    title: 'Employee Benefits & Leave Policy 2026',
    department: 'Human Resources',
    content:
      'Full-time employees accrue 20 days of PTO annually, with an additional 5 sick days. Parental leave provides 16 weeks paid leave for primary caregivers. Health insurance enrollment occurs during the first 30 days of employment.',
    confidence: 0.87,
    page: 4,
    lastUpdated: '2026-02-01',
  },
  {
    id: 'src-3',
    title: 'Data Security & Access Control Framework',
    department: 'Engineering',
    content:
      'Role-based access control (RBAC) is enforced at the API gateway level. All data access is logged and retained for 90 days. PII fields must be encrypted at rest using AES-256. Multi-factor authentication is mandatory for all production systems.',
    confidence: 0.91,
    page: 7,
    lastUpdated: '2026-01-28',
  },
]

const SAMPLE_AI_RESPONSE = `Based on the retrieved policy documents, here's a comprehensive overview:

## Expense Approval Thresholds

For **FinSolve Technologies**, the approval workflow depends on the transaction amount:

| Amount Range | Required Approver |
|---|---|
| Under $5,000 | Direct Manager |
| $5,000 – $50,000 | Department Head |
| Over $50,000 | Dual authorization (Finance Manager + VP) |

## Key Compliance Requirements

1. **SOX Controls** — All revenue recognition must follow documented procedures
2. **Audit Trail** — Every approval is logged with timestamp and approver ID
3. **Quarterly Reviews** — Compliance audits due within 15 business days of quarter end

> **Note:** As a Finance team member, you have access to the full expense policy documentation. Contact the Compliance team for exceptions.`

export const INITIAL_CONVERSATIONS: Conversation[] = [
  {
    id: 'conv-1',
    title: 'Q4 Expense Policy Review',
    createdAt: new Date(Date.now() - 86400000 * 2),
    updatedAt: new Date(Date.now() - 3600000),
    messages: [
      {
        id: 'msg-1',
        role: 'user',
        content: 'What are the expense approval thresholds for Q4?',
        timestamp: new Date(Date.now() - 3600000 * 2),
      },
      {
        id: 'msg-2',
        role: 'assistant',
        content: SAMPLE_AI_RESPONSE,
        timestamp: new Date(Date.now() - 3600000),
        sources: MOCK_SOURCES.slice(0, 2),
      },
    ],
  },
  {
    id: 'conv-2',
    title: 'Employee PTO Accrual Rules',
    createdAt: new Date(Date.now() - 86400000 * 5),
    updatedAt: new Date(Date.now() - 86400000),
    messages: [
      {
        id: 'msg-3',
        role: 'user',
        content: 'How does PTO accrual work for new hires?',
        timestamp: new Date(Date.now() - 86400000),
      },
      {
        id: 'msg-4',
        role: 'assistant',
        content:
          'New hires at FinSolve Technologies begin accruing PTO from their start date at a prorated rate of **1.67 days per month** (20 days annually). PTO becomes available for use after completing the 90-day probationary period.\n\nSick days (5 annually) are available immediately upon hire.',
        timestamp: new Date(Date.now() - 86400000 + 30000),
        sources: [MOCK_SOURCES[1]],
      },
    ],
  },
  {
    id: 'conv-3',
    title: 'RBAC Security Framework',
    createdAt: new Date(Date.now() - 86400000 * 7),
    updatedAt: new Date(Date.now() - 86400000 * 3),
    messages: [
      {
        id: 'msg-5',
        role: 'user',
        content: 'Explain our RBAC implementation for production systems',
        timestamp: new Date(Date.now() - 86400000 * 3),
      },
      {
        id: 'msg-6',
        role: 'assistant',
        content:
          'FinSolve implements **role-based access control** at multiple layers:\n\n- **API Gateway** — Role validation on every request\n- **Data Layer** — Department-scoped document retrieval\n- **Audit Logging** — 90-day retention of all access events\n\nMFA is mandatory for all production system access.',
        timestamp: new Date(Date.now() - 86400000 * 3 + 45000),
        sources: [MOCK_SOURCES[2]],
      },
    ],
  },
]

export const STREAMING_RESPONSES: Record<string, string> = {
  default: `I've analyzed the relevant policy documents for your query. Here's what I found:

## Summary

Based on FinSolve Technologies' current policies, the information you're requesting is governed by our internal compliance framework.

### Key Points

1. **Access Control** — Your current role determines which document sets are searchable
2. **Data Retention** — All query logs are retained for audit purposes
3. **Escalation Path** — For policy exceptions, contact your department head

Would you like me to dive deeper into any specific aspect?`,
}

export const ANALYTICS_DATA = {
  totalChats: 12847,
  activeUsers: 342,
  avgResponseTime: '1.2s',
  satisfactionRate: 94.2,
  chatsChange: 12.5,
  usersChange: 8.3,
  responseChange: -15.2,
  satisfactionChange: 2.1,
}

export const DEPARTMENT_USAGE: DepartmentUsage[] = [
  { department: 'Finance', queries: 3842, users: 89, color: '#10b981' },
  { department: 'HR', queries: 2156, users: 45, color: '#8b5cf6' },
  { department: 'Engineering', queries: 2891, users: 112, color: '#3b82f6' },
  { department: 'Marketing', queries: 1543, users: 38, color: '#f59e0b' },
  { department: 'Executive', queries: 987, users: 12, color: '#f43f5e' },
  { department: 'Operations', queries: 1428, users: 46, color: '#71717a' },
]

export const QUERY_STATS = [
  { date: 'Mon', queries: 420 },
  { date: 'Tue', queries: 380 },
  { date: 'Wed', queries: 510 },
  { date: 'Thu', queries: 470 },
  { date: 'Fri', queries: 390 },
  { date: 'Sat', queries: 120 },
  { date: 'Sun', queries: 85 },
]

export const SECURITY_ALERTS: SecurityAlert[] = [
  {
    id: 'alert-1',
    severity: 'high',
    message: 'Unusual query pattern detected from IP 192.168.1.45 — 847 requests in 10 minutes',
    timestamp: new Date(Date.now() - 3600000),
    resolved: false,
  },
  {
    id: 'alert-2',
    severity: 'medium',
    message: 'Role escalation attempt blocked for user jsmith — requested executive-level documents',
    timestamp: new Date(Date.now() - 7200000),
    resolved: false,
  },
  {
    id: 'alert-3',
    severity: 'low',
    message: 'Document index sync delayed by 12 minutes — auto-recovered',
    timestamp: new Date(Date.now() - 86400000),
    resolved: true,
  },
  {
    id: 'alert-4',
    severity: 'critical',
    message: 'Potential data exfiltration attempt — bulk document download blocked',
    timestamp: new Date(Date.now() - 172800000),
    resolved: true,
  },
]
