import { useState, useEffect } from "react";
import axios from "axios";
import { Upload, TrendingUp, TrendingDown, AlertCircle, Activity, CheckCircle2, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import FileUpload from "@/components/FileUpload";
import MetricCard from "@/components/MetricCard";
import InsightPanel from "@/components/InsightPanel";
import ActionLogsPanel from "@/components/ActionLogsPanel";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const [metrics, setMetrics] = useState([]);
  const [insights, setInsights] = useState([]);
  const [actionLogs, setActionLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTab, setSelectedTab] = useState("overview");

  useEffect(() => {
    fetchMetrics();
    fetchInsights();
    fetchActionLogs();
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await axios.get(`${API}/metrics`);
      setMetrics(response.data);
    } catch (error) {
      console.error("Error fetching metrics:", error);
    }
  };

  const fetchInsights = async () => {
    try {
      const response = await axios.get(`${API}/insights`);
      setInsights(response.data);
    } catch (error) {
      console.error("Error fetching insights:", error);
    }
  };

  const fetchActionLogs = async () => {
    try {
      const response = await axios.get(`${API}/action-logs`);
      setActionLogs(response.data);
    } catch (error) {
      console.error("Error fetching action logs:", error);
    }
  };

  const handleFileUpload = async (file, type) => {
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const response = await axios.post(`${API}/upload/${type}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      
      toast.success(`${type.charAt(0).toUpperCase() + type.slice(1)} data uploaded successfully`, {
        description: `${response.data.record_count} records processed`
      });
      
      // Refresh metrics after upload
      await fetchMetrics();
    } catch (error) {
      toast.error("Upload failed", {
        description: error.response?.data?.detail || "Please check your file format"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeMetric = async (anomalyId) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API}/analyze/${anomalyId}`);
      toast.success("Analysis complete", {
        description: "AI insights generated successfully"
      });
      await fetchInsights();
    } catch (error) {
      toast.error("Analysis failed", {
        description: error.response?.data?.detail || "Please try again"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerAction = async (insightId, metric, actionType) => {
    setLoading(true);
    try {
      await axios.post(`${API}/action/trigger`, {
        insight_id: insightId,
        metric: metric,
        action_type: actionType
      });
      
      toast.success("Action triggered", {
        description: `${actionType === 'moengage' ? 'Campaign' : 'Jira task'} created successfully`
      });
      
      await fetchActionLogs();
    } catch (error) {
      toast.error("Action failed", {
        description: error.response?.data?.detail || "Please try again"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen" data-testid="dashboard-page">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 backdrop-blur-sm bg-white/80">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                  Growth Copilot
                </h1>
                <p className="text-sm text-slate-500">AI-powered growth analytics</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="px-3 py-1">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                Live
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        <Tabs value={selectedTab} onValueChange={setSelectedTab} className="space-y-6">
          <TabsList className="grid w-full max-w-md grid-cols-3" data-testid="dashboard-tabs">
            <TabsTrigger value="overview" data-testid="tab-overview">Overview</TabsTrigger>
            <TabsTrigger value="insights" data-testid="tab-insights">Insights</TabsTrigger>
            <TabsTrigger value="actions" data-testid="tab-actions">Actions</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6" data-testid="overview-tab-content">
            {/* File Upload Section */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="w-5 h-5" />
                  Data Integration
                </CardTitle>
                <CardDescription>
                  Upload your Mixpanel, MoEngage, and Jira data files
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <FileUpload
                    title="Mixpanel CSV"
                    description="Date, metric, value, platform, cohort"
                    onUpload={(file) => handleFileUpload(file, "mixpanel")}
                    disabled={loading}
                    dataTestId="upload-mixpanel"
                  />
                  <FileUpload
                    title="MoEngage JSON"
                    description="Campaign metadata"
                    onUpload={(file) => handleFileUpload(file, "moengage")}
                    disabled={loading}
                    dataTestId="upload-moengage"
                  />
                  <FileUpload
                    title="Jira CSV"
                    description="Release notes and features"
                    onUpload={(file) => handleFileUpload(file, "jira")}
                    disabled={loading}
                    dataTestId="upload-jira"
                  />
                </div>
              </CardContent>
            </Card>

            {/* Metrics Section */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                    Metric Anomalies
                  </h2>
                  <p className="text-sm text-slate-500 mt-1">
                    Detected changes greater than 5% week-over-week
                  </p>
                </div>
                <Badge variant="secondary" data-testid="anomaly-count">
                  {metrics.length} detected
                </Badge>
              </div>

              {metrics.length === 0 ? (
                <Card>
                  <CardContent className="py-12">
                    <div className="text-center text-slate-500">
                      <AlertCircle className="w-12 h-12 mx-auto mb-3 text-slate-300" />
                      <p className="text-lg font-medium">No anomalies detected</p>
                      <p className="text-sm mt-1">Upload Mixpanel data to start analyzing metrics</p>
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" data-testid="metrics-grid">
                  {metrics.map((metric) => (
                    <MetricCard
                      key={metric.id}
                      metric={metric}
                      onAnalyze={() => handleAnalyzeMetric(metric.id)}
                      disabled={loading}
                    />
                  ))}
                </div>
              )}
            </div>
          </TabsContent>

          {/* Insights Tab */}
          <TabsContent value="insights" className="space-y-6" data-testid="insights-tab-content">
            <div>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                    AI Insights
                  </h2>
                  <p className="text-sm text-slate-500 mt-1">
                    Generated by Gemini 2.5 Pro
                  </p>
                </div>
                <Badge variant="secondary" data-testid="insight-count">
                  {insights.length} insights
                </Badge>
              </div>

              {insights.length === 0 ? (
                <Card>
                  <CardContent className="py-12">
                    <div className="text-center text-slate-500">
                      <AlertCircle className="w-12 h-12 mx-auto mb-3 text-slate-300" />
                      <p className="text-lg font-medium">No insights generated yet</p>
                      <p className="text-sm mt-1">Click "Analyze" on metric cards to generate AI insights</p>
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <div className="space-y-4" data-testid="insights-list">
                  {insights.map((insight) => (
                    <InsightPanel
                      key={insight.id}
                      insight={insight}
                      onTriggerAction={(actionType) => handleTriggerAction(insight.id, insight.metric, actionType)}
                      disabled={loading}
                    />
                  ))}
                </div>
              )}
            </div>
          </TabsContent>

          {/* Actions Tab */}
          <TabsContent value="actions" className="space-y-6" data-testid="actions-tab-content">
            <ActionLogsPanel logs={actionLogs} />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default Dashboard;