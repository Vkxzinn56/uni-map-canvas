import { useMemo, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import { motion } from "motion/react";
import * as Icons from "lucide-react";
import { Sparkles, Lock, ArrowRight, ExternalLink } from "lucide-react";
import { useAuthStore } from "@/store/auth";
import { getVisibleServices, type ServiceItem } from "@/lib/services-visibility";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/servicos")({
  head: () => ({ meta: [
    { title: "Serviços — UniMap" },
    { name: "description", content: "Serviços públicos e acadêmicos da UNIPÊ em um só lugar." },
  ] }),
  component: ServicosPage,
});

function ServicosPage() {
  const user = useAuthStore((s) => s.user);
  const openLogin = useAuthStore((s) => s.openLogin);
  const role: "visitor" | "student" = user ? "student" : "visitor";
  const services = useMemo(() => getVisibleServices(role), [role]);
  const [restricted, setRestricted] = useState<ServiceItem | null>(null);

  const categories = useMemo(() => {
    const map = new Map<string, ServiceItem[]>();
    services.forEach((s) => {
      const arr = map.get(s.category) ?? [];
      arr.push(s);
      map.set(s.category, arr);
    });
    return Array.from(map.entries());
  }, [services]);

  return (
    <div className="px-4 lg:px-8 py-6 lg:py-8 max-w-6xl mx-auto">
      <div className="rounded-3xl bg-gradient-to-br from-primary-soft via-surface to-accent/40 border border-border p-7 lg:p-9 mb-6 relative overflow-hidden">
        <div className="absolute -right-12 -top-12 size-56 rounded-full bg-primary/15 blur-3xl" />
        <div className="relative max-w-2xl">
          <div className="size-11 rounded-2xl bg-surface border border-border grid place-items-center shadow-soft mb-4">
            <Sparkles className="size-5 text-primary" strokeWidth={2.2} />
          </div>
          <h1 className="text-[26px] lg:text-[32px] font-semibold tracking-[-0.025em]">Serviços UNIPÊ</h1>
          <p className="text-[14px] text-muted-foreground mt-2 leading-relaxed max-w-lg">
            {user
              ? "Tudo o que você precisa no campus e na sua vida acadêmica, em um só lugar."
              : "Conheça os serviços abertos à comunidade. Faça login para acessar também sua área acadêmica."}
          </p>
          {!user && (
            <button onClick={openLogin} className="mt-5 inline-flex items-center gap-2 rounded-2xl bg-primary text-primary-foreground px-5 h-11 text-[13.5px] font-medium shadow-soft hover:opacity-95 transition-opacity">
              Entrar com RGM <ArrowRight className="size-4" />
            </button>
          )}
        </div>
      </div>

      <div className="space-y-8">
        {categories.map(([cat, items]) => (
          <section key={cat}>
            <div className="flex items-baseline justify-between mb-3">
              <h2 className="text-[15px] font-semibold tracking-tight">{cat}</h2>
              <span className="text-[11.5px] text-muted-foreground">{items.length} serviço{items.length > 1 ? "s" : ""}</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {items.map((s, i) => {
                const Ico = (Icons as unknown as Record<string, React.ComponentType<{ className?: string; strokeWidth?: number }>>)[s.icon] ?? Icons.Box;
                const isPrivate = s.visibility === "private";
                const content = (
                  <motion.div
                    initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.03 }}
                    className="group h-full rounded-3xl border border-border bg-surface p-5 shadow-soft hover:shadow-elevated transition-all"
                  >
                    <div className="flex items-start gap-3">
                      <div className="size-10 rounded-2xl bg-primary-soft grid place-items-center shrink-0">
                        <Ico className="size-5 text-primary" strokeWidth={2.2} />
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center gap-1.5">
                          <div className="text-[14.5px] font-semibold tracking-tight truncate">{s.name}</div>
                          {isPrivate && <Lock className="size-3 text-muted-foreground" />}
                          {s.external && <ExternalLink className="size-3 text-muted-foreground" />}
                        </div>
                        <p className="text-[12.5px] text-muted-foreground mt-1 leading-relaxed line-clamp-2">{s.description}</p>
                        {(s.hours || s.contact) && (
                          <div className="text-[11.5px] text-muted-foreground mt-2 tabular-nums">{s.hours ?? s.contact}</div>
                        )}
                      </div>
                    </div>
                  </motion.div>
                );

                if (s.external) {
                  return (
                    <a key={s.id} href={s.external} target="_blank" rel="noopener noreferrer" className="block">
                      {content}
                    </a>
                  );
                }
                if (isPrivate) {
                  return (
                    <button key={s.id} type="button" onClick={() => setRestricted(s)} className="text-left">
                      {content}
                    </button>
                  );
                }
                if (s.href) {
                  return <Link key={s.id} to={s.href as any} className="block">{content}</Link>;
                }
                return <div key={s.id}>{content}</div>;
              })}
            </div>
          </section>
        ))}
      </div>

      <Dialog open={!!restricted} onOpenChange={(o) => !o && setRestricted(null)}>
        <DialogContent className="sm:max-w-md rounded-3xl border-border">
          <DialogHeader className="text-left space-y-2">
            <div className="size-10 rounded-2xl bg-primary-soft grid place-items-center mb-1">
              <Lock className="size-5 text-primary" />
            </div>
            <DialogTitle className="text-[20px] tracking-tight">Acesso Acadêmico</DialogTitle>
            <DialogDescription className="text-[13.5px]">
              Para visualizar informações acadêmicas, faça login com seu RGM ou e-mail institucional.
            </DialogDescription>
          </DialogHeader>
          <div className="flex gap-2 pt-2">
            <Button variant="ghost" className="flex-1" onClick={() => setRestricted(null)}>Voltar</Button>
            <Button className="flex-1" onClick={() => { setRestricted(null); openLogin(); }}>Entrar</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
