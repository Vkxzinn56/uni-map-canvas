import { useEffect, useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";
import { mockBlocks, mockRooms, mockEvents, mockServices } from "@/mock";
import { useHistoryStore } from "@/store/history";
import { Building2, DoorClosed, CalendarHeart, MapPin } from "lucide-react";

export function GlobalSearch({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (o: boolean) => void;
}) {
  const navigate = useNavigate();
  const push = useHistoryStore((s) => s.push);
  const [query, setQuery] = useState("");

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        onOpenChange(!open);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onOpenChange]);

  const go = (href: string, label: string) => {
    push({ id: href, kind: "search", label, meta: query, href });
    onOpenChange(false);
    setQuery("");
    navigate({ to: href });
  };

  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Buscar blocos, salas, eventos, serviços…" value={query} onValueChange={setQuery} />
      <CommandList>
        <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>
        <CommandGroup heading="Blocos">
          {mockBlocks.map((b) => (
            <CommandItem key={b.id} value={`${b.name} ${b.code}`} onSelect={() => go("/mapa", b.name)}>
              <Building2 className="size-4" /> {b.name}
            </CommandItem>
          ))}
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Salas">
          {mockRooms.slice(0, 8).map((r) => (
            <CommandItem key={r.id} value={r.name} onSelect={() => go("/mapa", r.name)}>
              <DoorClosed className="size-4" /> {r.name}
            </CommandItem>
          ))}
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Eventos">
          {mockEvents.map((e) => (
            <CommandItem key={e.id} value={e.title} onSelect={() => go("/eventos", e.title)}>
              <CalendarHeart className="size-4" /> {e.title}
            </CommandItem>
          ))}
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Serviços e clínicas">
          {mockServices.map((s) => (
            <CommandItem key={s.id} value={s.name} onSelect={() => go("/servicos", s.name)}>
              <MapPin className="size-4" /> {s.name}
            </CommandItem>
          ))}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
