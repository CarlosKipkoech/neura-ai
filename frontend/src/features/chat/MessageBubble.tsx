import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Bot, FileText, User } from 'lucide-react'
import type { ChatMessage } from '@/types'
import { cn } from '@/lib/utils'

interface MessageBubbleProps {
  message: ChatMessage
  index?: number
  onShowSources?: () => void
}

export function MessageBubble({ message, index = 0, onShowSources }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  if (isUser) {
    return (
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.35, delay: index * 0.03 }}
        className="flex justify-end gap-3"
      >
        <div className="max-w-[85%] sm:max-w-[70%]">
          <div className="inline-block rounded-2xl rounded-tr-sm px-5 py-3.5 text-sm leading-relaxed bg-gradient-to-br from-cyan-600/20 to-violet-600/20 border border-cyan-500/25 text-[var(--text-primary)] shadow-[0_4px_24px_-8px_rgba(6,182,212,0.25)]">
            {message.content}
          </div>
        </div>
        <div className="h-9 w-9 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border-default)] flex items-center justify-center shrink-0">
          <User className="h-4 w-4 text-[var(--text-muted)]" />
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.03 }}
      className="flex gap-4"
    >
      <div className="h-9 w-9 rounded-xl neura-orb-sm flex items-center justify-center shrink-0 mt-1">
        <Bot className="h-4 w-4 text-white" />
      </div>

      <div className="flex-1 min-w-0">
        <div className="relative rounded-2xl rounded-tl-sm border border-[var(--border-default)] bg-[var(--bg-glass)] backdrop-blur-xl overflow-hidden shadow-[0_8px_32px_-12px_rgba(0,0,0,0.4)]">
          <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-cyan-400 via-violet-500 to-cyan-400" />
          <div className="px-5 py-4 pl-6">
            <div className="prose-chat">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
              {message.isStreaming && (
                <span className="inline-block w-0.5 h-4 bg-cyan-400 ml-1 animate-pulse-soft rounded-sm align-middle" />
              )}
            </div>
          </div>
        </div>

        {!message.isStreaming && message.sources && message.sources.length > 0 && (
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            onClick={onShowSources}
            className={cn(
              'mt-3 inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium',
              'border border-violet-500/25 bg-violet-500/10 text-violet-300',
              'hover:bg-violet-500/20 hover:border-violet-500/40 transition-all duration-200',
            )}
          >
            <FileText className="h-3.5 w-3.5" />
            {message.sources.length} source{message.sources.length > 1 ? 's' : ''} cited
          </motion.button>
        )}
      </div>
    </motion.div>
  )
}
