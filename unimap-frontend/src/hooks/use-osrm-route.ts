import { useState, useCallback } from "react";

export interface OsrmWaypoint {
  lat: number;
  lng: number;
}

export interface OsrmStep {
  instruction: string;
  distance: number;
  duration: number;
}

export interface OsrmRouteData {
  coordinates: [number, number][];
  steps: OsrmStep[];
  distance: number;
  duration: number;
}

export function useOsrmRoute() {
  const [route, setRoute] = useState<OsrmRouteData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRoute = useCallback(async (from: OsrmWaypoint, to: OsrmWaypoint) => {
    setLoading(true);
    setError(null);
    try {
      const url = `https://router.project-osrm.org/route/v1/foot/${from.lng},${from.lat};${to.lng},${to.lat}?steps=true&geometries=geojson&overview=full&language=pt-BR`;
      const res = await fetch(url);
      const data = await res.json();
      if (data.code !== "Ok") {
        throw new Error("Falha ao calcular rota");
      }
      const leg = data.routes[0].legs[0];
      setRoute({
        coordinates: data.routes[0].geometry.coordinates.map(
          (c: [number, number]) => [c[1], c[0]] as [number, number]
        ),
        steps: leg.steps.map((s: any) => ({
          instruction: s.maneuver?.instruction || s.name || "Siga em frente",
          distance: Math.round(s.distance),
          duration: Math.round(s.duration),
        })),
        distance: Math.round(data.routes[0].distance),
        duration: Math.round(data.routes[0].duration / 60),
      });
    } catch (e: any) {
      setError(e.message || "Erro ao calcular rota");
    } finally {
      setLoading(false);
    }
  }, []);

  const clearRoute = useCallback(() => {
    setRoute(null);
    setError(null);
  }, []);

  return { route, loading, error, fetchRoute, clearRoute };
}
