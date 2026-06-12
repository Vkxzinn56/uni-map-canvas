import { useState } from "react";
import { Link, useRouterState } from "@tanstack/react-router";
import { motion } from "motion/react";
import {
  Home, Map, Calendar, CalendarHeart, Stethoscope, User as UserIcon,
  Search, Bell, Sparkles, Menu, X, LayoutGrid, LogOut,
} from "lucide-react";
import { useAuthStore } from "@/store/auth";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { GlobalSearch } from "@/components/global-search";

const allNav = [
  { to: "/", label: "Início", icon: Home, auth: false },
  { to: "/mapa", label: "Mapa", icon: Map, auth: false },
  { to: "/agenda", label: "Agenda", icon: Calendar, auth: true },
  { to: "/eventos", label: "Eventos", icon: CalendarHeart, auth: false },
  { to: "/servicos", label: "Serviços", icon: LayoutGrid, auth: false },
  { to: "/clinica", label: "Clínica", icon: Stethoscope, auth: false },
  { to: "/perfil", label: "Perfil", icon: UserIcon, auth: false },
] as const;

export function AppShell({ children }: { children: React.ReactNode }) {
  const path = useRouterState({ select: (s) => s.location.pathname });
  const openLogin = useAuthStore((s) => s.openLogin);
  const user = useAuthStore((s) => s.user);
  const [mobileMenu, setMobileMenu] = useState(false);

  const nav = allNav.filter((n) => !n.auth || !!user);
  const mobileNav = nav.filter((n) => n.to !== "/perfil").slice(0, 5);

  return (
    <div className="min-h-screen flex w-full bg-background">
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex w-64 shrink-0 flex-col border-r border-border bg-sidebar p-5 sticky top-0 h-screen">
        <Link to="/" className="flex items-center gap-2.5 mb-10 group">
          <div className="size-9 rounded-xl bg-primary grid place-items-center shadow-soft">
            <Sparkles className="size-4.5 text-primary-foreground" strokeWidth={2.4} />
          </div>
          <div className="leading-tight">
            <div className="text-[15px] font-semibold tracking-tight">UniMap</div>
            <div className="text-[11px] text-muted-foreground">UNIPÊ · v3.0</div>
          </div>
        </Link>

        <nav className="flex flex-col gap-1">
          {nav.map(({ to, label, icon: Icon }) => {
            const active = to === "/" ? path === "/" : path.startsWith(to);
            return (
              <Link
                key={to}
                to={to}
                className={`group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-[14px] font-medium transition-all ${
                  active ? "text-foreground" : "text-muted-foreground hover:text-foreground hover:bg-sidebar-accent"
                }`}
              >
                {active && (
                  <motion.div
                    layoutId="sidebar-active"
                    className="absolute inset-0 rounded-xl bg-sidebar-accent"
                    transition={{ type: "spring", stiffness: 380, damping: 32 }}
                  />
                )}
                <Icon className="size-4.5 relative z-10" strokeWidth={2} />
                <span className="relative z-10">{label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto rounded-2xl border border-border bg-surface p-4 shadow-soft">
          {user ? (
            <div className="flex items-center gap-3">
              <div className="size-9 rounded-full bg-gradient-to-br from-primary to-chart-5 grid place-items-center text-primary-foreground text-sm font-semibold">
                {user.name.split(" ").map(p => p[0]).slice(0,2).join("")}
              </div>
              <div className="min-w-0">
                <div className="text-[13px] font-medium truncate">{user.name}</div>
                <div className="text-[11px] text-muted-foreground truncate">{user.course}</div>
              </div>
            </div>
          ) : (
            <>
              <div className="text-[13px] font-semibold mb-1">Acesso de visitante</div>
              <p className="text-[11.5px] text-muted-foreground leading-relaxed mb-3">Entre para acessar agenda, notas e serviços.</p>
              <Button size="sm" className="w-full" onClick={openLogin}>Entrar</Button>
            </>
          )}
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 min-w-0 flex flex-col">
        {/* Top bar */}
        <header className="sticky top-0 z-30 glass border-b border-border">
          <div className="flex items-center gap-3 px-4 lg:px-8 h-14 lg:h-16">
            <button className="lg:hidden -ml-1 p-2" onClick={() => setMobileMenu(true)}><Menu className="size-5" /></button>
            <Link to="/" className="lg:hidden flex items-center gap-2">
              <div className="size-7 rounded-lg bg-primary grid place-items-center">
                <Sparkles className="size-3.5 text-primary-foreground" strokeWidth={2.4} />
              </div>
              <span className="font-semibold tracking-tight">UniMap</span>
            </Link>

            <div className="hidden md:flex flex-1 max-w-xl ml-2">
              <div className="relative w-full">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
                <input
                  placeholder="Buscar salas, blocos, eventos, professores…"
                  className="w-full h-10 pl-10 pr-16 rounded-xl bg-secondary/70 border border-transparent focus:border-border focus:bg-surface outline-none text-[13.5px] transition-colors"
                />
                <kbd className="absolute right-2.5 top-1/2 -translate-y-1/2 hidden lg:flex h-6 px-1.5 items-center rounded-md border border-border bg-surface text-[10.5px] text-muted-foreground font-medium">⌘K</kbd>
              </div>
            </div>

            <div className="flex-1 md:hidden" />

            <ThemeToggle />
            <button className="size-9 grid place-items-center rounded-xl hover:bg-secondary transition-colors relative">
              <Bell className="size-4.5" strokeWidth={2} />
              <span className="absolute top-2 right-2 size-2 rounded-full bg-primary" />
            </button>
          </div>
        </header>

        <main className="flex-1 pb-24 lg:pb-10">{children}</main>

        {/* Mobile bottom nav */}
        <nav className="lg:hidden fixed bottom-0 inset-x-0 z-30 glass border-t border-border pb-[env(safe-area-inset-bottom)]">
          <div className="grid grid-cols-5 h-16">
            {mobileNav.map(({ to, label, icon: Icon }) => {
              const active = to === "/" ? path === "/" : path.startsWith(to);
              return (
                <Link key={to} to={to} className="flex flex-col items-center justify-center gap-1 relative">
                  {active && (
                    <motion.div layoutId="mobnav-dot" className="absolute top-2 size-1 rounded-full bg-primary" />
                  )}
                  <Icon className={`size-5 transition-colors ${active ? "text-primary" : "text-muted-foreground"}`} strokeWidth={active ? 2.4 : 2} />
                  <span className={`text-[10.5px] font-medium ${active ? "text-foreground" : "text-muted-foreground"}`}>{label}</span>
                </Link>
              );
            })}
          </div>
        </nav>
      </div>

      {/* Mobile menu drawer */}
      {mobileMenu && (
        <div className="lg:hidden fixed inset-0 z-50">
          <div className="absolute inset-0 bg-foreground/30 backdrop-blur-sm" onClick={() => setMobileMenu(false)} />
          <motion.div
            initial={{ x: "-100%" }} animate={{ x: 0 }} exit={{ x: "-100%" }}
            transition={{ type: "spring", stiffness: 320, damping: 32 }}
            className="absolute left-0 top-0 bottom-0 w-72 bg-sidebar border-r border-border p-5 flex flex-col"
          >
            <div className="flex items-center justify-between mb-8">
              <Link to="/" onClick={() => setMobileMenu(false)} className="flex items-center gap-2">
                <div className="size-9 rounded-xl bg-primary grid place-items-center"><Sparkles className="size-4 text-primary-foreground" /></div>
                <span className="font-semibold tracking-tight">UniMap</span>
              </Link>
              <button onClick={() => setMobileMenu(false)} className="p-2"><X className="size-5" /></button>
            </div>
            <nav className="flex flex-col gap-1">
              {nav.map(({ to, label, icon: Icon }) => (
                <Link key={to} to={to} onClick={() => setMobileMenu(false)} className="flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium hover:bg-sidebar-accent">
                  <Icon className="size-4.5" /> {label}
                </Link>
              ))}
            </nav>
            <div className="mt-auto">
              {!user && <Button className="w-full" onClick={() => { setMobileMenu(false); openLogin(); }}>Entrar</Button>}
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
}
