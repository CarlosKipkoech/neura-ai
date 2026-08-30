import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Brain, UserPlus, ArrowRight } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { PageTransition } from '@/components/layout/PageTransition'
import { ROLE_OPTIONS } from '@/data/mockData'
import type { UserRole } from '@/types'
import { ApiError } from '@/lib/api'

const SIGNUP_ROLES = ROLE_OPTIONS.filter((option) => option.value !== 'admin')

export function SignUpPage() {
  const navigate = useNavigate()
  const { signup, isAuthenticated } = useAuth()
  const [name, setName] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<UserRole>('employee')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (isAuthenticated) {
    navigate('/chat', { replace: true })
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim() || !username.trim() || !password) return
    setLoading(true)
    setError('')
    try {
      await signup({
        name: name.trim(),
        username: username.trim(),
        password,
        role,
      })
      navigate('/chat')
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Unable to create account')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageTransition>
      <div className="min-h-screen gradient-mesh-neura flex items-center justify-center p-4 relative overflow-hidden">
        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          className="w-full max-w-md relative z-10"
        >
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl neura-orb-sm shadow-lg mb-4">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)] tracking-tight">
              Join <span className="text-gradient-neura">Neura AI</span>
            </h1>
            <p className="text-sm text-[var(--text-secondary)] mt-1.5">
              Create an account and choose your department role
            </p>
          </div>

          <div className="glass rounded-2xl p-8 shadow-elevated">
            <div className="flex items-center gap-2 mb-6">
              <UserPlus className="h-4 w-4 text-cyan-400" />
              <h2 className="text-lg font-semibold text-[var(--text-primary)]">Sign up</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <Input
                id="name"
                label="Full name"
                placeholder="Alex Morgan"
                value={name}
                onChange={(e) => setName(e.target.value)}
                autoComplete="name"
                required
              />

              <Input
                id="username"
                label="Username"
                placeholder="alex.morgan"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
                required
              />

              <Input
                id="password"
                label="Password"
                type="password"
                placeholder="At least 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="new-password"
                required
              />

              <Select
                id="role"
                label="Department role"
                value={role}
                onChange={(v) => setRole(v as UserRole)}
                options={SIGNUP_ROLES}
              />

              {error && (
                <p className="text-sm text-red-400 bg-red-500/10 border border-red-500/20 rounded-xl px-3 py-2">
                  {error}
                </p>
              )}

              <Button type="submit" className="w-full neura-btn" size="lg" loading={loading}>
                Create account
                <ArrowRight className="h-4 w-4" />
              </Button>
            </form>

            <p className="text-center text-sm text-[var(--text-muted)] mt-6">
              Already have an account?{' '}
              <Link to="/login" className="text-cyan-400 hover:text-cyan-300 font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </motion.div>
      </div>
    </PageTransition>
  )
}
