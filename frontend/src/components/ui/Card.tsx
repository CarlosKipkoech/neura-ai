import { cn } from '@/lib/utils'
import type { ReactNode } from 'react'

interface CardProps {
  children: ReactNode
  className?: string
  hover?: boolean
  glass?: boolean
}

export function Card({ children, className, hover, glass }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-xl border border-[var(--border-default)]',
        glass ? 'glass' : 'bg-[var(--bg-elevated)]',
        hover && 'transition-all duration-200 hover:border-[var(--border-default)] hover:shadow-lg hover:shadow-black/10',
        className,
      )}
    >
      {children}
    </div>
  )
}

export function CardHeader({ children, className }: { children: ReactNode; className?: string }) {
  return <div className={cn('px-5 pt-5 pb-3', className)}>{children}</div>
}

export function CardContent({ children, className }: { children: ReactNode; className?: string }) {
  return <div className={cn('px-5 pb-5', className)}>{children}</div>
}

export function CardTitle({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <h3 className={cn('text-sm font-semibold text-[var(--text-primary)]', className)}>
      {children}
    </h3>
  )
}
