import { useEffect, useRef, useState } from "react";
import { mockBlocks, mockServices } from "@/mock";

const CHART_COLORS: Record<string, string> = {
  "var(--chart-1)": "#ef4444",
  "var(--chart-2)": "#3b82f6",
  "var(--chart-3)": "#22c55e",
  "var(--chart-4)": "#f59e0b",
  "var(--chart-5)": "#8b5cf6",
};

const UNIPE_CENTER: [number, number] = [-7.15927, -34.85474];
const PORTARIA: [number, number] = [-7.15850, -34.85750];

interface Props {
  highlightedBlockId?: string | null;
  showBlocks?: boolean;
  showServices?: boolean;
  compact?: boolean;
  onSelectBlock?: (id: string) => void;
  routeCoordinates?: [number, number][];
  showEntrance?: boolean;
}

export function CampusMap({
  highlightedBlockId,
  showBlocks = true,
  showServices = true,
  compact = false,
  onSelectBlock,
  routeCoordinates,
  showEntrance = true,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const blockLayerRef = useRef<any>(null);
  const serviceLayerRef = useRef<any>(null);
  const routeLayerRef = useRef<any>(null);
  const entranceLayerRef = useRef<any>(null);
  const clickHandlerRef = useRef<any>(null);
  const [leaflet, setLeaflet] = useState<any>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => { setMounted(true); }, []);

  useEffect(() => {
    let cancelled = false;
    import("leaflet").then((mod) => {
      if (!cancelled) {
        import("leaflet/dist/leaflet.css");
        setLeaflet(mod.default || mod);
      }
    });
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (!leaflet || !containerRef.current || mapRef.current) return;
    const L = leaflet;

    const container = containerRef.current;
    container.innerHTML = "";

    const map = L.map(container, {
      center: UNIPE_CENTER,
      zoom: compact ? 16 : 17,
      zoomControl: !compact,
      scrollWheelZoom: !compact,
      dragging: !compact,
      attributionControl: !compact,
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    blockLayerRef.current = L.layerGroup().addTo(map);
    serviceLayerRef.current = L.layerGroup().addTo(map);
    routeLayerRef.current = L.layerGroup().addTo(map);
    entranceLayerRef.current = L.layerGroup().addTo(map);

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [leaflet, compact]);

  useEffect(() => {
    const map = mapRef.current;
    const layer = entranceLayerRef.current;
    const L = leaflet;
    if (!map || !L) return;

    layer.clearLayers();
    if (!showEntrance) return;

    const icon = L.divIcon({
      className: "",
      html: `<div style="width:30px;height:30px;border-radius:50%;background:#22c55e;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.15);display:flex;align-items:center;justify-content:center;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg></div>`,
      iconSize: [30, 30],
      iconAnchor: [15, 15],
    });
    L.marker(PORTARIA, { icon }).addTo(layer);
  }, [leaflet, showEntrance]);

  useEffect(() => {
    const map = mapRef.current;
    const layer = blockLayerRef.current;
    const L = leaflet;
    if (!map || !L) return;

    layer.clearLayers();
    if (!showBlocks) return;

    for (const b of mockBlocks) {
      const baseColor = CHART_COLORS[b.color] || "#6366f1";
      const hl = highlightedBlockId === b.id;
      const icon = L.divIcon({
        className: "",
        html: `<div style="background:${baseColor};width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:16px;border:3px solid white;box-shadow:${hl ? "0 0 0 4px rgba(59,130,246,0.5),0 2px 12px rgba(0,0,0,0.2)" : "0 2px 12px rgba(0,0,0,0.18)"};cursor:pointer;${hl ? "transform:scale(1.15)" : ""}">${b.code}</div>`,
        iconSize: [42, 42],
        iconAnchor: [21, 21],
      });
      const marker = L.marker([b.latitude, b.longitude], { icon }).addTo(layer);
      marker.bindPopup(`<div style="font-size:13px;font-weight:600">${b.code} — ${(b.name.split("—")[1] || b.name).trim()}</div><div style="font-size:11.5px;color:#666;margin-top:4px">${b.description}</div>`);
      marker.on("click", () => onSelectBlock?.(b.id));
    }
  }, [leaflet, showBlocks, highlightedBlockId, onSelectBlock]);

  useEffect(() => {
    const map = mapRef.current;
    const layer = serviceLayerRef.current;
    const L = leaflet;
    if (!map || !L) return;

    layer.clearLayers();
    if (!showServices) return;

    const icon = L.divIcon({
      className: "",
      html: `<div style="width:16px;height:16px;border-radius:50%;background:rgba(100,116,139,0.8);border:3px solid rgba(255,255,255,0.95);box-shadow:0 1px 6px rgba(0,0,0,0.15);"></div>`,
      iconSize: [16, 16],
      iconAnchor: [8, 8],
    });

    for (const s of mockServices) {
      const marker = L.marker([s.latitude, s.longitude], { icon }).addTo(layer);
      marker.bindPopup(`<div style="font-size:13px;font-weight:600">${s.name}</div><div style="font-size:11px;color:#666;margin-top:2px">${s.hours}</div>`);
    }
  }, [leaflet, showServices]);

  useEffect(() => {
    const map = mapRef.current;
    const layer = routeLayerRef.current;
    const L = leaflet;
    if (!map || !L) return;

    layer.clearLayers();
    if (!routeCoordinates || routeCoordinates.length === 0) return;

    const polyline = L.polyline(routeCoordinates, {
      color: "#3b82f6",
      weight: 4,
      opacity: 0.8,
      dashArray: "8 4",
    }).addTo(layer);

    map.fitBounds(polyline.getBounds().pad(0.1));
  }, [leaflet, routeCoordinates]);

  useEffect(() => {
    const map = mapRef.current;
    const L = leaflet;
    if (!map || !L) return;

    if (clickHandlerRef.current) {
      map.off("click", clickHandlerRef.current);
    }
    const handler = () => onSelectBlock?.("");
    clickHandlerRef.current = handler;
    map.on("click", handler);
  }, [leaflet, onSelectBlock]);

  if (!mounted) {
    return (
      <div className={`w-full ${compact ? "aspect-[16/10]" : "aspect-[16/11]"} rounded-3xl bg-accent/40 border border-border flex items-center justify-center`}>
        <svg className="animate-spin size-5 text-muted-foreground" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" fill="none" strokeDasharray="32" strokeLinecap="round" /></svg>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className={`w-full ${compact ? "aspect-[16/10]" : "aspect-[16/11]"} rounded-3xl overflow-hidden border border-border shadow-soft relative`}
    />
  );
}
