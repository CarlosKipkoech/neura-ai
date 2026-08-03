import { cn } from '@/lib/utils'
import { ChevronDown } from 'lucide-react'

interface SelectProps {
  label?: string
  value: string
  onChange: (value: string) => void
  options: { value: string; label: string }[]
  className?: string
  id?: string
}

export function Select({ label, value, onChange, options, className, id }: SelectProps) {
  return (
    <div className={cn('space-y-1.5', className)}>
      {label && (
        <label htmlFor={id} className="block text-sm font-medium text-[var(--text-secondary)]">
          {label}
        </label>
      )}
      <div className="relative">
        <select
          id={id}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className={cn(
            'w-full h-11 px-4 pr-10 rounded-xl text-sm appearance-none cursor-pointer',
            'bg-[var(--bg-tertiary)] border border-[var(--border-default)]',
            'text-[var(--text-primary)]',
            'transition-all duration-200',
            'focus:outline-none focus:ring-2 focus:ring-brand-500/40 focus:border-brand-500/50',
            'hover:border-[var(--border-default)] hover:bg-[var(--bg-elevated)]',
          )}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[var(--text-muted)] pointer-events-none" />
      </div>
    </div>
  )
}
