from flask import Flask, redirect, request, session
import requests

app = Flask(__name__)
app.secret_key = "ar_roleplay_secret_session_key"

CLIENT_ID = "1546980944408215653"  
CLIENT_SECRET = "yx4hnnxdZJ7PHdpb7JrJ_oOCC340ifFX" 
GUILD_ID = "1545798490838409336" 
ROLE_ID = "1546988108405547149"

HOME_BG_URL = "https://cdn.discordapp.com/attachments/1531373533760979055/1546896479115812864/file_00000000650481f5b7aa46ea9582d574.png?ex=6aa1731c&is=6aa0219c&hm=d0c0bb83e85af82ecf87396dab1ed823eb9a9b9333a97c878ff615a7d81d4822&"
RESULT_BG_URL = "https://cdn.discordapp.com/attachments/1531373533760979055/1546896421423419513/file_000000005658820688c680d594e622b6.png?ex=6aa1730e&is=6aa0218e&hm=3badafef87f454a9db836eba47f0a3976b17f8d456631431773280bec5dd5861&"

@app.route("/")
def home():
    if session.get('whitelisted'):
        return redirect("/success-page")

    host_url = request.host_url.rstrip('/')
    redirect_uri = f"{host_url}/callback"
    
    discord_auth_url = (
        f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}"
        f"&redirect_uri={redirect_uri}&response_type=code&scope=identify%20guilds.members.read"
    )
    return f"""
    <html>
        <head>
            <title>Arabe RolePlay Mobile - Authentication</title>
            <style>
                body {{
                    background: url('{HOME_BG_URL}') no-repeat center center fixed;
                    background-size: cover;
                    color: white;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                .container {{
                    background: rgba(15, 23, 42, 0.85);
                    color: #fff;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    width: 750px;
                    height: 400px;
                    display: flex;
                    border-radius: 8px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.8);
                    backdrop-filter: blur(6px);
                }}
                .left-pane {{
                    padding: 40px;
                    flex: 1.2;
                    border-right: 1px solid rgba(255, 255, 255, 0.1);
                    position: relative;
                }}
                .title-brand {{
                    font-size: 14px;
                    font-weight: bold;
                    letter-spacing: 1px;
                    margin-bottom: 5px;
                }}
                .left-pane h1 {{
                    font-size: 32px;
                    margin-top: 0;
                    font-weight: 800;
                    letter-spacing: 1px;
                    color: #ffffff;
                }}
                .left-pane p {{
                    color: #cbd5e1;
                    font-size: 13px;
                    line-height: 1.6;
                }}
                .right-pane {{
                    flex: 1;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 30px;
                }}
                .discord-btn {{
                    background-color: #1e3a8a;
                    color: white;
                    text-decoration: none;
                    padding: 16px 24px;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 100%;
                    box-shadow: 0 4px 12px rgba(30, 58, 138, 0.4);
                    transition: background 0.2s;
                }}
                .discord-btn:active {{
                    background-color: #dc2626 !important;
                }}
                .steps {{
                    font-size: 11px;
                    color: #94a3b8;
                    margin-top: 30px;
                }}
                .steps div {{
                    margin-bottom: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="left-pane">
                    <div class="title-brand">
                        <span style="color:#22c55e;">Arabe</span> 
                        <span style="color:#ef4444;">RolePlay</span> 
                        <span style="color:#0f172a; background:#e2e8f0; padding:2px 6px; border-radius:4px;">Mobile</span>
                    </div>
                    <h1>SIGN IN</h1>
                    <p>Continue with your Discord account to enter the game. Your whitelist role will be verified automatically.</p>
                    <div class="steps">
                        <div>◆ APPROVE THE REQUEST ON DISCORD</div>
                        <div>◆ VERIFY WHITELIST ROLE</div>
                        <div>◆ THE GAME RESUMES ON ITS OWN</div>
                    </div>
                </div>
                <div class="right-pane">
                    <a href="{discord_auth_url}" class="discord-btn">
                        CONTINUE WITH DISCORD
                    </a>
                </div>
            </div>
        </body>
    </html>
    """

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "<h2 style='color:red; text-align:center; margin-top:50px;'>❌ خطأ: لم يتم استلام كود التحقق من ديسكورد.</h2>"

    host_url = request.host_url.rstrip('/')
    redirect_uri = f"{host_url}/callback"

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    token_json = r.json()
    
    access_token = token_json.get("access_token")
    if not access_token:
        return f"<h3 style='color:orange; text-align:center;'>❌ فشل في جلب التوكن: {token_json}</h3>"

    auth_header = {"Authorization": f"Bearer {access_token}"}
    member_r = requests.get(f"https://discord.com/api/users/@me/guilds/{GUILD_ID}/member", headers=auth_header)
    
    if member_r.status_code != 200:
        return "<h2 style='color:#ef4444; text-align:center; margin-top:50px;'>⛔ غير مسموح! أنت لست عضواً في سيرفر Arabe RolePlay.</h2>"

    member_data = member_r.json()
    roles = member_data.get("roles", [])

    if ROLE_ID in roles:
        session['whitelisted'] = True
        return redirect("/success-page")
    else:
        return f"""
        <html>
            <head>
                <style>
                    body {{
                        background: url('{RESULT_BG_URL}') no-repeat center center fixed;
                        background-size: cover;
                        height: 100vh;
                        margin: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    }}
                    .card {{
                        background: rgba(24, 24, 27, 0.9);
                        color: #fff;
                        width: 400px;
                        padding: 25px;
                        border-radius: 16px;
                        text-align: center;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
                        border: 1px solid rgba(255, 255, 255, 0.15);
                        backdrop-filter: blur(10px);
                    }}
                    .logo {{
                        width: 55px;
                        height: 55px;
                        border-radius: 12px;
                        margin-bottom: 10px;
                        object-fit: cover;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
                    }}
                    .msg {{
                        font-size: 16px;
                        font-weight: bold;
                        color: #ef4444;
                        margin-bottom: 8px;
                        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
                    }}
                    .server-name {{
                        font-style: italic;
                        font-weight: 800;
                        font-size: 20px;
                        color: #ffffff;
                        margin-bottom: 15px;
                    }}
                    .btn-primary {{
                        background-color: #5865F2;
                        color: white;
                        text-decoration: none;
                        padding: 12px;
                        border-radius: 10px;
                        display: block;
                        font-weight: bold;
                        font-size: 14px;
                        margin-bottom: 8px;
                        box-shadow: 0 4px 12px rgba(88, 101, 242, 0.4);
                    }}
                    .btn-secondary {{
                        background-color: rgba(255, 255, 255, 0.08);
                        color: #9ca3af;
                        text-decoration: none;
                        padding: 10px;
                        border-radius: 10px;
                        display: block;
                        font-weight: 600;
                        font-size: 13px;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <img src="{HOME_BG_URL}" class="logo">
                    <div class="msg">Roh jewz whitelist 📝🔴</div>
                    <div class="server-name">ar roleplay</div>
                    <a href="https://discord.gg/2KD4v9nZQn" class="btn-primary">Aller sur le serveur</a>
                    <a href="#" onclick="window.close(); return false;" class="btn-secondary">Ignorer</a>
                </div>
            </body>
        </html>
        """

