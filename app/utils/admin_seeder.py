# app/utils/admin_seeder.py
from sqlalchemy import select
from app.database.session import SessionLocal
from app.database.models.user import User, UserRole
from app.database.models.user_profile import UserProfile
from app.utils.hash import get_password_hash

async def create_initial_admin():
    async with SessionLocal() as session:
        async with session.begin():
            # Check if admin already exists
            admin_email = "admin@gmail.com"
            result = await session.execute(select(User).where(User.email == admin_email))
            existing_admin = result.scalar_one_or_none()

            if existing_admin:
                print(f"Admin with email {admin_email} already exists.")
                return

            # Create new admin user
            admin_user = User(
                email=admin_email,
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                role=UserRole.admin
            )
            session.add(admin_user)
            await session.flush()  # To get the admin_user.id

            # Create admin profile
            admin_profile = UserProfile(
                user_id=admin_user.id,
                full_name="System Administrator",
                bio="Initial system administrator account."
            )
            session.add(admin_profile)
            
            print(f"Admin user created successfully with email: {admin_email}")
