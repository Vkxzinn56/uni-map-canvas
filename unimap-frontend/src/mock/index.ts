import type { User, Block, Room, ServiceLocation, AgendaItem, Event, Specialty, Route } from "@/types";

export const mockUser: User = {
  id: "u_001",
  name: "Mariana Albuquerque",
  email: "m.albuquerque@cs.unipe.edu.br",
  rgm: "20231045",
  role: "student",
  course: "Ciência da Computação",
  semester: 3,
  avatar: "",
  achievements: 9,
  progress: 35,
};

export const mockBlocks: Block[] = [
  {
    id: "b_a", name: "Bloco A — Saúde", code: "A",
    description: "Cursos da área de saúde, clínicas-escola e laboratórios.",
    about: "Inaugurado em 2012, o Bloco A concentra os cursos da área da saúde do UNIPÊ, com infraestrutura clínica de uso real para estudantes e comunidade.",
    purpose: "Formação prática em saúde e atendimento aberto à comunidade através das clínicas-escola.",
    serviceIds: ["s_clinic"],
    floors: 3, x: 22, y: 30, color: "var(--chart-1)",
  },
  {
    id: "b_b", name: "Bloco B — Engenharias", code: "B",
    description: "Engenharias, laboratórios técnicos e oficinas.",
    about: "Hub das engenharias e tecnologia, com laboratórios de hardware, redes, software e oficinas mecânicas.",
    purpose: "Desenvolver projetos aplicados de engenharia, computação e inovação tecnológica.",
    serviceIds: [],
    floors: 4, x: 48, y: 22, color: "var(--chart-2)",
  },
  {
    id: "b_c", name: "Bloco C — Humanas", code: "C",
    description: "Direito, pedagogia, psicologia e auditórios.",
    about: "Espaço dedicado às humanidades, com auditórios para eventos abertos, salas de júri simulado e clínicas de psicologia.",
    purpose: "Formação em ciências humanas, sociais aplicadas e atendimento psicossocial.",
    serviceIds: [],
    floors: 3, x: 70, y: 38, color: "var(--chart-5)",
  },
  {
    id: "b_d", name: "Bloco D — Negócios", code: "D",
    description: "Administração, contábeis, economia.",
    about: "Centro de negócios com salas de coworking, incubadora de startups e laboratórios de mercado financeiro.",
    purpose: "Formar profissionais de gestão, finanças e empreendedorismo.",
    serviceIds: [],
    floors: 2, x: 60, y: 60, color: "var(--chart-4)",
  },
  {
    id: "b_e", name: "Bloco E — Convivência", code: "E",
    description: "Praça de alimentação, biblioteca, atendimento.",
    about: "Coração do campus: convivência, alimentação, biblioteca e serviços de apoio ao estudante.",
    purpose: "Oferecer suporte acadêmico, alimentação e espaços de estudo e socialização.",
    serviceIds: ["s_food", "s_lib", "s_support"],
    floors: 2, x: 35, y: 65, color: "var(--chart-3)",
  },
];

export const mockRooms: Room[] = [
  { id: "r_a101", blockId: "b_a", name: "Sala A-101", floor: 1, type: "classroom" },
  { id: "r_a201", blockId: "b_a", name: "Sala A-201", floor: 2, type: "classroom" },
  { id: "r_a210", blockId: "b_a", name: "Lab. de Anatomia A-210", floor: 2, type: "lab" },
  { id: "r_a305", blockId: "b_a", name: "Clínica Odontológica A-305", floor: 3, type: "lab" },
  { id: "r_b201", blockId: "b_b", name: "Sala B-201", floor: 2, type: "classroom" },
  { id: "r_b303", blockId: "b_b", name: "Lab B-303 — Software", floor: 3, type: "lab" },
  { id: "r_b310", blockId: "b_b", name: "Lab B-310 — Hardware", floor: 3, type: "lab" },
  { id: "r_b410", blockId: "b_b", name: "Sala B-410", floor: 4, type: "classroom" },
  { id: "r_c101", blockId: "b_c", name: "Auditório C-101", floor: 1, type: "auditorium" },
  { id: "r_c205", blockId: "b_c", name: "Sala de Júri Simulado C-205", floor: 2, type: "office" },
  { id: "r_c302", blockId: "b_c", name: "Clínica de Psicologia C-302", floor: 3, type: "office" },
  { id: "r_d105", blockId: "b_d", name: "Sala D-105", floor: 1, type: "classroom" },
  { id: "r_d201", blockId: "b_d", name: "Lab. de Mercado D-201", floor: 2, type: "lab" },
  { id: "r_e101", blockId: "b_e", name: "Biblioteca Central", floor: 1, type: "office" },
  { id: "r_e110", blockId: "b_e", name: "Salas de Estudo E-110", floor: 1, type: "office" },
];

