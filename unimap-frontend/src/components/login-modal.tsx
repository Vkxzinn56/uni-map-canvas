import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useAuthStore } from "@/store/auth";
import { Sparkles, ShieldCheck } from "lucide-react";
import { toast } from "sonner";

export function LoginModal() {
  const open = useAuthStore((s) => s.loginModalOpen);
  const close = useAuthStore((s) => s.closeLogin);
  const login = useAuthStore((s) => s.login);
  const [rgm, setRgm] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!rgm || !email || !password) return;
    setLoading(true);
    setTimeout(() => {
      login(rgm);
      toast.success("Bem-vinda de volta!", { description: "Sua agenda e serviços já estão disponíveis." });
      setLoading(false);
      setRgm(""); setEmail(""); setPassword("");
    }, 600);
  };

  return (
    <Dialog open={open} onOpenChange={(o) => !o && close()}>
      <DialogContent className="sm:max-w-md p-0 overflow-hidden rounded-3xl border-border">
        <div className="bg-gradient-to-br from-primary-soft via-background to-accent/40 p-7 pb-5">
          <div className="size-10 rounded-2xl bg-primary grid place-items-center shadow-soft mb-4">
            <Sparkles className="size-5 text-primary-foreground" strokeWidth={2.4} />
          </div>
          <DialogHeader className="space-y-1.5 text-left">
            <DialogTitle className="text-[22px] font-semibold tracking-tight">Acesse sua conta UNIPÊ</DialogTitle>
            <DialogDescription className="text-[13.5px]">Use suas credenciais institucionais para liberar agenda, notas e serviços personalizados.</DialogDescription>
          </DialogHeader>
        </div>
        <form onSubmit={submit} className="p-7 pt-5 space-y-4">
          <div className="space-y-1.5">
            <Label htmlFor="rgm" className="text-[12.5px]">RGM</Label>
            <Input id="rgm" placeholder="20231045" value={rgm} onChange={(e) => setRgm(e.target.value)} className="h-11 rounded-xl" />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="email" className="text-[12.5px]">E-mail institucional</Label>
            <Input id="email" type="email" placeholder="nome@aluno.unipe.edu.br" value={email} onChange={(e) => setEmail(e.target.value)} className="h-11 rounded-xl" />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="pw" className="text-[12.5px]">Senha</Label>
            <Input id="pw" type="password" placeholder="••••••••" value={password} onChange={(e) => setPassword(e.target.value)} className="h-11 rounded-xl" />
          </div>
          <Button type="submit" disabled={loading} className="w-full h-11 rounded-xl text-[14px] font-medium">
            {loading ? "Entrando…" : "Entrar"}
          </Button>
          <div className="flex items-center justify-center gap-1.5 text-[11.5px] text-muted-foreground pt-1">
            <ShieldCheck className="size-3.5" /> Autenticação segura · Single Sign-On UNIPÊ
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
