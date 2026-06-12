import { create } from "zustand";
import type { User, UserRole } from "@/types";
import { mockUser } from "@/mock";

interface AuthState {
  user: User | null;
  isVisitor: boolean;
  loginModalOpen: boolean;
  openLogin: () => void;
  closeLogin: () => void;
  login: (rgm: string, role?: UserRole) => void;
  loginAs: (role: UserRole, identifier?: string) => void;
  logout: () => void;
}

const courseByRole: Partial<Record<UserRole, string>> = {
  student: "Ciência da Computação",
  teacher: "Docente · Engenharia de Software",
  coordination: "Coordenação · Computação",
  admin: "Administração Geral",
};

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isVisitor: true,
  loginModalOpen: false,
  openLogin: () => set({ loginModalOpen: true }),
  closeLogin: () => set({ loginModalOpen: false }),
  login: (rgm, role = "student") =>
    set({
      user: { ...mockUser, rgm, role, course: courseByRole[role] ?? mockUser.course },
      isVisitor: false,
      loginModalOpen: false,
    }),
  loginAs: (role, identifier) =>
    set({
      user: {
        ...mockUser,
        role,
        rgm: role === "student" ? identifier ?? mockUser.rgm : undefined,
        email: identifier && identifier.includes("@") ? identifier : mockUser.email,
        course: courseByRole[role] ?? mockUser.course,
      },
      isVisitor: false,
      loginModalOpen: false,
    }),
  logout: () => set({ user: null, isVisitor: true }),
}));
