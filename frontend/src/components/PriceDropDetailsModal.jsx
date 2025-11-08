import { useState } from "react";
import { X, TrendingDown, Package, MapPin, Users, MessageSquare, Send } from "lucide-react";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";

const PriceDropDetailsModal = ({ open, onOpenChange }) => {
  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      content: "Hi! I can help you understand the price drop details. Ask me anything about the affected items, categories, or notifications sent."
    }
  ]);
  const [chatInput, setChatInput] = useState("");

  // Mock data - hardcoded
  const mockPriceDrops = {
    changeId: "PD-2025-11-04-001",
    effectiveDate: "Nov 5, 2025",
    totalArticles: 45,
    categories: [
      {
        name: "Winter Jackets",
        articles: 25,
        avgDiscount: 30,
        items: [
          { id: "ART-001", name: "Heavy Winter Jacket - Black", oldPrice: 2999, newPrice: 2099, discount: 30 },
          { id: "ART-002", name: "Puffer Jacket - Navy", oldPrice: 3499, newPrice: 2449, discount: 30 },
          { id: "ART-003", name: "Wool Blend Coat - Grey", oldPrice: 4299, newPrice: 3009, discount: 30 }
        ]
      },
      {
        name: "Formal Shoes",
        articles: 12,
        avgDiscount: 25,
        items: [
          { id: "ART-011", name: "Oxford Leather - Brown", oldPrice: 2499, newPrice: 1874, discount: 25 },
          { id: "ART-012", name: "Derby Formal - Black", oldPrice: 2799, newPrice: 2099, discount: 25 }
        ]
      },
      {
        name: "Accessories",
        articles: 8,
        avgDiscount: 28,
        items: [
          { id: "ART-021", name: "Leather Wallet - Black", oldPrice: 999, newPrice: 719, discount: 28 },
          { id: "ART-022", name: "Designer Belt - Brown", oldPrice: 1499, newPrice: 1079, discount: 28 }
        ]
      }
    ],
    notifications: {
      groundTeams: { sent: 12, acknowledged: 9 },
      salesOfficers: { sent: 5, opened: 4 },
      partners: { sent: 3, synced: 2 },
      customers: { sent: 135, opened: 67 }
    },
    stores: [
      { id: "MUM-01", name: "Mumbai Central", articles: 18, status: "acknowledged" },
      { id: "MUM-02", name: "Mumbai Andheri", articles: 15, status: "acknowledged" },
      { id: "PUN-01", name: "Pune FC Road", articles: 12, status: "pending" }
    ]
  };

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;

    // Add user message
    const newMessages = [
      ...chatMessages,
      { role: "user", content: chatInput }
    ];

    // Mock AI response based on query
    const query = chatInput.toLowerCase();
    let response = "";

    if (query.includes("winter") || query.includes("jacket")) {
      response = "25 Winter Jackets have been marked for 30% discount. This includes items like Heavy Winter Jacket (₹2,999 → ₹2,099) and Puffer Jacket (₹3,499 → ₹2,449). These changes are effective from Nov 5, 2025.";
    } else if (query.includes("store") || query.includes("location")) {
      response = "The price changes affect 3 stores: Mumbai Central (18 articles), Mumbai Andheri (15 articles), and Pune FC Road (12 articles). Mumbai locations have acknowledged the changes, while Pune is still pending.";
    } else if (query.includes("notification") || query.includes("sent")) {
      response = "Notifications have been sent to 155 stakeholders: 12 ground teams (9 acknowledged), 5 sales officers (4 opened), 3 partners (2 synced), and 135 customers (67 opened).";
    } else if (query.includes("customer") || query.includes("response")) {
      response = "135 customers who previously viewed these items received push notifications. So far, 67 customers (49.6%) have opened the notification. Customer engagement is tracking well for this price drop campaign.";
    } else {
      response = "I can help you with information about the price drops. You can ask about specific categories (Winter Jackets, Formal Shoes, Accessories), store locations, notification status, or customer response rates.";
    }

    newMessages.push({ role: "assistant", content: response });
    setChatMessages(newMessages);
    setChatInput("");
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-5xl h-[85vh] p-0 gap-0">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200 bg-gradient-to-r from-orange-50 to-red-50">
          <div>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-lg flex items-center justify-center shadow-lg">
                <TrendingDown className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-slate-900">Price Drop Details</h2>
                <p className="text-sm text-slate-600">Change ID: {mockPriceDrops.changeId} • Effective: {mockPriceDrops.effectiveDate}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden">
          <Tabs defaultValue="overview" className="h-full flex flex-col">
            <TabsList className="mx-6 mt-4 bg-white border border-slate-200">
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="items">Items & Categories</TabsTrigger>
              <TabsTrigger value="notifications">Notifications</TabsTrigger>
              <TabsTrigger value="chat">
                <MessageSquare className="w-4 h-4 mr-2" />
                Chat
              </TabsTrigger>
            </TabsList>

            <div className="flex-1 overflow-hidden px-6 pb-6">
              {/* Overview Tab */}
              <TabsContent value="overview" className="h-full mt-4">
                <div className="h-full pr-4 overflow-y-auto">
                  <div className="space-y-4">
                    {/* Summary Cards */}
                    <div className="grid grid-cols-4 gap-4">
                      <Card className="border-slate-200">
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <Package className="w-8 h-8 mx-auto mb-2 text-orange-600" />
                            <p className="text-3xl font-bold text-slate-900">{mockPriceDrops.totalArticles}</p>
                            <p className="text-sm text-slate-600 mt-1">Total Articles</p>
                          </div>
                        </CardContent>
                      </Card>

                      <Card className="border-slate-200">
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <TrendingDown className="w-8 h-8 mx-auto mb-2 text-red-600" />
                            <p className="text-3xl font-bold text-slate-900">
                              {Math.round(mockPriceDrops.categories.reduce((acc, cat) => acc + cat.avgDiscount, 0) / mockPriceDrops.categories.length)}%
                            </p>
                            <p className="text-sm text-slate-600 mt-1">Avg Discount</p>
                          </div>
                        </CardContent>
                      </Card>

                      <Card className="border-slate-200">
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <MapPin className="w-8 h-8 mx-auto mb-2 text-blue-600" />
                            <p className="text-3xl font-bold text-slate-900">{mockPriceDrops.stores.length}</p>
                            <p className="text-sm text-slate-600 mt-1">Stores Affected</p>
                          </div>
                        </CardContent>
                      </Card>

                      <Card className="border-slate-200">
                        <CardContent className="pt-6">
                          <div className="text-center">
                            <Users className="w-8 h-8 mx-auto mb-2 text-green-600" />
                            <p className="text-3xl font-bold text-slate-900">
                              {Object.values(mockPriceDrops.notifications).reduce((acc, n) => acc + n.sent, 0)}
                            </p>
                            <p className="text-sm text-slate-600 mt-1">Notifications Sent</p>
                          </div>
                        </CardContent>
                      </Card>
                    </div>

                    {/* Categories Overview */}
                    <Card className="border-slate-200">
                      <CardHeader>
                        <CardTitle>Categories Summary</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          {mockPriceDrops.categories.map((category) => (
                            <div key={category.name} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                              <div className="flex items-center gap-3">
                                <div className="w-10 h-10 bg-gradient-to-br from-orange-100 to-red-100 rounded-lg flex items-center justify-center">
                                  <Package className="w-5 h-5 text-orange-600" />
                                </div>
                                <div>
                                  <p className="font-semibold text-slate-900">{category.name}</p>
                                  <p className="text-sm text-slate-600">{category.articles} articles</p>
                                </div>
                              </div>
                              <Badge variant="secondary" className="bg-red-100 text-red-700 border-red-200">
                                {category.avgDiscount}% OFF
                              </Badge>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>

                    {/* Store Status */}
                    <Card className="border-slate-200">
                      <CardHeader>
                        <CardTitle>Store Status</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          {mockPriceDrops.stores.map((store) => (
                            <div key={store.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                              <div>
                                <p className="font-semibold text-slate-900">{store.name}</p>
                                <p className="text-sm text-slate-600">{store.articles} articles affected</p>
                              </div>
                              <Badge 
                                variant="secondary" 
                                className={store.status === "acknowledged" 
                                  ? "bg-green-100 text-green-700 border-green-200" 
                                  : "bg-yellow-100 text-yellow-700 border-yellow-200"}
                              >
                                {store.status === "acknowledged" ? "✓ Acknowledged" : "⏳ Pending"}
                              </Badge>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </TabsContent>

              {/* Items & Categories Tab */}
              <TabsContent value="items" className="h-full mt-4">
                <div className="h-full pr-4 overflow-y-auto">
                  <div className="space-y-6">
                    {mockPriceDrops.categories.map((category) => (
                      <Card key={category.name} className="border-slate-200">
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <CardTitle>{category.name}</CardTitle>
                            <Badge variant="secondary" className="bg-red-100 text-red-700 border-red-200">
                              {category.articles} items • {category.avgDiscount}% OFF
                            </Badge>
                          </div>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-3">
                            {category.items.map((item) => (
                              <div key={item.id} className="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
                                <div className="flex-1">
                                  <p className="font-medium text-slate-900">{item.name}</p>
                                  <p className="text-sm text-slate-600 mt-1">Article ID: {item.id}</p>
                                </div>
                                <div className="text-right">
                                  <div className="flex items-center gap-2 justify-end mb-1">
                                    <span className="text-sm text-slate-500 line-through">₹{item.oldPrice}</span>
                                    <span className="text-lg font-bold text-red-600">₹{item.newPrice}</span>
                                  </div>
                                  <Badge variant="secondary" className="bg-red-100 text-red-700 border-red-200 text-xs">
                                    Save {item.discount}%
                                  </Badge>
                                </div>
                              </div>
                            ))}
                            {category.articles > category.items.length && (
                              <p className="text-center text-sm text-slate-500 py-2">
                                + {category.articles - category.items.length} more items in this category
                              </p>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              </TabsContent>

              {/* Notifications Tab */}
              <TabsContent value="notifications" className="h-full mt-4">
                <div className="h-full pr-4 overflow-y-auto">
                  <div className="space-y-4">
                    <Card className="border-slate-200">
                      <CardHeader>
                        <CardTitle>Ground Teams</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                            <div>
                              <p className="font-medium text-slate-900">WhatsApp Notifications</p>
                              <p className="text-sm text-slate-600">{mockPriceDrops.notifications.groundTeams.sent} team leads notified</p>
                            </div>
                            <Badge variant="secondary" className="bg-green-100 text-green-700 border-green-200">
                              {mockPriceDrops.notifications.groundTeams.acknowledged}/{mockPriceDrops.notifications.groundTeams.sent} Acknowledged
                            </Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="border-slate-200">
                      <CardHeader>
                        <CardTitle>Sales Officers</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                            <div>
                              <p className="font-medium text-slate-900">Email Notifications</p>
                              <p className="text-sm text-slate-600">{mockPriceDrops.notifications.salesOfficers.sent} officers notified</p>
                            </div>
                            <Badge variant="secondary" className="bg-blue-100 text-blue-700 border-blue-200">
                              {mockPriceDrops.notifications.salesOfficers.opened}/{mockPriceDrops.notifications.salesOfficers.sent} Opened
                            </Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="border-slate-200">
                      <CardHeader>
                        <CardTitle>Partner Networks</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                            <div>
                              <p className="font-medium text-slate-900">API Webhooks</p>
                              <p className="text-sm text-slate-600">{mockPriceDrops.notifications.partners.sent} partners notified</p>
                            </div>
                            <Badge variant="secondary" className="bg-purple-100 text-purple-700 border-purple-200">
                              {mockPriceDrops.notifications.partners.synced}/{mockPriceDrops.notifications.partners.sent} Synced
                            </Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="border-slate-200">
                      <CardHeader>
                        <CardTitle>Customers</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                            <div>
                              <p className="font-medium text-slate-900">Push Notifications</p>
                              <p className="text-sm text-slate-600">{mockPriceDrops.notifications.customers.sent} customers notified</p>
                            </div>
                            <Badge variant="secondary" className="bg-orange-100 text-orange-700 border-orange-200">
                              {mockPriceDrops.notifications.customers.opened}/{mockPriceDrops.notifications.customers.sent} Opened ({Math.round((mockPriceDrops.notifications.customers.opened / mockPriceDrops.notifications.customers.sent) * 100)}%)
                            </Badge>
                          </div>
                          <p className="text-sm text-slate-600 pl-3">
                            Notifications sent to customers who previously viewed or wishlisted these items
                          </p>
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </TabsContent>

              {/* Chat Tab */}
              <TabsContent value="chat" className="h-full mt-4 flex flex-col">
                <div className="flex-1 pr-4 overflow-y-auto">
                  <div className="space-y-4 pb-4">
                    {chatMessages.map((message, index) => (
                      <div
                        key={index}
                        className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                      >
                        <div
                          className={`max-w-[80%] rounded-lg p-4 ${
                            message.role === "user"
                              ? "bg-gradient-to-r from-blue-500 to-blue-600 text-white"
                              : "bg-slate-100 text-slate-900"
                          }`}
                        >
                          <p className="text-sm leading-relaxed">{message.content}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-200">
                  <div className="flex gap-2">
                    <Input
                      placeholder="Ask about price drops, categories, or notifications..."
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                      className="flex-1"
                    />
                    <Button
                      onClick={handleSendMessage}
                      className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700"
                    >
                      <Send className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </TabsContent>
            </div>
          </Tabs>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default PriceDropDetailsModal;
