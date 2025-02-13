import os
from bs4 import BeautifulSoup

def extract_percentage(text):
    """
    Convert coverage text to percentage format
    Args:
        text: Raw coverage text from HTML report
    Returns:
        Formatted percentage string
    """
    try:
        # Return directly if already contains percentage
        if '%' in text:
            return text
            
        # Return directly if n/a
        if text.lower() == 'n/a':
            return text
            
        # Handle fraction format (e.g. "561 of 653") 
        if ' of ' in text:
            numerator, denominator = map(int, text.split(' of '))
            if denominator == 0:
                return '0%'
            percentage = (numerator / denominator) * 100
            return f"{int(percentage)}%"
            
        # Handle two numbers format (e.g. "65 78")
        parts = text.strip().split()
        if len(parts) == 2 and all(p.isdigit() for p in parts):
            covered, total = map(int, parts)
            if total == 0:
                return '0%'
            percentage = (covered / total) * 100
            return f"{int(percentage)}%"
            
        # Handle single number
        if text.isdigit():
            return text + '%'
            
        return text  # Keep original text
    except:
        return text  # Return original text if parsing fails

def print_summary_report(soup):
    """
    Print coverage summary report from BeautifulSoup parsed HTML
    Args:
        soup: BeautifulSoup parsed HTML object
    """
    table = soup.find('table', class_='coverage')
    if not table:
        print("Cannot find coverage table in report")
        return

    print("\nCoverage Report Summary:")
    print("=" * 80)
    print(f"{'Element':<30} {'Instructions':<12} {'Branches':<12} {'Lines':<12} {'Methods':<12} {'Classes':<12}")
    print("-" * 80)

    rows = table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all(['td', 'th'])
        if len(cols) >= 8:
            element = cols[0].text.strip()
            instr = extract_percentage(cols[2].text.strip())
            branch = extract_percentage(cols[4].text.strip())
            lines = extract_percentage(cols[6].text.strip())
            # Handle Methods and Classes coverage which contain two numbers
            methods = extract_percentage(f"{cols[7].text.strip()} {cols[8].text.strip()}")
            classes = extract_percentage(f"{cols[9].text.strip()} {cols[10].text.strip()}")
            
            print(f"{element:<30} {instr:<12} {branch:<12} {lines:<12} {methods:<12} {classes:<12}")

    print("=" * 80)

def print_detailed_report(soup, report_path):
    """
    Print class-level coverage details
    Args:
        soup: BeautifulSoup parsed HTML object
        report_path: Path to main report file
    """
    print("\nClass-level Coverage Details:")
    print("=" * 80)
    
    # Find all package report links
    package_reports = []
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if href.endswith('index.html') and '.' in href:
            package_path = os.path.join(os.path.dirname(report_path), href)
            package_reports.append(package_path)
    
    # Parse each package report
    for package_report in package_reports:
        try:
            with open(package_report, 'r', encoding='utf-8') as f:
                package_soup = BeautifulSoup(f, 'html.parser')
                package_table = package_soup.find('table', class_='coverage')
                if package_table:
                    rows = package_table.find_all('tr')[1:]
                    for row in rows:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 8:
                            class_name = cols[0].text.strip()
                            instr = extract_percentage(cols[2].text.strip())
                            branch = extract_percentage(cols[4].text.strip())
                            lines = extract_percentage(cols[6].text.strip())
                            print(f"{class_name:<40} Inst:{instr:<10} Branch:{branch:<10} Lines:{lines:<10}")
        except Exception as e:
            print(f"Error parsing package report {package_report}: {str(e)}")

def parse_coverage_report(project_path):
    """
    Main function to parse JaCoCo coverage report
    Args:
        project_path: Path to project root directory
    Returns:
        True if parsing successful, None if failed
    """
    report_path = os.path.join(project_path, 'target', 'site', 'jacoco', 'index.html')
    if not os.path.exists(report_path):
        print("Coverage report not found")
        return None
    
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        print_summary_report(soup)
        print_detailed_report(soup, report_path)
        return True

    except Exception as e:
        print(f"Error parsing coverage report: {str(e)}")
        return None