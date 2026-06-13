import { Link } from "@tanstack/react-router";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Calendar, MapPin, Users, Clock, Mic, MessageSquare, Star, Check } from "lucide-react";
import type { Event } from "@/types";

interface Props {
  event: Event | null;
  isRegistered: boolean;
  onClose: () => void;
  onRegister: (id: string) => void;
}

function initials(name: string) {
  return name.split(" ").slice(0, 2).map((p) => p[0]).join("").toUpperCase();
}

function formatRange(e: Event) {
  const d1 = new Date(e.date).toLocaleDateString("pt-BR", { day: "2-digit", month: "short" });
  if (!e.endDate || e.endDate === e.date) return d1;
  const d2 = new Date(e.endDate).toLocaleDateString("pt-BR", { day: "2-digit", month: "short" });
  return `${d1} – ${d2}`;
}

function locationBlock(location: string): string | undefined {
  const map: Record<string, string> = {
    "bloco b": "b_b", "bloco c": "b_c", "bloco e": "b_e",
    "bloco d": "b_d", "bloco a": "b_a",
  };
  const key = Object.keys(map).find((k) => location.toLowerCase().includes(k));
  return key ? map[key] : undefined;
}

export function EventDetailsDialog({ event, isRegistered, onClose, onRegister }: Props) {
  return (
    <Dialog open={!!event} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-2xl p-0 overflow-hidden gap-0 max-h-[90vh] flex flex-col">
        {event && (
          <>
            <div className="h-40 relative shrink-0" style={{ background: event.cover }}>
              <div className="absolute inset-0 bg-gradient-to-t from-foreground/40 to-transparent" />
              <span className="absolute top-3 left-3 text-[10.5px] font-semibold uppercase tracking-wider bg-surface/95 backdrop-blur px-2.5 py-1 rounded-md">
                {event.category}
              </span>
            </div>

            <div className="px-6 pt-5 pb-6 overflow-y-auto">
              <DialogHeader className="text-left space-y-1.5">
                <DialogTitle className="text-[20px] font-semibold tracking-tight">{event.title}</DialogTitle>
                <p className="text-[13px] text-muted-foreground leading-relaxed">{event.description}</p>
              </DialogHeader>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-4">
                <div className="rounded-xl bg-secondary/60 p-2.5">
                  <div className="flex items-center gap-1.5 text-[10.5px] text-muted-foreground uppercase tracking-wider"><Calendar className="size-3" /> Data</div>
                  <div className="text-[12.5px] font-semibold mt-0.5">{formatRange(event)}</div>
                </div>
                <div className="rounded-xl bg-secondary/60 p-2.5">
                  <div className="flex items-center gap-1.5 text-[10.5px] text-muted-foreground uppercase tracking-wider"><Clock className="size-3" /> Horário</div>
                  <div className="text-[12.5px] font-semibold mt-0.5">{event.startTime}{event.endTime ? ` – ${event.endTime}` : ""}</div>
                </div>
                <div className="rounded-xl bg-secondary/60 p-2.5 col-span-2 sm:col-span-1">
                  <div className="flex items-center gap-1.5 text-[10.5px] text-muted-foreground uppercase tracking-wider"><MapPin className="size-3" /> Local</div>
                  <Link
                    to={locationBlock(event.location) ? "/mapa" : "."}
                    search={locationBlock(event.location) ? { block: locationBlock(event.location)! } : undefined}
                    className="text-[12.5px] font-semibold mt-0.5 truncate hover:text-primary transition-colors flex items-center gap-1"
                  >
                    {event.location}
                  </Link>
                </div>
              </div>

              {event.about && (
                <section className="mt-5">
                  <h4 className="text-[12px] font-semibold uppercase tracking-wider text-muted-foreground mb-2">Sobre o evento</h4>
                  <p className="text-[13.5px] leading-relaxed text-foreground/85">{event.about}</p>
                </section>
              )}

              {event.schedule && event.schedule.length > 0 && (
                <section className="mt-5">
                  <h4 className="text-[12px] font-semibold uppercase tracking-wider text-muted-foreground mb-2.5 flex items-center gap-1.5"><Clock className="size-3.5" /> Programação</h4>
                  <ol className="space-y-2.5 border-l border-border pl-4 ml-1">
                    {event.schedule.map((s, i) => (
                      <li key={i} className="relative">
                        <span className="absolute -left-[21px] top-1.5 size-2 rounded-full bg-primary ring-4 ring-surface" />
                        <div className="text-[11.5px] font-semibold text-primary tabular-nums">{s.time}</div>
                        <div className="text-[13px] font-medium leading-snug">{s.title}</div>
                        {s.description && <div className="text-[12px] text-muted-foreground leading-snug">{s.description}</div>}
                      </li>
                    ))}
                  </ol>
                </section>
              )}

              {event.speakers && event.speakers.length > 0 && (
                <section className="mt-5">
                  <h4 className="text-[12px] font-semibold uppercase tracking-wider text-muted-foreground mb-2.5 flex items-center gap-1.5"><Mic className="size-3.5" /> Palestrantes</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {event.speakers.map((sp, i) => (
                      <div key={i} className="flex items-center gap-2.5 rounded-xl border border-border bg-secondary/40 p-2.5">
                        <div className="size-9 rounded-full grid place-items-center text-[12px] font-bold bg-primary/15 text-primary shrink-0">{initials(sp.name)}</div>
                        <div className="min-w-0">
                          <div className="text-[13px] font-medium truncate">{sp.name}</div>
                          <div className="text-[11.5px] text-muted-foreground truncate">{sp.role}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              {event.comments && event.comments.length > 0 && (
                <section className="mt-5">
                  <h4 className="text-[12px] font-semibold uppercase tracking-wider text-muted-foreground mb-2.5 flex items-center gap-1.5"><MessageSquare className="size-3.5" /> Comentários</h4>
                  <div className="space-y-2">
                    {event.comments.map((c, i) => (
                      <div key={i} className="rounded-xl border border-border bg-surface p-3">
                        <div className="flex items-center justify-between gap-2">
                          <div className="text-[12.5px] font-semibold">{c.author} {c.role && <span className="font-normal text-muted-foreground">· {c.role}</span>}</div>
                          {c.rating && (
                            <div className="flex items-center gap-0.5 text-warning">
                              {Array.from({ length: c.rating }).map((_, k) => (<Star key={k} className="size-3 fill-current" />))}
                            </div>
                          )}
                        </div>
                        <p className="text-[12.5px] text-foreground/80 mt-1 leading-relaxed">{c.text}</p>
                      </div>
                    ))}
                  </div>
                </section>
              )}

              <div className="mt-6 flex items-center justify-between gap-3 pt-4 border-t border-border">
                <div className="flex items-center gap-1.5 text-[12px] text-muted-foreground">
                  <Users className="size-3.5" /> {event.attendees}/{event.capacity} inscritos
                </div>
                <button
                  disabled={isRegistered}
                  onClick={() => onRegister(event.id)}
                  className={`inline-flex items-center gap-1.5 rounded-xl px-4 h-10 text-[13px] font-medium transition-all ${
                    isRegistered ? "bg-success/15 text-success" : "bg-primary text-primary-foreground hover:opacity-95"
                  }`}
                >
                  {isRegistered ? <><Check className="size-4" /> Inscrito</> : "Inscrever-se"}
                </button>
              </div>
            </div>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}
