import os
from bs4 import BeautifulSoup

def parse_coverage_report(project_path):
    """Parse JaCoCo report and display in text format"""
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

def print_summary_report(soup):
    """Print summary report"""
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
            instr = cols[2].text.strip()
            branch = cols[4].text.strip()
            lines = cols[6].text.strip()
            methods = cols[7].text.strip()
            classes = cols[8].text.strip()
            
            print(f"{element:<30} {instr:<12} {branch:<12} {lines:<12} {methods:<12} {classes:<12}")

    print("=" * 80)

def print_detailed_report(soup, report_path):
    """Print detailed report"""
    print("\nClass-level Coverage Details:")
    print("=" * 80)
    
    package_reports = []
    for link in soup.find_all('a'):
        href = link.get('href', '')
        if href.endswith('index.html') and '.' in href:
            package_path = os.path.join(os.path.dirname(report_path), href)
            package_reports.append(package_path)
    
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
                            instr = cols[2].text.strip()
                            branch = cols[4].text.strip()
                            lines = cols[6].text.strip()
                            print(f"{class_name:<40} Inst:{instr:<10} Branch:{branch:<10} Lines:{lines:<10}")
        except Exception as e:
            print(f"Error parsing package report {package_report}: {str(e)}")