import { useState, useEffect } from "react";
import { Upload, Activity, MessageSquare, RefreshCw, RotateCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import api from "@/services/api";
import FileUpload from "@/components/FileUpload";
import MetricCard from "@/components/MetricCard";
import InsightPanel from "@/components/InsightPanel";
import ActionLogsPanel from "@/components/ActionLogsPanel";
import ChatInterface from "@/components/ChatInterface";

const Dashboard = () => {
  const [metrics, setMetrics] = useState([]);
  const [insights, setInsights] = useState([]);
  const [enhancedInsights, setEnhancedInsights] = useState([]);
  const [actionLogs, setActionLogs] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedTab, setSelectedTab] = useState("overview");

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    await Promise.all([
      fetchMetrics(),
      fetchInsights(),
      fetchEnhancedInsights(),
      fetchActionLogs(),
      fetchSummary(),
    ]);
  };

  const fetchMetrics = async () => {
    try {
      const data = await api.getMetrics();
      setMetrics(data);
    } catch (error) {
      console.error("Error fetching metrics:", error);
    }
  };

  const fetchInsights = async () => {
    try {
      const data = await api.getInsights();
      setInsights(data);
    } catch (error) {
      console.error("Error fetching insights:", error);
    }
  };

  const fetchEnhancedInsights = async () => {
    try {
      const data = await api.getEnhancedInsights();
      setEnhancedInsights(data);
    } catch (error) {
      console.error("Error fetching enhanced insights:", error);
    }
  };

  const fetchActionLogs = async () => {
    try {
      const data = await api.getActionLogs();
      setActionLogs(data);
    } catch (error) {
      console.error("Error fetching action logs:", error);
    }
  };

  const fetchSummary = async () => {
    try {
      const data = await api.getSummary();
      setSummary(data);
    } catch (error) {
      console.error("Error fetching summary:", error);
    }
  };

  const handleFileUpload = async (file, type) => {
    setLoading(true);
    try {
      let response;
      if (type === "mixpanel") {
        response = await api.uploadMixpanel(file);
      } else if (type === "moengage") {
        response = await api.uploadMoengage(file);
      } else if (type === "jira") {
        response = await api.uploadJira(file);
      }

      toast.success(`${type.charAt(0).toUpperCase() + type.slice(1)} data uploaded`, {
        description: `${response.record_count} records processed. ${response.insights_generated || 0} anomalies detected.`,
        descriptionClassName: "text-slate-700 font-medium"
      });

      // Refresh data after upload
      setTimeout(async () => {
        await fetchAllData();
      }, 1000);
    } catch (error) {
      toast.error("Upload failed", {
        description: error.response?.data?.detail || "Please check your file format",
        descriptionClassName: "text-red-700 font-medium"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeMetric = async (anomalyId) => {
    setLoading(true);
    try {
      await api.analyzeMetric(anomalyId);
      toast.success("Analysis complete", {
        description: "AI insights generated successfully",
        descriptionClassName: "text-slate-700 font-medium"
      });
      await fetchInsights();
    } catch (error) {
      toast.error("Analysis failed", {
        description: error.response?.data?.detail || "Please try again",
        descriptionClassName: "text-red-700 font-medium"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerAction = async (insightId, metric, actionType) => {
    setLoading(true);
    try {
      await api.triggerAction(insightId, metric, actionType);
      toast.success("Action triggered", {
        description: `${actionType === "moengage" ? "Campaign" : "Jira task"} created successfully`,
        descriptionClassName: "text-slate-700 font-medium"
      });
      await fetchActionLogs();
    } catch (error) {
      toast.error("Action failed", {
        description: error.response?.data?.detail || "Please try again",
        descriptionClassName: "text-red-700 font-medium"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleChatQuery = async (question) => {
    try {
      const response = await api.query(question);
      return response;
    } catch (error) {
      throw error;
    }
  };

  const handleRefreshData = async () => {
    setLoading(true);
    try {
      await fetchAllData();
      toast.success("Data refreshed", {
        description: "Latest data loaded from server",
        descriptionClassName: "text-slate-700 font-medium"
      });
    } catch (error) {
      toast.error("Refresh failed", {
        description: "Unable to reload data",
        descriptionClassName: "text-red-700 font-medium"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateInsights = async () => {
    setLoading(true);
    try {
      await api.triggerInsightsGeneration();
      toast.success("Insights generation started", {
        description: "AI is analyzing your data. This will take 20-40 seconds. Watch the Insights tab!",
        descriptionClassName: "text-slate-700 font-medium"
      });
      
      // Refresh after 35 seconds
      setTimeout(async () => {
        await fetchEnhancedInsights();
        await fetchSummary();
        toast.info("Insights ready!", {
          description: "Check the Insights tab for new analysis",
          descriptionClassName: "text-slate-700 font-medium"
        });
      }, 35000);
    } catch (error) {
      toast.error("Failed to trigger insights", {
        description: error.response?.data?.detail || "Please try again",
        descriptionClassName: "text-red-700 font-medium"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50" data-testid="dashboard-page">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 backdrop-blur-sm bg-white/95">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center shadow-lg">
                <Activity className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-900" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                  Growth Copilot
                </h1>
                <p className="text-sm text-slate-500">AI-powered growth analytics</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {summary && (
                <div className="flex gap-2">
                  <Badge variant="outline" className="px-3 py-1">
                    📊 {summary.mixpanel_records} metrics
                  </Badge>
                  <Badge variant="outline" className="px-3 py-1">
                    💡 {summary.generated_insights} insights
                  </Badge>
                </div>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={handleRefreshData}
                disabled={loading}
                className="gap-2"
              >
                <RotateCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
                Refresh
              </Button>
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
          <TabsList className="grid w-full max-w-md grid-cols-4 bg-white" data-testid="dashboard-tabs">
            <TabsTrigger value="overview" data-testid="tab-overview">Overview</TabsTrigger>
            <TabsTrigger value="insights" data-testid="tab-insights">Insights</TabsTrigger>
            <TabsTrigger value="chat" data-testid="tab-chat">
              <MessageSquare className="w-4 h-4 mr-2" />
              Chat
            </TabsTrigger>
            <TabsTrigger value="actions" data-testid="tab-actions">Actions</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6" data-testid="overview-tab-content">
            <Card className="border-slate-200 shadow-sm">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <Upload className="w-5 h-5 text-blue-600" />
                      Data Integration
                    </CardTitle>
                    <CardDescription>Upload your Mixpanel, MoEngage, and Jira data files</CardDescription>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleGenerateInsights}
                    disabled={loading || !summary || summary.mixpanel_records === 0}
                  >
                    <RefreshCw className={`w-4 h-4 mr-2 ${loading ? "animate-spin" : ""}`} />
                    Generate Insights
                  </Button>
                </div>
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
            <Card className="border-slate-200 shadow-sm">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Metric Anomalies</CardTitle>
                    <CardDescription>Detected changes greater than 5% week-over-week</CardDescription>
                  </div>
                  <Badge variant="secondary" data-testid="anomaly-count">
                    {metrics.length} detected
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                {metrics.length === 0 ? (
                  <div className="text-center py-12 text-slate-500">
                    <Upload className="w-12 h-12 mx-auto mb-3 text-slate-300" />
                    <p className="text-lg font-medium">No anomalies detected</p>
                    <p className="text-sm mt-1">Upload Mixpanel data to start analyzing metrics</p>
                  </div>
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
              </CardContent>
            </Card>
          </TabsContent>

          {/* Insights Tab */}
          <TabsContent value="insights" className="space-y-6" data-testid="insights-tab-content">
            <Card className="border-slate-200 shadow-sm">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>AI Insights</CardTitle>
                    <CardDescription>Comprehensive analysis powered by Gemini</CardDescription>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleRefreshData}
                      disabled={loading}
                    >
                      <RotateCw className={`w-4 h-4 mr-2 ${loading ? "animate-spin" : ""}`} />
                      Refresh
                    </Button>
                    <Badge variant="secondary" data-testid="insight-count">
                      {insights.length + enhancedInsights.length} total
                    </Badge>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {insights.length === 0 && enhancedInsights.length === 0 ? (
                  <div className="text-center py-12 text-slate-500">
                    <MessageSquare className="w-12 h-12 mx-auto mb-3 text-slate-300" />
                    <p className="text-lg font-medium">No insights generated yet</p>
                    <p className="text-sm mt-1 mb-4">Click "Generate Insights" or analyze specific metrics</p>
                    <Button
                      onClick={handleGenerateInsights}
                      disabled={loading || !summary || summary.mixpanel_records === 0}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      <RefreshCw className="w-4 h-4 mr-2" />
                      Generate Insights Now
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-4" data-testid="insights-list">
                    {insights.map((insight) => (
                      <InsightPanel
                        key={insight.id}
                        insight={insight}
                        onTriggerAction={(actionType) =>
                          handleTriggerAction(insight.id, insight.metric, actionType)
                        }
                        disabled={loading}
                      />
                    ))}
                    {enhancedInsights.map((insight) => (
                      <Card key={insight.id} className="border-l-4 border-l-purple-500">
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <CardTitle className="text-lg capitalize">
                              {insight.insight_type?.replace(/_/g, " ")}
                            </CardTitle>
                            <Badge variant={insight.confidence === "high" ? "default" : insight.confidence === "medium" ? "secondary" : "outline"}>
                              {insight.confidence} confidence
                            </Badge>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <p className="text-sm text-slate-700 mb-4">{insight.summary}</p>
                          {insight.recommendations && insight.recommendations.length > 0 && (
                            <div className="bg-blue-50 rounded-lg p-4">
                              <p className="text-sm font-semibold text-slate-900 mb-2">Recommendations:</p>
                              <ul className="space-y-1">
                                {insight.recommendations.map((rec, i) => (
                                  <li key={i} className="text-sm text-slate-700 flex items-start gap-2">
                                    <span className="text-blue-600 mt-0.5">→</span>
                                    <span>{typeof rec === 'object' ? rec.action || JSON.stringify(rec) : rec}</span>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Chat Tab */}
          <TabsContent value="chat" className="space-y-6" data-testid="chat-tab-content">
            <ChatInterface onSendQuery={handleChatQuery} loading={loading} />
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
