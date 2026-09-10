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
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    overflow: hidden;
                }}
                /* شريط العرض العلوي تماماً مثل الصورة */
                .top-bar {{
                    position: absolute;
                    top: 15px;
                    left: 30px;
                    right: 30px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
                    padding-bottom: 10px;
                }}
                .brand-logo-text {{
                    font-weight: 900;
                    letter-spacing: 2px;
                    font-size: 16px;
                }}
                .account-link-badge {{
                    background: rgba(34, 197, 94, 0.15);
                    border: 1px solid #22c55e;
                    color: #22c55e;
                    padding: 4px 12px;
                    font-size: 11px;
                    font-weight: bold;
                    letter-spacing: 1px;
                    border-radius: 2px;
                }}
                /* الصندوق الرئيسي العريض الذي يملأ الشاشة */
                .main-box {{
                    width: 90vw;
                    height: 75vh;
                    background: rgba(10, 15, 30, 0.85);
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    display: flex;
                    box-shadow: 0 20px 50px rgba(0,0,0,0.9);
                    backdrop-filter: blur(8px);
                    position: relative;
                }}
                .left-section {{
                    flex: 1.2;
                    padding: 40px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    border-right: 1px solid rgba(255, 255, 255, 0.1);
                }}
                .step-num {{
                    color: #22c55e;
                    font-weight: bold;
                    font-size: 13px;
                    letter-spacing: 1px;
                    margin-bottom: 5px;
                }}
                .left-section h1 {{
                    font-size: 38px;
                    margin: 0 0 15px 0;
                    font-weight: 900;
                    letter-spacing: 1px;
                }}
                .left-section p {{
                    color: #94a3b8;
                    font-size: 13px;
                    line-height: 1.5;
                    margin-bottom: 25px;
                }}
                .features-list div {{
                    font-size: 11px;
                    color: #cbd5e1;
                    margin-bottom: 8px;
                    letter-spacing: 0.5px;
                }}
                .right-section {{
                    flex: 1;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding: 40px;
                    background: rgba(0, 0, 0, 0.3);
                }}
                .discord-btn {{
                    background-color: #1e3a8a;
                    color: white;
                    text-decoration: none;
                    width: 100%;
                    max-width: 380px;
                    height: 60px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 20px;
                    font-weight: bold;
                    font-size: 15px;
                    border-radius: 4px;
                    box-shadow: 0 4px 15px rgba(30, 58, 138, 0.5);
                    transition: 0.2s;
                }}
                .discord-btn:hover {{
                    background-color: #2563eb;
                }}
            </style>
        </head>
        <body>
            <div class="top-bar">
                <div class="brand-logo-text">
                    <span style="color:#22c55e;">ARABE</span> <span style="color:#ef4444;">ROLEPLAY</span> <span style="background:#334155; color:#fff; padding:2px 6px; font-size:10px; border-radius:3px;">MENA</span>
                </div>
                <div class="account-link-badge">■ ACCOUNT LINK</div>
            </div>

            <div class="main-box">
                <div class="left-section">
                    <div>
                        <div class="step-num">01 &nbsp; DISCORD ACCOUNT</div>
                        <h1>SIGN IN</h1>
                        <p>Continue with your Discord account to enter the game. Your handle is linked to your player profile.</p>
                    </div>
                    <div class="features-list">
                        <div>◆ APPROVE THE REQUEST ON DISCORD</div>
                        <div>◆ YOUR HANDLE LINKS TO YOUR PLAYER PROFILE</div>
                        <div>◆ THE GAME RESUMES ON ITS OWN</div>
                    </div>
                </div>
                <div class="right-section">
                    <a href="{discord_auth_url}" class="discord-btn">
                        <span>CONTINUE WITH DISCORD</span>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.927 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/></svg>
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
        return "<h2 style='color:#ef4444; text-align:center; font-family:sans-serif; margin-top:50px;'>Error In Code Restart Site 🔴</h2>"

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
        return f"<h3 style='color:orange; text-align:center;'>❌ فشل جلب التوكن</h3>"

    auth_header = {"Authorization": f"Bearer {access_token}"}
    member_r = requests.get(f"https://discord.com/api/users/@me/guilds/{GUILD_ID}/member", headers=auth_header)
    
    if member_r.status_code != 200:
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
                    .msg {{
                        font-size: 18px;
                        font-weight: bold;
                        color: #ef4444;
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
                        box-shadow: 0 4px 12px rgba(88, 101, 242, 0.4);
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="msg">join de sirveur ⛔</div>
                    <a href="https://discord.gg/2KD4v9nZQn" class="btn-primary">Aller sur le serveur</a>
                </div>
            </body>
        </html>
        """

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
                </style>
            </head>
            <body>
                <div class="card">
                    <img src="{HOME_BG_URL}" class="logo">
                    <div class="msg">Roh jewz whitelist 📝🔴</div>
                    <div class="server-name">ar roleplay</div>
                    <a href="https://discord.gg/2KD4v9nZQn" class="btn-primary">Aller sur le serveur</a>
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
                    padding: 30px 40px;
                    border-radius: 12px;
                    border: 2px solid #22c55e;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.9);
                    backdrop-filter: blur(8px);
                    text-align: center;
                    width: 380px;
                }}
                h2 {{
                    color: #22c55e;
                    font-size: 20px;
                    margin: 0 0 15px 0;
                    text-shadow: 0 2px 5px rgba(0,0,0,0.9);
                }}
                p {{
                    color: #cbd5e1;
                    font-size: 13px;
                    line-height: 1.5;
                    margin: 0;
                }}
            </style>
        </head>
        <body>
            <div class="box">
                <h2>Welcome To Arabe RolePlay 🟢</h2>
                <p>Done Join Game Click Sur <b>(X)</b> 🟢</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
