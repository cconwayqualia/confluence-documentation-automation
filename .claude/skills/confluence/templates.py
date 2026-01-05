"""
Confluence Storage Format Templates

This module provides template functions for generating Confluence documentation pages.
All functions return HTML/XML content in Confluence Storage Format.
"""

import html
from typing import List, Dict, Any, Optional
from datetime import datetime


def escape_html(text: str) -> str:
    """Escape HTML special characters"""
    return html.escape(str(text))


def escape_cdata(text: str) -> str:
    """
    Escape CDATA end sequences in code content
    CDATA sections cannot contain ]]> so we replace it with ]]&gt;
    """
    return str(text).replace(']]>', ']]&gt;')


def code_block(
    code: str,
    language: str = 'text',
    title: Optional[str] = None,
    line_numbers: bool = True
) -> str:
    """
    Generate a Confluence code block macro

    Args:
        code: The code content
        language: Programming language for syntax highlighting
        title: Optional title for the code block
        line_numbers: Whether to show line numbers

    Returns:
        Confluence Storage Format code macro
    """
    code_escaped = escape_cdata(code)

    title_param = f'<ac:parameter ac:name="title">{escape_html(title)}</ac:parameter>' if title else ''
    linenumbers_param = '<ac:parameter ac:name="linenumbers">true</ac:parameter>' if line_numbers else ''

    return f'''<ac:structured-macro ac:name="code" ac:schema-version="1">
  <ac:parameter ac:name="language">{escape_html(language)}</ac:parameter>
  {linenumbers_param}
  {title_param}
  <ac:plain-text-body><![CDATA[{code_escaped}]]></ac:plain-text-body>
</ac:structured-macro>'''


def info_panel(content: str, panel_type: str = 'info') -> str:
    """
    Generate a Confluence info/warning/note panel

    Args:
        content: Panel content (can include HTML)
        panel_type: Type of panel (info, warning, note, tip)

    Returns:
        Confluence Storage Format panel macro
    """
    return f'''<ac:structured-macro ac:name="{panel_type}" ac:schema-version="1">
  <ac:rich-text-body>
    <p>{content}</p>
  </ac:rich-text-body>
</ac:structured-macro>'''


def metadata_table(metadata: Dict[str, str]) -> str:
    """
    Generate a metadata table (key-value pairs)

    Args:
        metadata: Dictionary of metadata key-value pairs

    Returns:
        HTML table with metadata
    """
    rows = []
    for key, value in metadata.items():
        rows.append(f'''<tr>
      <th>{escape_html(key)}</th>
      <td>{escape_html(value)}</td>
    </tr>''')

    return f'''<table>
  <tbody>
    {''.join(rows)}
  </tbody>
</table>'''


def dependency_table(dependencies: List[Dict[str, str]]) -> str:
    """
    Generate a dependencies table

    Args:
        dependencies: List of dicts with 'name' and 'version' keys

    Returns:
        HTML table with dependencies
    """
    if not dependencies:
        return '<p><em>No dependencies found</em></p>'

    rows = []
    for dep in dependencies:
        name = dep.get('name', 'Unknown')
        version = dep.get('version', 'N/A')
        rows.append(f'''<tr>
      <td><strong>{escape_html(name)}</strong></td>
      <td>{escape_html(version)}</td>
    </tr>''')

    return f'''<table>
  <thead>
    <tr>
      <th>Package</th>
      <th>Version</th>
    </tr>
  </thead>
  <tbody>
    {''.join(rows)}
  </tbody>
</table>'''


def table_of_contents() -> str:
    """Generate a table of contents macro"""
    return '<ac:structured-macro ac:name="toc" ac:schema-version="1"/>'


