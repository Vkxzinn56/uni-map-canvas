import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { Sparkles, ArrowLeft, GraduationCap, Briefcase, ClipboardList, ShieldAlert, Loader2, CheckCircle2, Clock } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import type { UserRole } from "@/types";

export const Route = createFileRoute("/cadastro")({
  head: () => ({
    meta: [
      { title: "Criar conta — UniMap UNIPÊ" },
      { name: "description", content: "Solicite o cadastro institucional no UniMap UNIPÊ — aluno, professor, coordenação ou administração." },
      { property: "og:title", content: "Criar conta — UniMap UNIPÊ" },
      { property: "og:description", content: "Solicite o cadastro institucional no UniMap UNIPÊ." },
    ],
  }),
  component: CadastroPage,
});

type ProfileKey = Exclude<UserRole, "visitor">;
type Status = "idle" | "loading" | "pending" | "success" | "error";

const profiles: { key: ProfileKey; label: string; icon: typeof GraduationCap; description: string }[] = [
  { key: "student", label: "Aluno", icon: GraduationCap, description: "Confirmação por RGM e e-mail acadêmico." },
  { key: "teacher", label: "Professor", icon: Briefcase, description: "Validação pela coordenação do curso." },
  { key: "coordination", label: "Coordenação", icon: ClipboardList, description: "Aprovação pela direção acadêmica." },
  { key: "admin", label: "Administrador", icon: ShieldAlert, description: "Liberação pela equipe de TI." },
];

function CadastroPage() {
  const [profile, setProfile] = useState<ProfileKey>("student");
  const [status, setStatus] = useState<Status>("idle");
  const [form, setForm] = useState({ name: "", email: "", rgmOrId: "", course: "", phone: "" });

  const update = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.email) {
      setStatus("error");
      return;
    }
    setStatus("loading");
    setTimeout(() => {
      // Sem persistência — apenas simulação visual
      setStatus(profile === "student" ? "success" : "pending");
    }, 900);
  };

  if (status === "success" || status === "pending") {
    const isPending = status === "pending";
    return (
      <div className="min-h-[100dvh] grid place-items-center bg-background px-6">
        <div className="max-w-md w-full rounded-3xl border border-border bg-surface p-8 text-center shadow-soft">
          <div className={`size-14 rounded-2xl ${isPending ? "bg-primary-soft" : "bg-emerald-500/10"} grid place-items-center mx-auto`}>
            {isPending ? <Clock className="size-6 text-primary" /> : <CheckCircle2 className="size-6 text-emerald-600" />}
          </div>
          <h1 className="text-xl font-semibold tracking-tight mt-4">
            {isPending ? "Conta pendente de aprovação" : "Cadastro recebido!"}
          </h1>
          <p className="mt-2 text-[13.5px] text-muted-foreground leading-relaxed">
            {isPending
              ? "Sua solicitação foi registrada e será analisada pela área responsável. Você receberá um e-mail quando o acesso for liberado."
              : "Enviamos um e-mail de confirmação para concluir a ativação da sua conta."}
          </p>
          <div className="mt-6 flex flex-col gap-2">
            <Link to="/login" className="w-full">
              <Button className="w-full h-11 rounded-xl">Ir para login</Button>
            </Link>
            <Link to="/" className="text-[12.5px] text-muted-foreground hover:text-foreground">Voltar ao início</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[100dvh] bg-background">
      <header className="max-w-3xl mx-auto px-6 sm:px-10 pt-8 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="size-9 rounded-xl bg-primary grid place-items-center shadow-soft">
            <Sparkles className="size-4.5 text-primary-foreground" strokeWidth={2.4} />
          </div>
          <span className="font-semibold tracking-tight">UniMap</span>
        </Link>
        <Link to="/login" className="text-[13px] text-muted-foreground hover:text-foreground inline-flex items-center gap-1.5">
          <ArrowLeft className="size-4" /> Já tenho conta
        </Link>
      </header>

      <main className="max-w-3xl mx-auto px-6 sm:px-10 py-10">
        <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight">Criar conta institucional</h1>
        <p className="text-[13.5px] text-muted-foreground mt-1.5 max-w-xl">
          Escolha o seu perfil e preencha os dados. O acesso é validado pela universidade.
        </p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-7" role="radiogroup" aria-label="Selecionar perfil de cadastro">
          {profiles.map(({ key, label, icon: Icon, description }) => {
            const active = profile === key;
            return (
              <button
                key={key}
                type="button"
                role="radio"
                aria-checked={active}
                onClick={() => setProfile(key)}
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

        <form onSubmit={submit} className="mt-8 grid sm:grid-cols-2 gap-4 rounded-3xl border border-border bg-surface p-6 sm:p-7 shadow-soft">
          <div className="space-y-1.5 sm:col-span-2">
            <Label htmlFor="name" className="text-[12.5px]">Nome completo</Label>
            <Input id="name" value={form.name} onChange={update("name")} className="h-11 rounded-xl" autoComplete="name" />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="email" className="text-[12.5px]">E-mail institucional</Label>
            <Input id="email" type="email" value={form.email} onChange={update("email")} className="h-11 rounded-xl" autoComplete="email" />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="rgmOrId" className="text-[12.5px]">
              {profile === "student" ? "RGM" : profile === "admin" ? "Matrícula administrativa" : "Matrícula docente"}
            </Label>
            <Input id="rgmOrId" value={form.rgmOrId} onChange={update("rgmOrId")} className="h-11 rounded-xl" />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="course" className="text-[12.5px]">
              {profile === "coordination" ? "Curso/Departamento" : profile === "student" ? "Curso" : "Área de atuação"}
            </Label>
            <Input id="course" value={form.course} onChange={update("course")} className="h-11 rounded-xl" />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="phone" className="text-[12.5px]">Telefone (opcional)</Label>
            <Input id="phone" value={form.phone} onChange={update("phone")} className="h-11 rounded-xl" autoComplete="tel" />
          </div>

          {status === "error" && (
            <div role="alert" className="sm:col-span-2 text-[12.5px] text-destructive bg-destructive/10 border border-destructive/20 rounded-xl px-3 py-2">
              Verifique os campos obrigatórios (nome e e-mail).
            </div>
          )}

          <div className="sm:col-span-2 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 pt-1">
            <p className="text-[11.5px] text-muted-foreground max-w-md">
              Ao continuar você concorda com os termos institucionais e a Política de Privacidade da UNIPÊ.
            </p>
            <Button type="submit" disabled={status === "loading"} className="h-11 rounded-xl px-6 text-[14px] font-medium">
              {status === "loading" ? (<><Loader2 className="size-4 animate-spin" /> Enviando…</>) : "Solicitar cadastro"}
            </Button>
          </div>
        </form>
      </main>
    </div>
  );
}
