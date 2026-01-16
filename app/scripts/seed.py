import asyncio

from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.building import Building
from app.models.organization import Organization, OrganizationPhone


async def seed() -> None:
    async with SessionLocal() as session:
        existing = await session.scalar(
            select(func.count()).select_from(Building)
        )
        if existing and existing > 0:
            return

        food = Activity(name="Food", depth=1)
        meat = Activity(name="Meat Products", depth=2, parent=food)
        dairy = Activity(name="Dairy Products", depth=2, parent=food)

        auto = Activity(name="Automobiles", depth=1)
        trucks = Activity(name="Trucks", depth=2, parent=auto)
        cars = Activity(name="Passenger Cars", depth=2, parent=auto)
        parts = Activity(name="Parts", depth=3, parent=cars)
        accessories = Activity(name="Accessories", depth=3, parent=cars)

        building_a = Building(
            address="Moscow, Lenina 1, Office 3",
            latitude=55.7558,
            longitude=37.6173,
        )
        building_b = Building(
            address="Yekaterinburg, Blukhera 32/1",
            latitude=56.8431,
            longitude=60.6454,
        )

        org_a = Organization(name="Roga i Kopyta LLC", building=building_b)
        org_a.phones = [
            OrganizationPhone(phone="2-222-222"),
            OrganizationPhone(phone="3-333-333"),
        ]
        org_a.activities = [food, meat]

        org_b = Organization(name="Milk City", building=building_b)
        org_b.phones = [OrganizationPhone(phone="8-923-666-13-13")]
        org_b.activities = [food, dairy]

        org_c = Organization(name="Truck Center", building=building_a)
        org_c.phones = [OrganizationPhone(phone="8-800-000-00-00")]
        org_c.activities = [auto, trucks]

        org_d = Organization(name="Auto Parts Hub", building=building_a)
        org_d.phones = [OrganizationPhone(phone="8-495-111-22-33")]
        org_d.activities = [auto, cars, parts, accessories]

        session.add_all(
            [
                food,
                meat,
                dairy,
                auto,
                trucks,
                cars,
                parts,
                accessories,
                building_a,
                building_b,
                org_a,
                org_b,
                org_c,
                org_d,
            ]
        )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
