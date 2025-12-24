import argparse
import json
import logging
import sys
from typing import Optional


from core.metadata import read_metadata
from core.execution import run_pandas_code
from core.visualization import generate_chartjs
from core.error_handling import ErrorType, handle_exception

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



def read_metadata_cli(file_path: str, output_path: Optional[str] = None) -> None:
    """CLI wrapper for read_metadata functionality."""
    try:
        result = read_metadata(file_path)
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Result saved to {output_path}")
        else:
            print(json.dumps(result, indent=2))
    except Exception as e:
        error = handle_exception(e, ErrorType.TOOL_EXECUTION_ERROR, "read_metadata_cli failed")
        print(f"Error: {error['message']}", file=sys.stderr)
        sys.exit(1)    
       

def run_pandas_code_cli(script_path: str, output_path: Optional[str] = None) -> None:
    """CLI wrapper for run_pandas_code functionality."""
    try:
        with open(script_path, 'r') as f:
            code = f.read()
        result = run_pandas_code(code)
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Result saved to {output_path}")
        else:
            print(json.dumps(result, indent=2))
    except FileNotFoundError:
        error = handle_exception(
            FileNotFoundError(f"Script file not found: {script_path}"),
            ErrorType.FILE_NOT_FOUND,
            "run_pandas_code_cli failed"
        )
        print(f"Error: {error['message']}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error = handle_exception(e, ErrorType.TOOL_EXECUTION_ERROR, "run_pandas_code_cli failed")
        print(f"Error: {error['message']}", file=sys.stderr)
        sys.exit(1)
       
def generate_chart_cli(
    data_path: str,
    chart_type: str = "bar",
    title: str = "Data Visualization",
    output_path: str = None
) -> None:
    """CLI wrapper for generate_chartjs functionality."""
    try:
        with open(data_path, 'r') as f:
            data = json.load(f)
        result = generate_chartjs(data, [chart_type], title)
        if output_path:
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Result saved to {output_path}")
        else:
            print(json.dumps(result, indent=2))
    except FileNotFoundError:
        error = handle_exception(
            FileNotFoundError(f"Data file not found: {data_path}"),
            ErrorType.FILE_NOT_FOUND,
            "generate_chart_cli failed"
        )
        print(f"Error: {error['message']}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error = handle_exception(e, ErrorType.TOOL_EXECUTION_ERROR, "generate_chart_cli failed")
        print(f"Error: {error['message']}", file=sys.stderr)
        sys.exit(1)
       
def interactive_mode():
    """Run in interactive menu-driven mode."""
    print("\nExcel Data Processing Tool")
    print("------------------------")
    
    while True:
        print("\nMain Menu:")
        print("1. Read file metadata")
        print("2. Execute pandas code")
        print("3. Generate chart")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            file_path = input("Enter file path (Excel/CSV): ").strip('"\'')
            output = input("Output file (leave blank for console): ").strip('"\'')
            try:
                read_metadata_cli(file_path, output)
            except Exception as e:
                error = handle_exception(e, ErrorType.TOOL_EXECUTION_ERROR, "Interactive metadata read failed")
                print(f"Error: {error['message']}", file=sys.stderr)
            
        elif choice == "2":
            file_path = input("Enter Python script path: ").strip('"\'')
            output = input("Output file (leave blank for console): ").strip('"\'')
            try:
                run_pandas_code_cli(file_path, output)
            except Exception as e:
                error = handle_exception(e, ErrorType.TOOL_EXECUTION_ERROR, "Interactive code execution failed")
                print(f"Error: {error['message']}", file=sys.stderr)
            
        elif choice == "3":
            file_path = input("Enter JSON data file path: ").strip('"\'')
            chart_type = input("Chart type (bar/line/pie) [bar]: ").strip('"\'') or "bar"
            title = input("Chart title [Data Visualization]: ").strip('"\'') or "Data Visualization"
            output = input("Output HTML file (leave blank for console): ").strip('"\'')
            try:
                if chart_type not in ['bar', 'line', 'pie']:
                    print("Invalid chart type. Must be one of: bar, line, pie")
                    continue
                generate_chart_cli(file_path, chart_type, title, output)
            except Exception as e:
                error = handle_exception(e, ErrorType.TOOL_EXECUTION_ERROR, "Interactive chart generation failed")
                print(f"Error: {error['message']}", file=sys.stderr)
            
        elif choice == "4":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice, please try again")

def main():
    # Check if running in interactive mode (no args)
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        # Original command-line mode
        parser = argparse.ArgumentParser(
            description="Excel Data Processing CLI Tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""Examples:
  # Read metadata from Excel file
  python cli.py metadata data.xlsx
  
  # Execute pandas code
  python cli.py execute script.py
  
  # Generate bar chart
  python cli.py chart data.json --type bar --title "Sales Data"
  
  # Interactive mode
  python cli.py
"""
        )
        
        subparsers = parser.add_subparsers(dest='command')
        
        # Metadata command
        meta_parser = subparsers.add_parser('metadata', help='Read metadata from Excel/CSV file')
        meta_parser.add_argument('file', help='Path to Excel/CSV file')
        meta_parser.add_argument('-o', '--output', help='Output file path (optional)')
        
        # Execute command
        exec_parser = subparsers.add_parser('execute', help='Execute pandas code from file')
        exec_parser.add_argument('file', help='Path to Python script with pandas code')
        exec_parser.add_argument('-o', '--output', help='Output file path (optional)')
        
        # Chart command
        chart_parser = subparsers.add_parser('chart', help='Generate chart from JSON data')
        chart_parser.add_argument('file', help='Path to JSON data file')
        chart_parser.add_argument('-t', '--type', choices=['bar', 'line', 'pie'],
                                default='bar', help='Chart type (default: bar)')
        chart_parser.add_argument('--title', default='Data Visualization',
                                help='Chart title (default: "Data Visualization")')
        chart_parser.add_argument('-o', '--output', help='Output HTML file path (optional)')
        
        args = parser.parse_args()
        
        if not hasattr(args, 'command'):
            interactive_mode()
        elif args.command == 'metadata':
            read_metadata_cli(args.file, args.output)
        elif args.command == 'execute':
            run_pandas_code_cli(args.file, args.output)
        elif args.command == 'chart':
            generate_chart_cli(args.file, args.type, args.title, args.output)

if __name__ == "__main__":
    main()