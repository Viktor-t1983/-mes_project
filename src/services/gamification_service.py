from sqlalchemy.orm import Session
from src.models.gamification import Achievement, EmployeeAchievement, Leaderboard
from src.models.employee import Employee

class GamificationService:
    """Сервис для управления геймификацией"""
    
    @staticmethod
    def award_achievement(db: Session, employee_id: int, achievement_name: str):
        """Назначает достижение сотруднику"""
        try:
            achievement = db.query(Achievement).filter(
                Achievement.name == achievement_name,
                Achievement.is_active == True
            ).first()
            
            if not achievement:
                print(f"[ERROR] Достижение '{achievement_name}' не найдено")
                return False
            
            existing = db.query(EmployeeAchievement).filter(
                EmployeeAchievement.employee_id == employee_id,
                EmployeeAchievement.achievement_id == achievement.id
            ).first()
            
            if existing:
                print(f"ℹ️ Сотрудник уже имеет достижение '{achievement_name}'")
                return True
            
            employee_achievement = EmployeeAchievement(
                employee_id=employee_id,
                achievement_id=achievement.id
            )
            db.add(employee_achievement)
            
            leaderboard = db.query(Leaderboard).filter(
                Leaderboard.employee_id == employee_id
            ).first()
            
            if leaderboard:
                leaderboard.total_points += achievement.points
                leaderboard.level = leaderboard.total_points // 100 + 1
            else:
                leaderboard = Leaderboard(
                    employee_id=employee_id,
                    total_points=achievement.points,
                    level=achievement.points // 100 + 1
                )
                db.add(leaderboard)
            
            db.commit()
            print(f"[OK] Достижение '{achievement_name}' назначено сотруднику #{employee_id}")
            return True
            
        except Exception as e:
            db.rollback()
            print(f"[ERROR] Ошибка назначения достижения: {e}")
            return False
    
    @staticmethod
    def get_leaderboard(db: Session, limit: int = 10):
        """Возвращает таблицу лидеров"""
        leaderboard = db.query(
            Leaderboard,
            Employee
        ).join(
            Employee, Leaderboard.employee_id == Employee.id
        ).order_by(
            Leaderboard.total_points.desc()
        ).limit(limit).all()
        
        result = []
        for rank, (lb, emp) in enumerate(leaderboard, 1):
            result.append({
                "rank": rank,
                "employee_name": f"{emp.first_name} {emp.last_name}",
                "total_points": lb.total_points,
                "level": lb.level,
                "badge_icon": "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "🏅"
            })
        
        return result