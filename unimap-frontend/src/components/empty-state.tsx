import type { LucideIcon } from "lucide-react";
import { Inbox } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

export function EmptyState({
  icon: Icon = Inbox,
  title,
  description,
  actionLabel,
  onAction,
  className = "",
}: EmptyStateProps) {
  return (
    <div
      className={`flex flex-col items-center justify-center text-center px-6 py-14 rounded-3xl border border-dashed border-border bg-surface/50 ${className}`}
      role="status"
      aria-live="polite"
    >
      <div className="size-14 rounded-2xl bg-primary-soft grid place-items-center mb-4">
        <Icon className="size-6 text-primary" strokeWidth={2} aria-hidden />
      </div>
      <h3 className="text-[15px] font-semibold tracking-tight">{title}</h3>
      {description && (
        <p className="mt-1.5 text-[13px] text-muted-foreground max-w-sm leading-relaxed">{description}</p>
      )}
      {actionLabel && onAction && (
        <Button size="sm" className="mt-5 rounded-xl" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
}
