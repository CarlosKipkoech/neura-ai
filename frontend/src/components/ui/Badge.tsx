import { cn } from '@/lib/utils'
import type { UserRole } from '@/types'
import { ROLE_COLORS, ROLE_LABELS } from '@/types'

interface BadgeProps {
  role?: UserRole
  label?: string
  variant?: 'role' | 'default' | 'success' | 'warning' | 'danger'
  className?: string
}

const variantStyles = {
  default: 'bg-[var(--bg-tertiary)] text-[var(--text-secondary)] border-[var(--border-default)]',
  success: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  warning: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  danger: 'bg-red-500/15 text-red-400 border-red-500/30',
  role: '',
}

export function Badge({ role, label, variant = 'default', className }: BadgeProps) {
  const text = label ?? (role ? ROLE_LABELS[role] : '')
  const style = variant === 'role' && role ? ROLE_COLORS[role] : variantStyles[variant]

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium',
        style,
        className,
      )}
    >
      {text}
    </span>
  )
}
