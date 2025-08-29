"""
Enhanced Templates and Productivity Features for Obsidian MCP Server
"""

from datetime import datetime, timedelta
import json
import os

class TemplateManager:
    """Manages note templates with customization and productivity features"""
    
    def __init__(self):
        self.templates = {
            # Academic & Research Templates
            'research': '''# {title}

## Research Context
- **Project**: {project}
- **Research Question**: {research_question}
- **Hypothesis**: {hypothesis}
- **Date**: {date}
- **Status**: {status}

## Key Findings & Insights
{content}

## Methodology
- **Approach**: {methodology}
- **Tools Used**: {tools}
- **Data Sources**: {data_sources}
- **Sample Size**: {sample_size}

## Results & Analysis
### Quantitative Results
{quantitative_results}

### Qualitative Insights
{qualitative_insights}

## Literature Review
{literature_review}

## Next Steps
- [ ] Validate findings with larger dataset
- [ ] Peer review and feedback
- [ ] Prepare publication/presentation
- [ ] Plan follow-up experiments

## Code & Data
```{code_language}
{code_snippets}
```

## Related Work
{backlinks}

---
**Tags**: {tags} #research #academia
**Confidence Level**: {confidence}/10
**Impact**: {impact}''',

            'literature-review': '''# Literature Review: {title}

## Overview
- **Topic**: {project}
- **Search Strategy**: {search_strategy}
- **Date Range**: {date_range}
- **Databases**: {databases}
- **Review Date**: {date}

## Key Papers & Sources
{content}

## Themes & Patterns
### Theme 1: {theme1}
{theme1_content}

### Theme 2: {theme2}
{theme2_content}

### Theme 3: {theme3}
{theme3_content}

## Research Gaps Identified
- {gap1}
- {gap2}
- {gap3}

## Synthesis & Conclusions
{synthesis}

## Bibliography
{bibliography}

## Future Research Directions
- [ ] {future_direction1}
- [ ] {future_direction2}
- [ ] {future_direction3}

---
**Tags**: {tags} #literature-review #research''',

            # Technical & Development Templates
            'pipeline': '''# Pipeline Design: {title}

## Project Overview
- **Objective**: {project}
- **Pipeline Type**: {pipeline_type}
- **Priority**: {priority}
- **Owner**: {owner}
- **Date**: {date}

## Current State Analysis
{content}

## Architecture Design
```mermaid
graph LR
    A[Input] --> B[Processing]
    B --> C[Output]
```

### Components
1. **Input Stage**: {input_stage}
2. **Processing Stage**: {processing_stage}
3. **Output Stage**: {output_stage}

## Technical Requirements
- **Memory**: {memory_req}
- **CPU**: {cpu_req}
- **Storage**: {storage_req}
- **Runtime**: {runtime_req}
- **Dependencies**: {dependencies}

## Implementation Roadmap
### Phase 1: MVP ({phase1_timeline})
- [ ] {phase1_task1}
- [ ] {phase1_task2}
- [ ] {phase1_task3}

### Phase 2: Enhancement ({phase2_timeline})
- [ ] {phase2_task1}
- [ ] {phase2_task2}

### Phase 3: Optimization ({phase3_timeline})
- [ ] {phase3_task1}
- [ ] {phase3_task2}

## Quality Assurance
- [ ] Unit tests coverage > 80%
- [ ] Integration tests
- [ ] Performance benchmarks
- [ ] Security audit
- [ ] Documentation complete

## Deployment Strategy
- **Environment**: {environment}
- **Monitoring**: {monitoring}
- **Rollback Plan**: {rollback_plan}

## Related Pipelines
{backlinks}

---
**Tags**: {tags} #pipeline #technical #development
**Complexity**: {complexity}/10
**Risk Level**: {risk_level}''',

            'troubleshooting': '''# Troubleshooting: {title}

## Issue Summary
- **System**: {system}
- **Severity**: {severity}
- **Reporter**: {reporter}
- **Date**: {date}
- **Status**: {status}

## Problem Description
{content}

## Environment Details
- **OS**: {os_version}
- **Software Version**: {software_version}
- **Dependencies**: {dependencies}
- **Configuration**: {configuration}

## Reproduction Steps
1. {step1}
2. {step2}
3. {step3}

## Investigation Log
### {investigation_date1}
{investigation_log1}

### {investigation_date2}
{investigation_log2}

## Root Cause Analysis
### Immediate Cause
{immediate_cause}

### Underlying Cause
{underlying_cause}

### Contributing Factors
- {factor1}
- {factor2}
- {factor3}

## Solution Implemented
{solution}

## Prevention Measures
- [ ] {prevention1}
- [ ] {prevention2}
- [ ] {prevention3}

## Lessons Learned
{lessons_learned}

---
**Tags**: {tags} #troubleshooting #technical #incident''',

            # Productivity & Planning Templates
            'daily-note': '''# Daily Note - {date}

## Today's Focus
- **Main Priority**: {main_priority}
- **Energy Level**: {energy_level}/10
- **Weather**: {weather}

## Schedule
### Morning ({morning_time})
{morning_schedule}

### Afternoon ({afternoon_time})
{afternoon_schedule}

### Evening ({evening_time})
{evening_schedule}

## Tasks & Accomplishments
### Completed ✅
- {completed_task1}
- {completed_task2}
- {completed_task3}

### In Progress 🔄
- {inprogress_task1}
- {inprogress_task2}

### Postponed ⏰
- {postponed_task1}
- {postponed_task2}

## Notes & Reflections
{content}

## Tomorrow's Prep
- [ ] {tomorrow_task1}
- [ ] {tomorrow_task2}
- [ ] {tomorrow_task3}

## Gratitude & Wins
- {gratitude1}
- {gratitude2}
- {gratitude3}

## Links & References
{backlinks}

---
**Tags**: {tags} #daily-note #productivity #planning''',

            'weekly-review': '''# Weekly Review - Week of {week_date}

## Week Overview
- **Theme**: {weekly_theme}
- **Overall Rating**: {week_rating}/10
- **Key Achievement**: {key_achievement}

## Goals Progress
### Professional Goals
- {prof_goal1}: {prof_progress1}
- {prof_goal2}: {prof_progress2}
- {prof_goal3}: {prof_progress3}

### Personal Goals
- {personal_goal1}: {personal_progress1}
- {personal_goal2}: {personal_progress2}

## Daily Highlights
### Monday
{monday_highlight}

### Tuesday
{tuesday_highlight}

### Wednesday
{wednesday_highlight}

### Thursday
{thursday_highlight}

### Friday
{friday_highlight}

### Weekend
{weekend_highlight}

## Metrics & Analytics
- **Deep Work Hours**: {deep_work_hours}
- **Meetings**: {meeting_count}
- **Notes Created**: {notes_created}
- **Books/Articles Read**: {reading_count}

## Lessons Learned
{content}

## Next Week Planning
### Priorities
1. {next_priority1}
2. {next_priority2}
3. {next_priority3}

### Schedule Changes
{schedule_changes}

### Experiments to Try
- {experiment1}
- {experiment2}

---
**Tags**: {tags} #weekly-review #productivity #reflection''',

            'project-brief': '''# Project Brief: {title}

## Project Overview
- **Client/Stakeholder**: {client}
- **Project Manager**: {pm}
- **Start Date**: {start_date}
- **Deadline**: {deadline}
- **Budget**: {budget}
- **Status**: {status}

## Problem Statement
{content}

## Objectives & Success Criteria
### Primary Objectives
1. {objective1}
2. {objective2}
3. {objective3}

### Success Metrics
- {metric1}: {target1}
- {metric2}: {target2}
- {metric3}: {target3}

## Scope & Deliverables
### In Scope
- {in_scope1}
- {in_scope2}
- {in_scope3}

### Out of Scope
- {out_scope1}
- {out_scope2}

### Key Deliverables
1. {deliverable1} - Due: {due1}
2. {deliverable2} - Due: {due2}
3. {deliverable3} - Due: {due3}

## Team & Resources
### Core Team
- **{role1}**: {person1}
- **{role2}**: {person2}
- **{role3}**: {person3}

### Required Resources
- {resource1}
- {resource2}
- {resource3}

## Risk Assessment
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {risk1} | {prob1} | {impact1} | {mitigation1} |
| {risk2} | {prob2} | {impact2} | {mitigation2} |

## Timeline & Milestones
```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    {milestone1} : {date1}, {duration1}
    section Phase 2
    {milestone2} : {date2}, {duration2}
```

## Related Projects
{backlinks}

---
**Tags**: {tags} #project #planning #management
**Priority**: {priority}
**Complexity**: {complexity}/10''',

            # Content & Communication Templates
            'blog-post': '''# Blog Post: {title}

## Post Details
- **Target Audience**: {target_audience}
- **Platform**: {platform}
- **Word Count Target**: {word_count}
- **Publication Date**: {pub_date}
- **Status**: {status}

## Content Strategy
- **Hook**: {hook}
- **Main Message**: {main_message}
- **Call to Action**: {cta}
- **SEO Keywords**: {seo_keywords}

## Outline
### Introduction
{intro_outline}

### Main Content
{content}

### Conclusion
{conclusion_outline}

## Research & Sources
{research_sources}

## Social Media Strategy
- **Twitter Thread**: {twitter_thread}
- **LinkedIn Post**: {linkedin_post}
- **Instagram Caption**: {instagram_caption}

## Performance Metrics
- **Target Views**: {target_views}
- **Target Engagement**: {target_engagement}
- **Conversion Goal**: {conversion_goal}

---
**Tags**: {tags} #blog #content #marketing''',

            'book-notes': '''# Book Notes: {title}

## Book Information
- **Author**: {author}
- **Genre**: {genre}
- **Publication Year**: {pub_year}
- **Pages**: {page_count}
- **ISBN**: {isbn}
- **Reading Date**: {date}
- **Rating**: {rating}/10

## Summary
{content}

## Key Concepts & Ideas
### Concept 1: {concept1}
{concept1_notes}

### Concept 2: {concept2}
{concept2_notes}

### Concept 3: {concept3}
{concept3_notes}

## Memorable Quotes
> {quote1}

> {quote2}

> {quote3}

## Actionable Insights
- [ ] {action1}
- [ ] {action2}
- [ ] {action3}

## Personal Reflections
{personal_reflections}

## Related Books & Resources
{related_books}

## Application to My Work
{work_application}

---
**Tags**: {tags} #book-notes #learning #knowledge
**Recommend**: {recommend_rating}/10''',

            # Meeting & Communication Templates
            'meeting-notes': '''# Meeting Notes: {title}

## Meeting Details
- **Date**: {date}
- **Duration**: {duration}
- **Type**: {meeting_type}
- **Location**: {location}

## Attendees
- **Organizer**: {organizer}
- **Participants**: {participants}
- **Absentees**: {absentees}

## Agenda
{agenda}

## Discussion Summary
{content}

## Decisions Made
1. **{decision1}**: {decision1_detail}
2. **{decision2}**: {decision2_detail}
3. **{decision3}**: {decision3_detail}

## Action Items
| Task | Owner | Deadline | Status |
|------|-------|----------|---------|
| {task1} | {owner1} | {deadline1} | {status1} |
| {task2} | {owner2} | {deadline2} | {status2} |
| {task3} | {owner3} | {deadline3} | {status3} |

## Follow-up Required
- [ ] {followup1}
- [ ] {followup2}
- [ ] {followup3}

## Next Meeting
- **Date**: {next_date}
- **Agenda Items**: {next_agenda}

## Parking Lot (Items to Revisit)
- {parking1}
- {parking2}

---
**Tags**: {tags} #meeting #notes #teamwork''',

            # Learning & Development Templates
            'course-notes': '''# Course Notes: {title}

## Course Information
- **Institution/Platform**: {institution}
- **Instructor**: {instructor}
- **Duration**: {duration}
- **Start Date**: {start_date}
- **Completion Date**: {completion_date}
- **Certificate**: {certificate_status}

## Learning Objectives
- {objective1}
- {objective2}
- {objective3}

## Module Notes
### Module 1: {module1_title}
{module1_notes}

### Module 2: {module2_title}
{module2_notes}

### Module 3: {module3_title}
{module3_notes}

## Key Takeaways
{content}

## Practical Applications
- {application1}
- {application2}
- {application3}

## Assignments & Projects
### Assignment 1: {assignment1_title}
- **Grade**: {assignment1_grade}
- **Feedback**: {assignment1_feedback}

### Final Project: {final_project_title}
- **Grade**: {final_project_grade}
- **Feedback**: {final_project_feedback}

## Skills Acquired
- {skill1}
- {skill2}
- {skill3}

## Next Steps
- [ ] {next_step1}
- [ ] {next_step2}
- [ ] {next_step3}

---
**Tags**: {tags} #course #learning #education
**Difficulty**: {difficulty}/10
**Usefulness**: {usefulness}/10''',

            # Podcast Template
            'podcast-script': '''# Podcast Script: {title}

## Episode Information
- **Episode Number**: {episode_number}
- **Release Date**: {date}
- **Duration**: {duration_minutes} minutes
- **Host**: {host}
- **Guests**: {guests}

## Episode Overview
**Topic**: {topic}
**Main Question**: {main_question}
**Key Takeaways**: 
1. {takeaway1}
2. {takeaway2}
3. {takeaway3}

## Pre-Show Preparation
### Research & Notes
{research_notes}

### Key Points to Cover
- {key_point1}
- {key_point2}
- {key_point3}

### Potential Questions
1. {question1}
2. {question2}
3. {question3}

## Show Intro (0-2 min)
**Host**: {intro_script}

## Main Content (2-{duration_minutes-5} min)
### Segment 1: Introduction & Context (2-5 min)
**Host**: {segment1_host}
**Guest**: {segment1_guest}

### Segment 2: Deep Dive Discussion ({segment2_start}-{segment2_end} min)
**Host**: {segment2_host}
**Guest**: {segment2_guest}

### Segment 3: Practical Applications ({segment3_start}-{segment3_end} min)
**Host**: {segment3_host}
**Guest**: {segment3_guest}

## Show Outro ({duration_minutes-5}-{duration_minutes} min)
**Host**: {outro_script}

## Post-Show Tasks
- [ ] Edit and produce audio
- [ ] Create show notes
- [ ] Upload to hosting platform
- [ ] Share on social media
- [ ] Send thank you to guest

## Show Notes
{show_notes}

## Links & Resources
- {link1}
- {link2}
- {link3}

## Quotes to Highlight
> {quote1}

> {quote2}

---
**Tags**: {tags} #podcast #audio #content
**Series**: {series_name}
**Category**: {category}''',
        }

        # Template categories for better organization
        self.categories = {
            'academic': ['research', 'literature-review', 'course-notes', 'book-notes'],
            'technical': ['pipeline', 'troubleshooting'],
            'productivity': ['daily-note', 'weekly-review', 'project-brief', 'meeting-notes'],
            'content': ['blog-post', 'book-notes', 'podcast-script'],
            'learning': ['course-notes', 'book-notes']
        }

        # Default variable values
        self.defaults = {
            'date': lambda: datetime.now().strftime('%Y-%m-%d'),
            'time': lambda: datetime.now().strftime('%H:%M'),
            'week_date': lambda: datetime.now().strftime('%Y-W%W'),
            'status': 'Draft',
            'priority': 'Medium',
            'energy_level': '7',
            'rating': '8',
            'confidence': '7',
            'complexity': '5',
            'risk_level': 'Medium',
            'phase1_timeline': '2 weeks',
            'phase2_timeline': '4 weeks',
            'phase3_timeline': '2 weeks',
        }

    def get_template(self, template_name: str) -> str:
        """Get a template by name"""
        return self.templates.get(template_name, '')

    def get_templates_by_category(self, category: str) -> list:
        """Get all templates in a category"""
        return self.categories.get(category, [])

    def get_all_categories(self) -> list:
        """Get all template categories"""
        return list(self.categories.keys())

    def fill_template(self, template_name: str, variables: dict) -> str:
        """Fill a template with variables, using defaults for missing values"""
        template = self.get_template(template_name)
        if not template:
            return f"Template '{template_name}' not found"

        # Merge with defaults
        filled_vars = {}
        
        # Apply callable defaults
        for key, default in self.defaults.items():
            if callable(default):
                filled_vars[key] = default()
            else:
                filled_vars[key] = default

        # Override with provided variables
        filled_vars.update(variables)

        # Fill template
        try:
            return template.format(**filled_vars)
        except KeyError as e:
            return f"Template error - missing variable: {e}"

    def create_custom_template(self, name: str, template: str, category: str = 'custom'):
        """Add a custom template"""
        self.templates[name] = template
        if category not in self.categories:
            self.categories[category] = []
        if name not in self.categories[category]:
            self.categories[category].append(name)

    def get_template_info(self) -> dict:
        """Get information about all available templates"""
        info = {}
        for category, templates in self.categories.items():
            info[category] = {}
            for template in templates:
                # Extract variables from template
                template_text = self.templates[template]
                variables = set()
                import re
                for match in re.finditer(r'\{([^}]+)\}', template_text):
                    variables.add(match.group(1))
                
                info[category][template] = {
                    'variables': sorted(list(variables)),
                    'description': self._get_template_description(template)
                }
        
        return info

    def _get_template_description(self, template_name: str) -> str:
        """Get a description for a template"""
        descriptions = {
            'research': 'Academic research note with methodology, findings, and next steps',
            'literature-review': 'Comprehensive literature review with themes and analysis',
            'pipeline': 'Technical pipeline design with architecture and implementation plan',
            'troubleshooting': 'Systematic troubleshooting documentation with root cause analysis',
            'daily-note': 'Daily productivity note with schedule, tasks, and reflections',
            'weekly-review': 'Weekly review with goal progress and planning',
            'project-brief': 'Comprehensive project brief with scope, timeline, and resources',
            'blog-post': 'Blog post outline with SEO strategy and social media plan',
            'book-notes': 'Book summary with key concepts and actionable insights',
            'meeting-notes': 'Meeting documentation with decisions and action items',
            'course-notes': 'Course documentation with modules, assignments, and takeaways',
            'podcast-script': 'Podcast episode script with segments, intro/outro, and production notes',
        }
        return descriptions.get(template_name, 'Custom template')

