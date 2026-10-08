import React, { useState, useRef } from 'react';
import { 
  Activity, Heart, ActivitySquare, Brain, Droplets, 
  Calendar, FileText, User, ChevronRight, Loader2, 
  AlertCircle, CheckCircle2, Printer, ShieldAlert
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, Cell, ReferenceLine
} from 'recharts';

const INITIAL_FORM_DATA = {
  age: 45,
  gender: 'Male',
  bmi: 26.5,
  bpSys: 125,
  bpDia: 80,
  glucose: 105,
  cholesterol: 190,
  smoking: 'Never',
  alcohol: 'Occasional',
  exercise: 'Moderate (2-3 times/week)',
  symptoms: 'Occasional fatigue after meals, mild lower back ache.'
};

const DOCTORS = [
  { id: 1, name: 'Dr. Sarah Jenkins', spec: 'Cardiologist', rating: 4.9, slots: ['09:00 AM', '11:30 AM', '02:00 PM'] },
  { id: 2, name: 'Dr. Marcus Chen', spec: 'Endocrinologist', rating: 4.8, slots: ['10:00 AM', '01:00 PM', '03:30 PM'] },
  { id: 3, name: 'Dr. Emily Russo', spec: 'General Physician', rating: 4.9, slots: ['08:30 AM', '09:15 AM', '04:00 PM'] },
  { id: 4, name: 'Dr. Alistair Vance', spec: 'Nephrologist', rating: 4.7, slots: ['11:00 AM', '02:45 PM'] }
];