def project_overview_template(
    name: str,
    description: str,
    tech_stack: List[str],
    metadata: Dict[str, str],
    quick_start: List[str],
    child_pages: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Generate the project overview page (parent page)

    Args:
        name: Project name
        description: Project description
        tech_stack: List of technologies used
        metadata: Dict of project metadata (version, license, etc.)
        quick_start: List of quick start steps
        child_pages: List of dicts with 'title' and 'url' keys for child pages

    Returns:
        Complete HTML page content
    """
    # Technology stack list
    tech_items = ''.join([f'<li>{escape_html(tech)}</li>' for tech in tech_stack])
    tech_stack_html = f'<ul>{tech_items}</ul>' if tech_items else '<p><em>Not specified</em></p>'

    # Quick start steps
    quick_start_items = ''.join([f'<li>{escape_html(step)}</li>' for step in quick_start])
    quick_start_html = f'<ol>{quick_start_items}</ol>' if quick_start_items else '<p><em>See setup documentation</em></p>'

    # Child pages navigation
    if child_pages:
        child_links = []
        for page in child_pages:
            title = escape_html(page.get('title', 'Untitled'))
            url = page.get('url', '#')
            child_links.append(f'<li><a href="{url}">{title}</a></li>')
        child_pages_html = f'''<h2>Documentation Sections</h2>
<ul>
{''.join(child_links)}
</ul>'''
    else:
        child_pages_html = ''

    # Auto-generation notice
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    notice = info_panel(
        f'This documentation was automatically generated on {timestamp} by Claude Code. '
        'Please review and update as needed.',
        'info'
    )

    return f'''<h2>Overview</h2>
<p>{escape_html(description)}</p>

<h2>Project Information</h2>
{metadata_table(metadata)}

<h2>Technology Stack</h2>
{tech_stack_html}

<h2>Quick Start</h2>
{quick_start_html}

{child_pages_html}

{notice}
'''


def architecture_overview_template(
    description: str,
    components: List[str],
    design_patterns: List[str],
    data_flow: str
) -> str:
    """
    Generate the architecture overview page

    Args:
        description: High-level architecture description
        components: List of system components
        design_patterns: List of design patterns used
        data_flow: Description of data flow through the system

    Returns:
        Complete HTML page content
    """
    # Components list
    component_items = ''.join([f'<li>{escape_html(comp)}</li>' for comp in components])
    components_html = f'<ul>{component_items}</ul>' if component_items else '<p><em>No major components identified</em></p>'

    # Design patterns
    pattern_items = ''.join([f'<li>{escape_html(pattern)}</li>' for pattern in design_patterns])
    patterns_html = f'<ul>{pattern_items}</ul>' if pattern_items else '<p><em>No specific patterns identified</em></p>'

    return f'''<h2>Architecture Description</h2>
<p>{escape_html(description)}</p>

<h2>System Components</h2>
{components_html}

<h2>Design Patterns</h2>
{patterns_html}

<h2>Data Flow</h2>
<p>{escape_html(data_flow)}</p>

{info_panel('This architecture documentation was automatically generated. Consider adding diagrams or detailed sequence flows for complex interactions.', 'tip')}
'''


def dependencies_template(
    prod_deps: List[Dict[str, str]],
    dev_deps: List[Dict[str, str]],
    notes: str = ''
) -> str:
    """
    Generate the dependencies page

    Args:
        prod_deps: List of production dependencies
        dev_deps: List of development dependencies
        notes: Additional notes about dependencies

    Returns:
        Complete HTML page content
    """
    notes_html = f'<p>{escape_html(notes)}</p>' if notes else ''

    warning = info_panel(
        'Always review dependencies for security vulnerabilities. '
        'Use tools like npm audit, pip-audit, or dependabot to stay updated.',
        'warning'
    )

    return f'''<h2>Production Dependencies</h2>
{dependency_table(prod_deps)}

<h2>Development Dependencies</h2>
{dependency_table(dev_deps)}

{notes_html}

{warning}
'''


def setup_installation_template(
    prerequisites: List[str],
    steps: List[str],
    config_examples: Dict[str, str],
    verification: List[str],
    troubleshooting: str = ''
) -> str:
    """
    Generate the setup and installation page

    Args:
        prerequisites: List of prerequisites (software, versions, etc.)
        steps: List of installation steps
        config_examples: Dict of config file names to example content
        verification: List of verification steps
        troubleshooting: Troubleshooting tips

    Returns:
        Complete HTML page content
    """
    # Prerequisites
    prereq_items = ''.join([f'<li>{escape_html(prereq)}</li>' for prereq in prerequisites])
    prereq_html = f'<ul>{prereq_items}</ul>' if prereq_items else '<p><em>No specific prerequisites</em></p>'

    # Installation steps
    step_items = ''.join([f'<li>{escape_html(step)}</li>' for step in steps])
    steps_html = f'<ol>{step_items}</ol>' if step_items else '<p><em>No installation steps documented</em></p>'

    # Configuration examples
    config_html = ''
    for filename, content in config_examples.items():
        # Detect language from filename
        if filename.endswith('.js') or filename.endswith('.json'):
            lang = 'javascript'
        elif filename.endswith('.py'):
            lang = 'python'
        elif filename.endswith(('.yml', '.yaml')):
            lang = 'yaml'
        elif filename.endswith('.toml'):
            lang = 'toml'
        elif filename.endswith('.xml'):
            lang = 'xml'
        elif filename.endswith('.env'):
            lang = 'bash'
        else:
            lang = 'text'

        config_html += f'<h3>{escape_html(filename)}</h3>\n{code_block(content, lang, filename)}\n'

    # Verification steps
    verify_items = ''.join([f'<li>{escape_html(step)}</li>' for step in verification])
    verify_html = f'<ol>{verify_items}</ol>' if verify_items else '<p><em>No verification steps specified</em></p>'

    # Troubleshooting
    troubleshooting_html = ''
    if troubleshooting:
        troubleshooting_html = f'''<h2>Troubleshooting</h2>
{info_panel(escape_html(troubleshooting), 'note')}'''

    return f'''<h2>Prerequisites</h2>
{prereq_html}

<h2>Installation Steps</h2>
{steps_html}

<h2>Configuration</h2>
{config_html if config_html else '<p><em>No configuration examples available</em></p>'}

<h2>Verification</h2>
<p>After installation, verify everything is working correctly:</p>
{verify_html}

{troubleshooting_html}
'''


def project_structure_template(
    directory_tree: str,
    directory_descriptions: Dict[str, str],
    file_conventions: str = ''
) -> str:
    """
    Generate the project structure page

    Args:
        directory_tree: ASCII tree representation of directory structure
        directory_descriptions: Dict mapping directory paths to descriptions
        file_conventions: Description of file naming conventions

    Returns:
        Complete HTML page content
    """
    # Directory tree
    tree_html = code_block(directory_tree, 'text', 'Project Directory Structure', False)

    # Directory descriptions
    desc_html = ''
    if directory_descriptions:
        desc_items = []
        for path, description in directory_descriptions.items():
            desc_items.append(f'''<tr>
      <td><code>{escape_html(path)}</code></td>
      <td>{escape_html(description)}</td>
    </tr>''')

        desc_html = f'''<h2>Directory Descriptions</h2>
<table>
  <thead>
    <tr>
      <th>Directory</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    {''.join(desc_items)}
  </tbody>
</table>'''

    # File conventions
    conventions_html = ''
    if file_conventions:
        conventions_html = f'''<h2>File Naming Conventions</h2>
<p>{escape_html(file_conventions)}</p>'''

    return f'''<h2>Project Structure</h2>
{tree_html}

{desc_html}

{conventions_html}
'''


def key_files_template(files: List[Dict[str, Any]]) -> str:
    """
    Generate the key files reference page

    Args:
        files: List of dicts with keys:
            - path: File path
            - type: File type (entry point, config, build, etc.)
            - description: File description
            - code_sample: Optional code sample from the file

    Returns:
        Complete HTML page content
    """
    if not files:
        return '<p><em>No key files identified</em></p>'

    files_html = ''
    for file_info in files:
        path = file_info.get('path', 'Unknown')
        file_type = file_info.get('type', 'File')
        description = file_info.get('description', 'No description available')
        code_sample = file_info.get('code_sample', '')

        # Detect language from file extension
        if path.endswith('.js'):
            lang = 'javascript'
        elif path.endswith('.ts'):
            lang = 'typescript'
        elif path.endswith('.py'):
            lang = 'python'
        elif path.endswith('.go'):
            lang = 'go'
        elif path.endswith('.java'):
            lang = 'java'
        elif path.endswith('.rs'):
            lang = 'rust'
        elif path.endswith('.rb'):
            lang = 'ruby'
        elif path.endswith('.php'):
            lang = 'php'
        elif path.endswith(('.c', '.cpp', '.h', '.hpp')):
            lang = 'cpp'
        elif path.endswith('.cs'):
            lang = 'csharp'
        elif path.endswith(('.yml', '.yaml')):
            lang = 'yaml'
        elif path.endswith('.json'):
            lang = 'json'
        elif path.endswith('.xml'):
            lang = 'xml'
        elif path.endswith('.toml'):
            lang = 'toml'
        elif path.endswith('.sh'):
            lang = 'bash'
        elif path.endswith(('.dockerfile', 'Dockerfile')):
            lang = 'dockerfile'
        else:
            lang = 'text'

        code_html = ''
        if code_sample:
            # Limit code sample length
            lines = code_sample.split('\n')
            if len(lines) > 100:
                code_sample = '\n'.join(lines[:100]) + '\n\n... (truncated)'

            code_html = code_block(code_sample, lang, path)

        files_html += f'''<h2><code>{escape_html(path)}</code></h2>
<p><strong>Type:</strong> {escape_html(file_type)}</p>
<p>{escape_html(description)}</p>
{code_html}
<hr />
'''

    return files_html


def generate_timestamp() -> str:
    """Generate a formatted timestamp for auto-generated content"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def jira_ticket_panel(
    issue_key: str,
    summary: str,
    status: str,
    issue_type: str,
    priority: str,
    assignee: str,
    jira_url: str
) -> str:
    """
    Generate a Jira ticket information panel

    Args:
        issue_key: Jira issue key (e.g., PROJ-123)
        summary: Issue summary/title
        status: Issue status
        issue_type: Type of issue (Bug, Story, Task, etc.)
        priority: Issue priority
        assignee: Assignee name
        jira_url: Full URL to the Jira issue

    Returns:
        Confluence Storage Format panel with ticket info
    """
    ticket_info = f'''<table>
  <tbody>
    <tr>
      <th>Ticket</th>
      <td><a href="{jira_url}">{escape_html(issue_key)}</a></td>
    </tr>
    <tr>
      <th>Summary</th>
      <td>{escape_html(summary)}</td>
    </tr>
    <tr>
      <th>Type</th>
      <td>{escape_html(issue_type)}</td>
    </tr>
    <tr>
      <th>Status</th>
      <td><strong>{escape_html(status)}</strong></td>
    </tr>
    <tr>
      <th>Priority</th>
      <td>{escape_html(priority)}</td>
    </tr>
    <tr>
      <th>Assignee</th>
      <td>{escape_html(assignee)}</td>
    </tr>
  </tbody>
</table>'''

    return info_panel(ticket_info, 'info')


