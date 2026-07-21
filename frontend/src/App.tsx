import { ChangeEvent, FormEvent, useEffect, useState } from 'react';
import { fetchWithAuth, setToken, getToken } from './api';

type Game = {
  id: number;
  name: string;
  last_played_at: string | null;
  total_play_time: number;
  installed: boolean;
};

type ConversationMessage = {
  id: number;
  user_id: number | null;
  game_id: number | null;
  message: string;
  role: string;
  created_at: string;
};

type MemoryItem = {
  id: number;
  user_id: number | null;
  category: string;
  content: string;
  created_at: string;
};
type VisionReport = {
  screen?: {
    width: number;
    height: number;
    edge_pixels: number;
  };

  message?: string;
  health_bar?: { approx_percent_color: number };
  energy_bar?: { approx_percent_color: number };
  minimap?: { found: boolean };
};

type HistoryEntry = {
  id: number;
  user_id: number | null;
  game_id: number | null;
  action: string;
  details: string;
  occurred_at: string;
};

function App() {
  const [active, setActive] = useState('dashboard');
  const [games, setGames] = useState<Game[]>([]);
  const [newGameName, setNewGameName] = useState('');
  const [loadingGames, setLoadingGames] = useState(false);
  const [creatingGame, setCreatingGame] = useState(false);
  const [plugins, setPlugins] = useState<{ name: string; version: string; enabled: boolean }[]>([]);
  const [loadingPlugins, setLoadingPlugins] = useState(false);
  const [conversation, setConversation] = useState<ConversationMessage[]>([]);
  const [visionReport, setVisionReport] = useState<VisionReport | null>(null);
  const [loadingVision, setLoadingVision] = useState(false);
  const [newMessage, setNewMessage] = useState('');
  const [loadingConversation, setLoadingConversation] = useState(false);
  const [memoryItems, setMemoryItems] = useState<MemoryItem[]>([]);
  const [memoryCategory, setMemoryCategory] = useState('');
  const [memoryContent, setMemoryContent] = useState('');
  const [memorySummary, setMemorySummary] = useState('');
  const [loadingMemory, setLoadingMemory] = useState(false);
  const [historyItems, setHistoryItems] = useState<HistoryEntry[]>([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [visionStatus, setVisionStatus] = useState('');
  const [voiceStatus, setVoiceStatus] = useState('');
  const [speechText, setSpeechText] = useState('');
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [transcriptionResult, setTranscriptionResult] = useState('');
  const [loadingSpeech, setLoadingSpeech] = useState(false);
  const [loadingTranscribe, setLoadingTranscribe] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [authToken, setAuthToken] = useState<string | null>(null);
  const [loginUser, setLoginUser] = useState('');
  const [loginPass, setLoginPass] = useState('');
  const [loginDisplayName, setLoginDisplayName] = useState('');
  const [loggingIn, setLoggingIn] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [loginError, setLoginError] = useState<string | null>(null);
  const protectedTabs = ['conversation', 'vision', 'history', 'memory', 'settings'];

  const handleLogin = async (ev?: FormEvent) => {
    ev?.preventDefault();
    setLoggingIn(true);
    setError(null);
    setLoginError(null);
    setSuccessMessage(null);
    try {
      const res = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: loginUser, password: loginPass }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        const msg = body.detail || 'Falha no login';
        setLoginError(msg);
        throw new Error(msg);
      }
      const data = await res.json();
      setToken(data.access_token);
      setAuthToken(data.access_token);
      setLoginPass('');
      setSuccessMessage('Login realizado com sucesso.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoggingIn(false);
    }
  };

  const handleRegister = async (ev?: FormEvent) => {
    ev?.preventDefault();
    setLoggingIn(true);
    setError(null);
    setLoginError(null);
    setSuccessMessage(null);
    try {
      const res = await fetch('http://127.0.0.1:8000/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: loginUser, password: loginPass, display_name: loginDisplayName }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        const msg = body.detail || 'Falha no registro';
        setLoginError(msg);
        throw new Error(msg);
      }
      const data = await res.json();
      setToken(data.access_token);
      setAuthToken(data.access_token);
      setLoginPass('');
      setLoginDisplayName('');
      setSuccessMessage('Registro realizado e login efetuado.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoggingIn(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setAuthToken(null);
  };

  useEffect(() => {
    const t = getToken();
    if (t) setAuthToken(t);
  }, []);

  const fetchGames = () => {
    setLoadingGames(true);
    setError(null);
    setSuccessMessage(null);

    fetchWithAuth('http://127.0.0.1:8000/games')
      .then((res) => res.json())
      .then((data) => {
        setGames(data);
      })
      .catch(() => {
        setError('Não foi possível carregar os jogos.');
      })
      .finally(() => setLoadingGames(false));
  };

  useEffect(() => {
    if (active === 'dashboard') {
      fetchGames();
    }

    if (active === 'plugins') {
      fetchPlugins();
    }

    if (active === 'conversation') {
      fetchConversation();
      fetchVoiceStatus();
    }

    if (active === 'memory') {
      fetchMemory();
      fetchMemorySummary();
    }

    if (active === 'history') {
      fetchHistory();
    }

    if (active === 'settings') {
      fetchVisionStatus();
      fetchVoiceStatus();
    }

    if (active === 'vision') {
      if (!authToken) {
        setError('Faça login para acessar Visão.');
        setActive('dashboard');
      } else {
        fetchVisionAnalyze();
      }
    }
  }, [active]);

  const requireAuthAndSetActive = (tab: string) => {
    if (protectedTabs.includes(tab) && !authToken) {
      setError('Faça login para acessar esta área.');
      setActive('dashboard');
      return;
    }
    setError(null);
    setActive(tab);
  };

  const handleCreateGame = async (event: FormEvent) => {
    event.preventDefault();

    if (!newGameName.trim()) {
      setError('Informe um nome de jogo para cadastrar.');
      return;
    }

    setCreatingGame(true);
    setError(null);

    try {
      const response = await fetchWithAuth('http://127.0.0.1:8000/games', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newGameName.trim() }),
      });

      if (!response.ok) {
        const message = await response.json();
        throw new Error(message.detail || 'Falha ao cadastrar o jogo.');
      }

      setNewGameName('');
      fetchGames();
      setSuccessMessage('Jogo criado com sucesso.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido.');
    } finally {
      setCreatingGame(false);
    }
  };

  const handleSendMessage = async (event: FormEvent) => {
    event.preventDefault();

    if (!newMessage.trim()) {
      setError('Digite uma mensagem para enviar.');
      return;
    }

    setLoadingConversation(true);
    setError(null);

    try {
      const response = await fetchWithAuth('http://127.0.0.1:8000/conversation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: newMessage.trim(), role: 'user' }),
      });

      if (!response.ok) {
        throw new Error('Falha ao enviar a mensagem.');
      }

      setNewMessage('');
      fetchConversation();
      setSuccessMessage('Mensagem enviada.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido.');
    } finally {
      setLoadingConversation(false);
    }
  };

  const fetchPlugins = () => {
    setLoadingPlugins(true);
    setError(null);

    fetchWithAuth('http://127.0.0.1:8000/plugins')
      .then((res) => res.json())
      .then((data) => {
        setPlugins(data);
      })
      .catch(() => {
        setError('Não foi possível carregar os plugins.');
      })
      .finally(() => setLoadingPlugins(false));
  };

  const fetchVisionAnalyze = () => {
    setLoadingVision(true);
    setError(null);

    fetchWithAuth('http://127.0.0.1:8000/vision/analyze')
      .then((res) => res.json())
      .then((data) => setVisionReport(data))
      .catch(() => {
        setError('Não foi possível analisar a visão.');
      })
      .finally(() => setLoadingVision(false));
  };

  const fetchConversation = () => {
    setLoadingConversation(true);
    setError(null);

    fetchWithAuth('http://127.0.0.1:8000/conversation')
      .then((res) => res.json())
      .then((data) => {
        setConversation(data);
      })
      .catch(() => {
        setError('Não foi possível carregar a conversa.');
      })
      .finally(() => setLoadingConversation(false));
  };

  const fetchMemory = () => {
    setLoadingMemory(true);
    setError(null);

    fetchWithAuth('http://127.0.0.1:8000/memory')
      .then((res) => res.json())
      .then((data) => {
        setMemoryItems(data);
      })
      .catch(() => {
        setError('Não foi possível carregar a memória.');
      })
      .finally(() => setLoadingMemory(false));
  };

  const fetchMemorySummary = () => {
    fetchWithAuth('http://127.0.0.1:8000/memory/summary')
      .then((res) => res.json())
      .then((data) => {
        setMemorySummary(data.summary ?? 'Nenhum resumo disponível');
      })
      .catch(() => {
        setMemorySummary('Falha ao carregar resumo de memória.');
      });
  };

  const fetchHistory = () => {
    setLoadingHistory(true);
    setError(null);

    fetchWithAuth('http://127.0.0.1:8000/history')
      .then((res) => res.json())
      .then((data) => {
        setHistoryItems(data);
      })
      .catch(() => {
        setError('Não foi possível carregar o histórico.');
      })
      .finally(() => setLoadingHistory(false));
  };

  const fetchVisionStatus = () => {
    fetchWithAuth('http://127.0.0.1:8000/vision/status')
      .then((res) => res.json())
      .then((data) => setVisionStatus(data.vision))
      .catch(() => setVisionStatus('erro'));
  };

  const fetchVoiceStatus = () => {
    fetchWithAuth('http://127.0.0.1:8000/voice/status')
      .then((res) => res.json())
      .then((data) => setVoiceStatus(data.voice))
      .catch(() => setVoiceStatus('erro'));
  };

  const handleSynthesizeVoice = async () => {
    if (!speechText.trim()) {
      setError('Digite texto para sintetizar.');
      return;
    }

    setLoadingSpeech(true);
    setError(null);
    setAudioUrl(null);

    try {
      const response = await fetchWithAuth('http://127.0.0.1:8000/voice/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: speechText.trim() }),
      });
      if (!response.ok) {
        throw new Error('Falha ao sintetizar áudio.');
      }
      const data = await response.json();
      setAudioUrl(`data:audio/wav;base64,${data.audio_base64}`);
      setSuccessMessage('Áudio sintetizado com sucesso.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido.');
    } finally {
      setLoadingSpeech(false);
    }
  };

  const handleTranscribeAudio = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    setLoadingTranscribe(true);
    setError(null);
    setTranscriptionResult('');

    try {
      const fileData = await file.arrayBuffer();
      const base64 = btoa(String.fromCharCode(...new Uint8Array(fileData)));
      const response = await fetchWithAuth('http://127.0.0.1:8000/voice/transcribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ audio_data: base64 }),
      });
      if (!response.ok) {
        throw new Error('Falha ao transcrever áudio.');
      }
      const data = await response.json();
      setTranscriptionResult(data.transcription || 'Sem transcrição retornada.');
      setSuccessMessage('Transcrição concluída.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido.');
    } finally {
      setLoadingTranscribe(false);
    }
  };

  const createMemory = async (event: FormEvent) => {
    event.preventDefault();

    if (!memoryCategory.trim() || !memoryContent.trim()) {
      setError('Preencha categoria e conteúdo da memória.');
      return;
    }

    setLoadingMemory(true);
    setError(null);

    try {
      const response = await fetchWithAuth('http://127.0.0.1:8000/memory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category: memoryCategory.trim(), content: memoryContent.trim() }),
      });

      if (!response.ok) {
        throw new Error('Falha ao criar memória.');
      }

      setMemoryCategory('');
      setMemoryContent('');
      fetchMemory();
      fetchMemorySummary();
      setSuccessMessage('Memória salva.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido.');
    } finally {
      setLoadingMemory(false);
    }
  };

  return (
    <div className="app-shell">
      <aside className="side-nav">
        <div className="brand">GameCopilot AI</div>
        {!authToken ? (
          <div className="auth-box">
            <input placeholder="Usuário" value={loginUser} onChange={(e) => setLoginUser(e.target.value)} />
            <input placeholder="Nome exibido (opcional)" value={loginDisplayName} onChange={(e) => setLoginDisplayName(e.target.value)} />
            <input placeholder="Senha" type="password" value={loginPass} onChange={(e) => setLoginPass(e.target.value)} />
            <div className="auth-actions">
              <button onClick={() => handleLogin()} disabled={loggingIn}>{loggingIn ? 'Entrando...' : 'Entrar'}</button>
              <button onClick={() => handleRegister()} disabled={loggingIn}>{loggingIn ? 'Registrando...' : 'Registrar'}</button>
            </div>
            {loginError && <p className="error">{loginError}</p>}
            {successMessage && <p className="success">{successMessage}</p>}
          </div>
        ) : (
          <div className="auth-box">
            <div>Logado</div>
            <button onClick={handleLogout}>Sair</button>
          </div>
        )}
        <button onClick={() => requireAuthAndSetActive('dashboard')} className={active === 'dashboard' ? 'active' : ''}>Dashboard</button>
        <button onClick={() => requireAuthAndSetActive('conversation')} disabled={!authToken} className={active === 'conversation' ? 'active' : ''}>Conversa</button>
        <button onClick={() => requireAuthAndSetActive('vision')} disabled={!authToken} className={active === 'vision' ? 'active' : ''}>Visão</button>
        <button onClick={() => requireAuthAndSetActive('plugins')} className={active === 'plugins' ? 'active' : ''}>Plugins</button>
        <button onClick={() => requireAuthAndSetActive('history')} disabled={!authToken} className={active === 'history' ? 'active' : ''}>Histórico</button>
        <button onClick={() => requireAuthAndSetActive('memory')} disabled={!authToken} className={active === 'memory' ? 'active' : ''}>Memória</button>
        <button onClick={() => requireAuthAndSetActive('settings')} disabled={!authToken} className={active === 'settings' ? 'active' : ''}>Configurações</button>
      </aside>

      <main className="main-panel">
        {!authToken && (
          <div className="login-banner">
            <strong>Faça login</strong>: algumas áreas estão protegidas. Use a caixa à esquerda para entrar ou registrar-se.
            <button className="banner-btn" onClick={() => setActive('dashboard')}>Ir para login</button>
          </div>
        )}
        <header>
          <h1>{active === 'dashboard' ? 'Dashboard' : active === 'conversation' ? 'Conversa' : active === 'vision' ? 'Visão' : active === 'plugins' ? 'Plugins' : active === 'history' ? 'Histórico' : active === 'memory' ? 'Memória' : 'Configurações'}</h1>
        </header>

        <section className="content">
          {active === 'dashboard' && (
            <div className="dashboard-panel">
              <p>Bem-vindo ao GameCopilot AI. Inicie a captura e monitore seus jogos em tempo real.</p>

              <form className="game-form" onSubmit={handleCreateGame}>
                <label htmlFor="game-name">Novo jogo</label>
                <div className="game-form-row">
                  <input
                    id="game-name"
                    type="text"
                    value={newGameName}
                    onChange={(event) => setNewGameName(event.target.value)}
                    placeholder="Nome do jogo"
                  />
                  <button type="submit" disabled={creatingGame}>
                    {creatingGame ? 'Salvando...' : 'Adicionar'}
                  </button>
                </div>
              </form>

              {loadingGames && <p>Carregando jogos...</p>}
              {error && <p className="error">{error}</p>}

              {!loadingGames && !error && (
                <div className="game-list">
                  {games.length > 0 ? (
                    games.map((game) => (
                      <div key={game.id} className="game-card">
                        <h3>{game.name}</h3>
                        <p>Último jogo: {game.last_played_at ?? 'Nunca'}</p>
                        <p>Tempo total: {game.total_play_time} segundos</p>
                        <p>{game.installed ? 'Instalado' : 'Não instalado'}</p>
                      </div>
                    ))
                  ) : (
                    <p>Nenhum jogo registrado ainda.</p>
                  )}
                </div>
              )}
            </div>
          )}
          {active === 'conversation' && (
            <div className="dashboard-panel">
              <p>Converse naturalmente com sua IA. Texto e voz serão suportados.</p>

              {loadingConversation && <p>Carregando conversa...</p>}

              <div className="conversation-list">
                {conversation.map((message) => (
                  <div key={message.id} className="game-card">
                    <strong>{message.role === 'user' ? 'Você' : 'Assistente'}</strong>
                    <p>{message.message}</p>
                    <small>{new Date(message.created_at).toLocaleString()}</small>
                  </div>
                ))}
              </div>

              <form className="game-form" onSubmit={handleSendMessage}>
                <label htmlFor="message-input">Enviar mensagem</label>
                <div className="game-form-row">
                  <input
                    id="message-input"
                    type="text"
                    value={newMessage}
                    onChange={(event) => setNewMessage(event.target.value)}
                    placeholder="Digite sua mensagem"
                  />
                  <button type="submit">Enviar</button>
                </div>
              </form>

              <div className="dashboard-panel mt-24">
                <h3>Voz e TTS/STT</h3>
                <label htmlFor="speech-text">Texto para sintetizar</label>
                <textarea
                  id="speech-text"
                  value={speechText}
                  onChange={(event) => setSpeechText(event.target.value)}
                  placeholder="Digite o texto que a IA deve falar"
                />
                <button onClick={handleSynthesizeVoice} disabled={loadingSpeech}>
                  {loadingSpeech ? 'Convertendo...' : 'Sintetizar áudio'}
                </button>
                {audioUrl && (
                  <div className="mt-12">
                    <audio controls src={audioUrl} />
                  </div>
                )}
                <div className="mt-16">
                  <label htmlFor="audio-upload">Upload de áudio para transcrição</label>
                  <input id="audio-upload" type="file" accept="audio/*" onChange={handleTranscribeAudio} />
                  {loadingTranscribe && <p>Transcrevendo áudio...</p>}
                  {transcriptionResult && <p><strong>Transcrição:</strong> {transcriptionResult}</p>}
                </div>
              </div>
            </div>
          )}
          {active === 'vision' && (
            <div className="dashboard-panel">
              <p>Visão do jogo e análise de tela em tempo real.</p>
              <button onClick={fetchVisionAnalyze} disabled={loadingVision}>
                {loadingVision ? 'Analisando...' : 'Atualizar análise'}
              </button>

              {visionReport && (
                <div className="game-list">
                  <div className="game-card">
                    <h3>Visão detectada</h3>
                    <p>Altura: {visionReport.screen?.height ?? 'N/A'}</p>
                    <p>Largura: {visionReport.screen?.width ?? 'N/A'}</p>
                    <p>Pixels de borda: {visionReport.screen?.edge_pixels ?? 'N/A'}</p>
                    <p>Vida (estimada): {visionReport.health_bar?.approx_percent_color ?? 'N/A'}%</p>
                    <p>Energia (estimada): {visionReport.energy_bar?.approx_percent_color ?? 'N/A'}%</p>
                    <p>Minimap detectado: {visionReport.minimap?.found ? 'Sim' : 'Não'}</p>
                    {visionReport.message && <p>{visionReport.message}</p>}
                  </div>
                </div>
              )}
            </div>
          )}
          {active === 'plugins' && (
            <div>
              <p>Gerencie plugins oficiais e integrações autorizadas.</p>

              {loadingPlugins && <p>Carregando plugins...</p>}
              {!loadingPlugins && plugins.length === 0 && <p>Nenhum plugin encontrado.</p>}

              <div className="plugin-list">
                {plugins.map((plugin) => (
                  <div key={`${plugin.name}-${plugin.version}`} className="game-card">
                    <h3>{plugin.name}</h3>
                    <p>Versão: {plugin.version}</p>
                    <p>{plugin.enabled ? 'Ativo' : 'Desativado'}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
          {active === 'history' && (
            <div className="dashboard-panel">
              <p>Veja o histórico de sessões, objetivos e eventos.</p>
              {loadingHistory && <p>Carregando histórico...</p>}
              {!loadingHistory && historyItems.length === 0 && <p>Nenhum histórico disponível.</p>}
              <div className="game-list">
                {historyItems.map((item) => (
                  <div key={item.id} className="game-card">
                    <h3>{item.action}</h3>
                    <p>{item.details}</p>
                    <small>{new Date(item.occurred_at).toLocaleString()}</small>
                  </div>
                ))}
              </div>
            </div>
          )}
          {active === 'memory' && (
            <div className="dashboard-panel">
              <p>Memória de partidas, preferências e itens identificados.</p>
              <button onClick={fetchMemorySummary}>Atualizar resumo de memória</button>
              {memorySummary && (
                <div className="game-card mt-16">
                  <h3>Resumo de memória</h3>
                  <p>{memorySummary}</p>
                </div>
              )}

              <form className="game-form" onSubmit={createMemory}>
                <label htmlFor="memory-category">Categoria</label>
                <input
                  id="memory-category"
                  type="text"
                  value={memoryCategory}
                  onChange={(event) => setMemoryCategory(event.target.value)}
                  placeholder="Ex: itens, objetivos"
                />

                <label htmlFor="memory-content">Conteúdo</label>
                <textarea
                  id="memory-content"
                  value={memoryContent}
                  onChange={(event) => setMemoryContent(event.target.value)}
                  placeholder="Detalhe o evento ou observação"
                />

                <button type="submit" disabled={loadingMemory}>
                  {loadingMemory ? 'Salvando...' : 'Salvar memória'}
                </button>
              </form>

              {loadingMemory && <p>Carregando memória...</p>}

              <div className="game-list">
                {memoryItems.map((item) => (
                  <div key={item.id} className="game-card">
                    <h3>{item.category}</h3>
                    <p>{item.content}</p>
                    <small>{new Date(item.created_at).toLocaleString()}</small>
                  </div>
                ))}
              </div>
            </div>
          )}
          {active === 'settings' && (
            <div className="dashboard-panel">
              <p>Configure alertas, voz, IA e integrações.</p>
              <div className="game-card">
                <h3>Status do Vision Engine</h3>
                <p>{visionStatus || 'Carregando...'}</p>
              </div>
              <div className="game-card">
                <h3>Status do Voice Engine</h3>
                <p>{voiceStatus || 'Carregando...'}</p>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
