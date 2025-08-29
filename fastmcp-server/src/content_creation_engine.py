#!/usr/bin/env python3
"""
Content Creation Engine for Research-to-Content Pipeline
Automatically generates blogs, summaries, newsletters, and video scripts from research papers
"""

import asyncio
from typing import List, Dict, Any, Optional
import json
import re
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from urllib.parse import quote, urljoin
from pathlib import Path
import os

# Optional dependencies - fallback gracefully
try:
    import aiohttp
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False
    aiohttp = None

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False
    feedparser = None

# Optional dependencies - fallback gracefully
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

class ResearchPaperFetcher:
    """Enhanced fetcher for arXiv and bioRxiv papers with advanced filtering"""
    
    def __init__(self):
        self.session = None
    
    async def search_arxiv(self, query: str, categories: List[str] = None, max_results: int = 20, days_back: int = 7) -> Dict[str, Any]:
        """
        Enhanced arXiv search with category filtering and date range
        
        Args:
            query: Search terms
            categories: arXiv categories (cs.AI, cs.LG, q-bio, etc.)
            max_results: Maximum papers to return
            days_back: Only papers from last N days
        """
        if not HAS_AIOHTTP:
            return {"error": "aiohttp dependency not installed - cannot fetch papers"}
        
        try:
            # Build advanced query
            search_terms = []
            if query:
                search_terms.append(f"all:{quote(query)}")
            
            if categories:
                cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
                search_terms.append(f"({cat_query})")
            
            # Date filtering
            date_filter = ""
            if days_back > 0:
                cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y%m%d")
                date_filter = f"&submittedDate:[{cutoff_date}0000+TO+*]"
            
            query_string = "+AND+".join(search_terms) if len(search_terms) > 1 else search_terms[0] if search_terms else "all:*"
            
            url = f"http://export.arxiv.org/api/query?search_query={query_string}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending{date_filter}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    content = await response.text()
            
            # Parse XML response
            root = ET.fromstring(content)
            papers = []
            
            for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
                # Extract categories
                paper_categories = []
                for category in entry.findall('.//{http://arxiv.org/schemas/atom}primary_category'):
                    paper_categories.append(category.get('term'))
                for category in entry.findall('.//{http://arxiv.org/schemas/atom}category'):
                    if category.get('term') not in paper_categories:
                        paper_categories.append(category.get('term'))
                
                # Extract PDF link
                pdf_link = ""
                for link in entry.findall('.//{http://www.w3.org/2005/Atom}link'):
                    if link.get('title') == 'pdf':
                        pdf_link = link.get('href')
                        break
                
                paper = {
                    "title": entry.find('.//{http://www.w3.org/2005/Atom}title').text.strip().replace('\\n', ' '),
                    "authors": [author.find('.//{http://www.w3.org/2005/Atom}name').text 
                              for author in entry.findall('.//{http://www.w3.org/2005/Atom}author')],
                    "summary": entry.find('.//{http://www.w3.org/2005/Atom}summary').text.strip().replace('\\n', ' '),
                    "published": entry.find('.//{http://www.w3.org/2005/Atom}published').text,
                    "updated": entry.find('.//{http://www.w3.org/2005/Atom}updated').text,
                    "link": entry.find('.//{http://www.w3.org/2005/Atom}id').text,
                    "pdf_link": pdf_link,
                    "categories": paper_categories,
                    "arxiv_id": entry.find('.//{http://www.w3.org/2005/Atom}id').text.split('/')[-1],
                    "source": "arXiv"
                }
                papers.append(paper)
            
            return {
                "source": "arXiv",
                "papers": papers,
                "count": len(papers),
                "search_terms": query,
                "categories_searched": categories or [],
                "date_range_days": days_back
            }
            
        except Exception as e:
            return {"error": f"arXiv search failed: {str(e)}"}
    
    async def search_biorxiv(self, query: str, server: str = "biorxiv", max_results: int = 20, days_back: int = 7) -> Dict[str, Any]:
        """
        Search bioRxiv and medRxiv preprints
        
        Args:
            query: Search terms
            server: "biorxiv" or "medrxiv"
            max_results: Maximum papers to return
            days_back: Only papers from last N days
        """
        if not HAS_AIOHTTP or not HAS_FEEDPARSER:
            return {"error": "Required dependencies not installed - cannot fetch papers"}
        
        try:
            # bioRxiv API endpoint
            base_url = f"https://api.biorxiv.org/details/{server}"
            
            # Date range
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            
            url = f"{base_url}/{start_date}/{end_date}/{max_results}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status != 200:
                        return {"error": f"bioRxiv API returned status {response.status}"}
                    
                    data = await response.json()
            
            papers = []
            if data.get("messages") and len(data["messages"]) > 0:
                for paper_data in data["messages"][0].get("collection", []):
                    # Filter by query if provided
                    if query:
                        title_match = query.lower() in paper_data.get("title", "").lower()
                        abstract_match = query.lower() in paper_data.get("abstract", "").lower()
                        if not (title_match or abstract_match):
                            continue
                    
                    paper = {
                        "title": paper_data.get("title", "").strip(),
                        "authors": paper_data.get("authors", "").split("; ") if paper_data.get("authors") else [],
                        "summary": paper_data.get("abstract", "").strip(),
                        "published": paper_data.get("date"),
                        "updated": paper_data.get("date"),
                        "link": f"https://www.biorxiv.org/content/{paper_data.get('doi')}v{paper_data.get('version')}",
                        "pdf_link": f"https://www.biorxiv.org/content/{paper_data.get('doi')}v{paper_data.get('version')}.full.pdf",
                        "doi": paper_data.get("doi"),
                        "categories": [paper_data.get("category", "biology")],
                        "source": server
                    }
                    papers.append(paper)
            
            return {
                "source": server,
                "papers": papers,
                "count": len(papers),
                "search_terms": query,
                "date_range_days": days_back
            }
            
        except Exception as e:
            return {"error": f"{server} search failed: {str(e)}"}
    
    async def get_trending_papers(self, fields: List[str] = None, days_back: int = 7, max_per_field: int = 10) -> Dict[str, Any]:
        """
        Get trending papers across multiple fields
        
        Args:
            fields: List of research fields/categories
            days_back: Look for papers from last N days
            max_per_field: Maximum papers per field
        """
        if not HAS_AIOHTTP or not HAS_FEEDPARSER:
            return {"error": "Required dependencies not installed - cannot fetch papers"}
        
        default_fields = {
            "AI/ML": {"arxiv_cats": ["cs.AI", "cs.LG", "cs.CL"], "queries": ["artificial intelligence", "machine learning", "deep learning"]},
            "Biology": {"arxiv_cats": ["q-bio"], "queries": ["biology", "genetics", "evolution"], "biorxiv": True},
            "Medicine": {"queries": ["medicine", "clinical", "therapeutic"], "biorxiv": True, "medrxiv": True},
            "Physics": {"arxiv_cats": ["physics"], "queries": ["quantum", "physics"]},
            "Neuroscience": {"arxiv_cats": ["q-bio.NC"], "queries": ["neuroscience", "brain"], "biorxiv": True}
        }
        
        if not fields:
            fields = list(default_fields.keys())
        
        all_papers = {}
        
        for field in fields:
            if field not in default_fields:
                continue
            
            field_config = default_fields[field]
            field_papers = []
            
            # Search arXiv if categories specified
            if "arxiv_cats" in field_config:
                for query in field_config.get("queries", [""]):
                    arxiv_result = await self.search_arxiv(
                        query=query,
                        categories=field_config["arxiv_cats"],
                        max_results=max_per_field,
                        days_back=days_back
                    )
                    if "papers" in arxiv_result:
                        field_papers.extend(arxiv_result["papers"])
            
            # Search bioRxiv if enabled
            if field_config.get("biorxiv"):
                for query in field_config.get("queries", [""]):
                    biorxiv_result = await self.search_biorxiv(
                        query=query,
                        server="biorxiv",
                        max_results=max_per_field,
                        days_back=days_back
                    )
                    if "papers" in biorxiv_result:
                        field_papers.extend(biorxiv_result["papers"])
            
            # Search medRxiv if enabled
            if field_config.get("medrxiv"):
                for query in field_config.get("queries", [""]):
                    medrxiv_result = await self.search_biorxiv(
                        query=query,
                        server="medrxiv",
                        max_results=max_per_field,
                        days_back=days_back
                    )
                    if "papers" in medrxiv_result:
                        field_papers.extend(medrxiv_result["papers"])
            
            # Remove duplicates and limit results
            seen_titles = set()
            unique_papers = []
            for paper in field_papers:
                title_key = paper.get("title", "").lower().strip()
                if title_key and title_key not in seen_titles:
                    seen_titles.add(title_key)
                    unique_papers.append(paper)
                    if len(unique_papers) >= max_per_field:
                        break
            
            all_papers[field] = unique_papers
        
        return {
            "trending_papers": all_papers,
            "total_papers": sum(len(papers) for papers in all_papers.values()),
            "fields_searched": fields,
            "date_range_days": days_back,
            "generated_at": datetime.now().isoformat()
        }


