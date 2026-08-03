import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Bot, User, FileText } from 'lucide-react'
import type { ChatMessage } from '@/types'
import { cn } from '@/lib/utils'

interface MessageBubbleProps {
  message: ChatMessage
  onShowSources?: () => void
}

export function MessageBubble({ message, onShowSources }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: [0.25, 0.46, 0.45, 0.94] }}
      className={cn('flex gap-3 max-w-3xl', isUser ? 'ml-auto flex-row-reverse' : '')}
    >
      {/* Avatar */}
      <div
        className={cn(
          'h-8 w-8 rounded-lg flex items-center justify-center shrink-0',
          isUser
            ? 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)]'
            : 'gradient-brand text-white',
        )}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>

      {/* Content */}
      <div className={cn('flex-1 min-w-0', isUser ? 'text-right' : '')}>
        <div
          className={cn(
            'inline-block rounded-2xl px-4 py-3 text-sm text-left',
            isUser
              ? 'bg-brand-500/15 text-[var(--text-primary)] border border-brand-500/20 rounded-tr-md'
              : 'bg-[var(--bg-elevated)] border border-[var(--border-default)] rounded-tl-md',
          )}
        >
          {isUser ? (
            <p className="leading-relaxed">{message.content}</p>
          ) : (
            <div className="prose-chat">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
              {message.isStreaming && (
                <span className="inline-block w-1.5 h-4 bg-brand-400 ml-0.5 animate-pulse-soft rounded-sm" />
              )}
            </div>
          )}
        </div>

        {/* Source citations */}
        {!isUser && message.sources && message.sources.length > 0 && !message.isStreaming && (
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            onClick={onShowSources}
            className="mt-2 flex items-center gap-1.5 text-xs text-[var(--text-muted)] hover:text-brand-400 transition-colors"
          >
            <FileText className="h-3 w-3" />
            {message.sources.length} source{message.sources.length > 1 ? 's' : ''} referenced
          </motion.button>
        )}
      </div>
    </motion.div>
  )
}
