import { motion } from 'framer-motion'
import {
  MessageSquare,
  Users,
  Clock,
  ThumbsUp,
  Shield,
  AlertTriangle,
  ArrowLeft,
  TrendingUp,
  TrendingDown,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import {
  ANALYTICS_DATA,
  DEPARTMENT_USAGE,
  QUERY_STATS,
  SECURITY_ALERTS,
} from '@/data/mockData'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { PageTransition } from '@/components/layout/PageTransition'
import { formatNumber } from '@/lib/utils'
import { cn } from '@/lib/utils'

const SEVERITY_STYLES = {
  low: 'bg-zinc-500/15 text-zinc-400 border-zinc-500/30',
  medium: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  high: 'bg-orange-500/15 text-orange-400 border-orange-500/30',
  critical: 'bg-red-500/15 text-red-400 border-red-500/30',
}

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
  },
}

const item = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
}

export function AnalyticsDashboard() {
  const navigate = useNavigate()

  const metrics = [
    {
      label: 'Total Chats',
      value: formatNumber(ANALYTICS_DATA.totalChats),
      change: ANALYTICS_DATA.chatsChange,
      icon: MessageSquare,
      color: 'text-brand-400 bg-brand-500/15',
    },
    {
      label: 'Active Users',
      value: ANALYTICS_DATA.activeUsers,
      change: ANALYTICS_DATA.usersChange,
      icon: Users,
      color: 'text-emerald-400 bg-emerald-500/15',
    },
    {
      label: 'Avg Response',
      value: ANALYTICS_DATA.avgResponseTime,
      change: ANALYTICS_DATA.responseChange,
      icon: Clock,
      color: 'text-violet-400 bg-violet-500/15',
    },
    {
      label: 'Satisfaction',
      value: `${ANALYTICS_DATA.satisfactionRate}%`,
      change: ANALYTICS_DATA.satisfactionChange,
      icon: ThumbsUp,
      color: 'text-amber-400 bg-amber-500/15',
    },
  ]

  return (
    <PageTransition>
      <div className="min-h-screen bg-[var(--bg-primary)] gradient-mesh">
        {/* Header */}
        <header className="border-b border-[var(--border-default)] bg-[var(--bg-secondary)]/80 backdrop-blur-xl sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => navigate('/chat')}>
                <ArrowLeft className="h-4 w-4" />
              </Button>
              <div>
                <h1 className="text-lg font-semibold text-[var(--text-primary)]">
                  Admin Analytics
                </h1>
                <p className="text-xs text-[var(--text-muted)]">
                  Neura AI Platform Overview
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-xs text-[var(--text-muted)]">
              <Shield className="h-3.5 w-3.5" />
              Admin Access · RBAC Level 7
            </div>
          </div>
        </header>

        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="max-w-7xl mx-auto px-6 py-8 space-y-8"
        >
          {/* Metric Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {metrics.map((metric) => (
              <motion.div key={metric.label} variants={item}>
                <Card hover className="p-5">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-xs text-[var(--text-muted)] font-medium">
                        {metric.label}
                      </p>
                      <p className="text-2xl font-bold text-[var(--text-primary)] mt-1">
                        {metric.value}
                      </p>
                      <div className="flex items-center gap-1 mt-1.5">
                        {metric.change > 0 ? (
                          <TrendingUp className="h-3 w-3 text-emerald-400" />
                        ) : (
                          <TrendingDown className="h-3 w-3 text-emerald-400" />
                        )}
                        <span
                          className={cn(
                            'text-xs font-medium',
                            metric.change > 0 ? 'text-emerald-400' : 'text-emerald-400',
                          )}
                        >
                          {metric.change > 0 ? '+' : ''}
                          {metric.change}%
                        </span>
                        <span className="text-xs text-[var(--text-muted)]">vs last week</span>
                      </div>
                    </div>
                    <div
                      className={cn(
                        'h-10 w-10 rounded-xl flex items-center justify-center',
                        metric.color,
                      )}
                    >
                      <metric.icon className="h-5 w-5" />
                    </div>
                  </div>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Query Statistics */}
            <motion.div variants={item} className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Query Volume — Last 7 Days</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={QUERY_STATS}>
                        <XAxis
                          dataKey="date"
                          axisLine={false}
                          tickLine={false}
                          tick={{ fill: '#71717a', fontSize: 12 }}
                        />
                        <YAxis
                          axisLine={false}
                          tickLine={false}
                          tick={{ fill: '#71717a', fontSize: 12 }}
                        />
                        <Tooltip
                          contentStyle={{
                            background: '#1a1a1f',
                            border: '1px solid rgba(255,255,255,0.08)',
                            borderRadius: '10px',
                            fontSize: '12px',
                          }}
                        />
                        <Bar
                          dataKey="queries"
                          fill="url(#barGradient)"
                          radius={[6, 6, 0, 0]}
                        />
                        <defs>
                          <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor="#3b82f6" />
                            <stop offset="100%" stopColor="#06b6d4" />
                          </linearGradient>
                        </defs>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Department Usage Pie */}
            <motion.div variants={item}>
              <Card className="h-full">
                <CardHeader>
                  <CardTitle>Department Usage</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-48">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={DEPARTMENT_USAGE}
                          dataKey="queries"
                          nameKey="department"
                          cx="50%"
                          cy="50%"
                          innerRadius={50}
                          outerRadius={75}
                          paddingAngle={3}
                        >
                          {DEPARTMENT_USAGE.map((entry) => (
                            <Cell key={entry.department} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip
                          contentStyle={{
                            background: '#1a1a1f',
                            border: '1px solid rgba(255,255,255,0.08)',
                            borderRadius: '10px',
                            fontSize: '12px',
                          }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="grid grid-cols-2 gap-2 mt-2">
                    {DEPARTMENT_USAGE.map((dept) => (
                      <div key={dept.department} className="flex items-center gap-2">
                        <div
                          className="h-2 w-2 rounded-full shrink-0"
                          style={{ background: dept.color }}
                        />
                        <span className="text-[10px] text-[var(--text-muted)] truncate">
                          {dept.department}
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          {/* Department Table + Security Alerts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Department Breakdown */}
            <motion.div variants={item}>
              <Card>
                <CardHeader>
                  <CardTitle>Department Breakdown</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {DEPARTMENT_USAGE.map((dept) => {
                      const maxQueries = Math.max(...DEPARTMENT_USAGE.map((d) => d.queries))
                      const width = (dept.queries / maxQueries) * 100
                      return (
                        <div key={dept.department}>
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm text-[var(--text-primary)]">
                              {dept.department}
                            </span>
                            <span className="text-xs text-[var(--text-muted)]">
                              {formatNumber(dept.queries)} queries · {dept.users} users
                            </span>
                          </div>
                          <div className="h-2 rounded-full bg-[var(--bg-tertiary)] overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${width}%` }}
                              transition={{ duration: 0.8, ease: 'easeOut' }}
                              className="h-full rounded-full"
                              style={{ background: dept.color }}
                            />
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Security Alerts */}
            <motion.div variants={item}>
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Security Alerts</CardTitle>
                    <span className="text-xs text-red-400 font-medium">
                      {SECURITY_ALERTS.filter((a) => !a.resolved).length} active
                    </span>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {SECURITY_ALERTS.map((alert) => (
                      <div
                        key={alert.id}
                        className={cn(
                          'flex items-start gap-3 p-3 rounded-xl border',
                          alert.resolved
                            ? 'border-[var(--border-subtle)] opacity-60'
                            : 'border-[var(--border-default)] bg-[var(--bg-tertiary)]',
                        )}
                      >
                        <AlertTriangle
                          className={cn(
                            'h-4 w-4 shrink-0 mt-0.5',
                            alert.severity === 'critical'
                              ? 'text-red-400'
                              : alert.severity === 'high'
                                ? 'text-orange-400'
                                : alert.severity === 'medium'
                                  ? 'text-amber-400'
                                  : 'text-zinc-400',
                          )}
                        />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <span
                              className={cn(
                                'text-[10px] font-semibold uppercase px-1.5 py-0.5 rounded border',
                                SEVERITY_STYLES[alert.severity],
                              )}
                            >
                              {alert.severity}
                            </span>
                            {alert.resolved && (
                              <span className="text-[10px] text-emerald-400">Resolved</span>
                            )}
                          </div>
                          <p className="text-xs text-[var(--text-secondary)] leading-relaxed">
                            {alert.message}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </PageTransition>
  )
}
