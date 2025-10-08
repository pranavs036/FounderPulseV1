import { TrendingUp, TrendingDown, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export const MetricCard = ({ metric, onAnalyze, disabled }) => {
  const isPositive = metric.change_percent > 0;
  const Icon = isPositive ? TrendingUp : TrendingDown;
  const colorClass = isPositive ? "text-green-600" : "text-red-600";
  const bgColorClass = isPositive ? "bg-green-50" : "bg-red-50";

  return (
    <Card className="hover:shadow-lg transition-shadow" data-testid={`metric-card-${metric.metric_name}`}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-lg capitalize" data-testid={`metric-name-${metric.metric_name}`}>
              {metric.metric_name.replace(/_/g, " ")}
            </CardTitle>
            <div className="flex items-center gap-2 mt-2">
              <Badge variant="secondary" className="text-xs" data-testid={`metric-platform-${metric.metric_name}`}>
                {metric.platform}
              </Badge>
              <Badge variant="outline" className="text-xs" data-testid={`metric-cohort-${metric.metric_name}`}>
                {metric.cohort}
              </Badge>
            </div>
          </div>
          <div className={`${bgColorClass} p-2 rounded-lg`}>
            <Icon className={`w-5 h-5 ${colorClass}`} />
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <div className="flex items-baseline justify-between">
            <span className="text-sm text-slate-500">Current</span>
            <span className="text-lg font-semibold text-slate-900" data-testid={`metric-current-${metric.metric_name}`}>
              {metric.current_value.toFixed(3)}
            </span>
          </div>
          <div className="flex items-baseline justify-between">
            <span className="text-sm text-slate-500">Previous</span>
            <span className="text-sm text-slate-600" data-testid={`metric-previous-${metric.metric_name}`}>
              {metric.previous_value.toFixed(3)}
            </span>
          </div>
          <div className="pt-2 border-t border-slate-100">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-slate-700">Change</span>
              <span className={`text-xl font-bold ${colorClass}`} data-testid={`metric-change-${metric.metric_name}`}>
                {isPositive ? "+" : ""}{metric.change_percent.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>

        <Button
          size="sm"
          className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800"
          onClick={onAnalyze}
          disabled={disabled}
          data-testid={`analyze-button-${metric.metric_name}`}
        >
          <Sparkles className="w-4 h-4 mr-2" />
          Analyze with AI
        </Button>
      </CardContent>
    </Card>
  );
};

export default MetricCard;