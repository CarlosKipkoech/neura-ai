import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, ChevronUp, FileText, X, Shield } from 'lucide-react'
import { useState } from 'react'
import type { SourceDocument } from '@/types'
import { cn } from '@/lib/utils'

interface SourcePanelProps {
  sources: SourceDocument[]
  isOpen: boolean
  onClose: () => void
}

function SourceCard({ source }: { source: SourceDocument }) {
  const [expanded, setExpanded] = useState(false)
  const confidencePercent = Math.round(source.confidence * 100)

  const confidenceColor =
    confidencePercent >= 90
      ? 'text-emerald-400 bg-emerald-500/15'
      : confidencePercent >= 75
        ? 'text-amber-400 bg-amber-500/15'
        : 'text-red-400 bg-red-500/15'

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-[var(--border-default)] bg-[var(--bg-elevated)] overflow-hidden"
    >
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-start gap-3 p-4 text-left hover:bg-[var(--bg-tertiary)] transition-colors"
      >
        <div className="h-8 w-8 rounded-lg bg-brand-500/10 flex items-center justify-center shrink-0">
          <FileText className="h-4 w-4 text-brand-400" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-[var(--text-primary)] leading-snug">
            {source.title}
          </p>
          <div className="flex items-center gap-2 mt-1.5">
            <span className="text-[10px] font-medium uppercase tracking-wider px-1.5 py-0.5 rounded bg-[var(--bg-tertiary)] text-[var(--text-muted)]">
              {source.department}
            </span>
            <span className={cn('text-[10px] font-semibold px-1.5 py-0.5 rounded', confidenceColor)}>
              {confidencePercent}% match
            </span>
            {source.page && (
              <span className="text-[10px] text-[var(--text-muted)]">p.{source.page}</span>
            )}
          </div>
        </div>
        {expanded ? (
          <ChevronUp className="h-4 w-4 text-[var(--text-muted)] shrink-0 mt-1" />
        ) : (
          <ChevronDown className="h-4 w-4 text-[var(--text-muted)] shrink-0 mt-1" />
        )}
      </button>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 border-t border-[var(--border-subtle)]">
              <p className="text-xs text-[var(--text-secondary)] leading-relaxed pt-3">
                {source.content}
              </p>
              {source.lastUpdated && (
                <p className="text-[10px] text-[var(--text-muted)] mt-2">
                  Last updated: {source.lastUpdated}
                </p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

export function SourcePanel({ sources, isOpen, onClose }: SourcePanelProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.aside
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: 360, opacity: 1 }}
          exit={{ width: 0, opacity: 0 }}
          transition={{ duration: 0.3, ease: [0.25, 0.46, 0.45, 0.94] }}
          className="h-full border-l border-[var(--border-default)] bg-[var(--bg-secondary)] overflow-hidden shrink-0"
        >
          <div className="w-[360px] h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-[var(--border-subtle)]">
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-brand-400" />
                <h3 className="text-sm font-semibold text-[var(--text-primary)]">
                  Source Documents
                </h3>
                <span className="text-xs text-[var(--text-muted)] bg-[var(--bg-tertiary)] px-1.5 py-0.5 rounded">
                  {sources.length}
                </span>
              </div>
              <button
                onClick={onClose}
                className="h-7 w-7 rounded-lg flex items-center justify-center text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-tertiary)] transition-colors"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            </div>

            {/* Sources list */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {sources.length === 0 ? (
                <div className="text-center py-12">
                  <FileText className="h-8 w-8 text-[var(--text-muted)] mx-auto mb-3 opacity-50" />
                  <p className="text-sm text-[var(--text-muted)]">No sources yet</p>
                  <p className="text-xs text-[var(--text-muted)] mt-1">
                    Sources appear when the AI references documents
                  </p>
                </div>
              ) : (
                sources.map((source) => <SourceCard key={source.id} source={source} />)
              )}
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  )
}
