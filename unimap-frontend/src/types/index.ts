export type UserRole = "visitor" | "student" | "teacher" | "coordination" | "admin";

export interface User {
  id: string;
  name: string;
  email: string;
  rgm?: string;
  role: UserRole;
  course?: string;
  semester?: number;
  avatar?: string;
  achievements: number;
  progress: number;
}

export interface Block {
  id: string;
  name: string;
  code: string;
  description: string;
  about?: string;
  purpose?: string;
  serviceIds?: string[];
  floors: number;
  x: number;
  y: number;
  color: string;
  latitude: number;
  longitude: number;
}

export interface Speaker {
  name: string;
  role: string;
  avatarColor?: string;
}

export interface ScheduleSlot {
  time: string;
  title: string;
  description?: string;
}

export interface EventComment {
  author: string;
  role?: string;
  text: string;
  rating?: number;
}

export interface Room {
  id: string;
  blockId: string;
  name: string;
  floor: number;
  type: "classroom" | "lab" | "auditorium" | "office";
}

export interface ServiceLocation {
  id: string;
  name: string;
  category: "clinic" | "food" | "library" | "support" | "sports" | "parking";
  description: string;
  x: number;
  y: number;
  hours: string;
  latitude: number;
  longitude: number;
}

export interface AgendaItem {
  id: string;
  title: string;
  type: "class" | "exam" | "event" | "personal";
  date: string;
  startTime: string;
  endTime: string;
  location: string;
  blockId?: string;
  teacher?: string;
}

export interface Event {
  id: string;
  title: string;
  category: string;
  visibility: "public" | "private";
  cover: string;
  date: string;
  endDate?: string;
  startTime: string;
  endTime?: string;
  location: string;
  description: string;
  about?: string;
  schedule?: ScheduleSlot[];
  speakers?: Speaker[];
  comments?: EventComment[];
  attendees: number;
  capacity: number;
  registered: boolean;
}

export interface Specialty {
  id: string;
  name: string;
  description: string;
  icon: string;
  durationMin: number;
  priceRange: string;
}

export interface Route {
  id?: string;
  from: string;
  to: string;
  steps: string[];
  distanceM: number;
  durationMin: number;
  coordinates?: [number, number][];
}
