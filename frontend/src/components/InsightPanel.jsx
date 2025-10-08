import { Brain, Target, Lightbulb, Send, FileText } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

export const InsightPanel = ({ insight, onTriggerAction, disabled }) => {
  return (
    <Card className="border-l-4 border-l-blue-500" data-testid={`insight-panel-${insight.metric}`}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Brain className="w-5 h-5 text-blue-600" />
              <CardTitle className="text-lg capitalize" data-testid={`insight-metric-${insight.metric}`}>
                {insight.metric.replace(/_/g, " ")}
              </CardTitle>
            </div>
            <Badge variant="secondary" data-testid={`insight-change-${insight.metric}`}>
              {insight.change}
            </Badge>
          </div>
          <div className="text-xs text-slate-500">
            {new Date(insight.created_at).toLocaleString()}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-3">
          {/* Probable Cause */}
          <div className="bg-slate-50 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className="mt-0.5">
                <Target className="w-4 h-4 text-slate-600" />
              </div>
              <div className="flex-1">
                <h4 className="text-sm font-semibold text-slate-900 mb-1">Probable Cause</h4>
                <p className="text-sm text-slate-700" data-testid={`insight-cause-${insight.metric}`}>
                  {insight.probable_cause}
                </p>
              </div>
            </div>
          </div>

          {/* Affected Segment */}
          <div className="bg-amber-50 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className="mt-0.5">
                <Target className="w-4 h-4 text-amber-600" />
              </div>
              <div className="flex-1">
                <h4 className="text-sm font-semibold text-slate-900 mb-1">Affected Segment</h4>
                <p className="text-sm text-slate-700" data-testid={`insight-segment-${insight.metric}`}>
                  {insight.affected_segment}
                </p>
              </div>
            </div>
          </div>

          {/* Recommended Action */}
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <div className="mt-0.5">
                <Lightbulb className="w-4 h-4 text-blue-600" />
              </div>
              <div className="flex-1">
                <h4 className="text-sm font-semibold text-slate-900 mb-1">Recommended Action</h4>
                <p className="text-sm text-slate-700" data-testid={`insight-action-${insight.metric}`}>
                  {insight.recommended_action}
                </p>
              </div>
            </div>
          </div>
        </div>

        <Separator />

        <div className="flex gap-2">
          <Button
            size="sm"
            className="flex-1 bg-purple-600 hover:bg-purple-700"
            onClick={() => onTriggerAction("moengage")}
            disabled={disabled}
            data-testid={`trigger-moengage-${insight.metric}`}
          >
            <Send className="w-4 h-4 mr-2" />
            Send Campaign
          </Button>
          <Button
            size="sm"
            variant="outline"
            className="flex-1"
            onClick={() => onTriggerAction("jira")}
            disabled={disabled}
            data-testid={`trigger-jira-${insight.metric}`}
          >
            <FileText className="w-4 h-4 mr-2" />
            Create Jira Task
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default InsightPanel;