export const mockServices: ServiceLocation[] = [
  { id: "s_clinic", name: "Clínica-Escola UNIPÊ", category: "clinic", description: "Atendimentos abertos à comunidade.", x: 24, y: 40, hours: "Seg–Sex · 08h–18h" },
  { id: "s_food", name: "Praça de Alimentação", category: "food", description: "Restaurantes, cafés e lanchonetes.", x: 38, y: 68, hours: "Seg–Sáb · 07h–22h" },
  { id: "s_lib", name: "Biblioteca Central", category: "library", description: "Acervo físico e digital, salas de estudo.", x: 32, y: 60, hours: "Seg–Sex · 07h–22h" },
  { id: "s_support", name: "Atendimento ao Aluno", category: "support", description: "Secretaria acadêmica e financeira.", x: 40, y: 62, hours: "Seg–Sex · 08h–20h" },
  { id: "s_sports", name: "Centro Esportivo", category: "sports", description: "Quadras, academia e piscina.", x: 80, y: 70, hours: "Seg–Sáb · 06h–22h" },
  { id: "s_park", name: "Estacionamento Principal", category: "parking", description: "Acesso pela portaria principal.", x: 10, y: 50, hours: "24h" },
];

const today = new Date();
const iso = (d: Date) => d.toISOString().slice(0, 10);
const addDays = (n: number) => { const d = new Date(today); d.setDate(d.getDate() + n); return iso(d); };

export const mockAgenda: AgendaItem[] = [
  { id: "ag_1", title: "Arquitetura de Software", type: "class", date: iso(today), startTime: "08:00", endTime: "10:00", location: "Lab B-303", blockId: "b_b", teacher: "Prof. Eduardo Lima" },
  { id: "ag_2", title: "Engenharia de Requisitos", type: "class", date: iso(today), startTime: "10:20", endTime: "12:00", location: "Sala B-201", blockId: "b_b", teacher: "Profa. Carla Souza" },
  { id: "ag_3", title: "Palestra: IA Generativa", type: "event", date: iso(today), startTime: "19:00", endTime: "21:00", location: "Auditório C-101", blockId: "b_c" },
  { id: "ag_4", title: "Banco de Dados II", type: "class", date: addDays(1), startTime: "08:00", endTime: "10:00", location: "Lab B-303", blockId: "b_b", teacher: "Prof. Renato Dias" },
  { id: "ag_5", title: "Prova — Sistemas Distribuídos", type: "exam", date: addDays(3), startTime: "14:00", endTime: "16:00", location: "Sala B-410", blockId: "b_b", teacher: "Prof. Eduardo Lima" },
];

