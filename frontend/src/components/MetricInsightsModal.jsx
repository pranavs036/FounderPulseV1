import { useMemo } from "react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import InsightPanel from "@/components/InsightPanel";
import ChatInterface from "@/components/ChatInterface";

export default function MetricInsightsModal({ open, onOpenChange, metric, insights, enhancedInsights, onTriggerAction, onSendQuery, loading }) {
  const allInsights = useMemo(() => {
    const list = [];
    if (Array.isArray(insights)) list.push(...insights);
    if (Array.isArray(enhancedInsights)) list.push(...enhancedInsights);
    return list;
  }, [insights, enhancedInsights]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-5xl max-h-[90vh] flex flex-col p-0">
        <DialogHeader className="px-6 pt-6 pb-4 border-b">
          <div className="flex items-center justify-between">
            <DialogTitle className="capitalize">{metric?.replace(/_/g, " ")}</DialogTitle>
            <Badge variant="secondary">{allInsights.length} insights</Badge>
          </div>
        </DialogHeader>
        <div className="flex-1 overflow-hidden grid grid-cols-1 lg:grid-cols-2 gap-0">
          {/* Left side - Insights */}
          <ScrollArea className="flex-1 max-h-[calc(90vh-80px)] px-6 py-4 border-r">
            <div className="space-y-3 pr-4">
              {allInsights.length === 0 ? (
                <Card>
                  <CardContent className="py-8 text-sm text-slate-600">No insights yet for this metric.</CardContent>
                </Card>
              ) : (
                allInsights.map((insight) => (
                  <InsightPanel
                    key={insight.id}
                    insight={insight}
                    onTriggerAction={(actionType) => onTriggerAction(insight.id, insight.metric, actionType)}
                    disabled={loading}
                  />
                ))
              )}
            </div>
          </ScrollArea>
          
          {/* Right side - Chat */}
          <div className="flex flex-col max-h-[calc(90vh-80px)]">
            <Card className="h-full flex flex-col border-0 rounded-none">
              <CardHeader className="border-b">
                <CardTitle className="text-base">Ask about this metric</CardTitle>
              </CardHeader>
              <CardContent className="flex-1 overflow-hidden p-0">
                <div className="h-full">
                  <ChatInterface onSendQuery={onSendQuery} loading={loading} />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

