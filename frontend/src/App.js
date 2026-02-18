import React, { useState, useEffect } from 'react';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [tasks, setTasks] = useState([]); // רשימת המשימות שתופיע בצד
  const [isLoading, setIsLoading] = useState(false);

  // פונקציה למשיכת המשימות מהשרת
  const fetchTasks = async () => {
    try {
      const response = await fetch('http://localhost:8000/tasks');
      const data = await response.json();
      setTasks(data.all_tasks || []);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  // משיכת משימות ראשונית כשהאפליקציה עולה
  useEffect(() => {
    fetchTasks();
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setIsLoading(true);
    const newMessages = [...messages, { role: 'user', text: input }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await response.json();
      setMessages([...newMessages, { role: 'bot', text: data.reply }]);
      
      // מיד אחרי שהבוט ענה, נעדכן את רשימת המשימות הצדדית
      fetchTasks();
    } catch (error) {
      setMessages([...newMessages, { role: 'bot', text: "שגיאה בחיבור לשרת..." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', backgroundColor: '#f0f2f5', fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif' }}>
      
    {/* רשימת משימות צדדית מעודכנת */}
<div style={{ width: '300px', backgroundColor: 'white', borderRight: '1px solid #ddd', padding: '20px', overflowY: 'auto' }}>
  <h2 style={{ color: '#008069' }}>המשימות שלי</h2>
  <ul style={{ listStyle: 'none', padding: 0 }}>
    {tasks.length === 0 ? <p style={{ color: '#888' }}>אין משימות כרגע...</p> : 
      tasks.map((task, index) => (
        <li key={index} style={{ 
          padding: '10px', 
          marginBottom: '8px', 
          backgroundColor: '#f8f9fa', 
          borderRadius: '5px',
          borderRight: '4px solid #008069',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          opacity: (task.status === 'completed' || task.status === 'done') ? 0.7 : 1 // קצת שקיפות למשימה שבוצעה
        }}>
          <div>
          <strong style={{ 
            textDecoration: (task.status === 'completed' || task.status === 'done') ? 'line-through' : 'none',
            color: (task.status === 'completed' || task.status === 'done') ? '#888' : 'black'
          }}>
            {task.title}
          </strong>
        </div>

        {/* ה-V המיוחל */}
        {(task.status === 'completed' || task.status === 'done') && (
          <span style={{ color: '#28a745', fontSize: '20px', fontWeight: 'bold' }}>✓</span>
        )}
      </li>
      ))
    }
  </ul>
</div>

      {/* אזור הצ'אט */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', maxWidth: '800px', margin: '0 auto', backgroundColor: '#e5ddd5', position: 'relative' }}>
        
        {/* גוף הצ'אט */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column' }}>
          {messages.map((msg, i) => (
            <div key={i} style={{ 
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.role === 'user' ? '#d9fdd3' : 'white',
              padding: '8px 15px',
              borderRadius: '10px',
              marginBottom: '10px',
              maxWidth: '70%',
              boxShadow: '0 1px 1px rgba(0,0,0,0.1)',
              position: 'relative',
              direction: 'rtl'
            }}>
              {msg.text}
            </div>
          ))}
          {isLoading && <div style={{ alignSelf: 'flex-start', backgroundColor: 'white', padding: '8px 15px', borderRadius: '10px', color: '#888' }}>מקליד...</div>}
        </div>

        {/* שורת קלט */}
        <div style={{ padding: '10px', backgroundColor: '#f0f2f5', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <input 
            value={input} 
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="הקלד הודעה..."
            style={{ flex: 1, padding: '12px', borderRadius: '25px', border: 'none', outline: 'none' }}
          />
          <button onClick={sendMessage} style={{ 
            backgroundColor: '#008069', 
            color: 'white', 
            border: 'none', 
            borderRadius: '50%', 
            width: '45px', 
            height: '45px', 
            cursor: 'pointer',
            fontSize: '20px'
          }}>
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;