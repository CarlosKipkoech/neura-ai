import type { DepartmentUsage, SecurityAlert, User, UserRole } from '@/types'

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

export const ROLE_SUGGESTIONS: Record<UserRole, string[]> = {
  finance: [
    'What are the expense limits for domestic travel?',
    'Summarize the FY2026 budget allocation by department',
    'What approval workflow applies to expenses over $2,000?',
  ],
  hr: [
    'What leave benefits do full-time employees receive?',
    'Explain the performance management review cycle',
    'What are the recruitment approval requirements?',
  ],
  marketing: [
    'What is the company revenue forecast for 2026?',
    'Summarize Q1 campaign performance and ROI',
    'What are our 2026 marketing strategic priorities?',
  ],
  engineering: [
    'What are the software development quality gates?',
    'Summarize the incident management process',
    'Explain the system architecture data flow',
  ],
  executive: [
    'What are the top enterprise risks this quarter?',
    'Summarize the 2026 corporate strategy pillars',
    'What did the board approve in Q1 2026?',
  ],
  employee: [
    'What is the expense reimbursement policy?',
    'What leave entitlements are available?',
    'Where can I find standard operating procedures?',
  ],
  admin: [
    'What compliance controls need improvement?',
    'Summarize operational risk register entries',
    'What security policies govern data access?',
  ],
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
