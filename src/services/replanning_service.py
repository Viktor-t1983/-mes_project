"""
Replanning Service for MES System
Handles production replanning due to defects or delays
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ReplanningService:
    """Production replanning service for defect handling"""
    
    def __init__(self):
        self.replanning_history = []
    
    async def replan_for_defect(self, 
                              manufacturing_order_id: str,
                              defect_details: Dict[str, Any],
                              original_schedule: Dict[str, Any]) -> Dict[str, Any]:
        """
        Replan manufacturing order due to defects
        
        Args:
            manufacturing_order_id: ID of the affected MO
            defect_details: Details about the defect
            original_schedule: Original production schedule
            
        Returns:
            Updated schedule with replanning adjustments
        """
        try:
            # Calculate impact
            defect_impact = self._calculate_defect_impact(defect_details)
            
            # Generate new schedule
            new_schedule = self._generate_new_schedule(
                original_schedule, 
                defect_impact
            )
            
            # Log replanning event
            replan_event = {
                'timestamp': datetime.utcnow(),
                'mo_id': manufacturing_order_id,
                'defect_type': defect_details.get('type'),
                'impact': defect_impact,
                'original_end_date': original_schedule.get('end_date'),
                'new_end_date': new_schedule.get('end_date')
            }
            
            self.replanning_history.append(replan_event)
            logger.info(f"Replanning completed for MO {manufacturing_order_id}")
            
            return {
                'status': 'replanned',
                'manufacturing_order_id': manufacturing_order_id,
                'new_schedule': new_schedule,
                'replanning_reason': 'defect',
                'impact_assessment': defect_impact
            }
            
        except Exception as e:
            logger.error(f"Replanning failed for MO {manufacturing_order_id}: {e}")
            raise
    
    def _calculate_defect_impact(self, defect_details: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate the impact of a defect on production schedule"""
        defect_type = defect_details.get('type', 'unknown')
        severity = defect_details.get('severity', 'medium')
        
        impact_hours = {
            'critical': 24,
            'high': 12,
            'medium': 6,
            'low': 2
        }.get(severity, 6)
        
        return {
            'defect_type': defect_type,
            'severity': severity,
            'delay_hours': impact_hours,
            'additional_costs': impact_hours * 100  # Simplified cost model
        }
    
    def _generate_new_schedule(self, 
                             original_schedule: Dict[str, Any],
                             impact: Dict[str, Any]) -> Dict[str, Any]:
        """Generate new production schedule based on impact"""
        original_end = original_schedule.get('end_date')
        if isinstance(original_end, str):
            original_end = datetime.fromisoformat(original_end.replace('Z', '+00:00'))
        
        delay_hours = impact.get('delay_hours', 0)
        new_end_date = original_end + timedelta(hours=delay_hours)
        
        return {
            **original_schedule,
            'end_date': new_end_date.isoformat(),
            'delay_hours': delay_hours,
            'replanned_at': datetime.utcnow().isoformat(),
            'status': 'replanned'
        }
    
    def get_replanning_history(self, mo_id: str = None) -> List[Dict[str, Any]]:
        """Get replanning history for specific MO or all"""
        if mo_id:
            return [event for event in self.replanning_history if event.get('mo_id') == mo_id]
        return self.replanning_history

# Factory function
def create_replanning_service() -> ReplanningService:
    return ReplanningService()
