from sqlalchemy.orm import Session
from .models.gamification import Achievement, EmployeeAchievement

class GamificationService:
    @staticmethod
    def award_achievement(db: Session, employee_id: int, achievement_name: str):
        achievement = db.query(Achievement).filter(
            Achievement.name == achievement_name,
            Achievement.is_active == True
        ).first()
        if not achievement:
            return False
        
        emp_ach = EmployeeAchievement(
            employee_id=employee_id,
            achievement_id=achievement.id
        )
        db.add(emp_ach)
        db.commit()
        return True
