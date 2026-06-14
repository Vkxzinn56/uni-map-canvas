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
    id: "b_a", name: "Bloco A — Administração", code: "A",
    description: "Administração, Ciências Contábeis, Gestão e Negócios.",
    about: "Principal bloco acadêmico voltado aos cursos de gestão e negócios. Salas de aula teóricas e laboratórios de práticas gerenciais.",
    purpose: "Formar profissionais em Administração, Ciências Contábeis, Gestão de RH, Marketing e Relações Internacionais.",
    serviceIds: [],
    floors: 3, x: 22, y: 30, color: "var(--chart-1)",
    latitude: -7.15942, longitude: -34.85420,
  },
  {
    id: "b_b", name: "Bloco B — Educação Física", code: "B",
    description: "Educação Física, esportes e atividades físicas.",
    about: "Bloco dedicado ao curso de Educação Física, com salas teóricas e acesso ao complexo esportivo.",
    purpose: "Formação de profissionais de Educação Física para atuação em escolas, academias e treinamento esportivo.",
    serviceIds: ["s_sports"],
    floors: 2, x: 48, y: 22, color: "var(--chart-2)",
    latitude: -7.15844, longitude: -34.85419,
  },
  {
    id: "b_c", name: "Bloco C — Direito e Humanas", code: "C",
    description: "Direito, Serviço Social, Pedagogia e Relações Internacionais.",
    about: "Bloco das ciências humanas e sociais, com salas de aula, auditório para eventos e núcleo de práticas jurídicas.",
    purpose: "Formação em Direito, Serviço Social, Pedagogia e Relações Internacionais com práticas simuladas e estágios.",
    serviceIds: [],
    floors: 3, x: 70, y: 38, color: "var(--chart-5)",
    latitude: -7.15848, longitude: -34.85526,
  },
  {
    id: "b_d", name: "Bloco D — CECOVE", code: "D",
    description: "Comissão de Vestibular e processos seletivos.",
    about: "Sede da CECOVE (Comissão de Concursos e Vestibulares) e apoio administrativo aos processos seletivos da instituição.",
    purpose: "Gerenciar e operacionalizar vestibulares, concursos e processos seletivos.",
    serviceIds: [],
    floors: 2, x: 60, y: 60, color: "var(--chart-4)",
    latitude: -7.15791, longitude: -34.85491,
  },
  {
    id: "b_e", name: "Bloco E — Psicologia", code: "E",
    description: "Psicologia e atendimento psicossocial.",
    about: "Bloco do curso de Psicologia com salas de aula, laboratórios e clínicas de atendimento psicológico à comunidade.",
    purpose: "Formação de psicólogos e atendimento psicossocial gratuito à comunidade.",
    serviceIds: ["s_psicologia"],
    floors: 3, x: 35, y: 65, color: "var(--chart-3)",
    latitude: -7.15949, longitude: -34.85479,
  },
  {
    id: "b_f", name: "Bloco F — Psicologia / Clínicas", code: "F",
    description: "Clínica-Escola de Psicologia e Administração.",
    about: "Bloco multiuso que abriga a Clínica-Escola de Psicologia (atendimento à comunidade) e salas de aula da Administração.",
    purpose: "Atendimento psicológico à comunidade e formação prática em Psicologia e Administração.",
    serviceIds: ["s_psicologia"],
    floors: 3, x: 48, y: 50, color: "var(--chart-1)",
    latitude: -7.16079, longitude: -34.85371,
  },
  {
    id: "b_g", name: "Bloco G — Fonoaudiologia", code: "G",
    description: "Fonoaudiologia e Clínica-Escola.",
    about: "Bloco do curso de Fonoaudiologia, com a Clínica-Escola de Fonoaudiologia (Quadra Ciano, 1º pavimento) realizando atendimentos gratuitos à comunidade.",
    purpose: "Formação de fonoaudiólogos e atendimento fonoaudiológico gratuito.",
    serviceIds: ["s_fono"],
    floors: 3, x: 42, y: 38, color: "var(--chart-5)",
    latitude: -7.16056, longitude: -34.85320,
  },
  {
    id: "b_i", name: "Bloco I — Oficina Digital", code: "I",
    description: "Tecnologia, computação e oficina digital.",
    about: "Oficina Digital do UNIPÊ com laboratórios de informática, salas de computação e suporte técnico para os cursos de TI.",
    purpose: "Apoiar aulas práticas de computação, análise de sistemas e tecnologia da informação.",
    serviceIds: [],
    floors: 2, x: 55, y: 55, color: "var(--chart-2)",
    latitude: -7.16100, longitude: -34.85467,
  },
  {
    id: "b_k", name: "Bloco K — Ginástica e Dança", code: "K",
    description: "Dança, ginástica e atividades corporais.",
    about: "Bloco com salas de dança, ginástica e atividades corporais. Abriga projetos de extensão como dança e ginástica em academia.",
    purpose: "Oferecer espaço para atividades físicas, dança e extensão comunitária.",
    serviceIds: [],
    floors: 2, x: 52, y: 28, color: "var(--chart-3)",
    latitude: -7.15865, longitude: -34.85257,
  },
  {
    id: "b_l", name: "Bloco L — Treinamento Esportivo", code: "L",
    description: "Treinamento funcional, ginástica artística e jiu-jítsu.",
    about: "Bloco esportivo com sala de ginástica artística, treinamento funcional (Sala 233/235) e jiu-jítsu. Projetos de extensão abertos à comunidade.",
    purpose: "Promover atividades esportivas e de extensão para a comunidade acadêmica e externa.",
    serviceIds: ["s_sports"],
    floors: 2, x: 58, y: 32, color: "var(--chart-4)",
    latitude: -7.15813, longitude: -34.85537,
  },
  {
    id: "b_n", name: "Bloco N — Enfermagem (COLACE)", code: "N",
    description: "Enfermagem e Clínica-Escola Florence Nightingale.",
    about: "Bloco do curso de Enfermagem com o COLACE (Complexo Laboratorial e Clínica-Escola Florence Nightingale), realizando atendimentos gratuitos.",
    purpose: "Formação de enfermeiros e atendimento de enfermagem à comunidade.",
    serviceIds: ["s_enfermagem"],
    floors: 4, x: 38, y: 45, color: "var(--chart-1)",
    latitude: -7.16084, longitude: -34.85417,
  },
  {
    id: "b_q", name: "Bloco Q — Odontologia", code: "Q",
    description: "Odontologia e Clínica-Escola Odontológica.",
    about: "Bloco do curso de Odontologia com a mais moderna clínica-escola odontológica do Nordeste: 104 consultórios, bloco cirúrgico, centro radiológico e laboratórios de simulação.",
    purpose: "Formação de cirurgiões-dentistas e atendimento odontológico gratuito à comunidade.",
    serviceIds: ["s_odonto"],
    floors: 4, x: 30, y: 40, color: "var(--chart-1)",
    latitude: -7.16105, longitude: -34.85311,
  },
  {
    id: "b_med", name: "Bloco de Medicina", code: "M",
    description: "Medicina e ciências médicas.",
    about: "Bloco moderno do curso de Medicina, inaugurado recentemente, com 9 salas de aula com capacidade para 60 alunos cada, laboratórios e centro de simulação.",
    purpose: "Formação de médicos generalistas com ênfase na atenção primária à saúde.",
    serviceIds: [],
    floors: 4, x: 65, y: 20, color: "var(--chart-2)",
    latitude: -7.15879, longitude: -34.85218,
  },
  {
    id: "b_reitoria", name: "Reitoria", code: "R",
    description: "Administração central e gabinetes.",
    about: "Sede da Reitoria do UNIPÊ, abriga a administração central, NAI (Núcleo de Apoio Institucional) e CEP (Comitê de Ética em Pesquisa).",
    purpose: "Gestão acadêmica e administrativa da instituição.",
    serviceIds: [],
    floors: 3, x: 75, y: 15, color: "var(--chart-5)",
    latitude: -7.15932, longitude: -34.85260,
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
  { id: "s_psicologia", name: "Clínica-Escola de Psicologia", category: "clinic", description: "Atendimento psicológico gratuito à comunidade. Agendamento pela recepção do Bloco F.", x: 48, y: 50, hours: "Seg–Sex · 08h–18h", latitude: -7.16079, longitude: -34.85371 },
  { id: "s_fono", name: "Clínica-Escola de Fonoaudiologia", category: "clinic", description: "Avaliação e terapia fonoaudiológica gratuita. Quadra Ciano, 1º pavimento do Bloco G.", x: 42, y: 38, hours: "Seg–Sex · 08h–17h", latitude: -7.16056, longitude: -34.85320 },
  { id: "s_odonto", name: "Clínica-Escola Odontológica", category: "clinic", description: "104 consultórios, bloco cirúrgico, centro radiológico e laboratórios de simulação. Atendimento gratuito.", x: 30, y: 40, hours: "Seg–Sex · 08h–20h · Sáb 08h–12h", latitude: -7.16105, longitude: -34.85311 },
  { id: "s_enfermagem", name: "COLACE — Clínica-Escola Florence Nightingale", category: "clinic", description: "Complexo Laboratorial e Clínica-Escola de Enfermagem. Curativos, aferições, vacinação e exames.", x: 38, y: 45, hours: "Seg–Sex · 08h–18h", latitude: -7.16084, longitude: -34.85417 },
  { id: "s_dona_xica", name: "Restaurante Dona Xica", category: "food", description: "Restaurante universitário com refeições completas a preço acessível. Almoço e jantar.", x: 36, y: 66, hours: "Seg–Sáb · 11h–14h · 18h–21h", latitude: -7.16033, longitude: -34.85511 },
  { id: "s_cantina", name: "Cantina do Biu", category: "food", description: "Lanches rápidos, salgados, sucos e café. Ponto de encontro dos alunos entre os turnos.", x: 44, y: 52, hours: "Seg–Sex · 07h–22h", latitude: -7.16062, longitude: -34.85488 },
  { id: "s_eva", name: "EVA — Espaço de Vivência Acadêmica", category: "food", description: "Área de convivência com mesas, sombra e alimentos. Ideal para intervalos e estudos em grupo.", x: 35, y: 58, hours: "Seg–Sex · 07h–22h", latitude: -7.15981, longitude: -34.85471 },
  { id: "s_lib", name: "Biblioteca Central", category: "library", description: "Acervo físico e digital com mais de 140 mil volumes. Salas de estudo individuais e em grupo.", x: 32, y: 60, hours: "Seg–Sex · 07h–22h · Sáb 08h–12h", latitude: -7.15970, longitude: -34.85558 },
  { id: "s_support", name: "Atendimento ao Aluno", category: "support", description: "Secretaria acadêmica, financeira e central de atendimento ao discente.", x: 40, y: 62, hours: "Seg–Sex · 08h–20h", latitude: -7.15979, longitude: -34.85510 },
  { id: "s_sports", name: "Complexo Poliesportivo", category: "sports", description: "Quadras poliesportivas, campo society, vestiários e arquibancada.", x: 78, y: 68, hours: "Seg–Sáb · 06h–22h", latitude: -7.15980, longitude: -34.85290 },
  { id: "s_pool", name: "Piscina Semiolímpica", category: "sports", description: "Piscina aquecida semiolímpica para aulas de Educação Física e projetos de extensão.", x: 75, y: 72, hours: "Seg–Sáb · 06h–20h", latitude: -7.15955, longitude: -34.85250 },
  { id: "s_park", name: "Estacionamento Principal", category: "parking", description: "Estacionamento amplo com acesso pela portaria principal da BR-230 e portão secundário.", x: 10, y: 50, hours: "24h", latitude: -7.15900, longitude: -34.85690 },
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
  {
    id: "rt_1", from: "Portaria Principal", to: "Lab B-303",
    steps: [
      "Entre pela portaria principal (BR-230)",
      "Siga reto pela alameda central por ~80m",
      "Vire à direita após a Biblioteca Central",
      "Siga até o Bloco B e suba ao 3º andar",
    ],
    distanceM: 220, durationMin: 4,
    coordinates: [
      [-7.15850, -34.85750],
      [-7.15880, -34.85650],
      [-7.15879, -34.85580],
      [-7.15870, -34.85480],
      [-7.15844, -34.85419],
    ],
  },
  {
    id: "rt_2", from: "Portaria Principal", to: "Clínica-Escola Odontológica",
    steps: [
      "Entre pela portaria principal (BR-230)",
      "Siga reto pela alameda central por ~50m",
      "Vire à esquerda no cruzamento principal",
      "Siga pela via lateral até o Bloco Q",
      "A Clínica fica no térreo do Bloco Q",
    ],
    distanceM: 350, durationMin: 6,
    coordinates: [
      [-7.15850, -34.85750],
      [-7.15930, -34.85650],
      [-7.16010, -34.85560],
      [-7.16060, -34.85460],
      [-7.16105, -34.85311],
    ],
  },
];
