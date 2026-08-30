import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from 'react'
import type { User, UserRole } from '@/types'
import { ROLE_LABELS } from '@/types'
import { fetchMe, login as apiLogin, signup as apiSignup, type AuthResponse } from '@/lib/api'

interface AuthContextType {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  signup: (payload: {
    username: string
    name: string
    password: string
    role: UserRole
  }) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

const STORAGE_KEY = 'neura-auth'

function toUser(auth: AuthResponse['user']): User {
  return {
    id: auth.id,
    username: auth.username,
    name: auth.name,
    role: auth.role as UserRole,
    department: auth.department || ROLE_LABELS[auth.role as UserRole] || auth.role,
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const persistAuth = useCallback((nextToken: string | null, nextUser: User | null) => {
    setToken(nextToken)
    setUser(nextUser)
    if (nextToken && nextUser) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ token: nextToken, user: nextUser }))
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [])

  useEffect(() => {
    const bootstrap = async () => {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (!stored) {
        setIsLoading(false)
        return
      }

      try {
        const parsed = JSON.parse(stored) as { token: string; user: User }
        const me = await fetchMe(parsed.token)
        persistAuth(parsed.token, toUser(me))
      } catch {
        localStorage.removeItem(STORAGE_KEY)
      } finally {
        setIsLoading(false)
      }
    }

    bootstrap()
  }, [persistAuth])

  const login = useCallback(
    async (username: string, password: string) => {
      const response = await apiLogin({ username, password })
      persistAuth(response.access_token, toUser(response.user))
    },
    [persistAuth],
  )

  const signup = useCallback(
    async (payload: { username: string; name: string; password: string; role: UserRole }) => {
      const response = await apiSignup(payload)
      persistAuth(response.access_token, toUser(response.user))
    },
    [persistAuth],
  )

  const logout = useCallback(() => {
    persistAuth(null, null)
  }, [persistAuth])

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
