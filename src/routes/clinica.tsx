import { createFileRoute } from "@tanstack/react-router";
import { motion } from "motion/react";
import { useQuery } from "@tanstack/react-query";
import * as Icons from "lucide-react";
import { Clock, FileText, CalendarPlus, Stethoscope } from "lucide-react";
import { clinicService } from "@/services";
import { toast } from "sonner";
import type { Specialty } from "@/types";

export const Route = createFileRoute("/clinica")({
  head: () => ({ meta: [{ title: "Clínica-Escola — UniMap" }, { name: "description", content: "Especialidades, agendamento e orçamento na Clínica-Escola UNIPÊ." }] }),
  component: ClinicaPage,
});

function ClinicaPage() {
  const { data: specialties } = useQuery({ queryKey: ["specialties"], queryFn: clinicService.specialties });

  const quote = async (s: Specialty) => {
    const r = await clinicService.requestQuote(s.id);
    toast.success(`Orçamento solicitado · ${s.name}`, { description: `Protocolo ${r.quoteId}. Retorno em até 24h.` });
  };
  const schedule = async (s: Specialty) => {
    const r = await clinicService.schedule(s.id, new Date().toISOString());
    toast.success(`Agendado · ${s.name}`, { description: `Confirmação ${r.bookingId} enviada por e-mail.` });
  };

  return (
    <div className="px-4 lg:px-8 py-6 lg:py-8 max-w-6xl mx-auto">
      <div className="rounded-3xl bg-gradient-to-br from-success/15 via-surface to-accent/40 border border-border p-7 lg:p-9 mb-6 relative overflow-hidden">
        <div className="absolute -right-12 -top-12 size-56 rounded-full bg-success/20 blur-3xl" />
        <div className="relative max-w-2xl">
          <div className="size-11 rounded-2xl bg-surface border border-border grid place-items-center shadow-soft mb-4">
            <Stethoscope className="size-5 text-success" strokeWidth={2.2} />
          </div>
          <h1 className="text-[26px] lg:text-[32px] font-semibold tracking-[-0.025em]">Clínica-Escola UNIPÊ</h1>
          <p className="text-[14px] text-muted-foreground mt-2 leading-relaxed max-w-lg">Atendimentos abertos à comunidade, conduzidos por estudantes sob supervisão de docentes especialistas.</p>
          <div className="mt-4 flex items-center gap-2 text-[12px] text-muted-foreground">
            <Clock className="size-3.5" /> Segunda a sexta · 08h às 18h
          </div>
        </div>
      </div>

      <h2 className="text-[18px] font-semibold tracking-tight mb-3">Especialidades</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {(specialties ?? []).map((s, i) => {
          const Icon = (Icons as any)[s.icon] ?? Stethoscope;
          return (
            <motion.div
              key={s.id}
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}
              className="group rounded-3xl border border-border bg-surface p-5 shadow-soft hover:shadow-elevated transition-all"
            >
              <div className="flex items-start gap-3 mb-4">
                <div className="size-11 rounded-2xl bg-primary-soft grid place-items-center">
                  <Icon className="size-5 text-primary" strokeWidth={2.2} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-[15px] font-semibold tracking-tight">{s.name}</div>
                  <div className="text-[12px] text-muted-foreground mt-0.5">{s.description}</div>
                </div>
              </div>
              <div className="flex items-center justify-between text-[11.5px] text-muted-foreground mb-4">
                <span className="inline-flex items-center gap-1"><Clock className="size-3.5" /> {s.durationMin} min</span>
                <span className="font-medium text-foreground">{s.priceRange}</span>
              </div>
              <div className="flex gap-2">
                <button onClick={() => schedule(s)} className="flex-1 inline-flex items-center justify-center gap-1.5 rounded-xl bg-primary text-primary-foreground h-9 text-[12.5px] font-medium hover:opacity-95 transition-opacity">
                  <CalendarPlus className="size-3.5" /> Agendar
                </button>
                <button onClick={() => quote(s)} className="inline-flex items-center justify-center gap-1.5 rounded-xl bg-secondary hover:bg-secondary/70 h-9 px-3.5 text-[12.5px] font-medium transition-colors">
                  <FileText className="size-3.5" /> Orçamento
                </button>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
