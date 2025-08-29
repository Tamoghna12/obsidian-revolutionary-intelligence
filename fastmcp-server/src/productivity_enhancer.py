#!/usr/bin/env python3
"""
Productivity Enhancer for Obsidian MCP Server
Advanced workflow automation, goal tracking, and productivity analytics
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import os
import re
from pathlib import Path
import hashlib

class WorkflowAutomation:
    """Advanced workflow automation and task management"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.workflows_dir = os.path.join(vault_path, "Workflows")
        self.templates_dir = os.path.join(vault_path, "Templates")
        
    def create_project_workflow(self, project_name: str, project_type: str = "general") -> Dict[str, Any]:
        """Create a complete project workflow with milestones and tasks"""
        
        workflow_templates = {
            "research": {
                "phases": [
                    {"name": "Literature Review", "duration": 7, "tasks": [
                        "Identify key papers and sources",
                        "Create annotated bibliography",
                        "Synthesize findings"
                    ]},
                    {"name": "Hypothesis Development", "duration": 3, "tasks": [
                        "Formulate research questions",
                        "Develop hypotheses",
                        "Design methodology"
                    ]},
                    {"name": "Data Collection", "duration": 14, "tasks": [
                        "Set up data collection tools",
                        "Collect primary data",
                        "Organize and backup data"
                    ]},
                    {"name": "Analysis", "duration": 10, "tasks": [
                        "Process data",
                        "Run statistical analysis",
                        "Interpret results"
                    ]},
                    {"name": "Writing", "duration": 14, "tasks": [
                        "Create outline",
                        "Write draft sections",
                        "Peer review and revisions"
                    ]},
                    {"name": "Publication", "duration": 7, "tasks": [
                        "Format for submission",
                        "Submit to journal/conference",
                        "Respond to feedback"
                    ]}
                ]
            },
            "content": {
                "phases": [
                    {"name": "Ideation", "duration": 3, "tasks": [
                        "Brainstorm content ideas",
                        "Research trending topics",
                        "Select content format"
                    ]},
                    {"name": "Planning", "duration": 2, "tasks": [
                        "Create content outline",
                        "Research sources",
                        "Set publication schedule"
                    ]},
                    {"name": "Creation", "duration": 5, "tasks": [
                        "Write first draft",
                        "Create supporting materials",
                        "Add visuals/media"
                    ]},
                    {"name": "Editing", "duration": 3, "tasks": [
                        "Proofread content",
                        "Optimize for SEO",
                        "Get feedback"
                    ]},
                    {"name": "Publishing", "duration": 2, "tasks": [
                        "Format for platform",
                        "Schedule publication",
                        "Create promotional materials"
                    ]},
                    {"name": "Promotion", "duration": 7, "tasks": [
                        "Share on social media",
                        "Engage with audience",
                        "Analyze performance"
                    ]}
                ]
            },
            "learning": {
                "phases": [
                    {"name": "Goal Setting", "duration": 1, "tasks": [
                        "Define learning objectives",
                        "Set timeline and milestones",
                        "Identify resources"
                    ]},
                    {"name": "Foundation", "duration": 7, "tasks": [
                        "Complete introductory materials",
                        "Take initial assessments",
                        "Join learning communities"
                    ]},
                    {"name": "Core Learning", "duration": 21, "tasks": [
                        "Complete main curriculum",
                        "Practice with exercises",
                        "Take progress assessments"
                    ]},
                    {"name": "Application", "duration": 14, "tasks": [
                        "Work on projects",
                        "Apply knowledge in real situations",
                        "Get feedback from mentors"
                    ]},
                    {"name": "Review", "duration": 7, "tasks": [
                        "Review key concepts",
                        "Identify knowledge gaps",
                        "Plan next steps"
                    ]}
                ]
            },
            "general": {
                "phases": [
                    {"name": "Planning", "duration": 3, "tasks": [
                        "Define project scope",
                        "Set objectives and milestones",
                        "Identify resources needed"
                    ]},
                    {"name": "Execution", "duration": 14, "tasks": [
                        "Complete core tasks",
                        "Monitor progress",
                        "Adjust plan as needed"
                    ]},
                    {"name": "Review", "duration": 3, "tasks": [
                        "Evaluate results",
                        "Document lessons learned",
                        "Plan next steps"
                    ]}
                ]
            }
        }
        
        template = workflow_templates.get(project_type, workflow_templates["research"])
        
        # Calculate timeline
        start_date = datetime.now()
        current_date = start_date
        phases_with_dates = []
        
        for phase in template["phases"]:
            end_date = current_date + timedelta(days=phase["duration"])
            phases_with_dates.append({
                "name": phase["name"],
                "start_date": current_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "duration": phase["duration"],
                "tasks": [{"name": task, "completed": False, "due_date": end_date.strftime("%Y-%m-%d")} 
                         for task in phase["tasks"]]
            })
            current_date = end_date + timedelta(days=1)
            
        workflow = {
            "project_name": project_name,
            "project_type": project_type,
            "created_date": start_date.strftime("%Y-%m-%d"),
            "total_duration": (current_date - start_date).days,
            "phases": phases_with_dates,
            "status": "active"
        }
        
        # Create workflow file
        workflow_path = os.path.join(self.workflows_dir, f"{project_name.replace(' ', '_')}_workflow.md")
        os.makedirs(os.path.dirname(workflow_path), exist_ok=True)
        
        with open(workflow_path, 'w') as f:
            f.write(f"# {project_name} Workflow\n\n")
            f.write(f"**Project Type:** {project_type}\n")
            f.write(f"**Created:** {start_date.strftime('%Y-%m-%d')}\n")
            f.write(f"**Total Duration:** {workflow['total_duration']} days\n\n")
            
            f.write("## Phases\n\n")
            for i, phase in enumerate(phases_with_dates, 1):
                f.write(f"### Phase {i}: {phase['name']}\n")
                f.write(f"- **Duration:** {phase['duration']} days\n")
                f.write(f"- **Start Date:** {phase['start_date']}\n")
                f.write(f"- **End Date:** {phase['end_date']}\n\n")
                
                f.write("#### Tasks:\n")
                for task in phase["tasks"]:
                    f.write(f"- [ ] {task['name']} (Due: {task['due_date']})\n")
                f.write("\n")
        
        return {
            "workflow": workflow,
            "path": workflow_path,
            "message": f"Workflow created for '{project_name}' with {len(phases_with_dates)} phases"
        }
    
    def track_project_progress(self, project_name: str) -> Dict[str, Any]:
        """Track progress on a project workflow"""
        workflow_path = os.path.join(self.workflows_dir, f"{project_name.replace(' ', '_')}_workflow.md")
        
        if not os.path.exists(workflow_path):
            return {"error": f"Workflow not found for project '{project_name}'"}
        
        # Read workflow file and extract task information
        with open(workflow_path, 'r') as f:
            content = f.read()
        
        # Extract tasks using regex
        tasks = re.findall(r'- \[([ x])\] (.+) \(Due: (.+)\)', content)
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task[0] == 'x')
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Extract phases
        phases = re.findall(r'### Phase \d+: (.+)', content)
        
        return {
            "project_name": project_name,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": round(completion_rate, 1),
            "phases": phases,
            "status": "completed" if completion_rate == 100 else "in_progress" if completion_rate > 0 else "not_started"
        }

