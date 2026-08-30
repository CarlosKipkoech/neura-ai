const API_BASE = import.meta.env.VITE_API_URL?.replace(/\/$/, '') ?? ''

export function getApiUrl(path: string): string {
  if (API_BASE) {
    return `${API_BASE}${path}`
  }
  return `/api${path}`
}

export interface AuthUser {
  id: string
  username: string
  name: string
  role: string
  department: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: AuthUser
}

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

async function parseResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    const message =
      typeof data?.detail === 'string'
        ? data.detail
        : Array.isArray(data?.detail)
          ? data.detail.map((item: { msg?: string }) => item.msg).join(', ')
          : 'Request failed'
    throw new ApiError(message, response.status)
  }
  return data as T
}

export async function signup(payload: {
  username: string
  name: string
  password: string
  role: string
}): Promise<AuthResponse> {
  const response = await fetch(getApiUrl('/auth/signup'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  return parseResponse<AuthResponse>(response)
}

export async function login(payload: {
  username: string
  password: string
}): Promise<AuthResponse> {
  const response = await fetch(getApiUrl('/auth/login'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  return parseResponse<AuthResponse>(response)
}

export async function fetchMe(token: string): Promise<AuthUser> {
  const response = await fetch(getApiUrl('/auth/me'), {
    headers: { Authorization: `Bearer ${token}` },
  })
  return parseResponse<AuthUser>(response)
}

export async function sendChatMessage(token: string, question: string) {
  const response = await fetch(getApiUrl('/chat'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ question }),
  })
  return parseResponse<{ answer: string; sources: unknown[] }>(response)
}
