import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
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
  FileText,
  CheckCircle2,
} from 'lucide-react';
import { api } from '../utils/api';
import { AssistantStepInfo, ChatClaim, ChatResponse, SchemeRecord } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { useAuth } from '../hooks/useAuth';
import { useTranslation } from '../i18n';

const AI_SKILLS = [
  {
    id: 'eligibility',
    label: '⚡ Eligibility Audit',
    query: (lang: string) =>
      lang === 'pa'
        ? 'ਮੇਰੇ ਮੌਜੂਦਾ ਪ੍ਰੋਫਾਈਲ ਦੇ ਆਧਾਰ ਤੇ ਸਾਰੀਆਂ ਯੋਗ ਸਕੀਮਾਂ ਦਾ ਪੂਰਾ ਯੋਗਤਾ ਨਿਰੀਖਣ ਕਰੋ।'
        : lang === 'hi'
        ? 'मेरी वर्तमान प्रोफ़ाइल के आधार पर सभी योजनाओं के लिए मेरी पूर्ण पात्रता की विस्तृत जाँच करें।'
        : 'Perform a comprehensive eligibility audit across all schemes for my current profile, specifying met and unmet criteria.',
  },
  {
    id: 'checklist',
    label: '📋 Document Checklist',
    query: (lang: string) =>
      lang === 'pa'
        ? 'ਮੇਰੇ ਲਈ ਯੋਗ ਸਕੀਮਾਂ ਲਈ ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼ਾਂ ਅਤੇ ਸਰਟੀਫਿਕੇਟਾਂ ਦੀ ਪੂਰੀ ਚੈੱਕਲਿਸਟ ਤਿਆਰ ਕਰੋ।'
        : lang === 'hi'
        ? 'मेरी पात्र योजनाओं के लिए आवश्यक प्रमाण पत्रों और दस्तावेज़ों की विस्तृत चेकलिस्ट तैयार करें।'
        : 'Generate a complete, prioritized document checklist with issuing authorities and verification prerequisites for my eligible schemes.',
  },
  {
    id: 'roadmap',
    label: '🚀 Application Roadmap',
    query: (lang: string) =>
      lang === 'pa'
        ? 'ਸਰਕਾਰੀ ਪੋਰਟਲ ਤੇ ਅਪਲਾਈ ਕਰਨ ਲਈ ਕਦਮ-ਦਰ-ਕਦਮ ਰੋਡਮੈਪ ਦੱਸੋ।'
        : lang === 'hi'
        ? 'आधिकारिक सरकारी पोर्टल्स पर आवेदन करने के लिए चरण-दर-चरण रोडमैप बताएं।'
        : 'Provide an exact step-by-step application roadmap for applying on official portals for my eligible schemes.',
  },
  {
    id: 'certificates',
    label: '🏛️ Certificate Guide',
    query: (lang: string) =>
      lang === 'pa'
        ? 'ਪੰਜਾਬ ਵਿੱਚ ਜਾਤੀ, ਆਮਦਨ ਅਤੇ ਰਿਹਾਇਸ਼ ਸਰਟੀਫਿਕੇਟ ਕਿਵੇਂ ਅਤੇ ਕਿੱਥੋਂ ਬਣਵਾਏ ਜਾ ਸਕਦੇ ਹਨ?'
        : lang === 'hi'
        ? 'जाति प्रमाण पत्र, आय प्रमाण पत्र और निवास प्रमाण पत्र कैसे और कहाँ से बनवाएं?'
        : 'How and where can I apply for digital Caste Certificate, Income Certificate, and Domicile Certificate in Punjab?',
  },
  {
    id: 'compare',
    label: '⚖️ Compare Top Schemes',
    query: (lang: string) =>
      lang === 'pa'
        ? 'ਮੇਰੇ ਪ੍ਰੋਫਾਈਲ ਮੁਤਾਬਕ ਸਭ ਤੋਂ ਵਧੀਆ ਸਕੀਮਾਂ ਦੇ ਲਾਭਾਂ ਅਤੇ ਸ਼ਰਤਾਂ ਦੀ ਆਪਸ ਵਿੱਚ ਤੁਲਨਾ ਕਰੋ।'
        : lang === 'hi'
        ? 'मेरी प्रोफ़ाइल के अनुसार शीर्ष योजनाओं के लाभों और शर्तों की आपस में तुलना करें।'
        : 'Compare the top welfare schemes matching my profile, highlighting differences in benefits, income limits, and disbursement modes.',
  },
];

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  claims?: ChatClaim[];
  suggestedRecordIds?: string[];
  profileExtracted?: Record<string, any>;
  steps?: AssistantStepInfo;
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
  const [recordsMap, setRecordsMap] = useState<Record<string, SchemeRecord>>({});

  useEffect(() => {
    api.records.list().then((res) => {
      const map: Record<string, SchemeRecord> = {};
      res.records.forEach((r) => {
        map[r.id] = r;
      });
      setRecordsMap(map);
    }).catch((err) => {
      console.error('Failed to load records map:', err);
    });
  }, []);

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
        steps: res.steps,
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
                  <div className="mt-3 pt-3 border-t border-slate-200 space-y-2">
                    <span className="text-[11px] font-bold text-slate-700 block">
                      {t('assistant.citations_title')}
                    </span>
                    {msg.claims.map((claim, idx) => (
                      <div
                        key={idx}
                        className="text-[11px] bg-white p-2.5 rounded-xl border border-slate-200 text-slate-700 flex items-start gap-2 shadow-xs"
                      >
                        <ShieldCheck className={`w-3.5 h-3.5 mt-0.5 shrink-0 ${
                          claim.label === 'verified' ? 'text-emerald-600' : claim.label === 'inferred' ? 'text-amber-500' : 'text-slate-400'
                        }`} />
                        <div className="flex-1">
                          <div className="flex items-center gap-1.5 mb-0.5">
                            <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider ${
                              claim.label === 'verified'
                                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                : claim.label === 'inferred'
                                ? 'bg-amber-50 text-amber-700 border border-amber-200'
                                : 'bg-slate-100 text-slate-600 border border-slate-200'
                            }`}>
                              {claim.label || (claim.verified ? 'verified' : 'inferred')}
                            </span>
                            {claim.source_title && (
                              <span className="text-[10px] text-slate-500 font-medium truncate max-w-[200px]">
                                {claim.source_title}
                              </span>
                            )}
                          </div>
                          <div className="text-slate-800 leading-snug">{claim.text}</div>
                          {claim.source_url && (
                            <a
                              href={claim.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline inline-flex items-center gap-1 mt-1 font-semibold text-[10px]"
                            >
                              <span>Official Verification Source</span>
                              <ExternalLink className="w-2.5 h-2.5" />
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {/* Interactive Recommended Scheme Action Cards */}
                {msg.suggestedRecordIds && msg.suggestedRecordIds.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-slate-200 space-y-2">
                    <span className="text-[11px] font-bold text-slate-700 flex items-center gap-1.5">
                      <FileText className="w-3.5 h-3.5 text-blue-600" />
                      Recommended Verified Schemes & Services
                    </span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {msg.suggestedRecordIds.map((recId) => {
                        const rec = recordsMap[recId];
                        if (!rec) return null;
                        return (
                          <div
                            key={recId}
                            className="p-3 bg-white rounded-xl border border-slate-200 text-slate-800 shadow-2xs hover:border-blue-300 transition flex flex-col justify-between"
                          >
                            <div>
                              <div className="flex items-center justify-between gap-1 mb-1">
                                <span className="font-bold text-[11px] text-slate-900 truncate">
                                  {rec.name}
                                </span>
                                <span className="px-1.5 py-0.5 rounded text-[8px] font-semibold bg-blue-50 text-blue-700 uppercase tracking-wider shrink-0">
                                  {rec.record_type}
                                </span>
                              </div>
                              {rec.benefits && (
                                <p className="text-[10px] text-slate-600 line-clamp-2 mb-2 leading-relaxed">
                                  {rec.benefits}
                                </p>
                              )}
                            </div>
                            <div className="flex items-center gap-2 pt-2 border-t border-slate-100 text-[10px]">
                              <Link
                                to={`/schemes/${rec.id}`}
                                className="text-blue-600 hover:underline font-semibold"
                              >
                                View Details
                              </Link>
                              <span className="text-slate-300">•</span>
                              <Link
                                to={`/checklist`}
                                className="text-emerald-700 hover:underline font-semibold"
                              >
                                Checklist
                              </Link>
                              {rec.application_url && (
                                <>
                                  <span className="text-slate-300">•</span>
                                  <a
                                    href={rec.application_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-slate-600 hover:underline inline-flex items-center gap-0.5"
                                  >
                                    Portal <ExternalLink className="w-2.5 h-2.5" />
                                  </a>
                                </>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Per-Message "How I got this answer" Drawer */}
                {msg.steps && (
                  <details className="mt-2 text-[11px] text-slate-600 bg-white/70 rounded-xl p-2 border border-slate-200">
                    <summary className="cursor-pointer font-semibold text-blue-700 hover:text-blue-800">
                      How I got this answer (Verified Pipeline)
                    </summary>
                    <div className="mt-2 space-y-1.5 pt-1.5 border-t border-slate-100 text-[10px]">
                      {msg.steps.understood && Object.keys(msg.steps.understood).length > 0 && (
                        <div>
                          <strong>1. Understood Profile:</strong>{' '}
                          {Object.entries(msg.steps.understood).map(([k, v]) => `${k}: ${v}`).join(', ')}
                        </div>
                      )}
                      {msg.steps.retrieved && msg.steps.retrieved.length > 0 && (
                        <div>
                          <strong>2. Verified Records Retrieved:</strong>{' '}
                          {msg.steps.retrieved.join(', ')}
                        </div>
                      )}
                      {msg.steps.assessed && msg.steps.assessed.length > 0 && (
                        <div>
                          <strong>3. Deterministic Assessment:</strong>
                          <ul className="list-disc pl-4 space-y-0.5 mt-0.5">
                            {msg.steps.assessed.map((a, i) => (
                              <li key={i}>{a.record_name}: {a.status} - {a.message}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </details>
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

        {/* AI Skills Action Bar */}
        <div className="px-3 sm:px-4 py-2.5 bg-slate-50/80 border-t border-slate-100 flex items-center gap-1.5 overflow-x-auto">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider shrink-0 flex items-center gap-1 mr-1">
            <Sparkles className="w-3 h-3 text-blue-600" />
            AI Skills:
          </span>
          {AI_SKILLS.map((skill) => (
            <button
              key={skill.id}
              type="button"
              disabled={loading}
              onClick={() => handleSend(skill.query(language))}
              className="px-2.5 py-1 text-[11px] font-medium bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-700 border border-slate-200 hover:border-blue-300 rounded-lg whitespace-nowrap shadow-2xs transition shrink-0 disabled:opacity-50"
            >
              {skill.label}
            </button>
          ))}
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
