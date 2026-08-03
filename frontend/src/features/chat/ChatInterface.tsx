import { AnimatePresence } from 'framer-motion'
import { Sparkles, PanelRightOpen } from 'lucide-react'
import { useChat } from '@/context/ChatContext'
import { useAuth } from '@/context/AuthContext'
import { useAutoScroll } from '@/hooks/useAutoScroll'
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

  const handleShowSources = (sources: typeof messages[0]['sources']) => {
    if (sources) {
      setActiveSources(sources)
      setSourcesPanelOpen(true)
    }
  }

  return (
    <div className="flex-1 flex flex-col min-w-0 h-full">
      {/* Chat Header */}
      <div className="flex items-center justify-between px-6 py-3 border-b border-[var(--border-subtle)] bg-[var(--bg-secondary)]">
        <div className="flex items-center gap-3">
          <h2 className="text-sm font-semibold text-[var(--text-primary)]">
            {activeConversation?.title ?? 'New Conversation'}
          </h2>
          {user && <Badge role={user.role} variant="role" />}
        </div>
        <div className="flex items-center gap-2">
          {!sourcesPanelOpen && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSourcesPanelOpen(true)}
            >
              <PanelRightOpen className="h-4 w-4" />
              Sources
            </Button>
          )}
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center px-6">
            <div className="h-16 w-16 rounded-2xl gradient-brand flex items-center justify-center mb-6 shadow-lg shadow-brand-500/20">
              <Sparkles className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-[var(--text-primary)] mb-2">
              Welcome, {user?.name?.split(' ')[0]}
            </h3>
            <p className="text-sm text-[var(--text-secondary)] text-center max-w-md mb-8">
              Ask questions about FinSolve policies, compliance requirements, or internal
              documentation. Your {user?.role} role determines accessible document scope.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 max-w-lg w-full">
              {[
                'What are the expense approval thresholds?',
                'Explain our PTO accrual policy',
                'Summarize SOX compliance requirements',
                'How does RBAC work in our systems?',
              ].map((suggestion) => (
                <SuggestionCard key={suggestion} text={suggestion} />
              ))}
            </div>
          </div>
        ) : (
          <div className="max-w-3xl mx-auto px-6 py-6 space-y-6">
            {messages.map((msg) => (
              <MessageBubble
                key={msg.id}
                message={msg}
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

function SuggestionCard({ text }: { text: string }) {
  const { sendMessage } = useChat()
  return (
    <button
      onClick={() => sendMessage(text)}
      className="text-left text-sm px-4 py-3 rounded-xl border border-[var(--border-default)] bg-[var(--bg-elevated)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:border-brand-500/30 hover:bg-brand-500/5 transition-all duration-200"
    >
      {text}
    </button>
  )
}
