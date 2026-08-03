import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import type { User, UserRole } from '@/types'
import { DEMO_USERS } from '@/data/mockData'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  login: (username: string, role: UserRole) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const stored = sessionStorage.getItem('finsolve-user')
    return stored ? JSON.parse(stored) : null
  })

  useEffect(() => {
    if (user) {
      sessionStorage.setItem('finsolve-user', JSON.stringify(user))
    } else {
      sessionStorage.removeItem('finsolve-user')
    }
  }, [user])

  const login = (username: string, role: UserRole) => {
    const existing = DEMO_USERS.find((u) => u.username === username)
    const newUser: User = existing ?? {
      id: crypto.randomUUID(),
      username,
      name: username.split('.').map((s) => s.charAt(0).toUpperCase() + s.slice(1)).join(' '),
      role,
      department: role.charAt(0).toUpperCase() + role.slice(1),
    }
    setUser({ ...newUser, role })
  }

  const logout = () => setUser(null)

  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