class ContentGenerator:
    """Generate various content formats from research papers"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load content generation templates"""
        return {
            "blog_post": """# {title}

## Introduction
{introduction}

## Key Findings
{key_findings}

## Research Details
**Authors:** {authors}
**Published:** {published}
**Source:** {source}

{detailed_analysis}

## Implications
{implications}

## Conclusion
{conclusion}

## References
- [{paper_title}]({paper_link})
{additional_references}

---
*This post was generated from the latest research paper: "{paper_title}" by {authors}*
""",
            
            "summary": """## {title}

**Quick Summary:** {executive_summary}

**Key Points:**
{key_points}

**Significance:** {significance}

**Authors:** {authors} | **Published:** {published} | **Source:** {source}
**Link:** [{paper_title}]({paper_link})
""",
            
            "newsletter": """# Research Roundup: {date}

## This Week's Breakthrough Papers

{featured_papers}

## Trending Research Areas
{trending_areas}

## Quick Reads
{quick_summaries}

## Deep Dive Recommendations
{deep_dive_papers}

---
*Curated by AI from the latest research across arXiv, bioRxiv, and medRxiv*
""",
            
            "video_script": """# Video Script: {title}

## Hook (0-15 seconds)
{hook}

## Introduction (15-45 seconds)
{introduction}

## Main Content (45 seconds - 5 minutes)
{main_content}

## Key Takeaways (5-6 minutes)
{takeaways}

## Call to Action (6-7 minutes)
{call_to_action}

## Visual Cues
{visual_cues}

## Technical Notes
- **Duration:** {estimated_duration}
- **Complexity Level:** {complexity_level}
- **Target Audience:** {target_audience}
""",
            
            "thread": """🧵 THREAD: {title}

1/🧵 {hook_tweet}

2/🧵 {key_finding_1}

3/🧵 {key_finding_2}

4/🧵 {key_finding_3}

5/🧵 {implications}

6/🧵 {conclusion_tweet}

Paper: {paper_link}
Authors: {authors}
""",

            "substack_post": """# {title}

*Welcome to this week's research deep-dive! Today we're exploring groundbreaking work in {field}.*

## The Big Question

{research_question}

## What They Found

{findings_section}

## Why This Matters

{significance_section}

## The Technical Details
*For those who want to dive deeper*

{technical_section}

## What's Next

{future_implications}

## My Take

{personal_commentary}

---

**Paper Details:**
- **Title:** {paper_title}
- **Authors:** {authors}
- **Published:** {published}
- **Read the full paper:** [{paper_title}]({paper_link})

*Found this interesting? Share it with fellow researchers and let me know your thoughts in the comments!*

---
*This analysis is part of my ongoing series tracking the latest breakthroughs in science and technology. Subscribe to never miss an update!*
""",

            "podcast_script": """# Podcast Script: {title}

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

## Main Content (2-{segment_end_time} min)
### Segment 1: Introduction & Context (2-5 min)
**Host**: {segment1_host}
**Guest**: {segment1_guest}

### Segment 2: Deep Dive Discussion ({segment2_start}-{segment2_end} min)
**Host**: {segment2_host}
**Guest**: {segment2_guest}

### Segment 3: Practical Applications ({segment3_start}-{segment3_end} min)
**Host**: {segment3_host}
**Guest**: {segment3_guest}

## Show Outro ({outro_start_time}-{duration_minutes} min)
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
**Tags**: #podcast #audio #content
**Series**: {series_name}
**Category**: {category}"""
        }
    
    def generate_blog_post(self, paper: Dict[str, Any], style: str = "technical") -> str:
        """Generate a blog post from a research paper"""
        
        # Analyze paper content
        title = paper.get("title", "Research Update")
        summary = paper.get("summary", "")
        authors = ", ".join(paper.get("authors", []))
        
        # Generate content sections
        introduction = self._generate_introduction(paper, style)
        key_findings = self._extract_key_findings(paper)
        detailed_analysis = self._generate_detailed_analysis(paper, style)
        implications = self._generate_implications(paper)
        conclusion = self._generate_conclusion(paper)
        
        return self.templates["blog_post"].format(
            title=title,
            introduction=introduction,
            key_findings=key_findings,
            authors=authors,
            published=paper.get("published", ""),
            source=paper.get("source", ""),
            detailed_analysis=detailed_analysis,
            implications=implications,
            conclusion=conclusion,
            paper_title=title,
            paper_link=paper.get("link", ""),
            additional_references=""
        )
    
    def generate_newsletter(self, papers_by_field: Dict[str, List[Dict]], week_date: str = None) -> str:
        """Generate a newsletter from multiple papers organized by field"""
        
        if not week_date:
            week_date = datetime.now().strftime("%B %d, %Y")
        
        featured_papers = ""
        trending_areas = ""
        quick_summaries = ""
        deep_dive_papers = ""
        
        for field, papers in papers_by_field.items():
            if not papers:
                continue
                
            # Featured paper (first/most relevant)
            if papers:
                top_paper = papers[0]
                featured_papers += f"### {field}: {top_paper.get('title', '')}\n"
                featured_papers += f"{self._generate_summary(top_paper)}\n\n"
            
            # Trending area
            trending_areas += f"**{field}:** {len(papers)} new papers\n"
            
            # Quick summaries for remaining papers
            for paper in papers[1:3]:  # Next 2 papers
                quick_summaries += f"- **{paper.get('title', '')}** ({paper.get('source', '')})\n"
                quick_summaries += f"  {paper.get('summary', '')[:150]}...\n\n"
            
            # Deep dive recommendation
            if papers:
                deep_dive_papers += f"- [{field}] {papers[0].get('title', '')} - {papers[0].get('link', '')}\n"
        
        return self.templates["newsletter"].format(
            date=week_date,
            featured_papers=featured_papers,
            trending_areas=trending_areas,
            quick_summaries=quick_summaries,
            deep_dive_papers=deep_dive_papers
        )
    
    def generate_video_script(self, paper: Dict[str, Any], duration_minutes: int = 5) -> str:
        """Generate a video script from a research paper"""
        
        title = paper.get("title", "Research Breakdown")
        
        # Generate script sections based on duration
        hook = self._generate_hook(paper)
        introduction = self._generate_video_intro(paper)
        main_content = self._generate_main_content(paper, duration_minutes)
        takeaways = self._generate_takeaways(paper)
        call_to_action = self._generate_cta(paper)
        visual_cues = self._generate_visual_cues(paper)
        
        complexity_level = self._assess_complexity(paper)
        target_audience = self._determine_audience(paper, complexity_level)
        
        return self.templates["video_script"].format(
            title=title,
            hook=hook,
            introduction=introduction,
            main_content=main_content,
            takeaways=takeaways,
            call_to_action=call_to_action,
            visual_cues=visual_cues,
            estimated_duration=f"{duration_minutes} minutes",
            complexity_level=complexity_level,
            target_audience=target_audience
        )
    
    def generate_substack_post(self, paper: Dict[str, Any], personal_commentary: str = "") -> str:
        """Generate a Substack post with personal commentary"""
        
        title = paper.get("title", "Research Deep Dive")
        field = self._identify_field(paper)
        research_question = self._extract_research_question(paper)
        findings_section = self._generate_findings_section(paper)
        significance_section = self._generate_significance_section(paper)
        technical_section = self._generate_technical_section(paper)
        future_implications = self._generate_future_implications(paper)
        
        if not personal_commentary:
            personal_commentary = self._generate_personal_commentary(paper)
        
        return self.templates["substack_post"].format(
            title=title,
            field=field,
            research_question=research_question,
            findings_section=findings_section,
            significance_section=significance_section,
            technical_section=technical_section,
            future_implications=future_implications,
            personal_commentary=personal_commentary,
            paper_title=paper.get("title", ""),
            authors=", ".join(paper.get("authors", [])),
            published=paper.get("published", ""),
            paper_link=paper.get("link", "")
        )
    
    def _generate_introduction(self, paper: Dict[str, Any], style: str) -> str:
        """Generate introduction based on style"""
        summary = paper.get("summary", "")
        title = paper.get("title", "")
        
        if style == "technical":
            return f"Recent research published in {paper.get('source', 'academic literature')} presents significant findings in {self._identify_field(paper)}. The study, titled '{title}', addresses fundamental questions in the field and provides new insights that could reshape our understanding."
        elif style == "accessible":
            return f"Scientists have just published fascinating new research that could change how we think about {self._identify_field(paper)}. Let's break down what they discovered and why it matters."
        else:
            return f"In a new study, researchers explore {title.lower()}. This work contributes to our growing understanding of {self._identify_field(paper)}."
    
    def _extract_key_findings(self, paper: Dict[str, Any]) -> str:
        """Extract key findings from paper summary"""
        summary = paper.get("summary", "")
        
        # Simple extraction - in production, would use NLP
        sentences = summary.split('. ')[:5]  # First 5 sentences
        findings = []
        
        for i, sentence in enumerate(sentences, 1):
            if sentence.strip():
                findings.append(f"{i}. {sentence.strip()}")
        
        return "\n".join(findings)
    
    def _generate_detailed_analysis(self, paper: Dict[str, Any], style: str) -> str:
        """Generate detailed analysis section"""
        summary = paper.get("summary", "")
        
        # Extract methodology and results
        analysis = f"## Methodology\nThe researchers {summary[:200]}...\n\n"
        analysis += f"## Results\nThe study reveals {summary[200:400]}...\n\n"
        
        return analysis
    
    def _generate_implications(self, paper: Dict[str, Any]) -> str:
        """Generate implications section"""
        field = self._identify_field(paper)
        return f"These findings have significant implications for {field} research. The results suggest new directions for investigation and potential applications in related fields. Future work could build upon these insights to develop practical solutions."
    
    def _generate_conclusion(self, paper: Dict[str, Any]) -> str:
        """Generate conclusion"""
        return f"This research represents an important step forward in understanding {self._identify_field(paper)}. As the field continues to evolve, studies like this provide the foundation for future breakthroughs."
    
    def _generate_summary(self, paper: Dict[str, Any]) -> str:
        """Generate a brief summary"""
        summary = paper.get("summary", "")
        return summary[:200] + "..." if len(summary) > 200 else summary
    
    def _identify_field(self, paper: Dict[str, Any]) -> str:
        """Identify research field from paper"""
        categories = paper.get("categories", [])
        title = paper.get("title", "").lower()
        summary = paper.get("summary", "").lower()
        
        field_keywords = {
            "artificial intelligence": ["ai", "artificial intelligence", "machine learning", "neural network"],
            "biology": ["biology", "genetic", "evolution", "species"],
            "medicine": ["medical", "clinical", "therapeutic", "patient"],
            "physics": ["quantum", "physics", "particle"],
            "neuroscience": ["brain", "neuron", "cognitive", "neural"]
        }
        
        for field, keywords in field_keywords.items():
            if any(keyword in title or keyword in summary for keyword in keywords):
                return field
        
        # Fallback to categories
        if categories:
            return categories[0]
        
        return "scientific research"
    
    def _generate_hook(self, paper: Dict[str, Any]) -> str:
        """Generate compelling hook for video"""
        title = paper.get("title", "")
        return f"What if I told you that new research could completely change how we understand {self._identify_field(paper)}? Let me show you what scientists just discovered..."
    
    def _generate_video_intro(self, paper: Dict[str, Any]) -> str:
        """Generate video introduction"""
        return f"Today we're diving into groundbreaking research from {', '.join(paper.get('authors', [])[:2])}. Their latest study tackles one of the biggest questions in {self._identify_field(paper)}."
    
    def _generate_main_content(self, paper: Dict[str, Any], duration: int) -> str:
        """Generate main video content"""
        summary = paper.get("summary", "")
        
        # Break into sections based on duration
        if duration <= 3:
            return f"Here's what they found: {summary[:300]}..."
        else:
            return f"Let me break this down for you:\n\nFirst, the researchers discovered that {summary[:150]}...\n\nSecond, they found {summary[150:300]}...\n\nFinally, their analysis shows {summary[300:450]}..."
    
    def _generate_takeaways(self, paper: Dict[str, Any]) -> str:
        """Generate key takeaways"""
        return f"The key takeaways are: 1) This research advances our understanding of {self._identify_field(paper)}, 2) It opens new possibilities for future research, and 3) The implications could be significant for practical applications."
    
    def _generate_cta(self, paper: Dict[str, Any]) -> str:
        """Generate call to action"""
        return f"If you found this research as fascinating as I did, make sure to subscribe for more science breakdowns. And let me know in the comments - what aspect of this research interests you most?"
    
    def _generate_visual_cues(self, paper: Dict[str, Any]) -> str:
        """Generate visual cues for video"""
        return f"- Show paper title and authors\n- Highlight key findings\n- Use diagrams to explain methodology\n- Include author photos if available\n- Show related research timeline"
    
    def _assess_complexity(self, paper: Dict[str, Any]) -> str:
        """Assess complexity level"""
        summary = paper.get("summary", "").lower()
        technical_terms = len(re.findall(r'\b[a-z]+(?:tion|ity|ness|ment|ence|ance)\b', summary))
        
        if technical_terms > 20:
            return "Advanced"
        elif technical_terms > 10:
            return "Intermediate"
        else:
            return "Beginner"
    
    def _determine_audience(self, paper: Dict[str, Any], complexity: str) -> str:
        """Determine target audience"""
        if complexity == "Advanced":
            return "Researchers and graduate students"
        elif complexity == "Intermediate":
            return "Science enthusiasts and undergraduates"
        else:
            return "General audience"
    
    def _extract_research_question(self, paper: Dict[str, Any]) -> str:
        """Extract the main research question"""
        title = paper.get("title", "")
        summary = paper.get("summary", "")
        
        # Simple heuristic - would use NLP in production
        if "?" in title:
            return title
        else:
            return f"How can we better understand {self._identify_field(paper)}?"
    
    def _generate_findings_section(self, paper: Dict[str, Any]) -> str:
        """Generate findings section for Substack"""
        summary = paper.get("summary", "")
        return f"The researchers made several key discoveries:\n\n{summary[:400]}..."
    
    def _generate_significance_section(self, paper: Dict[str, Any]) -> str:
        """Generate significance section"""
        field = self._identify_field(paper)
        return f"This research is significant because it advances our understanding of {field} in several important ways. The findings could lead to new approaches and applications in the field."
    
    def _generate_technical_section(self, paper: Dict[str, Any]) -> str:
        """Generate technical details section"""
        summary = paper.get("summary", "")
        return f"For those interested in the technical details:\n\nThe study employed {summary[100:300]}..."
    
    def _generate_future_implications(self, paper: Dict[str, Any]) -> str:
        """Generate future implications"""
        return f"Looking ahead, this research opens several exciting possibilities for future investigation. The methodology could be applied to related problems, and the findings suggest new directions for the field."
    
    def _generate_personal_commentary(self, paper: Dict[str, Any]) -> str:
        """Generate personal commentary placeholder"""
        return f"What strikes me most about this research is how it challenges conventional thinking in {self._identify_field(paper)}. The approach is innovative and the results are compelling. I'm particularly interested to see how this work will influence future research in the area."

    def generate_podcast_script(self, topic: str, duration_minutes: int = 30) -> str:
        """Generate a podcast script for a given topic"""
        
        # Create podcast structure
        podcast = {
            "title": f"Exploring {topic}",
            "topic": topic,
            "duration_minutes": duration_minutes,
            "episode_number": "001",  # Would be dynamically calculated in production
            "date": datetime.now().strftime("%Y-%m-%d"),  # Add the missing date variable
            "host": "Host Name",
            "guests": "Guest Experts",
            "main_question": f"What's new and exciting in {topic}?",
            "takeaway1": f"Key insight about {topic}",
            "takeaway2": f"Practical applications of {topic}",
            "takeaway3": f"Future directions in {topic}",
            "research_notes": f"Research notes about {topic}",
            "key_point1": f"Fundamentals of {topic}",
            "key_point2": f"Recent developments in {topic}",
            "key_point3": f"Future implications of {topic}",
            "question1": f"What are the biggest misconceptions about {topic}?",
            "question2": f"What exciting developments are happening in {topic}?",
            "question3": f"What should our listeners know about {topic}?",
            "intro_script": f"Welcome to our show where we explore {topic} and its impact on our world.",
            "segment1_host": f"Today we're diving into {topic} with our special guest.",
            "segment1_guest": f"Thanks for having me. {topic} is fascinating because...",
            "segment2_start": "5",
            "segment2_end": str(duration_minutes - 10),
            "segment2_host": f"Let's dig deeper into {topic}.",
            "segment2_guest": f"One of the most exciting aspects is...",
            "segment3_start": str(duration_minutes - 10),
            "segment3_end": str(duration_minutes - 5),
            "segment3_host": f"How can our listeners apply this to their work?",
            "segment3_guest": f"Here are three practical takeaways...",
            "outro_script": f"Thanks for listening to our discussion on {topic}. Don't forget to subscribe!",
            "show_notes": f"Detailed notes about {topic}",
            "link1": "https://example.com/resource1",
            "link2": "https://example.com/resource2",
            "link3": "https://example.com/resource3",
            "quote1": f"{topic} is changing the way we think about...",
            "quote2": f"The future of {topic} looks incredibly promising...",
            "series_name": "Knowledge Series",
            "category": topic,
            "segment_end_time": str(duration_minutes - 5),
            "outro_start_time": str(duration_minutes - 5)
        }
        
        return self.templates["podcast_script"].format(**podcast)


# Global instances
fetcher = ResearchPaperFetcher()
generator = ContentGenerator()

def get_content_creation_engine():
    """Get content creation engine components"""
    return {
        "fetcher": fetcher,
        "generator": generator
    }