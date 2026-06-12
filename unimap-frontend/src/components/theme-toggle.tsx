import { Sun, Moon, Monitor } from "lucide-react";
import { useTheme } from "@/hooks/use-theme";

export function ThemeToggle() {
  const { mode, cycle } = useTheme();
  const Icon = mode === "light" ? Sun : mode === "dark" ? Moon : Monitor;
  const label =
    mode === "light" ? "Tema: Claro" : mode === "dark" ? "Tema: Escuro" : "Tema: Sistema";

  return (
    <button
      onClick={cycle}
      aria-label={label}
      title={label}
      className="size-9 grid place-items-center rounded-xl hover:bg-secondary transition-colors"
    >
      <Icon className="size-4.5" strokeWidth={2} />
    </button>
  );
}