@app.route("/success-page")
def success_page():
    return f"""
    <html>
        <head>
            <style>
                body {{
                    background: url('{RESULT_BG_URL}') no-repeat center center fixed;
                    background-size: cover;
                    height: 100vh;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-family: sans-serif;
                }}
                .box {{
                    background: rgba(0, 0, 0, 0.85);
                    padding: 30px 50px;
                    border-radius: 12px;
                    border: 2px solid #22c55e;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.9);
                    backdrop-filter: blur(8px);
                    text-align: center;
                }}
                h2 {{
                    color: #22c55e;
                    font-size: 26px;
                    margin: 0 0 20px 0;
                    text-shadow: 0 2px 5px rgba(0,0,0,0.9);
                }}
                .btn-close {{
                    background-color: #22c55e;
                    color: white;
                    text-decoration: none;
                    padding: 12px 25px;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 15px;
                    box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
                    display: inline-block;
                    cursor: pointer;
                }}
            </style>
            <script>
                function closeTab() {{
                    try {{
                        window.close();
                    }} catch(e) {{}}
                    try {{
                        window.location.href = "about:blank";
                    }} catch(e) {{}}
                }}
            </script>
        </head>
        <body>
            <div class="box">
                <h2>Welcome To Arabe RolePlay 🟢</h2>
                <a href="javascript:void(0);" onclick="closeTab();" class="btn-close">Retour au jeu</a>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
