# J.A.R.V.I.S. – AI-Powered Mental Health Assistant 🧠🎵💚

**A comprehensive therapeutic AI system designed for clinical and mental health applications**

JARVIS leverages the intersection of **Telegram**, **Spotify**, and **Ollama** AI automation to create a connected therapeutic entity that provides:

- 🧠 **Advanced Emotion Analysis** using Ollama LLM for precise emotional state detection
- 📚 **Evidence-Based Therapeutic Content** from philosophical texts and psychology literature
- 🎵 **Music Therapy Integration** via Spotify for emotion regulation and mood enhancement
- 💬 **24/7 Accessible Support** through Telegram bot interface
- 🔄 **Real-time Emotion Regulation** with personalized comforting responses
- 📊 **Clinical Data Tracking** for mental health monitoring and progress assessment
- 🎯 **Preventive Mental Health Care** through proactive emotional wellbeing support

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create conda environment
conda create -n jarvis_env python=3.9
conda activate jarvis_env

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create `.env` file:
```bash
# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Telegram Bot
TELEGRAM_BOT_TOKEN_PHILOSOPHY=your_telegram_bot_token

# Spotify (Optional - will use simulation mode if not configured)
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8080/callback
```

### 3. Run JARVIS
```bash
python bot_launcher.py
```

## 📁 Project Structure

```
J.A.R.V.I.S/
├── main.py                   # Core JARVIS logic
├── bot_launcher.py           # Bot launcher
├── analyze_emotions.py       # Data analysis & visualization
├── src/
│   ├── telegram_bot.py      # Telegram integration
│   ├── commonconst.py       # All configuration (no hardcoding)
│   ├── application/
│   │   ├── mood_analyzer.py    # Emotion detection
│   │   ├── philosopher.py      # Philosophy matching
│   │   ├── music_player.py     # Real Spotify integration
│   │   └── db_manager.py       # Comprehensive logging
│   ├── interaction/music_mood/
│   │   └── music_vs_mood.py    # Music-emotion matching
│   └── book/                   # Philosophy books (JSON)
│       ├── analects.json
│       ├── iching.json
│       ├── mencius.json
│       ├── positive_psy.json
│       ├── social_psy.json
│       └── tao_te_ching.json
└── db/
    ├── emotion_logs.db         # Comprehensive emotion logging
    ├── emotion_history.csv     # Exportable data
    └── emotion_analysis.png    # Visualization charts
```

## 🔄 Therapeutic Process & Emotion Regulation

### Core Therapeutic Workflow
1. **Emotional State Assessment**: User shares feelings via Telegram interface
2. **AI-Powered Analysis**: Ollama LLM performs deep emotional analysis and pattern recognition
3. **Therapeutic Content Matching**: AI selects evidence-based philosophical and psychological content
4. **Personalized Response Generation**: Creates comforting, therapeutic responses tailored to individual needs
5. **Music Therapy Integration**: Automatically curates and plays emotion-regulating music via Spotify
6. **Progress Tracking**: Logs emotional patterns for clinical monitoring and wellbeing assessment

### Mental Health Features
- **Crisis Detection**: Identifies emotional distress patterns and provides immediate support
- **Mood Stabilization**: Uses philosophical wisdom and music therapy for emotional balance
- **Cognitive Behavioral Support**: Integrates CBT principles through philosophical teachings
- **Mindfulness Integration**: Incorporates meditation and mindfulness practices from ancient texts
- **Therapeutic Relationship**: Builds consistent, supportive AI-human interaction patterns

## 🤖 AI Automation & Connected Entity Framework

### Intelligent Connection Architecture
JARVIS operates as a **connected therapeutic entity** that seamlessly integrates three powerful platforms:

#### 🔗 **Telegram ↔ Ollama ↔ Spotify Integration**
- **Telegram Interface**: Secure, accessible mental health communication channel
- **Ollama LLM Engine**: Advanced natural language processing for emotional analysis and therapeutic response generation  
- **Spotify Music Therapy**: Automated playlist curation and playback for emotion regulation

### Automated Therapeutic Workflows
- **Real-Time Emotion Detection**: Instant analysis of user messages for emotional state assessment
- **Dynamic Content Selection**: AI automatically selects most appropriate philosophical and psychological content
- **Seamless Music Integration**: Automatic playlist generation and device playback without user intervention
- **Continuous Learning**: System adapts and improves therapeutic responses based on user interactions
- **Proactive Wellness Monitoring**: Automated check-ins and early intervention triggers

### Connected Entity Benefits
- **Unified Experience**: Single interface accessing multiple therapeutic modalities
- **Contextual Awareness**: AI maintains conversation history and emotional patterns across sessions
- **Predictive Support**: Anticipates user needs based on historical data and current emotional state
- **Multi-Modal Therapy**: Combines text, music, and philosophical wisdom for comprehensive support
- **24/7 Availability**: Continuous mental health support without human therapist limitations

## 🎵 Advanced Music Therapy Integration

### Spotify Therapeutic Features:
- **Emotion-Responsive Playlists**: AI curates music based on current emotional state and therapeutic goals
- **Automatic Device Detection**: Seamlessly plays on user's preferred Spotify-connected devices
- **Mood Progression Tracking**: Monitors how music affects emotional state over time
- **Therapeutic Music Library**: Curated collection of clinically-proven mood-regulating music
- **Real-Time Adaptation**: Adjusts music selection based on user feedback and emotional response

### Integration Modes:
- **Full Integration**: Complete Spotify control with playlist creation and device management
- **Simulation Mode**: Therapeutic music recommendations when Spotify credentials unavailable
- **Hybrid Mode**: Combines real playback with therapeutic guidance and music education

## 📚 Philosophy Books Included

