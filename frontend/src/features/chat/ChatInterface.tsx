import { AnimatePresence, motion } from 'framer-motion'
import { Brain, PanelRightOpen, Sparkles, Zap } from 'lucide-react'
import { useChat } from '@/context/ChatContext'
import { useAuth } from '@/context/AuthContext'
import { useAutoScroll } from '@/hooks/useAutoScroll'
import { ROLE_SUGGESTIONS } from '@/data/mockData'
import { MessageBubble } from './MessageBubble'
import { TypingIndicator } from './TypingIndicator'
import { ChatInput } from './ChatInput'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'

export function ChatInterface() {
  const { user } = useAuth()
  const {
    activeConversation,
    isStreaming,
    sourcesPanelOpen,
    setSourcesPanelOpen,
    setActiveSources,
  } = useChat()

  const messages = activeConversation?.messages ?? []
  const bottomRef = useAutoScroll([messages.length, messages[messages.length - 1]?.content])
  const suggestions = user ? ROLE_SUGGESTIONS[user.role] : []
  const isEmpty = messages.length === 0

  const handleShowSources = (sources: typeof messages[0]['sources']) => {
    if (sources) {
      setActiveSources(sources)
      setSourcesPanelOpen(true)
    }
  }

  return (
    <div className="flex-1 flex flex-col min-w-0 h-full relative">
      <div className="neura-grid absolute inset-0 pointer-events-none opacity-40" />

      {/* Header */}
      <div className="relative z-10 flex items-center justify-between px-6 py-4 border-b border-[var(--border-subtle)] glass-panel">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-60" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
            </span>
            <span className="text-[11px] font-medium uppercase tracking-[0.2em] text-[var(--text-muted)]">
              Knowledge base online
            </span>
          </div>
          {!isEmpty && (
            <>
              <div className="h-4 w-px bg-[var(--border-default)]" />
              <h2 className="text-sm font-medium text-[var(--text-primary)] truncate max-w-[240px]">
                {activeConversation?.title ?? 'New session'}
              </h2>
            </>
          )}
        </div>
        <div className="flex items-center gap-3">
          {user && <Badge role={user.role} variant="role" />}
          {!sourcesPanelOpen && (
            <Button variant="ghost" size="sm" onClick={() => setSourcesPanelOpen(true)}>
              <PanelRightOpen className="h-4 w-4" />
              Sources
            </Button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="relative z-10 flex-1 overflow-y-auto">
        {isEmpty ? (
          <div className="h-full flex flex-col items-center justify-center px-6 py-12">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }}
              className="relative mb-10"
            >
              <div className="neura-orb h-24 w-24 rounded-full flex items-center justify-center">
                <Brain className="h-10 w-10 text-white drop-shadow-lg" />
              </div>
              <motion.div
                className="absolute -inset-4 rounded-full border border-cyan-500/20"
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15, duration: 0.4 }}
              className="text-center max-w-xl mb-10"
            >
              <h1 className="text-3xl font-semibold tracking-tight mb-3">
                <span className="text-gradient-neura">Neura Intelligence</span>
              </h1>
              <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
                Ask anything about Neura AI policies, budgets, compliance, and internal docs.
                Your <span className="text-cyan-400/90 font-medium">{user?.role}</span> role
                scopes what the system can retrieve.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.25, duration: 0.4 }}
              className="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-3xl w-full"
            >
              {suggestions.map((suggestion, i) => (
                <SuggestionCard key={suggestion} text={suggestion} index={i} />
              ))}
            </motion.div>
          </div>
        ) : (
          <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-8">
            {messages.map((msg, i) => (
              <MessageBubble
                key={msg.id}
                message={msg}
                index={i}
                onShowSources={() => handleShowSources(msg.sources)}
              />
            ))}
            <AnimatePresence>
              {isStreaming && messages[messages.length - 1]?.content === '' && (
                <TypingIndicator />
              )}
            </AnimatePresence>
            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <ChatInput />
    </div>
  )
}

function SuggestionCard({ text, index }: { text: string; index: number }) {
  const { sendMessage } = useChat()

  return (
    <motion.button
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 + index * 0.08 }}
      whileHover={{ y: -2, transition: { duration: 0.2 } }}
      onClick={() => sendMessage(text)}
      className="group text-left p-4 rounded-2xl border border-[var(--border-default)] bg-[var(--bg-glass)] backdrop-blur-xl hover:border-cyan-500/30 hover:shadow-[0_0_30px_-10px_rgba(6,182,212,0.35)] transition-all duration-300"
    >
      <div className="flex items-start gap-3">
        <div className="h-8 w-8 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center shrink-0 group-hover:bg-cyan-500/20 transition-colors">
          {index === 0 ? (
            <Sparkles className="h-4 w-4 text-cyan-400" />
          ) : (
            <Zap className="h-4 w-4 text-violet-400" />
          )}
        </div>
        <p className="text-sm text-[var(--text-secondary)] group-hover:text-[var(--text-primary)] leading-relaxed transition-colors">
          {text}
        </p>
      </div>
    </motion.button>
  )
}
