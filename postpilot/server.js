import express from 'express';
import crypto from 'node:crypto';
import 'dotenv/config';

const app = express();
const PORT = process.env.PORT || 3000;
const VERSION = process.env.META_GRAPH_VERSION || 'v23.0';
const sessions = new Map();
const schedules = new Map();

app.use(express.json({ limit: '2mb' }));
app.use(express.static('postpilot/public'));

function graph(path, options = {}) {
  return fetch(`https://graph.facebook.com/${VERSION}${path}`, options).then(async r => {
    const data = await r.json();
    if (!r.ok || data.error) throw new Error(data.error?.message || `Graph API ${r.status}`);
    return data;
  });
}

app.get('/auth/facebook', (req, res) => {
  if (!process.env.META_APP_ID || !process.env.META_REDIRECT_URI) return res.status(500).send('Meta OAuth is not configured. Add META_APP_ID and META_REDIRECT_URI.');
  const state = crypto.randomBytes(24).toString('hex');
  sessions.set(state, { created: Date.now() });
  const params = new URLSearchParams({
    client_id: process.env.META_APP_ID,
    redirect_uri: process.env.META_REDIRECT_URI,
    state,
    response_type: 'code',
    scope: 'pages_show_list,pages_read_engagement,pages_manage_posts'
  });
  res.redirect(`https://www.facebook.com/dialog/oauth?${params}`);
});

app.get('/auth/facebook/callback', async (req, res) => {
  const { code, state } = req.query;
  if (!code || !state || !sessions.has(state)) return res.status(400).send('Invalid OAuth state.');
  sessions.delete(state);
  try {
    const token = await graph('/oauth/access_token', { method: 'POST', headers: {'content-type':'application/x-www-form-urlencoded'}, body: new URLSearchParams({client_id:process.env.META_APP_ID, client_secret:process.env.META_APP_SECRET, redirect_uri:process.env.META_REDIRECT_URI, code}) });
    const user = await graph(`/me?fields=id,name&access_token=${encodeURIComponent(token.access_token)}`);
    const pages = await graph(`/me/accounts?fields=id,name,access_token&access_token=${encodeURIComponent(token.access_token)}`);
    const sid = crypto.randomBytes(24).toString('hex');
    sessions.set(sid, { user, pages: pages.data || [], created: Date.now() });
    res.redirect(`/index.html?session=${encodeURIComponent(sid)}`);
  } catch (e) { res.status(400).send(`Facebook authorization failed: ${e.message}`); }
});

app.get('/api/session/:sid', (req, res) => {
  const s = sessions.get(req.params.sid);
  if (!s) return res.status(404).json({error:'Session expired'});
  res.json({user:s.user, pages:s.pages.map(p=>({id:p.id,name:p.name}))});
});

app.post('/api/page-post', async (req, res) => {
  const { sessionId, pageId, message } = req.body;
  const s = sessions.get(sessionId);
  if (!s) return res.status(401).json({error:'Not authorized'});
  const page = s.pages.find(p=>p.id===pageId);
  if (!page) return res.status(403).json({error:'Page is not authorized'});
  if (!message?.trim()) return res.status(400).json({error:'Post text is required'});
  try {
    const result = await graph(`/${page.id}/feed`, { method:'POST', headers:{'content-type':'application/x-www-form-urlencoded'}, body:new URLSearchParams({message:message.trim(), access_token:page.access_token}) });
    res.json({ok:true,result});
  } catch(e) { res.status(400).json({error:e.message}); }
});

app.post('/api/schedule', (req,res)=>{
  const {sessionId,pageId,message,intervalMinutes=5,repeat=1}=req.body;
  if (!sessions.has(sessionId)) return res.status(401).json({error:'Not authorized'});
  if (!Number.isFinite(intervalMinutes) || intervalMinutes < 5) return res.status(400).json({error:'Minimum interval is 5 minutes'});
  const id=crypto.randomBytes(10).toString('hex');
  schedules.set(id,{id,sessionId,pageId,message,intervalMinutes,repeat:Number(repeat)||1,created:Date.now(),next:Date.now()});
  res.json({ok:true,id});
});

app.get('/api/schedules',(req,res)=>res.json([...schedules.values()].map(({sessionId,...x})=>x)));

// Groups are deliberately a manual-share queue. This avoids bypassing Facebook group permissions.
app.post('/api/group-queue',(req,res)=>{
  const {message,groups=[]}=req.body;
  if (!message?.trim()) return res.status(400).json({error:'Post text is required'});
  const items=groups.slice(0,9).map((g,i)=>({slot:i+1,name:g.name||`Group ${i+1}`,url:g.url||'',status:'ready'}));
  res.json({message:message.trim(),items});
});

app.listen(PORT,()=>console.log(`PostPilot running at http://localhost:${PORT}`));
