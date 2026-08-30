export type UserRole =
  | 'finance'
  | 'hr'
  | 'marketing'
  | 'engineering'
  | 'executive'
  | 'employee'
  | 'admin'

export interface User {
  id: string
  username: string
  name: string
  role: UserRole
  avatar?: string
  department: string
}

export interface SourceDocument {
  id: string
  title: string
  department: string
  content: string
  confidence: number
  page?: number
  lastUpdated?: string
  source?: string
  classification?: string
  allowedRoles?: string[]
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  sources?: SourceDocument[]
  isStreaming?: boolean
}

export interface Conversation {
  id: string
  title: string
  messages: ChatMessage[]
  createdAt: Date
  updatedAt: Date
}

export interface AnalyticsMetric {
  label: string
  value: string | number
  change?: number
  changeLabel?: string
  icon?: string
}

export interface DepartmentUsage {
  department: string
  queries: number
  users: number
  color: string
}

export interface SecurityAlert {
  id: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  message: string
  timestamp: Date
  resolved: boolean
}

export const ROLE_LABELS: Record<UserRole, string> = {
  finance: 'Finance',
  hr: 'Human Resources',
  marketing: 'Marketing',
  engineering: 'Engineering',
  executive: 'Executive',
  employee: 'Employee',
  admin: 'Administrator',
}

export const ROLE_COLORS: Record<UserRole, string> = {
  finance: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  hr: 'bg-violet-500/15 text-violet-400 border-violet-500/30',
  marketing: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  engineering: 'bg-blue-500/15 text-blue-400 border-blue-500/30',
  executive: 'bg-rose-500/15 text-rose-400 border-rose-500/30',
  employee: 'bg-zinc-500/15 text-zinc-400 border-zinc-500/30',
  admin: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/30',
}
