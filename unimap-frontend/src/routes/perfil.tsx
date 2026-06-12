import { createFileRoute } from "@tanstack/react-router";
import { motion } from "motion/react";
import { Award, BookOpen, GraduationCap, Trophy, LogIn, LogOut } from "lucide-react";
import { useAuthStore } from "@/store/auth";
import { mockUser } from "@/mock";

export const Route = createFileRoute("/perfil")({
  head: () => ({ meta: [{ title: "Perfil — UniMap" }] }),
  component: PerfilPage,
});

function PerfilPage() {
  const isVisitor = useAuthStore((s) => s.isVisitor);
  const user = useAuthStore((s) => s.user) ?? mockUser;
  const openLogin = useAuthStore((s) => s.openLogin);
  const logout = useAuthStore((s) => s.logout);

  return (
    <div className="px-4 lg:px-8 py-6 lg:py-8 max-w-3xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
        className="rounded-3xl bg-gradient-to-br from-primary-soft via-surface to-accent/40 border border-border p-7 shadow-soft relative overflow-hidden"
      >
        <div className="absolute -right-14 -top-14 size-56 rounded-full bg-primary/15 blur-3xl" />
        <div className="relative flex flex-col sm:flex-row items-start sm:items-center gap-5">
          <div className="size-20 rounded-3xl bg-gradient-to-br from-primary to-chart-5 grid place-items-center text-primary-foreground text-[26px] font-semibold shadow-elevated">
            {user.name.split(" ").map(p => p[0]).slice(0, 2).join("")}
          </div>
          <div className="flex-1 min-w-0">
            <h1 className="text-[22px] font-semibold tracking-[-0.02em]">{isVisitor ? "Visitante" : user.name}</h1>
            <p className="text-[13px] text-muted-foreground mt-0.5">{isVisitor ? "Entre para personalizar sua experiência" : `${user.course} · ${user.semester}º semestre`}</p>
            {!isVisitor && <p className="text-[11.5px] text-muted-foreground mt-1.5">RGM {user.rgm} · {user.email}</p>}
          </div>
          <div>
            {isVisitor ? (
              <button onClick={openLogin} className="inline-flex items-center gap-1.5 rounded-2xl bg-primary text-primary-foreground px-4 h-10 text-[13px] font-medium shadow-soft">
                <LogIn className="size-4" /> Entrar
              </button>
            ) : (
              <button onClick={logout} className="inline-flex items-center gap-1.5 rounded-2xl bg-surface border border-border px-4 h-10 text-[13px] font-medium hover:bg-secondary transition-colors">
                <LogOut className="size-4" /> Sair
              </button>
            )}
          </div>
        </div>
      </motion.div>

      {!isVisitor && (
        <>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mt-5">
            {[
              { icon: Trophy, label: "Conquistas", value: user.achievements },
              { icon: GraduationCap, label: "Progresso", value: `${user.progress}%` },
              { icon: BookOpen, label: "Disciplinas", value: 6 },
              { icon: Award, label: "Créditos", value: 142 },
            ].map((s) => (
              <div key={s.label} className="rounded-2xl border border-border bg-surface p-4 shadow-soft">
                <s.icon className="size-4 text-primary mb-2" />
                <div className="text-[20px] font-semibold tabular-nums tracking-tight">{s.value}</div>
                <div className="text-[11.5px] text-muted-foreground">{s.label}</div>
              </div>
            ))}
          </div>

          <div className="mt-5 rounded-3xl border border-border bg-surface p-6 shadow-soft">
            <div className="flex items-baseline justify-between mb-2">
              <div className="text-[14px] font-semibold">Progresso do curso</div>
              <div className="text-[12.5px] text-muted-foreground tabular-nums">{user.progress}% concluído</div>
            </div>
            <div className="h-2.5 rounded-full bg-secondary overflow-hidden">
              <motion.div
                initial={{ width: 0 }} animate={{ width: `${user.progress}%` }}
                transition={{ duration: 1, ease: [0.2, 0.8, 0.2, 1] }}
                className="h-full bg-gradient-to-r from-primary to-chart-5"
              />
            </div>
            <div className="mt-4 grid grid-cols-3 gap-3 text-center">
              {["Iniciado", "Andamento", "Próxima formatura"].map((s, i) => (
                <div key={s} className={`rounded-xl p-2.5 ${i === 1 ? "bg-primary-soft" : "bg-secondary/60"}`}>
                  <div className="text-[10.5px] uppercase tracking-wider text-muted-foreground">{s}</div>
                  <div className="text-[12px] font-semibold mt-0.5">{["2023.1", "2025.2", "2027.2"][i]}</div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