export const mockEvents: Event[] = [
  {
    id: "e_1", title: "Semana de Inovação UNIPÊ", category: "Tecnologia", visibility: "public",
    cover: "linear-gradient(135deg, oklch(0.7 0.15 30), oklch(0.6 0.18 350))",
    date: addDays(5), endDate: addDays(9), startTime: "09:00", endTime: "21:00",
    location: "Auditório Central — Bloco C",
    description: "Cinco dias de palestras, workshops e demo-day com startups da região.",
    about: "A maior semana de inovação do Nordeste reúne lideranças de tecnologia, pesquisa e empreendedorismo em cinco dias intensos de conteúdo, conexões e oportunidades para a comunidade acadêmica.",
    schedule: [
      { time: "09:00", title: "Abertura oficial", description: "Reitoria e parceiros estratégicos." },
      { time: "10:30", title: "Keynote: O futuro do trabalho com IA", description: "Painel inaugural." },
      { time: "14:00", title: "Workshops paralelos", description: "UX, Cloud, Cibersegurança e Produto." },
      { time: "19:00", title: "Demo Day", description: "Pitch de startups incubadas." },
    ],
    speakers: [
      { name: "Ana Beatriz Costa", role: "Head of AI · Nubank" },
      { name: "Rafael Mendes", role: "CTO · Stone" },
      { name: "Juliana Reis", role: "Pesquisadora · USP" },
    ],
    comments: [
      { author: "João P.", role: "Aluno · ADS", text: "Edição passada foi transformadora, recomendo demais.", rating: 5 },
      { author: "Profa. Lúcia", role: "Coord. Computação", text: "Conteúdo de altíssimo nível e muito networking.", rating: 5 },
    ],
    attendees: 312, capacity: 500, registered: false,
  },
  {
    id: "e_2", title: "Mostra de Profissões", category: "Carreira", visibility: "public",
    cover: "linear-gradient(135deg, oklch(0.75 0.13 220), oklch(0.6 0.14 270))",
    date: addDays(8), startTime: "14:00", endTime: "20:00",
    location: "Praça Central — Bloco E",
    description: "Conheça os cursos do UNIPÊ com experiências interativas.",
    about: "Evento aberto à comunidade onde futuros estudantes vivenciam um dia em cada curso através de estações práticas conduzidas por professores e alunos veteranos.",
    schedule: [
      { time: "14:00", title: "Credenciamento e abertura" },
      { time: "15:00", title: "Estações por área", description: "Saúde, Engenharias, Humanas e Negócios." },
      { time: "18:00", title: "Roda de conversa", description: "Egressos compartilham suas trajetórias." },
    ],
    speakers: [
      { name: "Profa. Mariana Lopes", role: "Coord. Pedagógica" },
      { name: "Equipe de Veteranos", role: "Embaixadores UNIPÊ" },
    ],
    comments: [
      { author: "Família Silva", role: "Visitantes", text: "Meus filhos amaram a experiência prática.", rating: 5 },
    ],
    attendees: 188, capacity: 400, registered: true,
  },
  {
    id: "e_3", title: "Hackathon UNIPÊ 2026", category: "Tecnologia", visibility: "private",
    cover: "linear-gradient(135deg, oklch(0.7 0.18 155), oklch(0.65 0.15 200))",
    date: addDays(14), endDate: addDays(16), startTime: "08:00", endTime: "08:00",
    location: "Laboratórios do Bloco B",
    description: "48h de código com mentorias e premiação.",
    about: "Maratona de 48 horas onde equipes multidisciplinares prototipam soluções para desafios reais propostos por empresas parceiras. Premiação total de R$ 20.000 e estágio garantido para o time vencedor.",
    schedule: [
      { time: "Sex · 08:00", title: "Abertura e apresentação dos desafios" },
      { time: "Sex · 12:00", title: "Início do desenvolvimento" },
      { time: "Sáb · 14:00", title: "Mentorias técnicas" },
      { time: "Dom · 06:00", title: "Entrega das soluções" },
      { time: "Dom · 08:00", title: "Pitches e premiação" },
    ],
    speakers: [
      { name: "Carlos Henrique", role: "Mentor · AWS" },
      { name: "Patrícia Nunes", role: "Mentora · Google for Startups" },
    ],
    comments: [
      { author: "Time Vencedor 2025", role: "Alunos UNIPÊ", text: "Saímos com estágio e amigos para a vida.", rating: 5 },
    ],
    attendees: 96, capacity: 120, registered: false,
  },
  {
    id: "e_4", title: "Sarau Cultural", category: "Cultura", visibility: "public",
    cover: "linear-gradient(135deg, oklch(0.78 0.14 75), oklch(0.65 0.18 30))",
    date: addDays(21), startTime: "19:00", endTime: "22:30",
    location: "Praça de Convivência — Bloco E",
    description: "Música, poesia e arte produzida por estudantes.",
    about: "Noite cultural mensal aberta à comunidade, celebrando a produção artística dos estudantes em um ambiente acolhedor sob as luzes da praça de convivência.",
    schedule: [
      { time: "19:00", title: "Abertura — Coral UNIPÊ" },
      { time: "19:45", title: "Slam de poesia" },
      { time: "20:30", title: "Banda convidada" },
      { time: "22:00", title: "Microfone aberto" },
    ],
    speakers: [
      { name: "Coletivo Verso Livre", role: "Curadoria poética" },
      { name: "Banda Maré Alta", role: "Atração musical" },
    ],
    comments: [
      { author: "Bruna L.", role: "Aluna · Letras", text: "Espaço seguro e inspirador para artistas iniciantes.", rating: 5 },
    ],
    attendees: 54, capacity: 200, registered: false,
  },
];

export const mockSpecialties: Specialty[] = [
  { id: "sp_odo", name: "Odontologia", description: "Limpeza, restauração, ortodontia.", icon: "Smile", durationMin: 50, priceRange: "Gratuito · R$ 80" },
  { id: "sp_psi", name: "Psicologia", description: "Atendimento clínico individual.", icon: "Brain", durationMin: 50, priceRange: "Gratuito" },
  { id: "sp_fis", name: "Fisioterapia", description: "Avaliação e tratamento postural.", icon: "Activity", durationMin: 60, priceRange: "R$ 40 · R$ 120" },
  { id: "sp_nut", name: "Nutrição", description: "Consulta e plano alimentar.", icon: "Apple", durationMin: 45, priceRange: "R$ 35" },
  { id: "sp_far", name: "Farmácia", description: "Atenção farmacêutica e exames.", icon: "Pill", durationMin: 30, priceRange: "Gratuito" },
  { id: "sp_enf", name: "Enfermagem", description: "Curativos, aferições e vacinação.", icon: "HeartPulse", durationMin: 30, priceRange: "Gratuito" },
];

export const mockRoutes: Route[] = [
  { id: "rt_1", from: "Portaria Principal", to: "Lab B-303", steps: ["Entre pela portaria principal", "Siga reto pela alameda central por 80m", "Vire à direita após a Biblioteca", "Suba até o 3º andar do Bloco B"], distanceM: 220, durationMin: 4 },
];
