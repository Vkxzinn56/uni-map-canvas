import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Sparkles, ShieldCheck, ArrowLeft, GraduationCap, Briefcase, ClipboardList, ShieldAlert, Loader2 } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useAuthStore } from "@/store/auth";
import { toast } from "sonner";
import type { UserRole } from "@/types";

export const Route = createFileRoute("/login")({
  head: () => ({
    meta: [
      { title: "Entrar — UniMap UNIPÊ" },
      { name: "description", content: "Acesse sua conta UniMap UNIPÊ como aluno, professor, coordenação ou administração." },
      { property: "og:title", content: "Entrar — UniMap UNIPÊ" },
      { property: "og:description", content: "Acesse sua conta UniMap UNIPÊ." },
    ],
  }),
  component: LoginPage,
});

type ProfileKey = Exclude<UserRole, "visitor">;

const profiles: { key: ProfileKey; label: string; icon: typeof GraduationCap; description: string; idLabel: string; placeholder: string }[] = [
  { key: "student", label: "Aluno", icon: GraduationCap, description: "Acesse agenda, notas e serviços acadêmicos.", idLabel: "RGM ou e-mail institucional", placeholder: "20231045 ou nome@aluno.unipe.edu.br" },
  { key: "teacher", label: "Professor", icon: Briefcase, description: "Gerencie turmas, diários e materiais.", idLabel: "E-mail institucional", placeholder: "nome@unipe.edu.br" },
  { key: "coordination", label: "Coordenação", icon: ClipboardList, description: "Acompanhe cursos e indicadores.", idLabel: "E-mail institucional", placeholder: "coord@unipe.edu.br" },
  { key: "admin", label: "Administrador", icon: ShieldAlert, description: "Configurações e gestão da plataforma.", idLabel: "Usuário administrativo", placeholder: "admin.usuario" },
];

function LoginPage() {
  const [selected, setSelected] = useState<ProfileKey>("student");
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const loginAs = useAuthStore((s) => s.loginAs);
  const navigate = useNavigate();
  const profile = profiles.find((p) => p.key === selected)!;

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!identifier || !password) {
      setError("Preencha todos os campos para continuar.");
      return;
    }
    setLoading(true);
    setTimeout(() => {
      loginAs(selected, identifier);
      toast.success(`Bem-vindo(a), ${profile.label.toLowerCase()}!`);
      setLoading(false);
      navigate({ to: "/" });
    }, 700);
  };

  return (
    <div className="min-h-[100dvh] w-full grid lg:grid-cols-2 bg-background">
      <aside className="hidden lg:flex relative flex-col justify-between p-12 bg-gradient-to-br from-primary-soft via-background to-accent/40">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="size-9 rounded-xl bg-primary grid place-items-center shadow-soft">
            <Sparkles className="size-4.5 text-primary-foreground" strokeWidth={2.4} />
          </div>
          <div className="leading-tight">
            <div className="text-[15px] font-semibold tracking-tight">UniMap</div>
            <div className="text-[11px] text-muted-foreground">UNIPÊ · v3.0</div>
          </div>
        </Link>
        <div>
          <h2 className="text-3xl font-semibold tracking-tight leading-tight max-w-md">
            Tudo da sua universidade, em um só lugar.
          </h2>
          <p className="mt-3 text-[14px] text-muted-foreground max-w-md leading-relaxed">
            Agenda, mapas, eventos, clínicas-escola e serviços acadêmicos — adaptados para o seu perfil.
          </p>
        </div>
        <div className="flex items-center gap-2 text-[12px] text-muted-foreground">
          <ShieldCheck className="size-3.5" /> Autenticação institucional segura · LGPD
        </div>
      </aside>

      <section className="flex flex-col p-6 sm:p-10 lg:p-14">
        <Link to="/" className="inline-flex items-center gap-1.5 text-[13px] text-muted-foreground hover:text-foreground transition-colors mb-8 w-fit">
          <ArrowLeft className="size-4" /> Voltar para o início
        </Link>

        <div className="max-w-md w-full mx-auto lg:mx-0">
          <h1 className="text-2xl font-semibold tracking-tight">Acesse sua conta</h1>
          <p className="text-[13.5px] text-muted-foreground mt-1.5">Selecione seu perfil para continuar.</p>

          <div className="grid grid-cols-2 gap-2 mt-6" role="radiogroup" aria-label="Selecionar perfil">
            {profiles.map(({ key, label, icon: Icon, description }) => {
              const active = selected === key;
              return (
                <button
                  key={key}
                  type="button"
                  role="radio"
                  aria-checked={active}
                  onClick={() => setSelected(key)}
                  className={`text-left rounded-2xl border p-3.5 transition-all ${
                    active ? "border-primary bg-primary-soft" : "border-border bg-surface hover:border-foreground/20"
                  }`}
                >
                  <Icon className={`size-4.5 mb-2 ${active ? "text-primary" : "text-muted-foreground"}`} strokeWidth={2} />
                  <div className="text-[13.5px] font-semibold">{label}</div>
                  <div className="text-[11px] text-muted-foreground leading-snug mt-0.5">{description}</div>
                </button>
              );
            })}
          </div>

          <form onSubmit={submit} className="mt-6 space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="identifier" className="text-[12.5px]">{profile.idLabel}</Label>
              <Input id="identifier" value={identifier} onChange={(e) => setIdentifier(e.target.value)} placeholder={profile.placeholder} className="h-11 rounded-xl" autoComplete="username" />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="pw" className="text-[12.5px]">Senha</Label>
              <Input id="pw" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" className="h-11 rounded-xl" autoComplete="current-password" />
            </div>

            {error && (
              <div role="alert" className="text-[12.5px] text-destructive bg-destructive/10 border border-destructive/20 rounded-xl px-3 py-2">
                {error}
              </div>
            )}

            <Button type="submit" disabled={loading} className="w-full h-11 rounded-xl text-[14px] font-medium">
              {loading ? (<><Loader2 className="size-4 animate-spin" /> Entrando…</>) : "Entrar"}
            </Button>

            <div className="flex items-center justify-between text-[12.5px] pt-1">
              <Link to="/" className="text-muted-foreground hover:text-foreground">Continuar como visitante</Link>
              <Link to="/cadastro" className="text-primary font-medium hover:underline">Criar conta</Link>
            </div>
          </form>
        </div>
      </section>
    </div>
  );
}
