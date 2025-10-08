import { CheckCircle2, XCircle, Clock, Package } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

export const ActionLogsPanel = ({ logs }) => {
  if (logs.length === 0) {
    return (
      <Card>
        <CardContent className="py-12">
          <div className="text-center text-slate-500">
            <Package className="w-12 h-12 mx-auto mb-3 text-slate-300" />
            <p className="text-lg font-medium">No actions triggered yet</p>
            <p className="text-sm mt-1">Trigger actions from the Insights tab to see logs here</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-900" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Action Logs
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Detailed logs of all triggered actions
          </p>
        </div>
        <Badge variant="secondary" data-testid="action-logs-count">
          {logs.length} actions
        </Badge>
      </div>

      <ScrollArea className="h-[600px] pr-4">
        <div className="space-y-4" data-testid="action-logs-list">
          {logs.map((log, index) => (
            <Card key={log.id} className="border-l-4 border-l-green-500" data-testid={`action-log-${index}`}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      {log.status === "success" ? (
                        <CheckCircle2 className="w-5 h-5 text-green-600" />
                      ) : (
                        <XCircle className="w-5 h-5 text-red-600" />
                      )}
                      <CardTitle className="text-base" data-testid={`action-log-metric-${index}`}>
                        {log.metric.replace(/_/g, " ").toUpperCase()}
                      </CardTitle>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={log.action_type === "moengage" ? "default" : "secondary"}
                        data-testid={`action-log-type-${index}`}
                      >
                        {log.action_type === "moengage" ? "MoEngage Campaign" : "Jira Task"}
                      </Badge>
                      <Badge
                        variant={log.status === "success" ? "outline" : "destructive"}
                        data-testid={`action-log-status-${index}`}
                      >
                        {log.status}
                      </Badge>
                    </div>
                  </div>
                  <div className="flex items-center gap-1 text-xs text-slate-500">
                    <Clock className="w-3 h-3" />
                    {new Date(log.triggered_at).toLocaleString()}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="text-sm font-semibold text-slate-900 mb-2">Description</h4>
                  <p className="text-sm text-slate-700" data-testid={`action-log-description-${index}`}>
                    {log.description}
                  </p>
                </div>

                {log.details && (
                  <>
                    <Separator />
                    <div>
                      <h4 className="text-sm font-semibold text-slate-900 mb-3">Details</h4>
                      <div className="space-y-2" data-testid={`action-log-details-${index}`}>
                        {Object.entries(log.details).map(([key, value]) => (
                          <div key={key} className="flex justify-between text-sm">
                            <span className="text-slate-500 capitalize">{key.replace(/_/g, " ")}:</span>
                            <span className="text-slate-900 font-medium">
                              {typeof value === "boolean" ? (value ? "Yes" : "No") : value}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
};

export default ActionLogsPanel;