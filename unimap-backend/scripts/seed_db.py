"""
UniMap 3.0 - Database Seed Script
Populates development/staging databases with realistic data
Run: python scripts/seed_db.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.shared.database.engine import AsyncSessionFactory
from backend.api.modules.users.models.user import User
from backend.api.modules.maps.models.map_models import Block, Room
from backend.api.modules.events.models.event import Event
from backend.api.modules.clinics.models.clinic_models import Clinic
from backend.shared.security.jwt import password_service
from backend.shared.security.rbac import UserRole
from datetime import datetime, timezone, timedelta


BLOCKS_DATA = [
    {"code": "BL-A", "name": "Bloco A — Exatas", "short_name": "Bloco A", "block_type": "academic", "floor_count": 3, "latitude": -7.1195, "longitude": -34.8450},
    {"code": "BL-B", "name": "Bloco B — Humanas", "short_name": "Bloco B", "block_type": "academic", "floor_count": 2, "latitude": -7.1198, "longitude": -34.8445},
    {"code": "BL-C", "name": "Bloco C — Saúde", "short_name": "Bloco C", "block_type": "academic", "floor_count": 4, "latitude": -7.1200, "longitude": -34.8440},
    {"code": "BIB", "name": "Biblioteca Central", "short_name": "Biblioteca", "block_type": "library", "floor_count": 2, "latitude": -7.1193, "longitude": -34.8455},
    {"code": "REST", "name": "Restaurante Universitário", "short_name": "RU", "block_type": "food", "floor_count": 1, "latitude": -7.1202, "longitude": -34.8448},
    {"code": "ADM", "name": "Bloco Administrativo", "short_name": "ADM", "block_type": "administrative", "floor_count": 2, "latitude": -7.1190, "longitude": -34.8460},
    {"code": "CLIN", "name": "Clínicas Integradas", "short_name": "Clínicas", "block_type": "clinic", "floor_count": 2, "latitude": -7.1196, "longitude": -34.8442},
    {"code": "GIN", "name": "Ginásio Poliesportivo", "short_name": "Ginásio", "block_type": "sports", "floor_count": 1, "latitude": -7.1205, "longitude": -34.8438},
]

CLINICS_DATA = [
    {
        "name": "Clínica Odontológica",
        "clinic_type": "dental",
        "description": "Atendimento odontológico gratuito para alunos e comunidade",
        "location": "Bloco Clínicas — Térreo",
        "block_code": "CLIN",
        "phone": "(83) 3000-0001",
        "email": "odonto@unimap.edu.br",
        "schedule_info": "Segunda a Sexta: 8h às 17h",
        "accepts_walk_in": False,
    },
    {
        "name": "Clínica de Psicologia",
        "clinic_type": "psychology",
        "description": "Atendimento psicológico para a comunidade universitária",
        "location": "Bloco Clínicas — 1º Andar",
        "block_code": "CLIN",
        "phone": "(83) 3000-0002",
        "email": "psicologia@unimap.edu.br",
        "schedule_info": "Segunda a Sexta: 8h às 18h",
        "accepts_walk_in": False,
    },
    {
        "name": "Clínica de Fisioterapia",
        "clinic_type": "physiotherapy",
        "description": "Reabilitação e tratamento fisioterápico",
        "location": "Bloco C — 2º Andar",
        "block_code": "BL-C",
        "phone": "(83) 3000-0003",
        "email": "fisio@unimap.edu.br",
        "schedule_info": "Segunda a Sexta: 7h às 17h",
        "accepts_walk_in": True,
    },
    {
        "name": "Clínica de Nutrição",
        "clinic_type": "nutrition",
        "description": "Orientação nutricional e acompanhamento dietético",
        "location": "Bloco C — 1º Andar",
        "block_code": "BL-C",
        "phone": "(83) 3000-0004",
        "email": "nutricao@unimap.edu.br",
        "schedule_info": "Segunda a Quinta: 8h às 17h",
        "accepts_walk_in": False,
    },
]

EVENTS_DATA = [
    {
        "title": "Semana Acadêmica de Engenharia 2025",
        "category": "academic",
        "short_description": "Palestras, workshops e feira de oportunidades",
        "starts_at": datetime.now(timezone.utc) + timedelta(days=7),
        "ends_at": datetime.now(timezone.utc) + timedelta(days=12),
        "location_name": "Bloco A — Auditório Principal",
        "organizer_name": "Coordenação de Engenharia",
        "status": "published",
    },
    {
        "title": "Palestra: Inteligência Artificial na Saúde",
        "category": "academic",
        "short_description": "Como a IA está transformando diagnósticos médicos",
        "starts_at": datetime.now(timezone.utc) + timedelta(days=3),
        "ends_at": datetime.now(timezone.utc) + timedelta(days=3, hours=2),
        "location_name": "Bloco C — Auditório",
        "organizer_name": "Curso de Medicina",
        "status": "published",
    },
    {
        "title": "Torneio Universitário de Xadrez",
        "category": "cultural",
        "short_description": "Competição aberta para toda a comunidade universitária",
        "starts_at": datetime.now(timezone.utc) + timedelta(days=14),
        "ends_at": datetime.now(timezone.utc) + timedelta(days=14, hours=6),
        "location_name": "Biblioteca Central",
        "organizer_name": "Atlética UniMap",
        "status": "published",
    },
]


async def seed():
    async with AsyncSessionFactory() as session:
        print("🌱 Seeding UniMap database...")

        # ── Admin user ────────────────────────────────────────────────────────
        admin = User(
            email="admin@unimap.edu.br",
            hashed_password=password_service.hash("AdminPass123!"),
            full_name="Administrador UniMap",
            role=UserRole.ADMIN.value,
            is_verified=True,
            lgpd_consent_at=datetime.now(timezone.utc),
        )
        session.add(admin)

        # ── Test student ──────────────────────────────────────────────────────
        student_user = User(
            email="aluno@unimap.edu.br",
            hashed_password=password_service.hash("AlunoPass123!"),
            full_name="João da Silva",
            role=UserRole.STUDENT.value,
            is_verified=True,
            lgpd_consent_at=datetime.now(timezone.utc),
        )
        session.add(student_user)

        # ── Test visitor ──────────────────────────────────────────────────────
        visitor_user = User(
            email="visitante@unimap.edu.br",
            hashed_password=password_service.hash("VisitPass123!"),
            full_name="Maria Visitante",
            role=UserRole.VISITOR.value,
            lgpd_consent_at=datetime.now(timezone.utc),
        )
        session.add(visitor_user)

        await session.flush()

        # ── Blocks ────────────────────────────────────────────────────────────
        blocks = {}
        for b_data in BLOCKS_DATA:
            block = Block(**b_data)
            session.add(block)
            await session.flush()
            blocks[b_data["code"]] = block
            print(f"  ✅ Block: {b_data['name']}")

        # ── Rooms ─────────────────────────────────────────────────────────────
        for code, block in blocks.items():
            if block.block_type == "academic":
                for floor in range(block.floor_count):
                    for room_num in range(1, 6):
                        room = Room(
                            block_id=block.id,
                            code=f"{code}-{floor}{room_num:02d}",
                            name=f"Sala {floor}{room_num:02d}",
                            floor=floor,
                            capacity=40,
                            room_type="classroom",
                        )
                        session.add(room)

        # ── Clinics ───────────────────────────────────────────────────────────
        for c_data in CLINICS_DATA:
            clinic = Clinic(**c_data)
            session.add(clinic)
            print(f"  ✅ Clinic: {c_data['name']}")

        # ── Events ────────────────────────────────────────────────────────────
        for e_data in EVENTS_DATA:
            event = Event(**e_data, registration_required=False)
            session.add(event)
            print(f"  ✅ Event: {e_data['title']}")

        await session.commit()

    print("\n✅ Seed complete!")
    print("\nTest accounts:")
    print("  Admin:    admin@unimap.edu.br   / AdminPass123!")
    print("  Student:  aluno@unimap.edu.br   / AlunoPass123!")
    print("  Visitor:  visitante@unimap.edu.br / VisitPass123!")


if __name__ == "__main__":
    asyncio.run(seed())