const analyzeHealthData = async (formData) => {
  const apiKey = ""; // Canvas provides this securely
  const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`;

  const prompt = `
    Act as an advanced medical AI assistant (for simulation purposes only). 
    Analyze the following patient profile and provide simulated predictive risk scores 
    for four conditions: Diabetes, Heart Disease, Liver Disease, and Kidney Failure.
    Also generate SHAP-like feature importance values explaining why the score is what it is (impact values from -10 to +10, where negative means it reduces risk, positive means it increases risk).
    
    Patient Profile:
    - Age: ${formData.age}, Gender: ${formData.gender}
    - Vitals: BMI ${formData.bmi}, BP ${formData.bpSys}/${formData.bpDia} mmHg, Fasting Glucose ${formData.glucose} mg/dL, Cholesterol ${formData.cholesterol} mg/dL
    - Lifestyle: Smoking: ${formData.smoking}, Alcohol: ${formData.alcohol}, Exercise: ${formData.exercise}
    - Symptoms: ${formData.symptoms}
  `;

  const payload = {
    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    generationConfig: {
      responseMimeType: "application/json",
      responseSchema: {
        type: "OBJECT",
        properties: {
          predictions: {
            type: "ARRAY",
            items: {
              type: "OBJECT",
              properties: {
                disease: { type: "STRING" },
                riskScore: { type: "NUMBER", description: "Score from 0 to 100" },
                status: { type: "STRING", description: "Low, Moderate, or High" },
                explanation: { type: "STRING" },
                shapValues: {
                  type: "ARRAY",
                  items: {
                    type: "OBJECT",
                    properties: {
                      feature: { type: "STRING" },
                      impact: { type: "NUMBER" }
                    }
                  }
                }
              }
            }
          },
          recommendations: {
            type: "ARRAY",
            items: { type: "STRING" }
          }
        }
      }
    }
  };

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) throw new Error("Failed to fetch prediction.");
    
    const data = await response.json();
    const resultText = data.candidates?.[0]?.content?.parts?.[0]?.text;
    if (resultText) {
      return JSON.parse(resultText);
    } else {
      throw new Error("Invalid response format.");
    }
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

const PatientForm = ({ formData, setFormData, onSubmit, isLoading }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <form onSubmit={handleFormSubmit} className="space-y-6 bg-white p-6 rounded-xl shadow-sm border border-slate-200">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Demographics */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-800 flex items-center"><User className="w-5 h-5 mr-2 text-blue-600"/> Demographics & Vitals</h3>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-1">Age</label>
              <input type="number" name="age" value={formData.age} onChange={handleChange} className="w-full p-2 border rounded-md" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-1">Gender</label>
              <select name="gender" value={formData.gender} onChange={handleChange} className="w-full p-2 border rounded-md">
                <option>Male</option><option>Female</option><option>Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-1">BMI</label>
              <input type="number" step="0.1" name="bmi" value={formData.bmi} onChange={handleChange} className="w-full p-2 border rounded-md" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-1">Fasting Glucose</label>
              <input type="number" name="glucose" value={formData.glucose} onChange={handleChange} className="w-full p-2 border rounded-md" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-1">Systolic BP</label>
              <input type="number" name="bpSys" value={formData.bpSys} onChange={handleChange} className="w-full p-2 border rounded-md" required />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600 mb-1">Diastolic BP</label>
              <input type="number" name="bpDia" value={formData.bpDia} onChange={handleChange} className="w-full p-2 border rounded-md" required />
            </div>
          </div>
        </div>

        {/* Lifestyle */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-slate-800 flex items-center"><ActivitySquare className="w-5 h-5 mr-2 text-blue-600"/> Lifestyle</h3>
          
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-1">Total Cholesterol (mg/dL)</label>
            <input type="number" name="cholesterol" value={formData.cholesterol} onChange={handleChange} className="w-full p-2 border rounded-md" required />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-1">Smoking Habit</label>
            <select name="smoking" value={formData.smoking} onChange={handleChange} className="w-full p-2 border rounded-md">
              <option>Never</option><option>Former</option><option>Current (Light)</option><option>Current (Heavy)</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-1">Alcohol Consumption</label>
            <select name="alcohol" value={formData.alcohol} onChange={handleChange} className="w-full p-2 border rounded-md">
              <option>None</option><option>Occasional</option><option>Moderate</option><option>Heavy</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-600 mb-1">Exercise Frequency</label>
            <select name="exercise" value={formData.exercise} onChange={handleChange} className="w-full p-2 border rounded-md">
              <option>Sedentary</option><option>Light (1-2 times/week)</option><option>Moderate (2-3 times/week)</option><option>Active (4+ times/week)</option>
            </select>
          </div>
        </div>
      </div>

      <div className="pt-4 border-t border-slate-100">
        <label className="block text-sm font-medium text-slate-600 mb-1">Current Symptoms / Additional Notes</label>
        <textarea name="symptoms" value={formData.symptoms} onChange={handleChange} rows={3} className="w-full p-2 border rounded-md" placeholder="Describe any current symptoms..."></textarea>
      </div>

      <div className="flex justify-end pt-4">
        <button 
          type="submit" 
          disabled={isLoading}
          className="flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors disabled:opacity-70"
        >
          {isLoading ? <Loader2 className="w-5 h-5 mr-2 animate-spin" /> : <Activity className="w-5 h-5 mr-2" />}
          {isLoading ? 'Analyzing Risk Profile...' : 'Run Diagnostics Analysis'}
        </button>
      </div>
    </form>
  );
};

const ShapChart = ({ data }) => {
  // Sort data by absolute impact for better visualization
  const sortedData = [...data].sort((a, b) => Math.abs(b.impact) - Math.abs(a.impact));

  return (
    <div className="h-64 w-full text-xs">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={sortedData} layout="vertical" margin={{ top: 5, right: 30, left: 60, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
          <XAxis type="number" domain={[-10, 10]} />
          <YAxis dataKey="feature" type="category" width={100} tick={{fill: '#475569'}} />
          <Tooltip 
            formatter={(value) => [value > 0 ? `+${value} (Increases Risk)` : `${value} (Reduces Risk)`, 'Impact Score']}
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
          />
          <ReferenceLine x={0} stroke="#94a3b8" />
          <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
            {sortedData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.impact > 0 ? '#ef4444' : '#22c55e'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const ResultsView = ({ results }) => {
  if (!results) return null;

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200';
      case 'moderate': return 'text-orange-600 bg-orange-50 border-orange-200';
      default: return 'text-green-600 bg-green-50 border-green-200';
    }
  };

  const getProgressColor = (score) => {
    if (score > 66) return 'bg-red-500';
    if (score > 33) return 'bg-orange-500';
    return 'bg-green-500';
  };

  return (
    <div className="space-y-8" id="printable-report">
      <div className="print:block hidden mb-8 pb-4 border-b-2 border-slate-800">
        <h1 className="text-3xl font-bold text-slate-800 flex items-center">
          <ActivitySquare className="w-8 h-8 mr-3 text-blue-600" />
          MedAI Health Risk Assessment
        </h1>
        <p className="text-slate-500 mt-2">Generated on {new Date().toLocaleDateString()}</p>
        <p className="text-sm mt-4 text-red-600 font-medium">DISCLAIMER: This is an AI simulation. Not for medical diagnostic use.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {results.predictions.map((pred, idx) => (
          <div key={idx} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex flex-col print:break-inside-avoid">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-slate-800">{pred.disease}</h3>
              <span className={`px-3 py-1 rounded-full text-sm font-semibold border ${getStatusColor(pred.status)}`}>
                {pred.status} Risk
              </span>
            </div>
            
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-1 text-slate-600 font-medium">
                <span>Risk Score</span>
                <span>{pred.riskScore}/100</span>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-3">
                <div className={`h-3 rounded-full ${getProgressColor(pred.riskScore)}`} style={{ width: `${pred.riskScore}%` }}></div>
              </div>
            </div>

            <p className="text-slate-600 text-sm mb-6 flex-grow">{pred.explanation}</p>

            <div className="mt-auto">
              <h4 className="text-sm font-semibold text-slate-700 mb-2 flex items-center">
                <Brain className="w-4 h-4 mr-1.5 text-indigo-500"/> AI Feature Analysis (SHAP)
              </h4>
              <div className="bg-slate-50 rounded-lg p-2 border border-slate-100">
                <ShapChart data={pred.shapValues} />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-blue-50 rounded-xl p-6 border border-blue-100 print:break-inside-avoid">
        <h3 className="text-lg font-bold text-blue-900 mb-4 flex items-center">
          <ShieldAlert className="w-5 h-5 mr-2" />
          AI Lifestyle Recommendations
        </h3>
        <ul className="space-y-3">
          {results.recommendations.map((rec, idx) => (
            <li key={idx} className="flex items-start">
              <CheckCircle2 className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0 mt-0.5" />
              <span className="text-blue-800">{rec}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

const AppointmentBooking = () => {
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [isBooked, setIsBooked] = useState(false);

  const handleBook = () => {
    if (selectedDoc && selectedSlot) {
      setIsBooked(true);
      setTimeout(() => {
        setIsBooked(false);
        setSelectedDoc(null);
        setSelectedSlot(null);
      }, 3000);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center">
        <Calendar className="w-6 h-6 mr-2 text-blue-600" />
        Consult a Specialist
      </h2>

      {isBooked ? (
        <div className="bg-green-50 text-green-800 p-6 rounded-lg border border-green-200 text-center animate-fade-in">
          <CheckCircle2 className="w-12 h-12 text-green-500 mx-auto mb-3" />
          <h3 className="text-xl font-bold mb-2">Appointment Confirmed!</h3>
          <p>Your consultation has been successfully scheduled.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Available Doctors</h3>
            {DOCTORS.map(doc => (
              <div 
                key={doc.id}
                onClick={() => { setSelectedDoc(doc); setSelectedSlot(null); }}
                className={`p-4 rounded-lg border cursor-pointer transition-all ${selectedDoc?.id === doc.id ? 'border-blue-500 bg-blue-50 shadow-md' : 'border-slate-200 hover:border-blue-300 hover:bg-slate-50'}`}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <h4 className="font-bold text-slate-800">{doc.name}</h4>
                    <p className="text-sm text-slate-500">{doc.spec}</p>
                  </div>
                  <div className="flex items-center text-sm font-medium text-amber-500 bg-amber-50 px-2 py-1 rounded">
                    ★ {doc.rating}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div>
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">
              {selectedDoc ? `Available Slots for ${selectedDoc.name}` : 'Select a doctor to view slots'}
            </h3>
            
            {selectedDoc ? (
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-3">
                  {selectedDoc.slots.map(slot => (
                    <button
                      key={slot}
                      onClick={() => setSelectedSlot(slot)}
                      className={`p-3 rounded-lg border font-medium text-sm transition-all ${selectedSlot === slot ? 'border-blue-600 bg-blue-600 text-white' : 'border-slate-200 text-slate-700 hover:border-blue-400'}`}
                    >
                      {slot}
                    </button>
                  ))}
                </div>

                {selectedSlot && (
                  <button 
                    onClick={handleBook}
                    className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold shadow-lg transition-colors flex items-center justify-center"
                  >
                    Confirm Booking for {selectedSlot}
                  </button>
                )}
              </div>
            ) : (
              <div className="h-full min-h-[200px] flex flex-col items-center justify-center text-slate-400 border-2 border-dashed border-slate-200 rounded-xl p-6 text-center">
                <User className="w-12 h-12 mb-3 text-slate-300" />
                <p>Please select a specialist from the list to view their availability.</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState('form');
  const [formData, setFormData] = useState(INITIAL_FORM_DATA);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRunAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await analyzeHealthData(formData);
      setResults(data);
      setActiveTab('results');
    } catch (err) {
      setError("Analysis failed. Please check your network connection and try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200 selection:text-blue-900">
      {/* Top Navigation */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 print:hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <ActivitySquare className="w-8 h-8 text-blue-600" />
            <span className="font-bold text-xl tracking-tight text-slate-800">MedAI Diagnostics</span>
          </div>
          
          <div className="flex space-x-1">
            <button 
              onClick={() => setActiveTab('form')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${activeTab === 'form' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-100'}`}
            >
              Patient Profile
            </button>
            <button 
              onClick={() => setActiveTab('results')}
              disabled={!results}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${!results ? 'opacity-50 cursor-not-allowed' : activeTab === 'results' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-100'}`}
            >
              Risk Analysis
            </button>
            <button 
              onClick={() => setActiveTab('appointments')}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${activeTab === 'appointments' ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-100'}`}
            >
              Book Specialist
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 print:p-0 print:m-0">
        
        {/* Error Banner */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 flex items-center print:hidden">
            <AlertCircle className="w-5 h-5 mr-2" />
            <p>{error}</p>
          </div>
        )}

        {/* Tab Content */}
        <div className="print:block">
          {activeTab === 'form' && (
            <div className="max-w-4xl mx-auto animate-fade-in print:hidden">
              <div className="mb-6">
                <h1 className="text-2xl font-bold text-slate-800">Patient Intake Profile</h1>
                <p className="text-slate-500 mt-1">Enter current patient vitals and lifestyle habits to run the predictive multi-disease model.</p>
              </div>
              <PatientForm 
                formData={formData} 
                setFormData={setFormData} 
                onSubmit={handleRunAnalysis} 
                isLoading={isLoading} 
              />
            </div>
          )}

          {activeTab === 'results' && results && (
            <div className="animate-fade-in print:block">
              <div className="flex justify-between items-center mb-6 print:hidden">
                <div>
                  <h1 className="text-2xl font-bold text-slate-800">Diagnostic Risk Analysis</h1>
                  <p className="text-slate-500 mt-1">AI-generated predictive modeling based on current profile.</p>
                </div>
                <div className="flex space-x-3">
                  <button 
                    onClick={handlePrint}
                    className="flex items-center px-4 py-2 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-lg font-medium transition-colors shadow-sm"
                  >
                    <Printer className="w-4 h-4 mr-2" />
                    Download PDF
                  </button>
                  <button 
                    onClick={() => setActiveTab('appointments')}
                    className="flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors shadow-sm"
                  >
                    Book Specialist <ChevronRight className="w-4 h-4 ml-1" />
                  </button>
                </div>
              </div>
              <ResultsView results={results} />
            </div>
          )}

          {activeTab === 'appointments' && (
            <div className="max-w-4xl mx-auto animate-fade-in print:hidden">
              <div className="mb-6">
                <h1 className="text-2xl font-bold text-slate-800">Clinical Integration</h1>
                <p className="text-slate-500 mt-1">Based on the risk analysis, schedule a follow-up with the appropriate specialist.</p>
              </div>
              <AppointmentBooking />
            </div>
          )}
        </div>
      </main>

      {/* Footer / Disclaimer */}
      <footer className="mt-12 py-6 text-center text-slate-500 text-sm print:hidden border-t border-slate-200">
        <p className="max-w-3xl mx-auto">
          <strong>Disclaimer:</strong> This application is a simulated demonstration. The predictions and SHAP values are generated by a Large Language Model for illustrative purposes and do not represent actual diagnostic output from validated ML models. Do not use for real medical decisions.
        </p>
      </footer>
    </div>
  );
}