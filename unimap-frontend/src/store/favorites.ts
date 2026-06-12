import { create } from "zustand";
import { persist } from "zustand/middleware";

export type FavoriteKind = "block" | "place" | "route" | "service" | "event";

export interface Favorite {
  id: string;
  kind: FavoriteKind;
  title: string;
  subtitle?: string;
  href?: string;
  addedAt: number;
}

interface FavoritesState {
  items: Favorite[];
  toggle: (fav: Omit<Favorite, "addedAt">) => void;
  has: (id: string) => boolean;
  clear: () => void;
}

export const useFavoritesStore = create<FavoritesState>()(
  persist(
    (set, get) => ({
      items: [],
      has: (id) => get().items.some((i) => i.id === id),
      toggle: (fav) =>
        set((s) => {
          const exists = s.items.find((i) => i.id === fav.id);
          if (exists) return { items: s.items.filter((i) => i.id !== fav.id) };
          return { items: [{ ...fav, addedAt: Date.now() }, ...s.items].slice(0, 100) };
        }),
      clear: () => set({ items: [] }),
    }),
    { name: "unimap-favorites" }
  )
);
