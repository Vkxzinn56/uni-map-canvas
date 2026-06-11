// Service layer — returns mocks today, swap implementation when APIs land.
import { mockUser, mockBlocks, mockRooms, mockServices, mockAgenda, mockEvents, mockSpecialties, mockRoutes } from "@/mock";
import type { User, Block, Room, ServiceLocation, AgendaItem, Event, Specialty, Route } from "@/types";

const delay = <T>(data: T, ms = 200): Promise<T> => new Promise((r) => setTimeout(() => r(data), ms));

export const usersService = {
  me: () => delay<User>(mockUser),
  login: (rgm: string, _password: string) => delay<User>({ ...mockUser, rgm }),
};

export const mapService = {
  blocks: () => delay<Block[]>(mockBlocks),
  rooms: () => delay<Room[]>(mockRooms),
  services: () => delay<ServiceLocation[]>(mockServices),
  route: (_from: string, _to: string) => delay<Route>(mockRoutes[0]),
};

export const agendaService = {
  list: () => delay<AgendaItem[]>(mockAgenda),
  today: () => delay<AgendaItem[]>(mockAgenda.filter((a) => a.date === new Date().toISOString().slice(0, 10))),
};

export const eventService = {
  list: () => delay<Event[]>(mockEvents),
  register: (id: string) => delay<{ ok: true; id: string }>({ ok: true, id }),
};

export const clinicService = {
  specialties: () => delay<Specialty[]>(mockSpecialties),
  requestQuote: (specialtyId: string) => delay<{ ok: true; quoteId: string; specialtyId: string }>({ ok: true, quoteId: "Q-" + Math.random().toString(36).slice(2, 8).toUpperCase(), specialtyId }),
  schedule: (specialtyId: string, date: string) => delay<{ ok: true; bookingId: string; specialtyId: string; date: string }>({ ok: true, bookingId: "B-" + Math.random().toString(36).slice(2, 8).toUpperCase(), specialtyId, date }),
};