# Productivity Features
class ProductivityFeatures:
    """Additional productivity features for the MCP server"""
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path

    def create_daily_note(self, date_str: str = None) -> dict:
        """Create or get today's daily note"""
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        daily_note_path = f"Daily Notes/{date_str}.md"
        
        return {
            'path': daily_note_path,
            'date': date_str,
            'template': 'daily-note',
            'suggested_tags': f"daily-note, {datetime.now().strftime('%Y')}, {datetime.now().strftime('%B').lower()}"
        }

    def create_weekly_review(self) -> dict:
        """Create this week's review note"""
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        week_str = week_start.strftime('%Y-W%W')
        
        return {
            'path': f"Weekly Reviews/{week_str}.md",
            'week_date': week_str,
            'template': 'weekly-review',
            'suggested_tags': f"weekly-review, {week_start.strftime('%Y')}, planning"
        }

    def get_task_summary(self, notes_content: list) -> dict:
        """Extract task summary from notes"""
        total_tasks = 0
        completed_tasks = 0
        pending_tasks = 0
        
        for content in notes_content:
            import re
            # Find all checkbox tasks
            tasks = re.findall(r'- \[([ x])\] (.+)', content, re.IGNORECASE)
            total_tasks += len(tasks)
            
            for task in tasks:
                if task[0].lower() == 'x':
                    completed_tasks += 1
                else:
                    pending_tasks += 1
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': round(completion_rate, 1)
        }

    def get_productivity_insights(self, notes: list) -> dict:
        """Generate productivity insights from notes"""
        today = datetime.now()
        
        # Note creation patterns
        notes_by_day = {}
        notes_by_template = {}
        
        for note in notes:
            # Assuming note has created date
            created_date = note.get('created', today).date()
            day_name = created_date.strftime('%A')
            
            notes_by_day[day_name] = notes_by_day.get(day_name, 0) + 1
            
            # Template analysis
            template = note.get('template', 'unknown')
            notes_by_template[template] = notes_by_template.get(template, 0) + 1
        
        most_productive_day = max(notes_by_day.items(), key=lambda x: x[1]) if notes_by_day else ('Unknown', 0)
        most_used_template = max(notes_by_template.items(), key=lambda x: x[1]) if notes_by_template else ('Unknown', 0)
        
        return {
            'notes_by_day': notes_by_day,
            'notes_by_template': notes_by_template,
            'most_productive_day': most_productive_day[0],
            'most_used_template': most_used_template[0],
            'total_notes': len(notes)
        }

    def suggest_next_actions(self, recent_notes: list) -> list:
        """Suggest next actions based on recent activity"""
        suggestions = []
        
        # Check if daily note exists for today
        today = datetime.now().strftime('%Y-%m-%d')
        has_daily_note = any(today in note.get('path', '') for note in recent_notes)
        
        if not has_daily_note:
            suggestions.append({
                'type': 'daily_note',
                'action': 'Create today\'s daily note',
                'priority': 'high',
                'template': 'daily-note'
            })
        
        # Check if weekly review is needed
        monday = datetime.now() - timedelta(days=datetime.now().weekday())
        week_str = monday.strftime('%Y-W%W')
        has_weekly_review = any(week_str in note.get('path', '') for note in recent_notes)
        
        if datetime.now().weekday() == 6 and not has_weekly_review:  # Sunday
            suggestions.append({
                'type': 'weekly_review',
                'action': 'Create this week\'s review',
                'priority': 'medium',
                'template': 'weekly-review'
            })
        
        # Suggest literature review if many research notes
        research_notes = [n for n in recent_notes if 'research' in n.get('template', '')]
        if len(research_notes) >= 5:
            suggestions.append({
                'type': 'literature_review',
                'action': 'Consider creating a literature review to synthesize recent research',
                'priority': 'low',
                'template': 'literature-review'
            })
        
        return suggestions[:5]  # Limit to 5 suggestions