import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { motion } from "motion/react";
import { useQuery } from "@tanstack/react-query";
import { Calendar, MapPin, Users, Check, ArrowRight, Lock } from "lucide-react";
import { eventService } from "@/services";
import { useAuthStore } from "@/store/auth";
import { toast } from "sonner";
import { EventDetailsDialog } from "@/components/event-details-dialog";
import type { Event } from "@/types";

export const Route = createFileRoute("/eventos")({
  head: () => ({ meta: [{ title: "Eventos — UniMap" }, { name: "description", content: "Descubra eventos, palestras e workshops no UNIPÊ." }] }),
  component: EventosPage,
});

const categories = ["Todos", "Tecnologia", "Carreira", "Cultura"] as const;
const visibilityFilters = ["Todos", "Públicos", "Privados"] as const;

function EventosPage() {
  const { data: events } = useQuery({ queryKey: ["events"], queryFn: eventService.list });
  const isVisitor = useAuthStore((s) => s.isVisitor);
  const openLogin = useAuthStore((s) => s.openLogin);
  const [cat, setCat] = useState<typeof categories[number]>("Todos");
  const [vis, setVis] = useState<typeof visibilityFilters[number]>("Todos");
  const [registered, setRegistered] = useState<Record<string, boolean>>({});
  const [open, setOpen] = useState<Event | null>(null);

  const filtered = (events ?? [])
    .filter((e) => (cat === "Todos" || e.category === cat))
    .filter((e) => (vis === "Todos" ? true : vis === "Públicos" ? e.visibility === "public" : e.visibility === "private"))
    .filter((e) => (isVisitor ? e.visibility === "public" : true));

  const privateCount = (events ?? []).filter((e) => e.visibility === "private").length;

  const register = async (id: string) => {
    const ev = (events ?? []).find((x) => x.id === id);
    if (ev?.visibility === "private" && isVisitor) {
      openLogin();
      return;
    }
    await eventService.register(id);
    setRegistered((p) => ({ ...p, [id]: true }));
    toast.success("Inscrição confirmada!", { description: "Você receberá lembretes antes do evento." });
  };

  return (
    <div className="px-4 lg:px-8 py-6 lg:py-8 max-w-7xl mx-auto">
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4 mb-6">
        <div>
          <h1 className="text-[26px] lg:text-[32px] font-semibold tracking-[-0.025em]">Eventos</h1>
          <p className="text-[13.5px] text-muted-foreground mt-1">
            Palestras, workshops e atividades do campus.
            {isVisitor && privateCount > 0 && (
              <span className="ml-2 inline-flex items-center gap-1 text-primary"><Lock className="size-3" /> {privateCount} eventos privados para alunos</span>
            )}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <div className="flex gap-1.5 p-1 rounded-2xl bg-secondary/70 border border-border w-fit overflow-x-auto scrollbar-none">
            {visibilityFilters.map((v) => (
              <button
                key={v}
                onClick={() => setVis(v)}
                disabled={isVisitor && v === "Privados"}
                className={`relative px-3 h-9 rounded-xl text-[12px] font-medium whitespace-nowrap transition-colors disabled:opacity-40 disabled:cursor-not-allowed ${vis === v ? "text-foreground" : "text-muted-foreground hover:text-foreground"}`}
              >
                {vis === v && <motion.div layoutId="evt-vis-pill" className="absolute inset-0 rounded-xl bg-surface shadow-soft" transition={{ type: "spring", stiffness: 380, damping: 32 }} />}
                <span className="relative z-10 inline-flex items-center gap-1">{v === "Privados" && <Lock className="size-3" />}{v}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="mb-5 flex gap-1.5 p-1 rounded-2xl bg-secondary/70 border border-border w-fit overflow-x-auto scrollbar-none">
        {categories.map((c) => (
          <button
            key={c}
            onClick={() => setCat(c)}
            className={`relative px-3.5 h-9 rounded-xl text-[12.5px] font-medium whitespace-nowrap transition-colors ${cat === c ? "text-foreground" : "text-muted-foreground hover:text-foreground"}`}
          >
            {cat === c && <motion.div layoutId="evt-pill" className="absolute inset-0 rounded-xl bg-surface shadow-soft" transition={{ type: "spring", stiffness: 380, damping: 32 }} />}
            <span className="relative z-10">{c}</span>
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {filtered.map((e, i) => {
          const isReg = registered[e.id] || e.registered;
          return (
            <motion.article
              key={e.id}
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
              className="group rounded-3xl border border-border bg-surface shadow-soft hover:shadow-elevated transition-all overflow-hidden flex flex-col"
            >
              <button onClick={() => setOpen(e)} className="text-left">
                <div className="h-40 relative overflow-hidden" style={{ background: e.cover }}>
                  <div className="absolute inset-0 bg-gradient-to-t from-foreground/30 to-transparent" />
                  <div className="absolute top-3 left-3 flex items-center gap-1.5">
                    <span className="text-[10.5px] font-semibold uppercase tracking-wider bg-surface/95 backdrop-blur px-2.5 py-1 rounded-md">{e.category}</span>
                    {e.visibility === "private" && (
                      <span className="inline-flex items-center gap-1 text-[10.5px] font-semibold uppercase tracking-wider bg-primary/95 text-primary-foreground backdrop-blur px-2 py-1 rounded-md">
                        <Lock className="size-3" /> Privado
                      </span>
                    )}
                  </div>
                </div>
              </button>
              <div className="p-5 flex-1 flex flex-col">
                <button onClick={() => setOpen(e)} className="text-left">
                  <h3 className="text-[16px] font-semibold tracking-tight leading-snug hover:text-primary transition-colors">{e.title}</h3>
                </button>
                <p className="text-[12.5px] text-muted-foreground mt-1.5 line-clamp-2 leading-relaxed">{e.description}</p>
                <div className="grid grid-cols-2 gap-2 mt-4 text-[11.5px] text-muted-foreground">
                  <div className="flex items-center gap-1.5"><Calendar className="size-3.5" /> {new Date(e.date).toLocaleDateString("pt-BR", { day: "2-digit", month: "short" })} · {e.startTime}</div>
                  <div className="flex items-center gap-1.5"><MapPin className="size-3.5" /> {e.location}</div>
                </div>

                {e.speakers && e.speakers.length > 0 && (
                  <div className="mt-3 flex items-center gap-1.5">
                    <div className="flex -space-x-1.5">
                      {e.speakers.slice(0, 3).map((sp, k) => (
                        <div key={k} className="size-6 rounded-full grid place-items-center text-[9.5px] font-bold bg-primary/15 text-primary ring-2 ring-surface">
                          {sp.name.split(" ").slice(0, 2).map((p) => p[0]).join("")}
                        </div>
                      ))}
                    </div>
                    <span className="text-[11px] text-muted-foreground truncate">{e.speakers[0].name}{e.speakers.length > 1 ? ` +${e.speakers.length - 1}` : ""}</span>
                  </div>
                )}

                <div className="mt-auto pt-4 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1.5 text-[11.5px] text-muted-foreground">
                    <Users className="size-3.5" /> {e.attendees}/{e.capacity}
                  </div>
                  <div className="flex items-center gap-1.5">
                    <button onClick={() => setOpen(e)} className="inline-flex items-center gap-1 rounded-xl px-3 h-9 text-[12.5px] font-medium text-foreground/80 hover:bg-secondary transition-colors">
                      Detalhes <ArrowRight className="size-3.5" />
                    </button>
                    <button
                      disabled={isReg}
                      onClick={() => register(e.id)}
                      className={`inline-flex items-center gap-1.5 rounded-xl px-3.5 h-9 text-[12.5px] font-medium transition-all ${
                        isReg ? "bg-success/15 text-success" : "bg-primary text-primary-foreground hover:opacity-95"
                      }`}
                    >
                      {isReg ? <><Check className="size-3.5" /> Inscrito</> : "Inscrever-se"}
                    </button>
                  </div>
                </div>
              </div>
            </motion.article>
          );
        })}
      </div>

      <EventDetailsDialog
        event={open}
        isRegistered={open ? !!(registered[open.id] || open.registered) : false}
        onClose={() => setOpen(null)}
        onRegister={register}
      />
    </div>
  );
}
