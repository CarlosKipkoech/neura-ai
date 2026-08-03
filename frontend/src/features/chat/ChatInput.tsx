import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Send, Paperclip } from 'lucide-react'
import { useChat } from '@/context/ChatContext'
import { cn } from '@/lib/utils'

export function ChatInput() {
  const { sendMessage, isStreaming } = useChat()
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = `${Math.min(el.scrollHeight, 160)}px`
    }
  }, [input])

  const handleSubmit = () => {
    if (!input.trim() || isStreaming) return
    sendMessage(input)
    setInput('')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="border-t border-[var(--border-subtle)] bg-[var(--bg-secondary)] p-4">
      <div className="max-w-3xl mx-auto">
        <motion.div
          layout
          className={cn(
            'flex items-end gap-2 rounded-2xl border border-[var(--border-default)]',
            'bg-[var(--bg-tertiary)] p-2 transition-shadow duration-200',
            'focus-within:border-brand-500/40 focus-within:shadow-glow',
          )}
        >
          <button
            className="h-10 w-10 rounded-xl flex items-center justify-center text-[var(--text-muted)] hover:text-[var(--text-secondary)] hover:bg-[var(--bg-elevated)] transition-colors shrink-0"
            title="Attach document"
          >
            <Paperclip className="h-4 w-4" />
          </button>

          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about policies, compliance, or internal docs…"
            rows={1}
            disabled={isStreaming}
            className={cn(
              'flex-1 resize-none bg-transparent text-sm text-[var(--text-primary)]',
              'placeholder:text-[var(--text-muted)] focus:outline-none py-2.5',
              'max-h-40 leading-relaxed',
            )}
          />

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSubmit}
            disabled={!input.trim() || isStreaming}
            className={cn(
              'h-10 w-10 rounded-xl flex items-center justify-center shrink-0 transition-all',
              input.trim() && !isStreaming
                ? 'gradient-brand text-white shadow-md shadow-brand-500/25'
                : 'bg-[var(--bg-elevated)] text-[var(--text-muted)]',
            )}
          >
            <Send className="h-4 w-4" />
          </motion.button>
        </motion.div>

        <p className="text-[10px] text-[var(--text-muted)] text-center mt-2">
          FinSolve AI may make mistakes. Verify critical information with official policy documents.
        </p>
      </div>
    </div>
  )
}
