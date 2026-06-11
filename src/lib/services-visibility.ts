import type { UserRole } from "@/types";

export interface ServiceItem {
  id: string;
  name: string;
  description: string;
  icon: string; // lucide name
  category: string;
  visibility: "public" | "private";
  href?: string;
  contact?: string;
  hours?: string;
}

export const PUBLIC_SERVICES: ServiceItem[] = [
  { id: "biblioteca", name: "Biblioteca", description: "Acervo, salas de estudo e horários de funcionamento.", icon: "BookOpen", category: "Estudo", visibility: "public", hours: "Seg–Sex · 07h–22h" },
  { id: "clinicas", name: "Clínicas-Escola", description: "Atendimentos abertos à comunidade em diversas especialidades.", icon: "Stethoscope", category: "Saúde", visibility: "public", href: "/clinica" },
  { id: "central", name: "Central de Atendimento", description: "Informações gerais, ouvidoria e suporte ao público.", icon: "Headphones", category: "Atendimento", visibility: "public", contact: "(83) 2106-9700" },
  { id: "secretaria", name: "Secretaria Geral", description: "Contatos e protocolos institucionais.", icon: "Mail", category: "Atendimento", visibility: "public", contact: "secretaria@unipe.edu.br" },
  { id: "coordenacoes", name: "Coordenação dos cursos", description: "Lista de coordenadores e contatos por curso.", icon: "Users", category: "Acadêmico", visibility: "public" },
  { id: "horarios", name: "Horários institucionais", description: "Funcionamento dos blocos, biblioteca e atendimentos.", icon: "Clock", category: "Institucional", visibility: "public" },
  { id: "mapa", name: "Localização dos blocos", description: "Mapa interativo do campus com salas e serviços.", icon: "Map", category: "Campus", visibility: "public", href: "/mapa" },
  { id: "estacionamento", name: "Estacionamento", description: "Áreas disponíveis, acessos e regras.", icon: "Car", category: "Campus", visibility: "public" },
  { id: "alimentacao", name: "Restaurantes e alimentação", description: "Praça de alimentação, cafés e cantinas do campus.", icon: "UtensilsCrossed", category: "Campus", visibility: "public" },
  { id: "auditorios", name: "Auditórios", description: "Espaços para eventos, palestras e defesas.", icon: "Mic2", category: "Campus", visibility: "public" },
  { id: "laboratorios", name: "Laboratórios abertos", description: "Laboratórios com acesso público em horários definidos.", icon: "FlaskConical", category: "Campus", visibility: "public" },
  { id: "eventos", name: "Eventos", description: "Programação aberta de eventos, palestras e workshops.", icon: "CalendarHeart", category: "Institucional", visibility: "public", href: "/eventos" },
  { id: "calendario", name: "Calendário institucional", description: "Datas letivas, recessos e marcos do semestre.", icon: "Calendar", category: "Institucional", visibility: "public" },
  { id: "contatos", name: "Contatos da universidade", description: "Telefones, e-mails e endereços oficiais.", icon: "PhoneCall", category: "Atendimento", visibility: "public" },
];

export const PRIVATE_SERVICES: ServiceItem[] = [
  { id: "portal", name: "Portal do Aluno", description: "Acesso unificado às informações acadêmicas.", icon: "LayoutDashboard", category: "Acadêmico", visibility: "private" },
  { id: "historico", name: "Histórico", description: "Histórico escolar completo.", icon: "ScrollText", category: "Acadêmico", visibility: "private" },
  { id: "notas", name: "Notas", description: "Acompanhamento de avaliações por disciplina.", icon: "GraduationCap", category: "Acadêmico", visibility: "private" },
  { id: "frequencia", name: "Frequência", description: "Controle de presença nas disciplinas.", icon: "CheckSquare", category: "Acadêmico", visibility: "private" },
  { id: "solicitacoes", name: "Solicitações acadêmicas", description: "Requerimentos e protocolos online.", icon: "FileSignature", category: "Acadêmico", visibility: "private" },
  { id: "matricula", name: "Matrícula", description: "Renovação e ajustes de matrícula.", icon: "FilePlus2", category: "Acadêmico", visibility: "private" },
  { id: "financeiro", name: "Financeiro", description: "Boletos, mensalidades e negociações.", icon: "Wallet", category: "Financeiro", visibility: "private" },
  { id: "documentos", name: "Documentos", description: "Declarações, atestados e certificados.", icon: "FileText", category: "Acadêmico", visibility: "private" },
  { id: "agenda", name: "Agenda acadêmica", description: "Aulas, provas e compromissos sincronizados.", icon: "Calendar", category: "Acadêmico", visibility: "private", href: "/agenda" },
  { id: "blackboard", name: "Blackboard", description: "Ambiente virtual de aprendizagem.", icon: "MonitorPlay", category: "Acadêmico", visibility: "private" },
];

export function getVisibleServices(role: UserRole | "visitor"): ServiceItem[] {
  if (role === "visitor") return PUBLIC_SERVICES;
  return [...PUBLIC_SERVICES, ...PRIVATE_SERVICES];
}
