import { useState, useEffect } from "react";
import { createFileRoute, useSearch } from "@tanstack/react-router";
import { motion, AnimatePresence } from "motion/react";
import { Layers, Building2, DoorOpen, Coffee, Navigation, Clock, MapPin, X, Target, Info, Sparkles, Loader2 } from "lucide-react";
import { CampusMap } from "@/components/campus-map";
import { mockBlocks, mockRooms, mockServices } from "@/mock";
import { useOsrmRoute } from "@/hooks/use-osrm-route";

export const Route = createFileRoute("/mapa")({
  validateSearch: (search: Record<string, unknown>) => ({
    block: search.block as string | undefined,
  }),
  head: () => ({ meta: [
    { title: "Mapa do Campus — UniMap" },
    { name: "description", content: "Encontre blocos, salas e serviços do UNIPÊ com rotas estimadas." },
  ] }),
  component: MapaPage,
});

const PORTARIA_COORDS = { lat: -7.15850, lng: -34.85750 };

const filters = [
  { id: "all", label: "Todos", icon: Layers },
  { id: "blocks", label: "Blocos", icon: Building2 },
  { id: "rooms", label: "Salas", icon: DoorOpen },
  { id: "services", label: "Serviços", icon: Coffee },
] as const;

function MapaPage() {
  const { block: initialBlock } = useSearch({ from: Route.id });
  const [filter, setFilter] = useState<typeof filters[number]["id"]>("all");
  const [selected, setSelected] = useState<string | null>(initialBlock ?? null);
  const { route, loading, error, fetchRoute, clearRoute } = useOsrmRoute();
  const block = mockBlocks.find((b) => b.id === selected);

  useEffect(() => {
    if (selected && block) {
      fetchRoute(PORTARIA_COORDS, { lat: block.latitude, lng: block.longitude });
    } else {
      clearRoute();
    }
  }, [selected]);

  const handleSelect = (id: string) => {
    setSelected(id === selected ? null : id);
  };

  return (
    <div className="px-4 lg:px-8 py-6 lg:py-8 max-w-7xl mx-auto">
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-4 mb-5">
        <div>
          <h1 className="text-[26px] lg:text-[32px] font-semibold tracking-[-0.025em]">Mapa do campus</h1>
          <p className="text-[13.5px] text-muted-foreground mt-1">Navegue pelos blocos e serviços do UNIPÊ.</p>
        </div>
        <div className="flex gap-1.5 p-1 rounded-2xl bg-secondary/70 border border-border w-fit overflow-x-auto scrollbar-none">
          {filters.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setFilter(id)}
              className={`relative inline-flex items-center gap-1.5 px-3.5 h-9 rounded-xl text-[12.5px] font-medium whitespace-nowrap transition-colors ${
                filter === id ? "text-foreground" : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {filter === id && (
                <motion.div layoutId="filter-pill" className="absolute inset-0 rounded-xl bg-surface shadow-soft" transition={{ type: "spring", stiffness: 380, damping: 32 }} />
              )}
              <Icon className="size-3.5 relative z-10" />
              <span className="relative z-10">{label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[1fr_380px] gap-5">
        <CampusMap
          highlightedBlockId={selected}
          showBlocks={filter === "all" || filter === "blocks" || filter === "rooms"}
          showServices={filter === "all" || filter === "services"}
          onSelectBlock={handleSelect}
          routeCoordinates={route?.coordinates}
        />

        <AnimatePresence mode="wait">
          {selected && block ? (
            <motion.aside
              key={selected}
              initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: 8 }}
              className="rounded-3xl border border-border bg-surface shadow-soft p-5 h-fit max-h-[calc(100vh-7rem)] overflow-y-auto"
            >
              <div className="flex items-start justify-between gap-3 mb-3">
                <div className="flex items-center gap-3">
                  <div className="size-11 rounded-2xl grid place-items-center text-primary-foreground text-[15px] font-bold" style={{ background: block.color }}>{block.code}</div>
                  <div>
                    <div className="text-[15px] font-semibold tracking-tight">{block.name}</div>
                    <div className="text-[12px] text-muted-foreground">{block.floors} andares · {mockRooms.filter((r) => r.blockId === block.id).length} salas</div>
                  </div>
                </div>
                <button onClick={() => setSelected(null)} className="p-1.5 rounded-lg hover:bg-secondary"><X className="size-4" /></button>
              </div>

              {block.about && (
                <section className="mt-1">
                  <div className="flex items-center gap-1.5 text-[10.5px] font-semibold uppercase tracking-wider text-muted-foreground mb-1.5"><Info className="size-3" /> Sobre o bloco</div>
                  <p className="text-[12.5px] text-foreground/80 leading-relaxed">{block.about}</p>
                </section>
              )}

              {block.purpose && (
                <section className="mt-4 rounded-2xl bg-accent/40 border border-border p-3">
                  <div className="flex items-center gap-1.5 text-[10.5px] font-semibold uppercase tracking-wider text-foreground/70 mb-1"><Target className="size-3" /> Principal objetivo</div>
                  <p className="text-[12.5px] text-foreground/85 leading-relaxed">{block.purpose}</p>
                </section>
              )}

              <section className="mt-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-1.5 text-[10.5px] font-semibold uppercase tracking-wider text-muted-foreground"><DoorOpen className="size-3" /> Salas</div>
                  <span className="text-[10.5px] text-muted-foreground tabular-nums">{mockRooms.filter((r) => r.blockId === block.id).length}</span>
                </div>
                <ul className="space-y-1.5">
                  {mockRooms.filter((r) => r.blockId === block.id).map((r) => (
                    <li key={r.id} className="flex items-center justify-between gap-2 rounded-xl bg-secondary/50 px-3 py-2">
                      <span className="text-[12.5px] font-medium truncate">{r.name}</span>
                      <span className="text-[10.5px] uppercase tracking-wider text-muted-foreground shrink-0">{r.type === "lab" ? "Lab" : r.type === "auditorium" ? "Auditório" : r.type === "office" ? "Espaço" : "Sala"} · {r.floor}º</span>
                    </li>
                  ))}
                  {mockRooms.filter((r) => r.blockId === block.id).length === 0 && (
                    <li className="text-[12px] text-muted-foreground italic">Nenhuma sala mapeada.</li>
                  )}
                </ul>
              </section>

              {block.serviceIds && block.serviceIds.length > 0 && (
                <section className="mt-4">
                  <div className="flex items-center gap-1.5 text-[10.5px] font-semibold uppercase tracking-wider text-muted-foreground mb-2"><Sparkles className="size-3" /> Serviços prestados</div>
                  <ul className="space-y-1.5">
                    {mockServices.filter((s) => block.serviceIds?.includes(s.id)).map((s) => (
                      <li key={s.id} className="rounded-xl border border-border bg-surface px-3 py-2">
                        <div className="text-[12.5px] font-medium">{s.name}</div>
                        <div className="text-[11px] text-muted-foreground leading-snug">{s.description}</div>
                        <div className="flex items-center gap-1 text-[10.5px] text-muted-foreground mt-1"><Clock className="size-3" /> {s.hours}</div>
                      </li>
                    ))}
                  </ul>
                </section>
              )}

              <div className="mt-5 rounded-2xl bg-primary-soft border border-primary/10 p-4">
                <div className="flex items-center gap-2 text-[12px] font-medium text-primary mb-1.5">
                  <Navigation className="size-3.5" /> Rota da Portaria Principal
                </div>
                {loading ? (
                  <div className="flex items-center gap-2 text-[12.5px] text-muted-foreground py-2">
                    <Loader2 className="size-3.5 animate-spin" /> Calculando rota…
                  </div>
                ) : error ? (
                  <div className="text-[12px] text-destructive py-1">{error}</div>
                ) : route ? (
                  <>
                    <div className="flex items-center gap-4 text-[13px]">
                      <div>
                        <div className="text-muted-foreground text-[11px]">Distância</div>
                        <div className="font-semibold tabular-nums">{route.distance} m</div>
                      </div>
                      <div className="h-8 w-px bg-border" />
                      <div>
                        <div className="text-muted-foreground text-[11px]">Tempo</div>
                        <div className="font-semibold tabular-nums">~{route.duration} min</div>
                      </div>
                    </div>
                    {route.steps.length > 0 && (
                      <ol className="mt-3 space-y-1.5">
                        {route.steps.map((s, i) => (
                          <li key={i} className="flex gap-2 text-[12px] text-foreground/80">
                            <span className="size-4 shrink-0 rounded-full bg-primary text-primary-foreground text-[10px] font-semibold grid place-items-center mt-0.5">{i + 1}</span>
                            {s.instruction}
                          </li>
                        ))}
                      </ol>
                    )}
                  </>
                ) : null}
              </div>
            </motion.aside>
          ) : (
            <motion.aside
              initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="rounded-3xl border border-dashed border-border bg-surface/60 p-7 h-fit text-center"
            >
              <MapPin className="size-6 mx-auto text-muted-foreground mb-2.5" />
              <div className="text-[14px] font-medium">Selecione um bloco</div>
              <p className="text-[12px] text-muted-foreground mt-1">Toque em qualquer marcador no mapa para ver detalhes e rotas.</p>
              <div className="mt-5 grid grid-cols-2 gap-2 text-left">
                {[
                  { label: "Blocos", value: mockBlocks.length },
                  { label: "Serviços", value: mockServices.length },
                  { label: "Salas mapeadas", value: 48 },
                  { label: "Acessibilidade", value: "100%" },
                ].map((s) => (
                  <div key={s.label} className="rounded-2xl bg-secondary/60 p-3">
                    <div className="text-[11px] text-muted-foreground">{s.label}</div>
                    <div className="text-[16px] font-semibold tabular-nums">{s.value}</div>
                  </div>
                ))}
              </div>
              <div className="mt-4 flex items-center justify-center gap-1.5 text-[11px] text-muted-foreground">
                <Clock className="size-3.5" /> Mapa OpenStreetMap em tempo real
              </div>
            </motion.aside>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