- **Analects** - Confucian wisdom
- **I Ching** - Ancient Chinese divination
- **Mencius** - Confucian philosophy
- **Tao Te Ching** - Taoist philosophy
- **Positive Psychology** - Modern psychological concepts
- **Social Psychology** - Social behavior insights

## 💡 Clinical Application Examples

### Example 1: Anxiety Management
**User**: "I feel overwhelmed and stressed about my upcoming presentation"

**JARVIS Therapeutic Response**:
- 🧠 **Emotional Analysis**: Anxiety with performance-related stress patterns
- 📚 **Therapeutic Wisdom**: *"The superior man is modest in his speech but exceeds in his actions" - Analects*
- 🎵 **Music Therapy**: Calming instrumental playlist automatically playing on your device
- 💚 **Regulation Technique**: Guided breathing exercise and confidence-building affirmations
- 📊 **Progress Note**: Anxiety episode logged for pattern analysis

### Example 2: Depression Support
**User**: "I feel hopeless and don't see the point in anything"

**JARVIS Therapeutic Response**:
- 🧠 **Crisis Assessment**: Depressive episode detected, supportive intervention initiated
- 📚 **Healing Wisdom**: *"Even the darkest night will end and the sun will rise" - Positive Psychology*
- 🎵 **Mood Elevation**: Uplifting, hope-inspiring playlist curated for gradual mood improvement
- 💚 **Immediate Support**: Crisis resources provided, encouragement for professional help if needed
- 📊 **Clinical Alert**: Mood pattern flagged for healthcare provider review

### Example 3: Stress Regulation
**User**: "Work is overwhelming me, I can't cope anymore"

**JARVIS Therapeutic Response**:
- 🧠 **Stress Analysis**: Chronic stress indicators, burnout risk assessment
- 📚 **Coping Strategy**: *"Flow with whatever may happen and let your mind be free" - Tao Te Ching*
- 🎵 **Stress Relief**: Nature sounds and meditation music for immediate calming
- 💚 **Wellness Plan**: Personalized stress management techniques and boundary-setting advice
- 📊 **Wellbeing Tracking**: Stress levels monitored for preventive care recommendations

## 📊 Clinical Data & Mental Health Analytics

### Therapeutic Commands Available:
- `/status` - View comprehensive mental health statistics and emotional patterns
- `/export` - Export detailed emotion history for clinical review
- `/wellness_report` - Generate personalized wellbeing assessment
- `/crisis_log` - Access crisis intervention history and patterns
- `python analyze_emotions.py` - Create clinical visualization charts and trend analysis

### Clinical Data Tracking:
- **Emotional Patterns**: Detailed timestamp and emotional state progression
- **Therapeutic Interventions**: Record of philosophical content and music therapy used
- **Response Effectiveness**: User feedback and emotional improvement metrics
- **Crisis Indicators**: Early warning signs and intervention success rates
- **Wellbeing Trends**: Long-term mental health trajectory analysis
- **Treatment Compliance**: Engagement patterns and therapeutic relationship quality
- **Personalization Data**: Individual preferences and effective intervention strategies

### Mental Health Monitoring Features:
- **Risk Assessment**: Automated detection of concerning emotional patterns
- **Progress Tracking**: Quantifiable improvement metrics over time
- **Intervention Analytics**: Effectiveness analysis of different therapeutic approaches
- **Predictive Insights**: Early identification of potential mental health episodes
- **Clinical Integration**: Export-ready data for healthcare provider collaboration

## 🛠️ AI Automation & Integration Architecture

### Core Technical Features:
- **Advanced Semantic Matching**: Sentence transformers for intelligent therapeutic content selection
- **Multi-Modal AI Integration**: Seamless connection between Telegram, Spotify, and Ollama LLM
- **Real-Time Emotion Processing**: Instant analysis and response generation for crisis intervention
- **Adaptive Learning**: Self-improving therapeutic responses based on user feedback
- **Clinical-Grade Security**: HIPAA-compliant data handling and privacy protection
- **Cross-Platform Compatibility**: Works across all devices with Telegram and Spotify access

### AI Automation Capabilities:
- **Proactive Mental Health Monitoring**: Automated check-ins and wellness assessments
- **Intelligent Crisis Detection**: AI-powered early warning system for mental health episodes
- **Personalized Therapy Curation**: Dynamic content selection based on individual therapeutic needs
- **Automated Progress Reporting**: Clinical summaries and improvement metrics generation
- **Smart Intervention Timing**: Optimal moment detection for therapeutic interventions

## 🎯 Clinical & Mental Health Philosophy

### Therapeutic Approach:
- **Evidence-Based Practice**: Integration of proven psychological and philosophical therapeutic methods
- **Holistic Wellbeing**: Addressing emotional, cognitive, and behavioral aspects of mental health
- **Preventive Care**: Early intervention and continuous emotional support
- **Personalized Treatment**: AI-driven customization for individual therapeutic needs
- **Accessibility**: 24/7 mental health support regardless of location or time constraints

### Clinical Applications:
- **Primary Mental Health Support**: First-line emotional assistance and crisis intervention
- **Therapeutic Augmentation**: Complement to traditional therapy and counseling
- **Wellness Maintenance**: Ongoing emotional regulation and mental health monitoring
- **Crisis Prevention**: Early detection and intervention for mental health episodes
- **Healthcare Integration**: Seamless data sharing with mental health professionals

### Ethical Considerations:
- **Privacy Protection**: Secure handling of sensitive mental health data
- **Professional Boundaries**: Clear limitations and referral protocols for serious conditions
- **Informed Consent**: Transparent communication about AI capabilities and limitations
- **Cultural Sensitivity**: Respectful integration of diverse philosophical and therapeutic traditions