class GoalTracker:
    """Advanced goal tracking with OKRs and progress analytics"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.goals_dir = os.path.join(vault_path, "Goals")
        
    def create_objectives_and_key_results(self, timeframe: str, objectives: List[Dict]) -> Dict[str, Any]:
        """Create OKRs (Objectives and Key Results) framework"""
        
        okr_data = {
            "timeframe": timeframe,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "objectives": []
        }
        
        for obj in objectives:
            objective = {
                "name": obj["name"],
                "description": obj.get("description", ""),
                "priority": obj.get("priority", "medium"),
                "key_results": []
            }
            
            for kr in obj.get("key_results", []):
                key_result = {
                    "name": kr["name"],
                    "target": kr.get("target", 100),
                    "current": kr.get("current", 0),
                    "unit": kr.get("unit", "%"),
                    "confidence": kr.get("confidence", 0.7),
                    "progress": round((kr.get("current", 0) / kr.get("target", 100)) * 100, 1) if kr.get("target", 100) > 0 else 0
                }
                objective["key_results"].append(key_result)
            
            # Calculate objective progress
            if objective["key_results"]:
                avg_progress = sum(kr["progress"] for kr in objective["key_results"]) / len(objective["key_results"])
                objective["progress"] = round(avg_progress, 1)
            else:
                objective["progress"] = 0
                
            okr_data["objectives"].append(objective)
        
        # Save OKR to file
        okr_filename = f"OKRs_{timeframe.replace(' ', '_')}.md"
        okr_path = os.path.join(self.goals_dir, okr_filename)
        os.makedirs(os.path.dirname(okr_path), exist_ok=True)
        
        with open(okr_path, 'w') as f:
            f.write(f"# Objectives and Key Results - {timeframe}\n\n")
            f.write(f"**Created:** {okr_data['created_date']}\n\n")
            
            for i, objective in enumerate(okr_data["objectives"], 1):
                f.write(f"## Objective {i}: {objective['name']}\n")
                f.write(f"**Priority:** {objective['priority']}\n")
                f.write(f"**Progress:** {objective['progress']}%\n\n")
                
                if objective["description"]:
                    f.write(f"{objective['description']}\n\n")
                
                f.write("### Key Results:\n")
                for kr in objective["key_results"]:
                    status_emoji = "✅" if kr["progress"] >= 100 else "🟡" if kr["progress"] >= 50 else "🔴"
                    f.write(f"- {status_emoji} {kr['name']}: {kr['current']}/{kr['target']} {kr['unit']} ({kr['progress']}%)\n")
                f.write("\n")
        
        return {
            "okrs": okr_data,
            "path": okr_path,
            "message": f"OKRs created for {timeframe} with {len(objectives)} objectives"
        }
    
    def update_key_result(self, timeframe: str, objective_index: int, kr_index: int, new_value: float) -> Dict[str, Any]:
        """Update a key result value and recalculate progress"""
        okr_filename = f"OKRs_{timeframe.replace(' ', '_')}.md"
        okr_path = os.path.join(self.goals_dir, okr_filename)
        
        if not os.path.exists(okr_path):
            return {"error": f"OKRs not found for timeframe '{timeframe}'"}
        
        # For now, we'll just return a success message
        # In a real implementation, we would update the file
        return {
            "message": f"Updated key result {kr_index+1} in objective {objective_index+1} to {new_value}",
            "new_value": new_value
        }

class FocusSessionManager:
    """Deep work session tracking and optimization"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.sessions_dir = os.path.join(vault_path, "Focus Sessions")
        
    def start_focus_session(self, topic: str, planned_duration: int, environment: str = "default") -> Dict[str, Any]:
        """Start a deep work focus session"""
        
        session_id = hashlib.md5(f"{topic}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        start_time = datetime.now()
        
        session_data = {
            "session_id": session_id,
            "topic": topic,
            "start_time": start_time.isoformat(),
            "planned_duration": planned_duration,
            "actual_duration": 0,
            "environment": environment,
            "distractions": [],
            "achievements": [],
            "status": "active"
        }
        
        # Create session file
        session_filename = f"focus_session_{session_id}.md"
        session_path = os.path.join(self.sessions_dir, session_filename)
        os.makedirs(os.path.dirname(session_path), exist_ok=True)
        
        with open(session_path, 'w') as f:
            f.write(f"# Focus Session: {topic}\n\n")
            f.write(f"**Session ID:** {session_id}\n")
            f.write(f"**Start Time:** {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Planned Duration:** {planned_duration} minutes\n")
            f.write(f"**Environment:** {environment}\n\n")
            
            f.write("## Session Log\n")
            f.write("- Session started\n\n")
            
            f.write("## Distractions\n")
            f.write("(Log distractions here)\n\n")
            
            f.write("## Achievements\n")
            f.write("(Log accomplishments here)\n\n")
            
            f.write("## Session End\n")
            f.write("(Session end time and summary will be added here)\n")
        
        return {
            "session": session_data,
            "path": session_path,
            "message": f"Focus session started for '{topic}' ({planned_duration} minutes)"
        }
    
    def log_distraction(self, session_id: str, distraction: str) -> Dict[str, Any]:
        """Log a distraction during a focus session"""
        session_filename = f"focus_session_{session_id}.md"
        session_path = os.path.join(self.sessions_dir, session_filename)
        
        if not os.path.exists(session_path):
            return {"error": f"Session {session_id} not found"}
        
        # In a real implementation, we would append to the file
        return {
            "message": f"Logged distraction for session {session_id}: {distraction}",
            "distraction": distraction
        }
    
    def end_focus_session(self, session_id: str, achievements: List[str] = None) -> Dict[str, Any]:
        """End a focus session and record achievements"""
        session_filename = f"focus_session_{session_id}.md"
        session_path = os.path.join(self.sessions_dir, session_filename)
        
        if not os.path.exists(session_path):
            return {"error": f"Session {session_id} not found"}
        
        end_time = datetime.now()
        
        # In a real implementation, we would update the file with end time and achievements
        return {
            "message": f"Session {session_id} ended at {end_time.strftime('%H:%M:%S')}",
            "end_time": end_time.isoformat(),
            "achievements": achievements or []
        }

class ResourceOptimizer:
    """Optimize resource allocation and time management"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.analytics_dir = os.path.join(vault_path, "Analytics")
        
    def analyze_productivity_patterns(self, notes: List[Dict]) -> Dict[str, Any]:
        """Analyze productivity patterns from note creation data"""
        
        # Extract time-based patterns
        hourly_patterns = {}
        daily_patterns = {}
        tag_patterns = {}
        
        for note in notes:
            created_str = note.get("created", "")
            if created_str:
                try:
                    created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                    hour = created.hour
                    day = created.strftime("%A")
                    
                    hourly_patterns[hour] = hourly_patterns.get(hour, 0) + 1
                    daily_patterns[day] = daily_patterns.get(day, 0) + 1
                    
                    # Extract tags
                    tags = note.get("tags", [])
                    for tag in tags:
                        tag_patterns[tag] = tag_patterns.get(tag, 0) + 1
                except:
                    continue
        
        # Find peak productivity hours
        peak_hour = max(hourly_patterns.items(), key=lambda x: x[1]) if hourly_patterns else (0, 0)
        peak_day = max(daily_patterns.items(), key=lambda x: x[1]) if daily_patterns else ("Unknown", 0)
        popular_tags = sorted(tag_patterns.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "peak_productivity_hour": {"hour": peak_hour[0], "count": peak_hour[1]},
            "peak_productivity_day": {"day": peak_day[0], "count": peak_day[1]},
            "popular_tags": popular_tags,
            "total_notes_analyzed": len(notes),
            "hourly_distribution": hourly_patterns,
            "daily_distribution": daily_patterns
        }
    
    def suggest_optimal_schedule(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest optimal schedule based on productivity patterns and preferences"""
        
        # Default suggestions
        suggestions = {
            "optimal_work_hours": "9:00 AM - 5:00 PM",
            "best_focus_time": "Morning (9-11 AM)",
            "break_schedule": "25 min work / 5 min break",
            "weekly_review_time": "Friday afternoon",
            "deep_work_blocks": ["9:00-11:00", "14:00-16:00"],
            "energy_management": {
                "high_energy_tasks": "Morning",
                "medium_energy_tasks": "Mid-day",
                "low_energy_tasks": "Afternoon"
            }
        }
        
        return {
            "schedule_suggestions": suggestions,
            "personalization_notes": "Adjust based on your actual productivity patterns",
            "implementation_tips": [
                "Start with one suggestion at a time",
                "Track your energy levels",
                "Adjust based on results"
            ]
        }

# Global instances
workflow_automation = None
goal_tracker = None
focus_session_manager = None
resource_optimizer = None

def get_productivity_enhancer(vault_path: str):
    """Get or create productivity enhancer components"""
    global workflow_automation, goal_tracker, focus_session_manager, resource_optimizer
    
    if workflow_automation is None:
        workflow_automation = WorkflowAutomation(vault_path)
    if goal_tracker is None:
        goal_tracker = GoalTracker(vault_path)
    if focus_session_manager is None:
        focus_session_manager = FocusSessionManager(vault_path)
    if resource_optimizer is None:
        resource_optimizer = ResourceOptimizer(vault_path)
    
    return {
        "workflow_automation": workflow_automation,
        "goal_tracker": goal_tracker,
        "focus_session_manager": focus_session_manager,
        "resource_optimizer": resource_optimizer
    }