import { create } from "zustand";
import { persist } from "zustand/middleware";

export type HistoryKind = "place" | "search" | "route";

export interface HistoryEntry {
  id: string;
  kind: HistoryKind;
  label: string;
  meta?: string;
  href?: string;
  at: number;
}

interface HistoryState {
  entries: HistoryEntry[];
  push: (e: Omit<HistoryEntry, "at">) => void;
  clear: () => void;
}

export const useHistoryStore = create<HistoryState>()(
  persist(
    (set) => ({
      entries: [],
      push: (e) =>
        set((s) => {
          const next = [{ ...e, at: Date.now() }, ...s.entries.filter((x) => x.id !== e.id)];
          return { entries: next.slice(0, 25) };
        }),
      clear: () => set({ entries: [] }),
    }),
    { name: "unimap-history" }
  )
);
