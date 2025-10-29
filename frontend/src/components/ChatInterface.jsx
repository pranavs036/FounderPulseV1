import { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Loader2, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

export const ChatInterface = ({ onSendQuery, loading }) => {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hi! I'm your AI analyst. Ask me anything about your metrics, releases, or campaigns!",
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || sending) return;

    const userMessage = {
      role: "user",
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setSending(true);

    try {
      const response = await onSendQuery(input.trim());
      
      const assistantMessage = {
        role: "assistant",
        content: response.answer,
        supporting_evidence: response.supporting_evidence,
        key_insights: response.key_insights,
        recommendations: response.recommendations,
        caveats: response.caveats,
        follow_up_suggestions: response.follow_up_suggestions,
        confidence: response.confidence,
        confidence_explanation: response.confidence_explanation,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: "assistant",
        content: "Sorry, I encountered an error processing your question. Please try again.",
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setSending(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const suggestedQuestions = [
    "Why did activation rate drop for Android users?",
    "Which campaign performed best?",
    "What caused the biggest metric change?",
    "How do tier1 users compare to tier2 users?"
  ];

  const handleSuggestionClick = (question) => {
    setInput(question);
  };

  return (
    <Card className="h-[600px] flex flex-col" data-testid="chat-interface">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Bot className="w-5 h-5 text-blue-600" />
              AI Chat Assistant
            </CardTitle>
            <CardDescription>
              Ask questions about your data in natural language
            </CardDescription>
          </div>
          <Badge variant="outline" className="gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            Online
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col space-y-4 p-0">
        {/* Messages Area */}
        <ScrollArea className="flex-1 px-6" ref={scrollRef}>
          <div className="space-y-4 pb-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}
                data-testid={`chat-message-${index}`}
              >
                {message.role === "assistant" && (
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-blue-600" />
                  </div>
                )}

                <div
                  className={`max-w-[80%] rounded-lg p-4 ${
                    message.role === "user"
                      ? "bg-blue-600 text-white"
                      : message.isError
                      ? "bg-red-50 text-red-900 border border-red-200"
                      : "bg-slate-50 text-slate-900"
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>

                  {/* Supporting Evidence */}
                  {message.supporting_evidence && message.supporting_evidence.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-slate-200">
                      <p className="text-xs font-semibold text-slate-600 mb-2">📊 Evidence:</p>
                      <ul className="space-y-1">
                        {message.supporting_evidence.map((evidence, i) => (
                          <li key={i} className="text-xs text-slate-600 flex items-start gap-2">
                            <span className="text-blue-600 mt-0.5">•</span>
                            <span>{evidence}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Key Insights */}
                  {message.key_insights && message.key_insights.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-slate-200">
                      <p className="text-xs font-semibold text-slate-600 mb-2">💡 Key Insights:</p>
                      <ul className="space-y-1">
                        {message.key_insights.map((insight, i) => (
                          <li key={i} className="text-xs text-slate-600 flex items-start gap-2">
                            <span className="text-purple-600 mt-0.5">→</span>
                            <span className="italic">{insight}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Recommendations */}
                  {message.recommendations && message.recommendations.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-slate-200">
                      <p className="text-xs font-semibold text-slate-600 mb-2">✨ Recommendations:</p>
                      <div className="space-y-2">
                        {message.recommendations.map((rec, i) => (
                          <div key={i} className="text-xs">
                            {typeof rec === 'object' ? (
                              <div className="bg-green-50 rounded p-2">
                                <div className="flex items-start gap-2">
                                  <span className="text-green-600 font-bold mt-0.5">{rec.priority}.</span>
                                  <div className="flex-1">
                                    <p className="text-slate-700 font-medium">{rec.action}</p>
                                    {rec.expected_outcome && (
                                      <p className="text-slate-600 mt-1">Expected: {rec.expected_outcome}</p>
                                    )}
                                    {rec.effort_level && (
                                      <p className="text-slate-500 mt-1 text-xs">Effort: {rec.effort_level} | Priority: {rec.priority}</p>
                                    )}
                                  </div>
                                </div>
                              </div>
                            ) : (
                              <div className="text-slate-600 flex items-start gap-2">
                                <span className="text-green-600 mt-0.5">→</span>
                                <span>{rec}</span>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Caveats */}
                  {message.caveats && message.caveats.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-slate-200">
                      <p className="text-xs font-semibold text-slate-600 mb-2">⚠️ Important Notes:</p>
                      <ul className="space-y-1">
                        {message.caveats.map((caveat, i) => (
                          <li key={i} className="text-xs text-amber-700 flex items-start gap-2">
                            <span className="mt-0.5">!</span>
                            <span>{caveat}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Follow-up Suggestions */}
                  {message.follow_up_suggestions && message.follow_up_suggestions.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-slate-200">
                      <p className="text-xs font-semibold text-slate-600 mb-2">🔍 Dig Deeper:</p>
                      <ul className="space-y-1">
                        {message.follow_up_suggestions.map((suggestion, i) => (
                          <li 
                            key={i} 
                            className="text-xs text-blue-600 hover:text-blue-700 cursor-pointer flex items-start gap-2"
                            onClick={() => setInput(suggestion)}
                          >
                            <span className="mt-0.5">→</span>
                            <span className="underline">{suggestion}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Confidence Badge with Explanation */}
                  {message.confidence && (
                    <div className="mt-2">
                      <div className="flex items-center justify-end gap-2">
                        <Badge 
                          variant="secondary" 
                          className={`text-xs ${
                            message.confidence === 'high' 
                              ? 'bg-green-100 text-green-700' 
                              : message.confidence === 'medium'
                              ? 'bg-yellow-100 text-yellow-700'
                              : 'bg-slate-100 text-slate-700'
                          }`}
                          title={message.confidence_explanation || ''}
                        >
                          {message.confidence} confidence
                        </Badge>
                      </div>
                      {message.confidence_explanation && (
                        <p className="text-xs text-slate-500 mt-1 text-right italic">
                          {message.confidence_explanation}
                        </p>
                      )}
                    </div>
                  )}

                  <p className="text-xs text-slate-400 mt-2">
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>

                {message.role === "user" && (
                  <div className="w-8 h-8 bg-slate-200 rounded-full flex items-center justify-center flex-shrink-0">
                    <User className="w-5 h-5 text-slate-600" />
                  </div>
                )}
              </div>
            ))}

            {sending && (
              <div className="flex gap-3 justify-start">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <Bot className="w-5 h-5 text-blue-600" />
                </div>
                <div className="bg-slate-50 rounded-lg p-4">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
                    <span className="text-sm text-slate-600">Analyzing your question...</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Suggested Questions (show only if no user messages yet) */}
        {messages.filter(m => m.role === "user").length === 0 && (
          <div className="px-6 pb-4">
            <p className="text-xs text-slate-500 mb-2">Try asking:</p>
            <div className="flex flex-wrap gap-2">
              {suggestedQuestions.map((question, index) => (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  className="text-xs"
                  onClick={() => handleSuggestionClick(question)}
                  disabled={sending}
                >
                  <Sparkles className="w-3 h-3 mr-1" />
                  {question}
                </Button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t border-slate-200 p-4">
          <div className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about your metrics, releases, or campaigns..."
              disabled={sending || loading}
              className="flex-1"
              data-testid="chat-input"
            />
            <Button
              onClick={handleSend}
              disabled={!input.trim() || sending || loading}
              className="bg-blue-600 hover:bg-blue-700"
              data-testid="chat-send-button"
            >
              {sending ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ChatInterface;
