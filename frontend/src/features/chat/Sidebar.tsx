import { motion, AnimatePresence } from 'framer-motion'
import {
  Plus,
  MessageSquare,
  PanelLeftClose,
  PanelLeft,
  LogOut,
  BarChart3,
  Brain,
} from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'
import { useChat } from '@/context/ChatContext'
import { Avatar } from '@/components/ui/Avatar'
import { Badge } from '@/components/ui/Badge'
import { ThemeToggle } from '@/components/ui/ThemeToggle'
import { Button } from '@/components/ui/Button'
import { formatRelativeTime } from '@/lib/utils'
import { cn } from '@/lib/utils'

export function Sidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const {
    conversations,
    activeConversationId,
    sidebarCollapsed,
    setSidebarCollapsed,
    selectConversation,
    createConversation,
  } = useChat()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <motion.aside
      animate={{ width: sidebarCollapsed ? 72 : 280 }}
      transition={{ duration: 0.3, ease: [0.25, 0.46, 0.45, 0.94] }}
      className={cn(
        'h-full flex flex-col border-r border-[var(--border-subtle)] shrink-0 overflow-hidden',
        'bg-[var(--bg-secondary)]/80 backdrop-blur-xl',
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-[var(--border-subtle)]">
        <AnimatePresence mode="wait">
          {!sidebarCollapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-3"
            >
              <div className="h-9 w-9 rounded-xl neura-orb-sm flex items-center justify-center">
                <Brain className="h-4 w-4 text-white" />
              </div>
              <div>
                <p className="text-sm font-semibold text-[var(--text-primary)] leading-none tracking-tight">
                  Neura <span className="text-gradient-neura">AI</span>
                </p>
                <p className="text-[10px] text-[var(--text-muted)] mt-1 uppercase tracking-[0.2em]">
                  Enterprise
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <button
          onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          className="h-8 w-8 rounded-lg flex items-center justify-center text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-tertiary)] transition-colors"
        >
          {sidebarCollapsed ? (
            <PanelLeft className="h-4 w-4" />
          ) : (
            <PanelLeftClose className="h-4 w-4" />
          )}
        </button>
      </div>

      {/* New Chat */}
      <div className="p-3">
        <Button
          variant="primary"
          size={sidebarCollapsed ? 'icon' : 'md'}
          className={cn('w-full neura-btn', sidebarCollapsed && 'mx-auto')}
          onClick={createConversation}
        >
          <Plus className="h-4 w-4" />
          {!sidebarCollapsed && 'New session'}
        </Button>
      </div>

      {/* Conversations */}
      <div className="flex-1 overflow-y-auto px-3 py-1">
        {!sidebarCollapsed && (
          <p className="text-[10px] font-medium uppercase tracking-[0.2em] text-[var(--text-muted)] px-2 mb-2">
            Sessions
          </p>
        )}

        {conversations.length === 0 && !sidebarCollapsed ? (
          <div className="px-3 py-8 text-center">
            <MessageSquare className="h-8 w-8 text-[var(--text-muted)]/40 mx-auto mb-3" />
            <p className="text-xs text-[var(--text-muted)] leading-relaxed">
              No sessions yet. Start a new query to begin.
            </p>
          </div>
        ) : (
          <div className="space-y-0.5">
            {conversations.map((conv) => (
              <motion.button
                key={conv.id}
                whileHover={{ x: 2 }}
                onClick={() => selectConversation(conv.id)}
                className={cn(
                  'w-full flex items-center gap-2.5 rounded-xl px-2.5 py-2.5 text-left transition-all duration-200',
                  activeConversationId === conv.id
                    ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/20'
                    : 'text-[var(--text-secondary)] hover:bg-[var(--bg-tertiary)] hover:text-[var(--text-primary)] border border-transparent',
                )}
                title={sidebarCollapsed ? conv.title : undefined}
              >
                <MessageSquare className="h-4 w-4 shrink-0 opacity-70" />
                {!sidebarCollapsed && (
                  <div className="flex-1 min-w-0">
                    <p className="text-sm truncate">{conv.title}</p>
                    <p className="text-[10px] text-[var(--text-muted)]">
                      {formatRelativeTime(conv.updatedAt)}
                    </p>
                  </div>
                )}
              </motion.button>
            ))}
          </div>
        )}
      </div>

      {/* User Profile */}
      <div className="border-t border-[var(--border-subtle)] p-3 space-y-2">
        {!sidebarCollapsed && user && (
          <div className="flex items-center gap-2.5 px-2 py-2">
            <Avatar name={user.name} size="sm" />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-[var(--text-primary)] truncate">
                {user.name}
              </p>
              <Badge role={user.role} variant="role" className="mt-1" />
            </div>
          </div>
        )}

        <div className={cn('flex items-center gap-1', sidebarCollapsed ? 'flex-col' : 'px-1')}>
          <ThemeToggle />
          {user?.role === 'admin' && (
            <button
              onClick={() => navigate('/admin')}
              className="h-9 w-9 rounded-lg flex items-center justify-center text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-tertiary)] transition-colors"
              title="Analytics Dashboard"
            >
              <BarChart3 className="h-4 w-4" />
            </button>
          )}
          <button
            onClick={handleLogout}
            className="h-9 w-9 rounded-lg flex items-center justify-center text-[var(--text-muted)] hover:text-red-400 hover:bg-red-500/10 transition-colors"
            title="Sign out"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </motion.aside>
  )
}
