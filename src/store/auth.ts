import { create } from "zustand";
import type { User } from "@/types";
import { mockUser } from "@/mock";

interface AuthState {
  user: User | null;
  isVisitor: boolean;
  loginModalOpen: boolean;
  openLogin: () => void;
  closeLogin: () => void;
  login: (rgm: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isVisitor: true,
  loginModalOpen: false,
  openLogin: () => set({ loginModalOpen: true }),
  closeLogin: () => set({ loginModalOpen: false }),
  login: (rgm) => set({ user: { ...mockUser, rgm }, isVisitor: false, loginModalOpen: false }),
  logout: () => set({ user: null, isVisitor: true }),
}));
