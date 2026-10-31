import React, { useState, useRef, useEffect } from 'react';
import {
  Sparkles,
  Send,
  User,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  AlertCircle,
  ExternalLink,
  Edit2,
  Check,
  HelpCircle,
  Clock,
  RotateCcw,
} from 'lucide-react';
import { api } from '../utils/api';
import { ChatClaim, ChatResponse } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { useAuth } from '../hooks/useAuth';
import { useTranslation } from '../i18n';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  claims?: ChatClaim[];
  suggestedRecordIds?: string[];
  profileExtracted?: Record<string, any>;
}

export const Assistant: React.FC = () => {
  const { user } = useAuth();
  const { language, t } = useTranslation();

  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      sender: 'assistant',
      text: t('assistant.welcome'),
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => 'sess_' + Math.random().toString(36).substring(2, 9));

  // Extracted profile panel
  const [confirmedProfile, setConfirmedProfile] = useState<Record<string, any>>(() => {
    return user?.profile_data || {};
  });
  const [editingProfile, setEditingProfile] = useState(false);
  const [showHowItWorks, setShowHowItWorks] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (messageText?: string) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || loading) return;

    const userMsgId = 'msg_' + Date.now();
    const userMsg: Message = {
      id: userMsgId,
      sender: 'user',
      text: textToSend.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.assistant.chat({
        message: textToSend.trim(),
        session_id: sessionId,
        language: language,
        profile: confirmedProfile,
      });

      // Update extracted profile if any
      if (res.profile_extracted && Object.keys(res.profile_extracted).length > 0) {
        setConfirmedProfile((prev) => ({ ...prev, ...res.profile_extracted }));
      }

      const asstMsg: Message = {
        id: 'asst_' + Date.now(),
        sender: 'assistant',
        text: res.reply,
        claims: res.claims,
        suggestedRecordIds: res.suggested_records,
        profileExtracted: res.profile_extracted,
      };

      setMessages((prev) => [...prev, asstMsg]);
    } catch (err: any) {
      const errorMsg: Message = {
        id: 'err_' + Date.now(),
        sender: 'assistant',
        text: 'Sorry, I encountered an error connecting to the service. Please try again or explore schemes directly via the Schemes & Services directory.',
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleUseDemoProfile = () => {
    const demoQuery =
      language === 'pa'
        ? 'ਮੈਂ ਪੰਜਾਬ ਤੋਂ 20 ਸਾਲਾ ਐੱਸ.ਸੀ. ਵਿਦਿਆਰਥੀ ਹਾਂ ਅਤੇ ਮੇਰੇ ਪਰਿਵਾਰ ਦੀ ਸਾਲਾਨਾ ਆਮਦਨ 2 ਲੱਖ ਰੁਪਏ ਹੈ। ਮੇਰੇ ਲਈ ਕਿਹੜੀਆਂ ਸਕੀਮਾਂ ਹਨ?'
        : language === 'hi'
        ? 'मैं पंजाब से 20 वर्षीय एससी छात्र हूं और परिवार की वार्षिक आय 2 लाख रुपये है। मुझे किन योजनाओं का लाभ मिल सकता है?'
        : 'I am a 20-year-old SC student from Punjab with a family income of 2 lakh. What schemes can I apply for?';

    setInput(demoQuery);
    handleSend(demoQuery);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Top Banner for retrieval-only mode or info */}
      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-2xl flex items-center justify-between gap-3 text-xs text-blue-900">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-blue-600 shrink-0" />
          <span>
            <strong>Grounded Agentic Workflow:</strong> Multi-step reasoning with facts validated directly against official government documents.
          </span>
        </div>
        <button
          onClick={handleUseDemoProfile}
          className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shrink-0 shadow-sm transition"
        >
          {t('assistant.demo_button')}
        </button>
      </div>

      {/* Extracted Profile Panel */}
      {Object.keys(confirmedProfile).length > 0 && (
        <div className="mb-4 p-4 bg-white rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
              <User className="w-3.5 h-3.5 text-blue-600" />
              {t('assistant.understood_title')}
            </span>
            <button
              onClick={() => setEditingProfile(!editingProfile)}
              className="text-[11px] text-blue-600 hover:underline flex items-center gap-1 font-semibold"
            >
              <Edit2 className="w-3 h-3" />
              {editingProfile ? 'Done Editing' : 'Edit profile'}
            </button>
          </div>

          <div className="flex flex-wrap gap-2 text-xs">
            {confirmedProfile.age && (
              <span className="px-2.5 py-1 bg-slate-100 rounded-lg text-slate-700 font-medium">
                Age: <strong>{confirmedProfile.age}</strong>
              </span>
            )}
            {confirmedProfile.state && (
              <span className="px-2.5 py-1 bg-slate-100 rounded-lg text-slate-700 font-medium">
                State: <strong>{confirmedProfile.state}</strong>
              </span>
            )}
            {confirmedProfile.annual_family_income && (
              <span className="px-2.5 py-1 bg-slate-100 rounded-lg text-slate-700 font-medium">
                Income: <strong>₹{confirmedProfile.annual_family_income.toLocaleString('en-IN')}</strong>
              </span>
            )}
            {confirmedProfile.occupation && (
              <span className="px-2.5 py-1 bg-slate-100 rounded-lg text-slate-700 font-medium capitalize">
                Occupation: <strong>{confirmedProfile.occupation}</strong>
              </span>
            )}
            {confirmedProfile.category && (
              <span className="px-2.5 py-1 bg-slate-100 rounded-lg text-slate-700 font-medium">
                Category: <strong>{confirmedProfile.category}</strong>
              </span>
            )}
            {confirmedProfile.gender && (
              <span className="px-2.5 py-1 bg-slate-100 rounded-lg text-slate-700 font-medium capitalize">
                Gender: <strong>{confirmedProfile.gender}</strong>
              </span>
            )}
          </div>
        </div>
      )}

      {/* Chat Messages Container */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm flex flex-col h-[560px]">
        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex gap-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.sender === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-sm">
                  CA
                </div>
              )}

              <div
                className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'bg-slate-50 border border-slate-200 text-slate-800'
                }`}
              >
                <div className="whitespace-pre-line">{msg.text}</div>

                {/* Grounded Claims & Citations */}
                {msg.claims && msg.claims.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-slate-200 space-y-1.5">
                    <span className="text-[11px] font-bold text-slate-700 block">
                      {t('assistant.citations_title')}
                    </span>
                    {msg.claims.map((claim, idx) => (
                      <div
                        key={idx}
                        className="text-[11px] bg-white p-2 rounded-lg border border-slate-200 text-slate-600 flex items-start gap-1.5"
                      >
                        <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <div className="flex-1">
                          <span>{claim.text}</span>
                          {claim.source_url && (
                            <a
                              href={claim.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline block mt-0.5 font-medium"
                            >
                              Official Portal Link ↗
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {msg.sender === 'user' && (
                <div className="w-8 h-8 rounded-xl bg-slate-800 text-white flex items-center justify-center font-bold text-xs shrink-0 shadow-sm">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3 items-center">
              <div className="w-8 h-8 rounded-xl bg-blue-600 text-white flex items-center justify-center font-bold text-xs shrink-0">
                CA
              </div>
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-2xl text-xs text-slate-500 flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-600 animate-ping" />
                <span>Analyzing criteria, retrieving verified schemes, and validating citations...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Collapsible How It Works Drawer */}
        <div className="border-t border-slate-100 bg-slate-50 px-4 py-2 text-xs">
          <button
            onClick={() => setShowHowItWorks(!showHowItWorks)}
            className="flex items-center justify-between w-full text-slate-500 hover:text-slate-800"
          >
            <span className="font-semibold flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-blue-600" />
              How CitizenAssist answers (Agentic 5-Step Pipeline)
            </span>
            {showHowItWorks ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {showHowItWorks && (
            <div className="mt-2 pt-2 border-t border-slate-200 text-[11px] text-slate-600 space-y-1">
              <p><strong>1. Understand:</strong> Extracts profile criteria (age, state, income, caste, student status) without hallucinating missing fields.</p>
              <p><strong>2. Retrieve:</strong> Hybrid search runs FTS5 keyword matching and dense vector similarity over official documents.</p>
              <p><strong>3. Assess:</strong> Deterministic eligibility engine calculates MET/NOT_MET criteria strictly with certified rules.</p>
              <p><strong>4. Compose:</strong> Structured prompt with untrusted data delimiters produces grounded answers in your language.</p>
              <p><strong>5. Validate:</strong> Audits citations against stored sources, removing ungrounded claims.</p>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-3 sm:p-4 border-t border-slate-200 bg-white rounded-b-3xl">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={t('assistant.placeholder')}
              className="flex-1 px-4 py-3 bg-slate-50 border border-slate-300 rounded-xl text-xs sm:text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-5 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white font-semibold rounded-xl text-xs shadow-md transition flex items-center gap-1.5 shrink-0"
            >
              <span>{t('assistant.send')}</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
