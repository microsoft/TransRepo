import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

ERROR_DESCRIPTIONS = {
    'CS0103': 'Name does not exist in current context',
    'CS0117': 'Type does not contain definition',
    'CS0200': 'Property or indexer cannot be assigned to',
    'CS0106': 'Modifier is not valid for this item',
    'CS1061': 'Type does not contain method',
}

# Errors to ignore
IGNORE_ERRORS = ['compiling_error_CS1513', 'compiling_error_CS1026', 'compiling_error_CS1002']

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_json_data(data):
    results = []
    for entry in data['summary']:
        iteration = entry['iteration']
        error_types = entry['error_types']
        
        # Filter out ignored errors
        filtered_errors = {k: v for k, v in error_types.items() if k not in IGNORE_ERRORS}
        
        # Calculate total for proportions
        total = sum(filtered_errors.values())
        
        if total > 0:
            proportions = {k: (v / total) * 100 for k, v in filtered_errors.items()}
            results.append({
                'iteration': iteration,
                'proportions': proportions
            })
    return results

def create_plot(all_data, output_path):
    # Create subplots for each iteration
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle('Distribution of Error Types by Iteration', fontsize=16, fontweight='bold', y=1.02)
    
    # Process data for each iteration
    for iteration in range(1, 4):
        # Combine data from all models for this iteration
        combined_errors = {}
        for model_data in all_data.values():
            for entry in model_data:
                if entry['iteration'] == iteration:
                    for error_type, prop in entry['proportions'].items():
                        cleaned_error = error_type.replace('compiling_error_', '').replace('runtime_error_', '')
                        if cleaned_error in combined_errors:
                            combined_errors[cleaned_error] += prop
                        else:
                            combined_errors[cleaned_error] = prop
        
        # Average the proportions
        combined_errors = {k: v / len(all_data) for k, v in combined_errors.items()}
        
        # Get top 5 errors
        top_5_errors = dict(sorted(combined_errors.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # Sum up the rest as "Others"
        others_sum = sum(v for k, v in combined_errors.items() if k not in top_5_errors)
        if others_sum > 0:
            top_5_errors['Others'] = others_sum
        
        # Create labels with error descriptions
        labels = []
        for error in top_5_errors.keys():
            if error == 'Others':
                labels.append('Others')
            elif error == 'unknown':
                labels.append('Runtime Error')
            else:
                desc = ERROR_DESCRIPTIONS.get(error, '')
                if desc:
                    labels.append(f'{error}\n{desc}')
                else:
                    labels.append(error)
        
        # Create pie chart
        ax = axes[iteration-1]
        wedges, texts, autotexts = ax.pie(top_5_errors.values(), 
                                        labels=labels,
                                        autopct='%1.1f%%',
                                        textprops={'fontsize': 9})
        
        # Ensure percentage labels are readable
        plt.setp(autotexts, size=9, weight="bold")
        plt.setp(texts, size=9)
        
        ax.set_title(f'Iteration {iteration}', pad=20, fontsize=12, fontweight='bold')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    output_file = os.path.join(output_path, 'error_analysis_pie.png')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"Plot saved as: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Generate error analysis plot from JSON files')
    parser.add_argument('path', help='Path to the directory containing JSON files')
    args = parser.parse_args()
    
    if not os.path.isdir(args.path):
        raise ValueError(f"Directory not found: {args.path}")
    
    json_files = [f for f in os.listdir(args.path) if f.endswith('.json')]
    
    if not json_files:
        raise ValueError(f"No JSON files found in {args.path}")
    
    all_data = {}
    
    for file_name in json_files:
        file_path = os.path.join(args.path, file_name)
        try:
            data = read_json_file(file_path)
            processed_data = process_json_data(data)
            model_name = file_name.replace('.json', '')
            all_data[model_name] = processed_data
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")
    
    create_plot(all_data, args.path)

if __name__ == "__main__":
    main()
