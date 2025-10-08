import requests
import sys
import json
import os
from datetime import datetime
from pathlib import Path

class GrowthCopilotAPITester:
    def __init__(self, base_url="https://saas-copilot.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def test_api_health(self):
        """Test basic API connectivity"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                details += f", Response: {response.json()}"
            self.log_test("API Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("API Health Check", False, str(e))
            return False

    def test_mixpanel_upload(self):
        """Test Mixpanel CSV upload"""
        try:
            # Use sample data
            sample_file = Path("/app/sample_data/mixpanel_sample.csv")
            if not sample_file.exists():
                self.log_test("Mixpanel Upload", False, "Sample file not found")
                return False
            
            with open(sample_file, 'rb') as f:
                files = {'file': ('mixpanel_sample.csv', f, 'text/csv')}
                response = requests.post(f"{self.api_url}/upload/mixpanel", files=files, timeout=30)
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Records: {data.get('record_count', 'N/A')}"
            else:
                details += f", Error: {response.text}"
            
            self.log_test("Mixpanel Upload", success, details)
            return success, response.json() if success else None
        except Exception as e:
            self.log_test("Mixpanel Upload", False, str(e))
            return False, None

    def test_moengage_upload(self):
        """Test MoEngage JSON upload"""
        try:
            sample_file = Path("/app/sample_data/moengage_sample.json")
            if not sample_file.exists():
                self.log_test("MoEngage Upload", False, "Sample file not found")
                return False
            
            with open(sample_file, 'rb') as f:
                files = {'file': ('moengage_sample.json', f, 'application/json')}
                response = requests.post(f"{self.api_url}/upload/moengage", files=files, timeout=30)
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Records: {data.get('record_count', 'N/A')}"
            else:
                details += f", Error: {response.text}"
            
            self.log_test("MoEngage Upload", success, details)
            return success
        except Exception as e:
            self.log_test("MoEngage Upload", False, str(e))
            return False

    def test_jira_upload(self):
        """Test Jira CSV upload"""
        try:
            sample_file = Path("/app/sample_data/jira_sample.csv")
            if not sample_file.exists():
                self.log_test("Jira Upload", False, "Sample file not found")
                return False
            
            with open(sample_file, 'rb') as f:
                files = {'file': ('jira_sample.csv', f, 'text/csv')}
                response = requests.post(f"{self.api_url}/upload/jira", files=files, timeout=30)
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Records: {data.get('record_count', 'N/A')}"
            else:
                details += f", Error: {response.text}"
            
            self.log_test("Jira Upload", success, details)
            return success
        except Exception as e:
            self.log_test("Jira Upload", False, str(e))
            return False

    def test_get_metrics(self):
        """Test getting metric anomalies"""
        try:
            response = requests.get(f"{self.api_url}/metrics", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                metrics = response.json()
                details += f", Anomalies found: {len(metrics)}"
                # Check if we have expected anomalies from sample data
                if len(metrics) > 0:
                    details += f", First metric: {metrics[0].get('metric_name', 'N/A')}"
                return success, metrics
            else:
                details += f", Error: {response.text}"
                self.log_test("Get Metrics", success, details)
                return success, []
            
        except Exception as e:
            self.log_test("Get Metrics", False, str(e))
            return False, []

    def test_ai_analysis(self, anomaly_id):
        """Test AI analysis for a metric anomaly"""
        try:
            response = requests.post(f"{self.api_url}/analyze/{anomaly_id}", timeout=60)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                insight = response.json()
                details += f", Insight generated for: {insight.get('metric', 'N/A')}"
                self.log_test("AI Analysis", success, details)
                return success, insight
            else:
                details += f", Error: {response.text}"
                self.log_test("AI Analysis", success, details)
                return success, None
            
        except Exception as e:
            self.log_test("AI Analysis", False, str(e))
            return False, None

    def test_get_insights(self):
        """Test getting AI insights"""
        try:
            response = requests.get(f"{self.api_url}/insights", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                insights = response.json()
                details += f", Insights found: {len(insights)}"
                self.log_test("Get Insights", success, details)
                return success, insights
            else:
                details += f", Error: {response.text}"
                self.log_test("Get Insights", success, details)
                return success, []
            
        except Exception as e:
            self.log_test("Get Insights", False, str(e))
            return False, []

    def test_trigger_action(self, insight_id, metric, action_type):
        """Test triggering an action"""
        try:
            payload = {
                "insight_id": insight_id,
                "metric": metric,
                "action_type": action_type
            }
            response = requests.post(f"{self.api_url}/action/trigger", json=payload, timeout=30)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Action: {action_type}"
            
            if success:
                action_log = response.json()
                details += f", Status: {action_log.get('status', 'N/A')}"
                self.log_test(f"Trigger {action_type.title()} Action", success, details)
                return success, action_log
            else:
                details += f", Error: {response.text}"
                self.log_test(f"Trigger {action_type.title()} Action", success, details)
                return success, None
            
        except Exception as e:
            self.log_test(f"Trigger {action_type.title()} Action", False, str(e))
            return False, None

    def test_get_action_logs(self):
        """Test getting action logs"""
        try:
            response = requests.get(f"{self.api_url}/action-logs", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                logs = response.json()
                details += f", Action logs found: {len(logs)}"
                self.log_test("Get Action Logs", success, details)
                return success, logs
            else:
                details += f", Error: {response.text}"
                self.log_test("Get Action Logs", success, details)
                return success, []
            
        except Exception as e:
            self.log_test("Get Action Logs", False, str(e))
            return False, []

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🚀 Starting Growth Copilot API Tests")
        print(f"🔗 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Test 1: API Health
        if not self.test_api_health():
            print("❌ API is not accessible. Stopping tests.")
            return False
        
        # Test 2: File Uploads
        mixpanel_success, mixpanel_data = self.test_mixpanel_upload()
        moengage_success = self.test_moengage_upload()
        jira_success = self.test_jira_upload()
        
        # Test 3: Get Metrics (should have anomalies after Mixpanel upload)
        metrics_success, metrics = self.test_get_metrics()
        if metrics_success and len(metrics) > 0:
            self.log_test("Anomaly Detection", True, f"Found {len(metrics)} anomalies")
        else:
            self.log_test("Anomaly Detection", False, "No anomalies detected from sample data")
        
        # Test 4: AI Analysis (if we have metrics)
        insight_generated = False
        if metrics_success and len(metrics) > 0:
            first_metric = metrics[0]
            ai_success, insight = self.test_ai_analysis(first_metric['id'])
            if ai_success and insight:
                insight_generated = True
                
                # Test 5: Trigger Actions (if we have insights)
                self.test_trigger_action(insight['id'], insight['metric'], 'moengage')
                self.test_trigger_action(insight['id'], insight['metric'], 'jira')
        
        # Test 6: Get Insights
        self.test_get_insights()
        
        # Test 7: Get Action Logs
        self.test_get_action_logs()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        print(f"✅ Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    tester = GrowthCopilotAPITester()
    success = tester.run_comprehensive_test()
    
    # Save detailed results
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": tester.tests_run,
        "passed_tests": tester.tests_passed,
        "success_rate": (tester.tests_passed/tester.tests_run)*100 if tester.tests_run > 0 else 0,
        "test_details": tester.test_results
    }
    
    with open("/app/backend_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())