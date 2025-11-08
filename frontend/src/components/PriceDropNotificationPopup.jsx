import { Bell, TrendingDown, Package, Users, CheckCircle } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const PriceDropNotificationPopup = ({ open, onOpenChange, onViewDetails }) => {
  // Mock data - hardcoded
  const mockData = {
    totalArticles: 45,
    totalCategories: 3,
    avgDiscount: 28,
    affectedStores: 12,
    notificationsSent: 156
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px] border-0 shadow-2xl">
        {/* Animated gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-orange-50 via-red-50 to-pink-50 rounded-lg opacity-50"></div>
        
        <div className="relative">
          {/* Icon with pulse animation */}
          <div className="flex justify-center mb-4">
            <div className="relative">
              <div className="absolute inset-0 bg-orange-400 rounded-full blur-xl opacity-50 animate-pulse"></div>
              <div className="relative w-20 h-20 bg-gradient-to-br from-orange-500 to-red-500 rounded-full flex items-center justify-center shadow-lg">
                <Bell className="w-10 h-10 text-white animate-bounce" />
              </div>
            </div>
          </div>

          <DialogHeader>
            <DialogTitle className="text-center text-2xl font-bold text-slate-900 mb-2">
              🎉 Price Drop Alert!
            </DialogTitle>
          </DialogHeader>

          <div className="mt-6 space-y-4">
            {/* Main message */}
            <div className="text-center">
              <p className="text-lg font-semibold text-slate-800">
                Price Drop Notifications Sent Successfully
              </p>
              <p className="text-sm text-slate-600 mt-2">
                Operational leads have been notified about the latest price changes
              </p>
            </div>

            {/* Stats grid */}
            <div className="grid grid-cols-2 gap-3 mt-6">
              <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
                <div className="flex items-center gap-2 mb-1">
                  <Package className="w-4 h-4 text-orange-600" />
                  <span className="text-xs font-medium text-slate-600">Articles</span>
                </div>
                <p className="text-2xl font-bold text-slate-900">{mockData.totalArticles}</p>
              </div>

              <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
                <div className="flex items-center gap-2 mb-1">
                  <TrendingDown className="w-4 h-4 text-orange-600" />
                  <span className="text-xs font-medium text-slate-600">Avg Discount</span>
                </div>
                <p className="text-2xl font-bold text-slate-900">{mockData.avgDiscount}%</p>
              </div>

              <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
                <div className="flex items-center gap-2 mb-1">
                  <Users className="w-4 h-4 text-orange-600" />
                  <span className="text-xs font-medium text-slate-600">Stores</span>
                </div>
                <p className="text-2xl font-bold text-slate-900">{mockData.affectedStores}</p>
              </div>

              <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
                <div className="flex items-center gap-2 mb-1">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span className="text-xs font-medium text-slate-600">Notified</span>
                </div>
                <p className="text-2xl font-bold text-slate-900">{mockData.notificationsSent}</p>
              </div>
            </div>

            {/* Notification badges */}
            <div className="flex flex-wrap gap-2 justify-center pt-4">
              <Badge variant="secondary" className="bg-green-100 text-green-700 border-green-200">
                ✓ Ground Teams Notified
              </Badge>
              <Badge variant="secondary" className="bg-blue-100 text-blue-700 border-blue-200">
                ✓ Sales Officers Informed
              </Badge>
              <Badge variant="secondary" className="bg-purple-100 text-purple-700 border-purple-200">
                ✓ Partners Synced
              </Badge>
            </div>

            {/* Action buttons */}
            <div className="flex gap-3 pt-4">
              <Button
                onClick={() => {
                  onOpenChange(false);
                  onViewDetails();
                }}
                className="flex-1 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white shadow-lg"
              >
                View Details
              </Button>
              <Button
                onClick={() => onOpenChange(false)}
                variant="outline"
                className="flex-1 border-slate-300 hover:bg-slate-50"
              >
                Dismiss
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default PriceDropNotificationPopup;
