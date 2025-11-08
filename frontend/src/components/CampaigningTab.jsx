import { useState } from "react";
import { Bell, Send, CheckCircle, Mail, MessageSquare, TrendingDown, Package, Users } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import PriceDropNotificationPopup from "@/components/PriceDropNotificationPopup";
import PriceDropDetailsModal from "@/components/PriceDropDetailsModal";

const CampaigningTab = () => {
  const [notificationPopupOpen, setNotificationPopupOpen] = useState(false);
  const [detailsModalOpen, setDetailsModalOpen] = useState(false);
  const [sendingNotifications, setSendingNotifications] = useState(false);

  // Detailed product list for notification
  const detailedProducts = [
    // Winter Jackets
    { id: "ART-001", name: "Heavy Winter Jacket - Black", oldPrice: 2999, newPrice: 2099, discount: 30, category: "Winter Jackets" },
    { id: "ART-002", name: "Puffer Jacket - Navy", oldPrice: 3499, newPrice: 2449, discount: 30, category: "Winter Jackets" },
    { id: "ART-003", name: "Wool Blend Coat - Grey", oldPrice: 4299, newPrice: 3009, discount: 30, category: "Winter Jackets" },
    { id: "ART-004", name: "Hooded Winter Jacket - Brown", oldPrice: 3299, newPrice: 2309, discount: 30, category: "Winter Jackets" },
    { id: "ART-005", name: "Quilted Jacket - Olive", oldPrice: 2799, newPrice: 1959, discount: 30, category: "Winter Jackets" },
    { id: "ART-006", name: "Leather Jacket - Black", oldPrice: 5999, newPrice: 4199, discount: 30, category: "Winter Jackets" },
    { id: "ART-007", name: "Bomber Jacket - Maroon", oldPrice: 2899, newPrice: 2029, discount: 30, category: "Winter Jackets" },
    { id: "ART-008", name: "Denim Jacket - Blue", oldPrice: 2499, newPrice: 1749, discount: 30, category: "Winter Jackets" },
    
    // Formal Shoes
    { id: "ART-011", name: "Oxford Leather - Brown", oldPrice: 2499, newPrice: 1874, discount: 25, category: "Formal Shoes" },
    { id: "ART-012", name: "Derby Formal - Black", oldPrice: 2799, newPrice: 2099, discount: 25, category: "Formal Shoes" },
    { id: "ART-013", name: "Brogues - Tan", oldPrice: 2999, newPrice: 2249, discount: 25, category: "Formal Shoes" },
    { id: "ART-014", name: "Monk Strap - Black", oldPrice: 3299, newPrice: 2474, discount: 25, category: "Formal Shoes" },
    { id: "ART-015", name: "Loafers - Brown", oldPrice: 2399, newPrice: 1799, discount: 25, category: "Formal Shoes" },
    
    // Accessories
    { id: "ART-021", name: "Leather Wallet - Black", oldPrice: 999, newPrice: 719, discount: 28, category: "Accessories" },
    { id: "ART-022", name: "Designer Belt - Brown", oldPrice: 1499, newPrice: 1079, discount: 28, category: "Accessories" },
    { id: "ART-023", name: "Leather Wallet - Brown", oldPrice: 1099, newPrice: 791, discount: 28, category: "Accessories" },
    { id: "ART-024", name: "Formal Belt - Black", oldPrice: 1299, newPrice: 935, discount: 28, category: "Accessories" },
    { id: "ART-025", name: "Card Holder - Navy", oldPrice: 799, newPrice: 575, discount: 28, category: "Accessories" }
  ];

  // Hardcoded price drop data
  const priceDropData = {
    changeId: "DISCOUNT-NOV-2025-1", // Discount Campaign ID - First discount of November 2025
    effectiveDate: "Nov 9, 2025",
    totalArticles: 45,
    totalCategories: 3,
    avgDiscount: 28,
    categories: [
      {
        name: "Winter Jackets",
        articles: 25,
        avgDiscount: 30,
        priceRange: "₹2,099 - ₹4,299"
      },
      {
        name: "Formal Shoes",
        articles: 12,
        avgDiscount: 25,
        priceRange: "₹1,874 - ₹2,799"
      },
      {
        name: "Accessories",
        articles: 8,
        avgDiscount: 28,
        priceRange: "₹719 - ₹1,499"
      }
    ],
    affectedStores: [
      { id: "MUM-01", name: "Mumbai Central", articles: 18 },
      { id: "MUM-02", name: "Mumbai Andheri", articles: 15 },
      { id: "PUN-01", name: "Pune FC Road", articles: 12 }
    ],
    operationalLeads: [
      { name: "Rajesh Kumar", role: "Regional Manager - Mumbai", contact: "+91 98765 43210", store: "Mumbai Central" },
      { name: "Priya Sharma", role: "Store Manager", contact: "+91 98765 43211", store: "Mumbai Andheri" },
      { name: "Amit Patel", role: "Store Manager", contact: "+91 98765 43212", store: "Pune FC Road" }
    ]
  };

  const handleSendNotifications = async () => {
    setSendingNotifications(true);
    
    // Simulate notification sending with delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    toast.success("Notifications sent successfully!", {
      description: "All operational leads have been notified via WhatsApp and Email",
      descriptionClassName: "text-green-700 font-medium"
    });
    
    setSendingNotifications(false);
    setNotificationPopupOpen(true);
  };

  const notificationMessage = `🔔 *Discount Campaign Alert - ${priceDropData.changeId}*

📅 *Effective Date:* ${priceDropData.effectiveDate}

📦 *Summary:*
• ${priceDropData.totalArticles} articles across ${priceDropData.totalCategories} categories
• Average discount: ${priceDropData.avgDiscount}%

📋 *Product IDs with Discounts:*

*Winter Jackets (30% OFF):*
${detailedProducts.filter(p => p.category === "Winter Jackets").map(p => `• ${p.id} - ${p.name}
  ₹${p.oldPrice} → ₹${p.newPrice} (Save ${p.discount}%)`).join('\n')}

*Formal Shoes (25% OFF):*
${detailedProducts.filter(p => p.category === "Formal Shoes").map(p => `• ${p.id} - ${p.name}
  ₹${p.oldPrice} → ₹${p.newPrice} (Save ${p.discount}%)`).join('\n')}

*Accessories (28% OFF):*
${detailedProducts.filter(p => p.category === "Accessories").map(p => `• ${p.id} - ${p.name}
  ₹${p.oldPrice} → ₹${p.newPrice} (Save ${p.discount}%)`).join('\n')}

View complete details in the system dashboard.`;

  return (
    <div className="space-y-6">
      {/* Header Card */}
      <Card className="border-orange-200 bg-gradient-to-br from-orange-50 to-red-50">
        <CardHeader>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-lg flex items-center justify-center shadow-lg">
              <Bell className="w-6 h-6 text-white" />
            </div>
            <div>
              <CardTitle className="text-2xl">Discount Campaign Manager</CardTitle>
              <CardDescription className="text-slate-700">
                Notify operational leads about monthly discount campaigns
              </CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-4 gap-4">
            <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <Package className="w-5 h-5 text-orange-600" />
                <span className="text-sm font-medium text-slate-600">Total Articles</span>
              </div>
              <p className="text-3xl font-bold text-slate-900">{priceDropData.totalArticles}</p>
            </div>

            <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <TrendingDown className="w-5 h-5 text-red-600" />
                <span className="text-sm font-medium text-slate-600">Avg Discount</span>
              </div>
              <p className="text-3xl font-bold text-slate-900">{priceDropData.avgDiscount}%</p>
            </div>

            <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <Package className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-medium text-slate-600">Categories</span>
              </div>
              <p className="text-3xl font-bold text-slate-900">{priceDropData.totalCategories}</p>
            </div>

            <div className="bg-white rounded-lg p-4 border border-orange-100 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <Users className="w-5 h-5 text-green-600" />
                <span className="text-sm font-medium text-slate-600">Leads to Notify</span>
              </div>
              <p className="text-3xl font-bold text-slate-900">{priceDropData.operationalLeads.length}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Price Drop Details */}
      <Card className="border-slate-200 shadow-sm">
        <CardHeader>
          <CardTitle>Discount Campaign Details - {priceDropData.changeId}</CardTitle>
          <CardDescription>Effective from {priceDropData.effectiveDate}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {priceDropData.categories.map((category, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-orange-100 to-red-100 rounded-lg flex items-center justify-center">
                    <Package className="w-5 h-5 text-orange-600" />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">{category.name}</p>
                    <p className="text-sm text-slate-600">
                      {category.articles} articles • Price range: {category.priceRange}
                    </p>
                  </div>
                </div>
                <Badge variant="secondary" className="bg-red-100 text-red-700 border-red-200 text-base px-3 py-1">
                  {category.avgDiscount}% OFF
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Affected Stores */}
      <Card className="border-slate-200 shadow-sm">
        <CardHeader>
          <CardTitle>Affected Store Locations</CardTitle>
          <CardDescription>{priceDropData.affectedStores.length} stores need to update pricing</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {priceDropData.affectedStores.map((store, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                <div>
                  <p className="font-semibold text-slate-900">{store.name}</p>
                  <p className="text-sm text-slate-600">Store ID: {store.id}</p>
                </div>
                <Badge variant="outline" className="text-blue-700 border-blue-200">
                  {store.articles} articles
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Operational Leads */}
      <Card className="border-slate-200 shadow-sm">
        <CardHeader>
          <CardTitle>Operational Leads - Notification Recipients</CardTitle>
          <CardDescription>These leads will receive WhatsApp and Email notifications</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {priceDropData.operationalLeads.map((lead, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center">
                    <Users className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-semibold text-slate-900">{lead.name}</p>
                    <p className="text-sm text-slate-600">{lead.role}</p>
                    <p className="text-xs text-slate-500 mt-1">
                      📍 {lead.store} • 📞 {lead.contact}
                    </p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                    <MessageSquare className="w-3 h-3 mr-1" />
                    WhatsApp
                  </Badge>
                  <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                    <Mail className="w-3 h-3 mr-1" />
                    Email
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Notification Preview */}
      <Card className="border-slate-200 shadow-sm">
        <CardHeader>
          <CardTitle>Notification Message Preview</CardTitle>
          <CardDescription>This message will be sent to all operational leads with complete product IDs</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="bg-slate-900 rounded-lg p-6 font-mono text-xs text-white whitespace-pre-line overflow-auto max-h-96">
            {notificationMessage}
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex gap-4">
        <Button
          onClick={handleSendNotifications}
          disabled={sendingNotifications}
          className="flex-1 bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white shadow-lg h-14 text-lg"
        >
          {sendingNotifications ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
              Sending Notifications...
            </>
          ) : (
            <>
              <Send className="w-5 h-5 mr-2" />
              Send Notifications to All Leads
            </>
          )}
        </Button>

        <Button
          variant="outline"
          onClick={() => setDetailsModalOpen(true)}
          className="px-8 h-14 text-lg border-slate-300"
        >
          View Detailed Report
        </Button>
      </div>

      {/* Success Message */}
      <Card className="border-green-200 bg-green-50">
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <CheckCircle className="w-6 h-6 text-green-600 mt-0.5" />
            <div>
              <p className="font-semibold text-green-900 mb-1">Ready to Send</p>
              <p className="text-sm text-green-700">
                All discounts have been validated. Click "Send Notifications" to notify operational leads 
                via WhatsApp and Email about the discount campaign effective from {priceDropData.effectiveDate}.
              </p>
              <p className="text-sm text-green-700 mt-2">
                <strong>Note:</strong> This notification includes all {detailedProducts.length} product IDs with complete discount details 
                (old price → new discounted price → discount %) organized by category.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Modals */}
      <PriceDropNotificationPopup
        open={notificationPopupOpen}
        onOpenChange={setNotificationPopupOpen}
        onViewDetails={() => {
          setNotificationPopupOpen(false);
          setDetailsModalOpen(true);
        }}
      />

      <PriceDropDetailsModal
        open={detailsModalOpen}
        onOpenChange={setDetailsModalOpen}
      />
    </div>
  );
};

export default CampaigningTab;
