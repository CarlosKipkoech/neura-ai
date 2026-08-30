import { motion } from 'framer-motion'
import { Bot } from 'lucide-react'

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      className="flex gap-4"
    >
      <div className="h-9 w-9 rounded-xl neura-orb-sm flex items-center justify-center shrink-0">
        <Bot className="h-4 w-4 text-white" />
      </div>

      <div className="flex items-center gap-3 px-5 py-4 rounded-2xl rounded-tl-sm border border-[var(--border-default)] bg-[var(--bg-glass)] backdrop-blur-xl">
        <div className="flex gap-1.5">
          {[0, 1, 2].map((i) => (
            <motion.span
              key={i}
              className="h-2 w-2 rounded-full bg-gradient-to-r from-cyan-400 to-violet-400"
              animate={{ opacity: [0.3, 1, 0.3], scale: [0.85, 1.1, 0.85] }}
              transition={{
                duration: 1.2,
                repeat: Infinity,
                delay: i * 0.2,
                ease: 'easeInOut',
              }}
            />
          ))}
        </div>
        <span className="text-xs font-medium uppercase tracking-[0.15em] text-[var(--text-muted)]">
          Synthesizing response
        </span>
      </div>
    </motion.div>
  )
}