def work_session_template(
    task_name: str,
    overview: str,
    actions_done: List[str],
    files_involved: List[Dict[str, str]],
    code_snippets: List[Dict[str, str]],
    commands_run: List[str],
    how_to_recreate: List[str],
    notes: str = '',
    errors_encountered: str = '',
    jira_info: Optional[Dict[str, str]] = None,
    documented_by: str = 'Claude Code'
) -> str:
    """
    Generate a work session documentation page (for ticket/task mode)

    Args:
        task_name: Name of the task
        overview: Brief summary of what this work session was about
        actions_done: List of actions performed
        files_involved: List of dicts with 'path' and 'description' keys
        code_snippets: List of dicts with 'code', 'language', and optional 'title' keys
        commands_run: List of bash commands executed
        how_to_recreate: Step-by-step recreation instructions
        notes: Additional notes or context
        errors_encountered: Description of errors and how they were solved
        jira_info: Optional dict with Jira ticket information (issue_key, summary, status, etc.)
        documented_by: Who documented this (default: Claude Code)

    Returns:
        Complete HTML page content for work session documentation
    """
    timestamp = generate_timestamp()

    # Jira ticket panel (if provided)
    jira_html = ''
    if jira_info:
        jira_html = f'''<h2>Jira Ticket</h2>
{jira_ticket_panel(
    jira_info.get('key', ''),
    jira_info.get('summary', ''),
    jira_info.get('status', ''),
    jira_info.get('issue_type', ''),
    jira_info.get('priority', ''),
    jira_info.get('assignee', ''),
    jira_info.get('url', '')
)}
'''

    # Overview
    overview_html = f'<p>{escape_html(overview)}</p>'

    # Actions done
    actions_items = ''.join([f'<li>{escape_html(action)}</li>' for action in actions_done])
    actions_html = f'<ul>{actions_items}</ul>' if actions_items else '<p><em>No actions documented</em></p>'

    # Files involved
    files_html = ''
    if files_involved:
        file_items = []
        for file_info in files_involved:
            path = file_info.get('path', 'Unknown')
            description = file_info.get('description', 'Modified')
            file_items.append(f'<li><code>{escape_html(path)}</code> - {escape_html(description)}</li>')
        files_html = f'<ul>{"".join(file_items)}</ul>'
    else:
        files_html = '<p><em>No files documented</em></p>'

    # Code snippets
    code_html = ''
    if code_snippets:
        for snippet in code_snippets:
            code = snippet.get('code', '')
            language = snippet.get('language', 'text')
            title = snippet.get('title', None)
            if code:
                code_html += code_block(code, language, title) + '\n'
    else:
        code_html = '<p><em>No code snippets</em></p>'

    # Commands run
    commands_html = ''
    if commands_run:
        all_commands = '\n'.join(commands_run)
        commands_html = code_block(all_commands, 'bash', 'Commands Executed')
    else:
        commands_html = '<p><em>No commands documented</em></p>'

    # How to recreate
    recreate_items = ''.join([f'<li>{escape_html(step)}</li>' for step in how_to_recreate])
    recreate_html = f'<ol>{recreate_items}</ol>' if recreate_items else '<p><em>No recreation steps provided</em></p>'

    # Errors encountered
    errors_html = ''
    if errors_encountered:
        errors_html = f'''<h2>Errors Encountered</h2>
{info_panel(escape_html(errors_encountered), 'warning')}
'''

    # Notes
    notes_html = ''
    if notes:
        notes_html = f'''<h2>Notes</h2>
<p>{escape_html(notes)}</p>
'''

    # Footer
    footer = f'<p><em>Documented by: {escape_html(documented_by)} on {timestamp}</em></p>'

    return f'''{jira_html}
<h2>Overview</h2>
{overview_html}

<h2>What Was Done</h2>
{actions_html}

<h2>Key Files</h2>
{files_html}

<h2>Code/Scripts</h2>
{code_html}

<h2>Commands Run</h2>
{commands_html}

<h2>How to Recreate</h2>
{recreate_html}

{errors_html}

{notes_html}

{footer}
'''
