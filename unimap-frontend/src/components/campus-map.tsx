import { useEffect, useMemo, useRef, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap, useMapEvents } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { mockBlocks, mockServices } from "@/mock";

const UNIPE_CENTER: [number, number] = [-7.15927, -34.85474];
const PORTARIA: [number, number] = [-7.15850, -34.85750];
const DEFAULT_ZOOM = 17;

const CHART_COLORS: Record<string, string> = {
  "var(--chart-1)": "#ef4444",
  "var(--chart-2)": "#3b82f6",
  "var(--chart-3)": "#22c55e",
  "var(--chart-4)": "#f59e0b",
  "var(--chart-5)": "#8b5cf6",
};

function blockIcon(color: string, code: string, highlighted: boolean): L.DivIcon {
  const baseColor = CHART_COLORS[color] || "#6366f1";
  const border = highlighted ? "3px solid #fff" : "3px solid #fff";
  const shadow = highlighted
    ? "0 0 0 4px rgba(59,130,246,0.5),0 2px 12px rgba(0,0,0,0.2)"
    : "0 2px 12px rgba(0,0,0,0.18)";
  const scale = highlighted ? "transform:scale(1.15);" : "";
  return L.divIcon({
    className: "",
    html: `<div style="background:${baseColor};width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:16px;border:${border};box-shadow:${shadow};cursor:pointer;transition:all 0.2s;${scale}">${code}</div>`,
    iconSize: [42, 42],
    iconAnchor: [21, 21],
  });
}

const serviceIcon = L.divIcon({
  className: "",
  html: `<div style="width:16px;height:16px;border-radius:50%;background:rgba(100,116,139,0.8);border:3px solid rgba(255,255,255,0.95);box-shadow:0 1px 6px rgba(0,0,0,0.15);"></div>`,
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});

const entranceIcon = L.divIcon({
  className: "",
  html: `<div style="width:30px;height:30px;border-radius:50%;background:#22c55e;border:3px solid white;box-shadow:0 2px 8px rgba(0,0,0,0.15);display:flex;align-items:center;justify-content:center;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg></div>`,
  iconSize: [30, 30],
  iconAnchor: [15, 15],
});

interface FitBoundsProps {
  coordinates: [number, number][];
}

function FitBounds({ coordinates }: FitBoundsProps) {
  const map = useMap();
  useEffect(() => {
    if (coordinates.length > 0) {
      const bounds = L.latLngBounds(coordinates.map(c => L.latLng(c[0], c[1])));
      map.fitBounds(bounds, { padding: [60, 60], maxZoom: 18 });
    }
  }, [coordinates, map]);
  return null;
}

interface ClickCatcherProps {
  onMapClick?: () => void;
}

function ClickCatcher({ onMapClick }: ClickCatcherProps) {
  useMapEvents({ click: () => onMapClick?.() });
  return null;
}

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
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  const blocks = useMemo(() => mockBlocks, []);
  const services = useMemo(() => mockServices, []);

  const hasRoute = routeCoordinates && routeCoordinates.length > 0;

  if (!mounted) {
    return (
      <div className={`w-full ${compact ? "aspect-[16/10]" : "aspect-[16/11]"} rounded-3xl bg-accent/40 border border-border flex items-center justify-center`}>
        <svg className="animate-spin size-5 text-muted-foreground" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" fill="none" strokeDasharray="32" strokeLinecap="round" /></svg>
      </div>
    );
  }

  return (
    <div className={`w-full ${compact ? "aspect-[16/10]" : "aspect-[16/11]"} rounded-3xl overflow-hidden border border-border shadow-soft relative`}>
      <MapContainer
        center={UNIPE_CENTER}
        zoom={compact ? 16 : DEFAULT_ZOOM}
        className="w-full h-full"
        zoomControl={!compact}
        scrollWheelZoom={!compact}
        dragging={!compact}
        doubleClickZoom={!compact}
        touchZoom={!compact}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <ClickCatcher onMapClick={() => onSelectBlock?.("")} />

        {showEntrance && (
          <Marker position={PORTARIA} icon={entranceIcon}>
            <Popup><div className="text-sm font-medium">Portaria Principal</div></Popup>
          </Marker>
        )}

        {showBlocks && blocks.map((b) => {
          const pos: [number, number] = [b.latitude, b.longitude];
          const hl = highlightedBlockId === b.id;
          return (
            <Marker
              key={b.id}
              position={pos}
              icon={blockIcon(b.color, b.code, hl)}
              eventHandlers={{ click: () => onSelectBlock?.(b.id) }}
            >
              <Popup>
                <div className="text-sm min-w-[140px]">
                  <div className="font-semibold text-[14px]">{b.code} — {b.name.split("—")[1]?.trim() || b.name}</div>
                  <div className="text-muted-foreground text-[11.5px] mt-1 leading-snug">{b.description}</div>
                  <div className="text-[11px] text-muted-foreground mt-1">{b.floors} andares</div>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {showServices && services.map((s) => {
          const pos: [number, number] = [s.latitude, s.longitude];
          return (
            <Marker key={s.id} position={pos} icon={serviceIcon}>
              <Popup>
                <div className="text-sm min-w-[120px]">
                  <div className="font-semibold text-[13px]">{s.name}</div>
                  <div className="text-muted-foreground text-[11px] mt-0.5">{s.hours}</div>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {hasRoute && (
          <>
            <Polyline
              positions={routeCoordinates!}
              pathOptions={{ color: "#3b82f6", weight: 4, opacity: 0.8, dashArray: "8 4" }}
            />
            <FitBounds coordinates={routeCoordinates!} />
          </>
        )}
      </MapContainer>
    </div>
  );
}
