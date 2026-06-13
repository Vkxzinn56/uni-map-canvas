import { useState, useEffect } from "react";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { motion, AnimatePresence } from "motion/react";
import { useQuery } from "@tanstack/react-query";
import { MapPin, Navigation, Lock, User as UserIcon, Sparkles } from "lucide-react";
import { agendaService } from "@/services";
import { useAuthStore } from "@/store/auth";
import { mockBlocks } from "@/mock";
import type { AgendaItem } from "@/types";

export const Route = createFileRoute("/agenda")({
  head: () => ({ meta: [{ title: "Agenda — UniMap" }, { name: "description", content: "Sua agenda acadêmica, aulas, provas e eventos." }] }),
  component: AgendaPage,
});

const typeStyles: Record<AgendaItem["type"], { bg: string; text: string; label: string }> = {
  class: { bg: "bg-primary-soft", text: "text-primary", label: "Aula" },
  exam: { bg: "bg-destructive/10", text: "text-destructive", label: "Prova" },
  event: { bg: "bg-accent", text: "text-accent-foreground", label: "Evento" },
  personal: { bg: "bg-success/15", text: "text-success", label: "Pessoal" },
};

function AgendaPage() {
  const navigate = useNavigate();
  const isVisitor = useAuthStore((s) => s.isVisitor);
  const openLogin = useAuthStore((s) => s.openLogin);
  const { data: items } = useQuery({ queryKey: ["agenda"], queryFn: agendaService.list, enabled: !isVisitor });
  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().slice(0, 10));

  const days = (() => {
    const arr: { iso: string; weekday: string; day: string }[] = [];
    const base = new Date();
    for (let i = 0; i < 7; i++) {
      const d = new Date(base); d.setDate(base.getDate() + i);
      arr.push({
        iso: d.toISOString().slice(0, 10),
        weekday: d.toLocaleDateString("pt-BR", { weekday: "short" }).replace(".", "").slice(0, 3),
        day: String(d.getDate()).padStart(2, "0"),
      });
    }
    return arr;
  })();

  const dayItems = (items ?? []).filter((i) => i.date === selectedDate);

  const goToMap = (blockId?: string) => {
    if (blockId) {
      navigate({ to: "/mapa", search: { block: blockId } });
    } else {
      navigate({ to: "/mapa" });
    }
  };

  if (isVisitor) {
    return (
      <div className="px-4 lg:px-8 py-16 max-w-md mx-auto text-center">
        <div className="size-14 mx-auto rounded-2xl bg-primary-soft grid place-items-center mb-5">
          <Lock className="size-6 text-primary" />
        </div>
        <h1 className="text-[22px] font-semibold tracking-tight">Agenda é exclusiva para alunos</h1>
        <p className="text-[13.5px] text-muted-foreground mt-2 leading-relaxed">Entre com seu RGM e e-mail institucional para acessar sua agenda completa, com aulas, provas e eventos.</p>
        <button onClick={openLogin} className="mt-6 inline-flex items-center gap-2 rounded-2xl bg-primary text-primary-foreground px-5 h-11 text-[13.5px] font-medium shadow-soft">
          <UserIcon className="size-4" /> Entrar agora
        </button>
      </div>
    );
  }

  return (
    <div className="px-4 lg:px-8 py-6 lg:py-8 max-w-5xl mx-auto">
      <div className="flex items-end justify-between mb-5">
        <div>
          <h1 className="text-[26px] lg:text-[32px] font-semibold tracking-[-0.025em]">Sua agenda</h1>
          <p className="text-[13.5px] text-muted-foreground mt-1">Próximas atividades desta semana.</p>
        </div>
        <div className="hidden md:flex items-center gap-1.5 text-[11.5px] text-muted-foreground bg-secondary/70 border border-border px-3 py-1.5 rounded-full">
          <Sparkles className="size-3.5 text-primary" /> Sincronizado com Blackboard
        </div>
      </div>

      <div className="flex gap-2 overflow-x-auto scrollbar-none pb-2 mb-5 -mx-1 px-1">
        {days.map((d) => {
          const active = d.iso === selectedDate;
          return (
            <button
              key={d.iso}
              onClick={() => setSelectedDate(d.iso)}
              className={`shrink-0 flex flex-col items-center justify-center w-16 h-20 rounded-2xl border transition-all ${
                active ? "bg-primary text-primary-foreground border-primary shadow-soft" : "bg-surface border-border text-foreground hover:bg-secondary"
              }`}
            >
              <span className={`text-[10.5px] uppercase font-medium ${active ? "opacity-80" : "text-muted-foreground"}`}>{d.weekday}</span>
              <span className="text-[20px] font-semibold tabular-nums mt-0.5">{d.day}</span>
            </button>
          );
        })}
      </div>

      <div className="space-y-3">
        {dayItems.length === 0 && (
          <div className="rounded-3xl border border-dashed border-border bg-surface/60 p-10 text-center">
            <div className="text-[14px] font-medium">Nenhuma atividade neste dia</div>
            <p className="text-[12.5px] text-muted-foreground mt-1">Aproveite para se preparar para a próxima semana.</p>
          </div>
        )}
        {dayItems.map((item, i) => {
          const style = typeStyles[item.type];
          return (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.04 }}
              className="group rounded-3xl border border-border bg-surface p-5 shadow-soft hover:shadow-elevated transition-shadow"
            >
              <div className="flex items-start gap-4">
                <div className="flex flex-col items-center min-w-14">
                  <div className="text-[18px] font-semibold tabular-nums">{item.startTime}</div>
                  <div className="text-[10.5px] text-muted-foreground tabular-nums mt-0.5">até {item.endTime}</div>
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className={`text-[10.5px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-md ${style.bg} ${style.text}`}>{style.label}</span>
                  </div>
                  <div className="text-[15.5px] font-semibold tracking-tight">{item.title}</div>
                  {item.teacher && <div className="text-[12.5px] text-muted-foreground mt-0.5">{item.teacher}</div>}
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mt-2.5 text-[12.5px] text-muted-foreground">
                    <span className="inline-flex items-center gap-1"><MapPin className="size-3.5" /> {item.location}</span>
                  </div>
                </div>
                <button
                  onClick={() => goToMap(item.blockId)}
                  className="hidden sm:inline-flex items-center gap-1.5 rounded-xl bg-secondary hover:bg-secondary/70 px-3 h-9 text-[12px] font-medium transition-colors"
                >
                  <Navigation className="size-3.5" /> Ver rota
                </button>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
