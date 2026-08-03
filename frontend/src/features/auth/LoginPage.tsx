import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Shield, Sparkles, Lock, ArrowRight } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Select } from '@/components/ui/Select'
import { PageTransition } from '@/components/layout/PageTransition'
import { ROLE_OPTIONS } from '@/data/mockData'
import type { UserRole } from '@/types'

export function LoginPage() {
  const navigate = useNavigate()
  const { login, isAuthenticated } = useAuth()
  const [username, setUsername] = useState('')
  const [role, setRole] = useState<UserRole>('finance')
  const [loading, setLoading] = useState(false)

  if (isAuthenticated) {
    navigate('/chat', { replace: true })
    return null
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!username.trim()) return
    setLoading(true)
    setTimeout(() => {
      login(username.trim(), role)
      navigate(role === 'admin' ? '/admin' : '/chat')
    }, 800)
  }

  return (
    <PageTransition>
      <div className="min-h-screen gradient-mesh flex items-center justify-center p-4 relative overflow-hidden">
        {/* Background orbs */}
        <div className="absolute top-1/4 -left-32 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-accent-cyan/10 rounded-full blur-3xl" />

        <motion.div
          initial={{ opacity: 0, y: 20, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }}
          className="w-full max-w-md relative z-10"
        >
          {/* Logo & Branding */}
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              className="inline-flex items-center justify-center w-16 h-16 rounded-2xl gradient-brand shadow-lg shadow-brand-500/30 mb-4"
            >
              <Sparkles className="h-8 w-8 text-white" />
            </motion.div>
            <h1 className="text-2xl font-bold text-[var(--text-primary)] tracking-tight">
              FinSolve <span className="text-gradient">AI</span>
            </h1>
            <p className="text-sm text-[var(--text-secondary)] mt-1.5">
              Enterprise Knowledge Assistant
            </p>
            <p className="text-xs text-[var(--text-muted)] mt-0.5">
              FinSolve Technologies
            </p>
          </div>

          {/* Login Card */}
          <div className="glass rounded-2xl p-8 shadow-elevated">
            <div className="flex items-center gap-2 mb-6">
              <Lock className="h-4 w-4 text-brand-400" />
              <h2 className="text-lg font-semibold text-[var(--text-primary)]">Sign In</h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <Input
                id="username"
                label="Username"
                placeholder="e.g. alice.chen"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                autoComplete="username"
                required
              />

              <Select
                id="role"
                label="Department Role"
                value={role}
                onChange={(v) => setRole(v as UserRole)}
                options={ROLE_OPTIONS}
              />

              <Button type="submit" className="w-full" size="lg" loading={loading}>
                Continue to Dashboard
                <ArrowRight className="h-4 w-4" />
              </Button>
            </form>

            <div className="mt-6 pt-5 border-t border-[var(--border-subtle)]">
              <div className="flex items-start gap-3">
                <Shield className="h-4 w-4 text-emerald-400 mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs font-medium text-[var(--text-secondary)]">
                    RBAC-Protected Access
                  </p>
                  <p className="text-xs text-[var(--text-muted)] mt-0.5 leading-relaxed">
                    Your role determines document access scope. All queries are logged for compliance.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <p className="text-center text-xs text-[var(--text-muted)] mt-6">
            Secured by FinSolve Identity Platform · SOC 2 Type II
          </p>
        </motion.div>
      </div>
    </PageTransition>
  )
}
