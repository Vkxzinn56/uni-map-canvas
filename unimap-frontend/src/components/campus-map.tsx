import { motion } from "motion/react";
import { mockBlocks, mockServices } from "@/mock";

interface Props {
  highlightedBlockId?: string | null;
  showBlocks?: boolean;
  showServices?: boolean;
  compact?: boolean;
  onSelectBlock?: (id: string) => void;
}

/**
 * Illustrated SVG campus map.
 * Pure presentation — coordinates come from mock data (0–100 viewport).
 */
export function CampusMap({ highlightedBlockId, showBlocks = true, showServices = true, compact = false, onSelectBlock }: Props) {
  return (
    <div className={`relative w-full ${compact ? "aspect-[16/10]" : "aspect-[16/11]"} rounded-3xl overflow-hidden border border-border shadow-soft bg-gradient-to-br from-accent/40 via-surface to-primary-soft/40`}>
      {/* Decorative grid */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.18]" preserveAspectRatio="none">
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="var(--color-foreground)" strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>

      {/* Pathways */}
      <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 60" preserveAspectRatio="none">
        <path d="M 5 50 Q 30 48 50 40 T 95 28" stroke="var(--color-border)" strokeWidth="2.4" fill="none" strokeLinecap="round" />
        <path d="M 25 5 Q 30 30 38 55" stroke="var(--color-border)" strokeWidth="1.8" fill="none" strokeDasharray="2 2" strokeLinecap="round" />
        <path d="M 70 5 Q 65 30 60 55" stroke="var(--color-border)" strokeWidth="1.8" fill="none" strokeDasharray="2 2" strokeLinecap="round" />
      </svg>

      {/* Green areas */}
      <div className="absolute" style={{ left: "12%", top: "8%", width: "16%", height: "14%" }}>
        <div className="w-full h-full rounded-[40%] bg-success/15" />
      </div>
      <div className="absolute" style={{ left: "82%", top: "55%", width: "12%", height: "16%" }}>
        <div className="w-full h-full rounded-[40%] bg-success/15" />
      </div>

      {/* Blocks */}
      {showBlocks && mockBlocks.map((b, i) => {
        const highlighted = highlightedBlockId === b.id;
        return (
          <motion.button
            key={b.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 * i, type: "spring", stiffness: 220, damping: 24 }}
            onClick={() => onSelectBlock?.(b.id)}
            className="absolute -translate-x-1/2 -translate-y-1/2 group focus:outline-none"
            style={{ left: `${b.x}%`, top: `${b.y}%` }}
          >
            <div className={`relative flex items-center gap-2 rounded-2xl bg-surface border border-border pl-1.5 pr-3 py-1.5 shadow-soft transition-all group-hover:shadow-elevated ${highlighted ? "ring-2 ring-primary scale-105" : ""}`}>
              <div className="size-7 rounded-xl grid place-items-center text-[12.5px] font-bold text-primary-foreground" style={{ background: b.color }}>
                {b.code}
              </div>
              <span className="text-[11.5px] font-medium whitespace-nowrap">{b.name.split("—")[1]?.trim() ?? b.code}</span>
            </div>
            {highlighted && (
              <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} className="absolute -top-1 -right-1 size-3 rounded-full bg-primary ring-2 ring-background" />
            )}
          </motion.button>
        );
      })}

      {/* Services */}
      {showServices && mockServices.map((s, i) => (
        <motion.div
          key={s.id}
          initial={{ opacity: 0, scale: 0.6 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 + 0.04 * i }}
          className="absolute -translate-x-1/2 -translate-y-1/2"
          style={{ left: `${s.x}%`, top: `${s.y}%` }}
        >
          <div className="size-3 rounded-full bg-foreground/70 ring-4 ring-background/80" title={s.name} />
        </motion.div>
      ))}

      {/* You are here */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="absolute -translate-x-1/2 -translate-y-1/2"
        style={{ left: "10%", top: "50%" }}
      >
        <div className="relative">
          <div className="absolute inset-0 rounded-full bg-primary/40 animate-ping" />
          <div className="size-3.5 rounded-full bg-primary ring-4 ring-background" />
        </div>
      </motion.div>
    </div>
  );
}
