#!/usr/bin/python3

import argparse
import json
import re

def analyze_errors(log_file, output_format):
    error_count = 0
    errors = []
    with open(log_file, 'r') as file:
        for line in file:
            if "error" in line.lower():
                error_count += 1
                errors.append(line)
    if output_format == "json":
        return {"error_count": error_count, "errors": errors}
    else:
        error_messages = "".join(errors)
        return f"\nERROR COUNT: {error_count} \n\nERRORS:\n{error_messages}"


def analyze_user_activity(log_file, output_format):
    user_activity_count = 0
    user_activity = {
        "logins": [],
        "logouts": [],
        "other": []
    }

    with open(log_file, 'r') as file:
        for line in file:
            if "user" in line.lower() and "error" not in line.lower() and "performance" not in line.lower():
                user_activity_count += 1
                if "login" in line.lower():
                    user_activity["logins"].append(line)
                elif "logout" in line.lower():
                    user_activity["logouts"].append(line)
                else:
                    user_activity["other"].append(line)

    if output_format == "json":
        return {"user_activity_count": user_activity_count, "user_activity": user_activity, "login_count": len(user_activity["logins"]), "logout_count": len(user_activity["logouts"]), "other_count": len(user_activity["other"])}
    else:
        login_messages = "".join(user_activity["logins"])
        logout_messages = "".join(user_activity["logouts"])
        other_messages = "".join(user_activity["other"])
        return f"\nUSER ACTIVITY COUNT: {user_activity_count} \n\nLOGIN COUNT: {len(user_activity['logins'])}\n{login_messages}\n\nLOGOUT COUNT: {len(user_activity['logouts'])}\n{logout_messages}\n\nOTHER COUNT: {len(user_activity['other'])}\n{other_messages}"


def analyze_performance(log_file, output_format, metric=None):
    response_times = []
    data = []
    metric_data = []
    metric_response_times = []

    with open(log_file, 'r') as file:
        for line in file:
            if "error" not in line.lower() and "ms" in line.lower():
                if metric and metric in line.lower():
                    metric_data.append(line)
                elif not metric:
                    data.append(line)
                
                match = re.search(r'(\d+)\s*ms', line)
                if match:
                    number_before_ms = int(match.group(1))
                    if metric and metric in line.lower():
                        metric_response_times.append(number_before_ms)
                    elif not metric:
                        response_times.append(number_before_ms)

    results = {
        "metric": None,
        "data": [],
        "average_response_time": 0,
        "min_response_time": 0,
        "max_response_time": 0
    }
    if metric:
        results["metric"] = metric 
        results["data"] = metric_data
        if metric_response_times:
            results["average_response_time"] = sum(metric_response_times) / len(metric_response_times)
            results["min_response_time"] = min(metric_response_times) if metric_response_times else 0
            results["max_response_time"] = max(metric_response_times) if metric_response_times else 0
            
    else:
        results["data"] = data
        if response_times:
            results["average_response_time"] = sum(response_times) / len(response_times)
            results["min_response_time"] = min(response_times) if response_times else 0
            results["max_response_time"] = max(response_times) if response_times else 0

    if output_format == "json":
        return json.dumps(results, indent=4)
    else:
        if metric:
            data_str = "".join(metric_data)
            return f"\nMETRIC: {metric}\n\nDATA:\n{data_str}\n\nAVERAGE RESPONSE TIME: {results['average_response_time']} ms\nMIN RESPONSE TIME: {results['min_response_time']} ms\nMAX RESPONSE TIME: {results['max_response_time']} ms"
        else:
            data_str = "".join(data)
            return f"\nDATA:\n{data_str}\n\nAVERAGE RESPONSE TIME: {results['average_response_time']} ms\nMIN RESPONSE TIME: {results['min_response_time']} ms\nMAX RESPONSE TIME: {results['max_response_time']} ms"


def main():
    parser = argparse.ArgumentParser(description="Log File Analyzer")
    parser.add_argument("--log_file", type=str, required=True, help="Path to the log file")
    parser.add_argument("--analysis_type", choices=["errors", "user_activity", "performance"], required=True, help="Type of analysis to perform")
    parser.add_argument("--output_format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--metric", type=str, help="Performance metric to analyze, e.g., 'Page Load'. Must be used with --analysis_type performance")

    args = parser.parse_args()

    if args.analysis_type == "errors":
        result = analyze_errors(args.log_file, args.output_format)
    elif args.analysis_type == "user_activity":
        result = analyze_user_activity(args.log_file, args.output_format)
    elif args.analysis_type == "performance":
        result = analyze_performance(args.log_file, args.output_format, args.metric)

    print(result)

if __name__ == "__main__":
    main()