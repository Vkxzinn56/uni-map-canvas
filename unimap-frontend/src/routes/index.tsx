import { createFileRoute, Link } from "@tanstack/react-router";
import { motion } from "motion/react";
import { useQuery } from "@tanstack/react-query";
import { ArrowUpRight, Calendar, MapPin, CalendarHeart, Stethoscope, Clock, Sparkles, Compass } from "lucide-react";
import { agendaService, eventService } from "@/services";
import { CampusMap } from "@/components/campus-map";
import { useAuthStore } from "@/store/auth";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "UniMap 3.0 — UNIPÊ" },
      { name: "description", content: "Sua universidade na palma da mão: mapa, agenda, eventos e serviços do UNIPÊ em um único lugar." },
      { property: "og:title", content: "UniMap 3.0 — UNIPÊ" },
      { property: "og:description", content: "Mapa, agenda, eventos e serviços do UNIPÊ em um único lugar." },
    ],
  }),
  component: Home,
});

function Home() {
  const isVisitor = useAuthStore((s) => s.isVisitor);
  const openLogin = useAuthStore((s) => s.openLogin);
  const { data: agenda } = useQuery({ queryKey: ["agenda-today"], queryFn: agendaService.today });
  const { data: events } = useQuery({ queryKey: ["events"], queryFn: eventService.list });
  const next = agenda?.[0];
  const upcomingEvent = events?.[0];

  return (
    <div className="px-4 lg:px-8 py-6 lg:py-10 max-w-7xl mx-auto space-y-8">
      {/* Hero */}
      <motion.section
        initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.2, 0.8, 0.2, 1] }}
        className="relative overflow-hidden rounded-3xl border border-border bg-gradient-to-br from-primary-soft via-surface to-accent/50 p-7 lg:p-10"
      >
        <div className="absolute -right-16 -top-16 size-72 rounded-full bg-primary/15 blur-3xl" />
        <div className="absolute -left-10 bottom-0 size-56 rounded-full bg-chart-2/20 blur-3xl" />
        <div className="relative max-w-2xl">
          <div className="inline-flex items-center gap-1.5 rounded-full bg-surface/80 border border-border px-3 py-1 text-[11.5px] font-medium text-muted-foreground mb-5 shadow-soft">
            <Sparkles className="size-3.5 text-primary" /> UniMap 3.0 · novo
          </div>
          <h1 className="text-[32px] lg:text-[44px] font-semibold tracking-[-0.025em] leading-[1.05] text-foreground">
            Toda a universidade, <br className="hidden md:block" />
            <span className="text-primary">em um só lugar.</span>
          </h1>
          <p className="mt-4 text-[15px] lg:text-[16px] text-muted-foreground leading-relaxed max-w-lg">
            Encontre salas, monte sua rota pelo campus, acompanhe sua agenda e descubra eventos e serviços do UNIPÊ.
          </p>
          <div className="mt-7 flex flex-wrap items-center gap-3">
            <Link to="/mapa" search={{ block: undefined }} className="inline-flex items-center gap-2 rounded-2xl bg-primary text-primary-foreground px-5 h-11 text-[13.5px] font-medium shadow-soft hover:opacity-95 transition-opacity">
              <Compass className="size-4" /> Abrir mapa do campus
            </Link>
            {isVisitor && (
              <button onClick={openLogin} className="inline-flex items-center gap-2 rounded-2xl bg-surface border border-border px-5 h-11 text-[13.5px] font-medium hover:bg-secondary transition-colors">
                Entrar como aluno <ArrowUpRight className="size-4" />
              </button>
            )}
          </div>
        </div>
      </motion.section>

      {/* Quick cards */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <QuickCard
          icon={Calendar}
          eyebrow="Próxima aula"
          title={next ? next.title : isVisitor ? "Entre para ver sua agenda" : "Sem aulas hoje"}
          meta={next ? `${next.startTime} · ${next.location}` : "—"}
          to="/agenda"
          tint="primary"
          locked={isVisitor && !next}
          onLockedClick={openLogin}
        />
        <QuickCard
          icon={CalendarHeart}
          eyebrow="Em destaque"
          title={upcomingEvent?.title ?? "Semana de Inovação"}
          meta={upcomingEvent ? `${upcomingEvent.location}` : "Auditório Central"}
          to="/eventos"
          tint="accent"
        />
        <QuickCard
          icon={Stethoscope}
          eyebrow="Clínica-escola"
          title="Atendimentos abertos"
          meta="6 especialidades · agendamento online"
          to="/clinica"
          tint="success"
        />
      </section>

      {/* Map preview */}
      <section className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-5">
        <div>
          <SectionHeader title="Mapa rápido" caption="Toque em um bloco para ver detalhes" to="/mapa" />
          <CampusMap compact />
        </div>
        <div className="space-y-3">
          <SectionHeader title="Hoje" caption={agenda?.length ? `${agenda.length} atividade(s)` : "—"} to="/agenda" />
          <div className="rounded-3xl border border-border bg-surface shadow-soft overflow-hidden">
            {(agenda ?? []).slice(0, 4).map((a, i) => (
              <div key={a.id} className={`flex items-start gap-3 p-4 ${i ? "border-t border-border" : ""}`}>
                <div className="flex flex-col items-center min-w-12">
                  <div className="text-[13px] font-semibold tabular-nums">{a.startTime}</div>
                  <div className="text-[10.5px] text-muted-foreground tabular-nums">{a.endTime}</div>
                </div>
                <div className="min-w-0">
                  <div className="text-[13.5px] font-medium truncate">{a.title}</div>
                  <div className="text-[11.5px] text-muted-foreground flex items-center gap-1 mt-0.5">
                    <MapPin className="size-3" /> {a.location}
                  </div>
                </div>
              </div>
            ))}
            {!agenda?.length && (
              <div className="p-6 text-center text-[13px] text-muted-foreground">
                <Clock className="size-5 mx-auto mb-2 opacity-50" />
                {isVisitor ? "Entre para ver sua agenda completa." : "Nenhuma atividade hoje."}
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

function SectionHeader({ title, caption, to }: { title: string; caption?: string; to: string }) {
  return (
    <div className="flex items-end justify-between mb-3">
      <div>
        <h2 className="text-[17px] font-semibold tracking-tight">{title}</h2>
        {caption && <p className="text-[12px] text-muted-foreground mt-0.5">{caption}</p>}
      </div>
      <Link to={to} className="text-[12px] font-medium text-muted-foreground hover:text-foreground inline-flex items-center gap-1">
        Ver tudo <ArrowUpRight className="size-3.5" />
      </Link>
    </div>
  );
}

function QuickCard({
  icon: Icon, eyebrow, title, meta, to, tint, locked, onLockedClick,
}: {
  icon: any; eyebrow: string; title: string; meta: string; to: string;
  tint: "primary" | "accent" | "success"; locked?: boolean; onLockedClick?: () => void;
}) {
  const tintBg = tint === "primary" ? "bg-primary-soft" : tint === "accent" ? "bg-accent" : "bg-success/15";
  const tintFg = tint === "primary" ? "text-primary" : tint === "accent" ? "text-accent-foreground" : "text-success";
  const content = (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ type: "spring", stiffness: 300, damping: 24 }}
      className="group h-full rounded-3xl border border-border bg-surface p-5 shadow-soft hover:shadow-elevated transition-shadow cursor-pointer"
    >
      <div className="flex items-center justify-between mb-4">
        <div className={`size-10 rounded-2xl grid place-items-center ${tintBg}`}>
          <Icon className={`size-5 ${tintFg}`} strokeWidth={2.2} />
        </div>
        <ArrowUpRight className="size-4 text-muted-foreground group-hover:text-foreground transition-colors" />
      </div>
      <div className="text-[11px] uppercase tracking-wider font-medium text-muted-foreground mb-1">{eyebrow}</div>
      <div className="text-[16px] font-semibold tracking-tight leading-snug">{title}</div>
      <div className="text-[12.5px] text-muted-foreground mt-1.5">{meta}</div>
    </motion.div>
  );
  if (locked) return <button onClick={onLockedClick} className="text-left">{content}</button>;
  return <Link to={to}>{content}</Link>;
}
