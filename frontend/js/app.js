function studySyncApp() {
  const API_BASE = "[http://127.0.0.1:8000](http://127.0.0.1:8000)";

  return {
    activeTab: 'ingest',
    
    // Ingest Tab State
    newCourse: { title: '', description: '' },
    newTopic: { course_id: 1, title: '', content: '' },

    // Session Tab State
    sessionTopicId: 1,
    loadingSession: false,
    sessionData: null,
    userAnswers: {},

    // Flashcard Tab State
    newCard: { topic_id: 1, front: '', back: '' },
    activeCard: { id: 1, topic_id: 1, front: "What is Mitosis?", back: "Cell division resulting in two daughter cells." },
    showAnswer: false,

    // Life Balance State
    workload: { upcoming_assignments: 2, recent_study_hours: 4.0 },
    balanceData: null,

    async createCourse() {
      const res = await fetch(`${API_BASE}/courses/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.newCourse)
      });
      const data = await res.json();
      alert(`Course created with ID: ${data.id}`);
      this.newCourse = { title: '', description: '' };
    },

    async createTopic() {
      const res = await fetch(`${API_BASE}/courses/topics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.newTopic)
      });
      const data = await res.json();
      alert(`Topic embedded into ChromaDB with ID: ${data.topic_id}`);
      this.newTopic = { course_id: 1, title: '', content: '' };
    },

    async startSession() {
      this.loadingSession = true;
      try {
        const res = await fetch(`${API_BASE}/sessions/start`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ topic_id: this.sessionTopicId })
        });
        this.sessionData = await res.json();
      } catch (err) {
        alert("Failed to run session. Make sure topic ID exists and backend is running.");
      } finally {
        this.loadingSession = false;
      }
    },

    async createFlashcard() {
      const res = await fetch(`${API_BASE}/flashcards/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.newCard)
      });
      const data = await res.json();
      this.activeCard = data;
      alert("Flashcard created!");
    },

    async rateCard(quality) {
      if (!this.activeCard) return;
      const res = await fetch(`${API_BASE}/flashcards/${this.activeCard.id}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quality: quality })
      });
      const data = await res.json();
      alert(`Card updated with SM-2 algorithm. Next review: ${data.next_review}`);
      this.showAnswer = false;
    },

    async computeBalance() {
      const res = await fetch(`${API_BASE}/life-balance/compute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.workload)
      });
      this.balanceData = await res.json();
    },

    formatMarkdown(text) {
      if (!text) return '';
      return text.replace(/\n/g, '<br>');
    }
  }
}
