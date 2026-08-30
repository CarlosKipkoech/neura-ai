import { useState, useRef, useEffect } from 'react'
import { motion } from 'framer-motion'
import { ArrowUp, Sparkles } from 'lucide-react'
import { useChat } from '@/context/ChatContext'
import { cn } from '@/lib/utils'

export function ChatInput() {
  const { sendMessage, isStreaming } = useChat()
  const [input, setInput] = useState('')
  const [focused, setFocused] = useState(false)
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
    <div className="relative z-10 px-4 sm:px-6 pb-6 pt-2">
      <div className="max-w-4xl mx-auto">
        <motion.div
          layout
          className={cn(
            'relative flex items-end gap-3 rounded-2xl border p-2 pl-4 transition-all duration-300',
            'bg-[var(--bg-glass)] backdrop-blur-2xl',
            focused
              ? 'border-cyan-500/40 shadow-[0_0_40px_-12px_rgba(6,182,212,0.4)]'
              : 'border-[var(--border-default)]',
          )}
        >
          <Sparkles className={cn(
            'h-4 w-4 shrink-0 mb-3 transition-colors duration-300',
            focused ? 'text-cyan-400' : 'text-[var(--text-muted)]',
          )} />

          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            placeholder="Query the enterprise knowledge graph…"
            rows={1}
            disabled={isStreaming}
            className={cn(
              'flex-1 resize-none bg-transparent text-sm text-[var(--text-primary)]',
              'placeholder:text-[var(--text-muted)] focus:outline-none py-3',
              'max-h-40 leading-relaxed',
            )}
          />

          <motion.button
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            onClick={handleSubmit}
            disabled={!input.trim() || isStreaming}
            className={cn(
              'h-10 w-10 rounded-xl flex items-center justify-center shrink-0 mb-0.5 transition-all duration-300',
              input.trim() && !isStreaming
                ? 'neura-orb-sm text-white shadow-lg shadow-cyan-500/30'
                : 'bg-[var(--bg-elevated)] text-[var(--text-muted)] border border-[var(--border-default)]',
            )}
          >
            <ArrowUp className="h-4 w-4" />
          </motion.button>
        </motion.div>

        <p className="text-[10px] text-[var(--text-muted)] text-center mt-3 tracking-wide">
          Neura AI retrieves role-scoped documents · Verify critical decisions with source citations
        </p>
      </div>
    </div>
  )
}
